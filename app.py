"""App spawning module."""
import cv2 as cv
from ogximg import OGXImageSeries

from blender import Blender
from image_loader import load_image, load_detection_data
from io_controller import IOController
from label_manager import LabelManager
from path_manager import PathManager
from utils import concatenate_images, display_info_text, resize_image


class Reviewer:
    """Main, top level, application code."""

    def __init__(self, path_manager: PathManager, start_folder: int=1,
                 show_image_mask: bool = True, show_pkl: bool = True, show_blenders: bool = True):
        self.show_image_mask = show_image_mask
        self.show_pkl = show_pkl
        self.show_blenders = show_blenders

        self.path_manager = path_manager
        self.blender = Blender()
        self.label_manager = LabelManager()
        self.io_controller = IOController(self.blender, self.label_manager, start_folder)

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
                    cv_img, _ = ogx_series.get_image(self.io_controller.current_image_index)
                    pkl_image = resize_image(cv_img)
                    self.label_manager.display_labels(pkl_image, series_path[0], self.io_controller.current_image_index)  # Display with labels

                    params = (self.label_manager, pkl_image, series_path[0], self.io_controller.current_image_index)
                    cv.imshow('pkl_image', pkl_image)
                    cv.setMouseCallback("pkl_image", self.label_manager.draw_rectangle, param=params)

                results_folder_number = self.io_controller.current_image_index // 10 + 1
                print(f'Folder: {results_folder_number}, image: {self.io_controller.current_image_index }')
                base_image, _ = load_image('base_image_3', series_path, results_folder_number)
                results_image, _ = load_image('result_clean', series_path, results_folder_number)

                # Displaying blended images
                if self.show_blenders:
                    self.blender.show_blended_images(series_path, results_folder_number)

                # Displaying image_mask pair image
                if self.show_image_mask:
                    detection, pollution_size = load_detection_data(series_path, results_folder_number)
                    concatenated_image = concatenate_images(base_image, results_image)
                    signed_image = display_info_text(concatenated_image, detection, pollution_size)
                    cv.imshow('window', signed_image)

                # GUI control for navigation and labeling
                is_break = self.io_controller.io_control(max_images)

                if is_break:
                    break

    def run(self):
        """Starts the reviewing process and handles the main program loop."""
        self.show_images()
        cv.destroyAllWindows()
