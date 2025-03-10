from pathlib import Path
from shutil import copyfile

import cv2 as cv


class LabelManager:
    def __init__(self):
        self.pollution_database = ['pollution']
        self.ref_point = []
        self.cropping = False
        self.current_image_size = (1, 1)
        self.labelled_pollutions = []  # Initialize labeled pollutions list
        self._labels_path: Path = Path()

    def set_image_size(self, width, height):
        """Set the current image dimensions for YOLO label normalization."""
        self.current_image_size = (width, height)

    def _load_labels(self):
        """Load existing labels from a YOLO format file."""
        self.labelled_pollutions = []
        if self._labels_path.exists():
            with open(self._labels_path, 'r') as file:
                for line in file:
                    self.labelled_pollutions.append([float(val) for val in line.strip().split()])

    def display_labels(self, image, image_path, idx):
        """Overlay existing labels on the image."""
        self._labels_path = Path(image_path) / 'images' / f'ogx_image_{idx}.txt'
        self._load_labels()

        height, width = image.shape[:2]
        self.set_image_size(width, height)

        for label in self.labelled_pollutions:
            x_center, y_center, w, h = label[1:]
            start_point = (int((x_center - w / 2) * width), int((y_center - h / 2) * height))
            end_point = (int((x_center + w / 2) * width), int((y_center + h / 2) * height))
            cv.rectangle(image, start_point, end_point, (0, 255, 0), 2)

    def add_pollution(self, start_point, end_point):
        """Add pollution label with bounding box normalized for YOLO format."""
        x_center = ((start_point[0] + end_point[0]) / 2) / self.current_image_size[0]
        y_center = ((start_point[1] + end_point[1]) / 2) / self.current_image_size[1]
        width = abs(end_point[0] - start_point[0]) / self.current_image_size[0]
        height = abs(end_point[1] - start_point[1]) / self.current_image_size[1]
        self.labelled_pollutions.append((0, x_center, y_center, width, height))
        self._save_labels()

    def _save_labels(self):
        """Save labels in YOLO format in the same directory as the image."""
        with open(self._labels_path, 'w') as f:
            for label in self.labelled_pollutions:
                f.write(" ".join(map(str, label)) + "\n")

    def clear_labels(self):
        """Clear all labels for the current image and delete the label file."""
        if self._labels_path.exists():
            self._labels_path.unlink()
        self.labelled_pollutions = []
        print(f"Labels {self._labels_path} cleared.")

    @staticmethod
    def draw_rectangle(event, x, y, flags, param):
        """Callback function to draw and save rectangles on an image for labeling purposes."""
        label_manager, pkl_image, series_path, image_index = param

        if event == cv.EVENT_LBUTTONDOWN:
            label_manager.ref_point = [(x, y)]
            label_manager.cropping = True
        elif event == cv.EVENT_MOUSEMOVE:
            # Refresh the image to clear previous drawings
            current_image = pkl_image.copy()

            # Draw crosshair lines from image edges to the cursor
            height, width = current_image.shape[:2]
            cv.line(current_image, (x, 0), (x, height), (0, 255, 0), 1)  # Vertical line
            cv.line(current_image, (0, y), (width, y), (0, 255, 0), 1)  # Horizontal line

            # If cropping, also draw the rectangle in real-time
            if label_manager.cropping:
                cv.rectangle(current_image, label_manager.ref_point[0], (x, y), (255, 0, 0), 2)

            # Display the updated image with crosshair and rectangle
            cv.imshow('Pkl image', current_image)

        elif event == cv.EVENT_LBUTTONUP:
            label_manager.ref_point.append((x, y))
            label_manager.cropping = False

            # Finalize and save the rectangle
            label_manager.add_pollution(label_manager.ref_point[0], label_manager.ref_point[1])
            cv.rectangle(pkl_image, label_manager.ref_point[0], label_manager.ref_point[1], (255, 0, 0), 2)

            # Display the final image with the completed rectangle
            cv.imshow('Pkl image', pkl_image)

    def copy_labels(self, dest_path: Path):
        """Copy labels from current to destination directory."""
        if not dest_path.parts:
            print('ERROR: png images save path not specified')
            return
        if not self._labels_path.exists():
            print('No labels found.')
            return
        dest_label_path = dest_path / 'labels' / self._labels_path.name
        dest_label_path.parent.mkdir(parents=True, exist_ok=True)
        copyfile(self._labels_path, dest_label_path)
        print(f'Copied labels {self._labels_path.parent} to {dest_label_path.parent}')


def get_image_labels(labels_path):
    labelled_pollutions = []

    if labels_path.exists():
        with open(labels_path, 'r') as file:
            for line in file:
                labelled_pollutions.append([float(val) for val in line.strip().split()])

    return labelled_pollutions
