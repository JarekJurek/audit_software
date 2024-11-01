import os

import cv2 as cv
import numpy as np
from ogximg import OGXImageSeries

from blender import Blender
from gui_controller import GUIController, GuiControlParams
from image_loader import load_image, get_detected_pollutions_pixels_count
from label_manager import LabelManager
from path_manager import PathManager


class Reviewer:
    """
    Orchestrates the review process for pollution detection, integrating path management,
    metadata loading, image processing, blending, labeling, and GUI control.
    """

    def __init__(self, data_path_main: str, meat_type: str, test_name: str, results_folder_name: str,
                 pollution_database: list):
        self.data_path_main = data_path_main
        self.meat_type = meat_type
        self.test_name = test_name
        self.results_folder_name = results_folder_name
        self.pollution_database = pollution_database
        self.path_manager = PathManager(data_path_main, meat_type, test_name, results_folder_name)
        self.blender = Blender()
        self.label_manager = LabelManager(pollution_database)
        self.gui_controller = GUIController(self.blender, self.label_manager)

    def show_labelled_results(self):
        series_path_list = self.path_manager.get_series_paths()

        for series_path in series_path_list:
            ogx_series = OGXImageSeries.from_pickle(series_path[0])
            self.gui_controller.initialize_gui()
            max_images = self.path_manager.get_max_images(series_path)

            while True:
                cv_img, _ = ogx_series.get_image(self.gui_controller.current_image_index)
                pkl_image = cv.resize(cv_img, (512, 512))
                cv.imshow('pkl_image', pkl_image)

                results_folder_number = self.gui_controller.current_image_index // 10 + 1
                base_image, _ = load_image('base_image_3', series_path, results_folder_number)
                results_image, _ = load_image('result_clean', series_path, results_folder_number)

                # Load necessary masks
                pair_0_diff_channel_image, _ = load_image('pair_0_diff_channel',
                                                          series_path,
                                                          results_folder_number)
                pair_1_diff_channel_image, _ = load_image('pair_1_diff_channel',
                                                          series_path,
                                                          results_folder_number)
                pair_0_pollution_image_mask, _ = load_image('pair_0_pollution_image_mask',
                                                            series_path,
                                                            results_folder_number)
                pair_1_pollution_image_mask, _ = load_image('pair_1_pollution_image_mask',
                                                            series_path,
                                                            results_folder_number)
                conveyor_image_mask, _ = load_image('pair_0_conveyor_mask',
                                                    series_path,
                                                    results_folder_number)

                if conveyor_image_mask is None:
                    conveyor_image_mask, _ = load_image('pair_1_conveyor_mask',
                                                        series_path,
                                                        results_folder_number)

                # Set images for blending
                self.blender.set_images(pair_0_diff_channel_image, conveyor_image_mask, pair_0_pollution_image_mask,
                                        pair_1_diff_channel_image, conveyor_image_mask, pair_1_pollution_image_mask,
                                        conveyor_image_mask)

                detected_pollutions_pixels_count = get_detected_pollutions_pixels_count(series_path,
                                                                                        results_folder_number)

                # Display blended images initially
                self.blender.show_blend(0)
                self.blender.show_blend(1)

                # GUI parameters
                params = GuiControlParams(
                    base_image=base_image,
                    results_image=results_image,
                    detected_pollutions_pixels_count=detected_pollutions_pixels_count,
                    max_images=max_images,
                    pollution_types_count=len(self.pollution_database)
                )

                # GUI control for navigation and labeling
                is_break, save_pkl_image = self.gui_controller.gui_control(params)

                if save_pkl_image and pkl_image is not None:
                    self.save_pkl_image(pkl_image, self.gui_controller.current_image_index)

                if is_break:
                    break

    def save_pkl_image(self, pkl_image, image_index: int):
        """
        Saves the current pickle image for a given meat type.

        :param np.ndarray pkl_image: The image to save.
        :param int image_index: The current index of the image.
        """
        pkl_folder_path = os.path.join('C:\\Users\\linnia1\\Pictures\\Saved Pictures\\', str(self.meat_type))
        os.makedirs(pkl_folder_path, exist_ok=True)
        pkl_image_path = os.path.join(pkl_folder_path, f'pkl_image_{image_index}.png')
        cv.imwrite(pkl_image_path, pkl_image)
        print(f'Saved pkl_image in {pkl_image_path}')

    def run(self):
        """
        Starts the reviewing process and handles the main program loop.
        """
        self.show_labelled_results()
        cv.destroyAllWindows()
