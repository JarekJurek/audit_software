"""App spawning module."""
from pathlib import Path

import cv2
import cv2 as cv
from ogximg import OGXImageSeries

from audit_software.blender import Blender
from audit_software.enums import KeyAction
from audit_software.image_loader import load_image, load_detection_data
from audit_software.io_controller import IOController
from audit_software.label_manager import LabelManager
from audit_software.path_manager import PathManager
from audit_software.utils import concatenate_images, display_info_text, resize_image


class Reviewer:
    """Main, top level, application code."""

    def __init__(self, path_manager: PathManager, start_folder: int = 1,
                 show_image_mask: bool = True, show_pkl: bool = True, show_blenders: bool = True,
                 save_path: Path = Path()):
        self.show_image_mask = show_image_mask
        self.show_pkl = show_pkl
        self.show_blenders = show_blenders

        self.path_manager = path_manager
        self.blender = Blender()
        self.label_manager = LabelManager()
        self.io_controller = IOController(self.blender, start_folder)

        self.save_path: Path = save_path
        self.cv_img = None
        self.cv_img2 = None

    def show_images(self):
        """Display images along with existing labels, if any, and provide GUI for navigation and labeling."""
        series_path_list = self.path_manager.get_series_paths()

        for series_path in series_path_list:
            ogx_series = OGXImageSeries.from_pickle(series_path[0])
            max_images = self.path_manager.get_max_images(series_path)

            if self.io_controller.current_image_index > max_images:
                print("ERROR: Provided starting folder index out of range. Correct 'run.py'")
                exit(0)

            while True:
                # Displaying pkl image
                if self.show_pkl:
                    self.cv_img, _ = ogx_series.get_image(self.io_controller.current_image_index)
                    self.cv_img2, _ = ogx_series.get_image(self.io_controller.current_image_index + 1)
                    pkl_image = resize_image(self.cv_img)
                    self.label_manager.display_labels(pkl_image, series_path[0],
                                                      self.io_controller.current_image_index)  # Display with labels

                    params = (self.label_manager, pkl_image, series_path[0], self.io_controller.current_image_index)
                    cv.imshow("Pkl image", pkl_image)
                    cv.setMouseCallback("Pkl image", self.label_manager.draw_rectangle, param=params)

                results_folder_number = self.io_controller.current_image_index // 10 + 1
                print(f'Folder: {results_folder_number}, image: {self.io_controller.current_image_index}')
                base_image, _ = load_image('base_image_1', series_path, results_folder_number)
                results_image, _ = load_image('result_clean', series_path, results_folder_number)

                # Displaying blended images
                if self.show_blenders:
                    self.blender.show_blended_images(series_path, results_folder_number)

                # Displaying image_mask pair image
                if self.show_image_mask:
                    detection, pollution_size = load_detection_data(series_path, results_folder_number)
                    concatenated_image = concatenate_images(base_image, results_image)
                    signed_image = display_info_text(concatenated_image, detection, pollution_size)
                    cv.imshow('Detection', signed_image)

                # GUI control for navigation and labeling
                action = self.io_controller.get_io_action(max_images)
                if action == KeyAction.NONE:
                    continue
                elif action == KeyAction.QUIT:
                    break
                elif action == KeyAction.CLEAR_LABELS:
                    self.label_manager.clear_labels()
                elif action == KeyAction.SAVE_IMAGE:
                    if self.cv_img is None or not self.save_path.parts:
                        print('No image or path specified')
                        continue
                    self.label_manager.copy_labels(dest_path=self.save_path)
                    self.save_png_img()
                else:
                    print('ERROR: received wrong key action')

    def _save_image(self, img, index):
        """Helper function to save an image in PNG format."""
        png_img_path = self.save_path / 'images' / f'ogx_image_{index}.png'
        png_img_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(png_img_path), img)
        print(f"Image saved in {png_img_path}")

    def save_png_img(self):
        """Save current images in PNG format in the specified save path."""
        if not self.save_path.parts:
            print('ERROR: PNG images save path not specified')
            return

        self._save_image(self.cv_img, self.io_controller.current_image_index)
        self._save_image(self.cv_img2, self.io_controller.current_image_index + 1)

    def run(self):
        """Starts the reviewing process and handles the main program loop."""
        self.show_images()
        cv.destroyAllWindows()
