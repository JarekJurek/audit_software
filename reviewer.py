import cv2 as cv
from ogximg import OGXImageSeries

from blender import Blender
from image_loader import load_image, load_pollution_size
from io_controller import IOController
from label_manager import LabelManager
from path_manager import PathManager
from utils import concatenate_images, display_info_text


class Reviewer:
    """
    Orchestrates the review process for pollution detection, integrating path management,
    metadata loading, image processing, blending, labeling, and GUI control.
    """

    def __init__(self, data_path_main: str, meat_type: str, test_name: str, results_folder_name: str,
                 show_image_mask: bool = True, show_pkl: bool = True, show_blenders: bool = True):
        self.data_path_main = data_path_main
        self.meat_type = meat_type
        self.test_name = test_name
        self.results_folder_name = results_folder_name

        self.show_image_mask = show_image_mask
        self.show_plk = show_pkl
        self.show_blenders = show_blenders

        self.path_manager = PathManager(data_path_main, meat_type, test_name, results_folder_name)
        self.blender = Blender()
        self.label_manager = LabelManager()
        self.gui_controller = IOController(self.blender, self.label_manager)

    def show_images(self):
        series_path_list = self.path_manager.get_series_paths()

        for series_path in series_path_list:
            ogx_series = OGXImageSeries.from_pickle(series_path[0])
            max_images = self.path_manager.get_max_images(series_path)

            while True:
                # displaying pkl image
                if self.show_plk:
                    cv_img, _ = ogx_series.get_image(self.gui_controller.current_image_index)
                    pkl_image = cv.resize(cv_img, (512, 512))
                    cv.imshow('pkl_image', pkl_image)

                results_folder_number = self.gui_controller.current_image_index // 10 + 1
                base_image, _ = load_image('base_image_3', series_path, results_folder_number)
                results_image, _ = load_image('result_clean', series_path, results_folder_number)

                # displaying blended images
                if self.show_blenders:
                    self.blender.show_blended_images(series_path, results_folder_number)

                # displaying image_mask pair image
                if self.show_image_mask:
                    detected_pollutions_pixels_count = load_pollution_size(series_path, results_folder_number)
                    concatenated_image = concatenate_images(base_image, results_image)
                    display_info_text(concatenated_image, detected_pollutions_pixels_count)
                    cv.imshow('window', concatenated_image)

                # GUI control for navigation and labeling
                is_break, save_pkl_image = self.gui_controller.io_control(max_images)

                if is_break:
                    break

    def run(self):
        """
        Starts the reviewing process and handles the main program loop.
        """
        self.show_images()
        cv.destroyAllWindows()
