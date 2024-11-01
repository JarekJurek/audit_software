from dataclasses import dataclass

import cv2 as cv
import numpy as np


@dataclass
class GuiControlParams:
    base_image: any
    results_image: any
    detected_pollutions_pixels_count: int
    max_images: int
    pollution_types_count: int


def concatenate_images(base_image: np.ndarray, results_image: np.ndarray) -> np.ndarray:
    """
    Concatenates base_image and results_image side by side.

    :param base_image: The main image to be displayed.
    :param results_image: Image with detection results.
    :return: Concatenated image.
    """
    if base_image.shape[:2] != results_image.shape[:2]:
        results_image = cv.resize(results_image, (base_image.shape[1], base_image.shape[0]))
    concatenated_image = np.concatenate((base_image, results_image), axis=1)
    return concatenated_image


class GUIController:
    """
    Controls the graphical user interface (GUI) elements and manages user interactions.
    """

    def __init__(self, blender, label_manager):
        """
        Initializes GUIController with instances of Blender and LabelManager.

        :param blender: Blender instance for handling image blending.
        :param label_manager: LabelManager instance for managing pollution labels.
        """
        self.blender = blender
        self.label_manager = label_manager
        self.current_image_index = 0
        self.current_pollution_type_index = 0
        self.max_image_index = 0

    def initialize_gui(self):
        """
        Sets up the GUI environment, including windows and trackbars.
        """
        self.blender.setup_windows_and_trackbars()

    def set_mouse_callbacks(self, record_labeled: bool):
        """
        Set mouse callbacks for interacting with the images.

        :param record_labeled: Boolean indicating if labeling mode is active.
        """
        cv.setMouseCallback('pair_0_diff_channel_image',
                            lambda *args: self.blender.print_pixel_color(*args, 'pair_0_diff_channel_image'))
        cv.setMouseCallback('pair_1_diff_channel_image',
                            lambda *args: self.blender.print_pixel_color(*args, 'pair_1_diff_channel_image'))
        if record_labeled:
            cv.setMouseCallback('window', self.label_manager.mark_pollution)

    def display_info_text(self, image, detected_results: int):
        """
        Displays pollution detection and current pollution information on the image.

        :param image: The image on which to overlay text information.
        :param detected_results: The number of detected pollutions in the current image.
        """
        font = cv.FONT_HERSHEY_SIMPLEX
        detected_pollutions_color = (255, 0, 0)
        current_pollutions_color = (0, 255, 0)

        cv.putText(image, f"Detected pollution : {detected_results}", (900, 20), font, 0.5, detected_pollutions_color,
                   1)
        current_pollution = self.label_manager.pollution_database[self.current_pollution_type_index]
        cv.putText(image, f"Current pollution : {current_pollution}", (900, 40), font, 0.5, current_pollutions_color, 1)

    def handle_key_press(self, key: int, params: GuiControlParams):
        """
        Handles key presses for image navigation, pollution labeling, and quitting.

        :param int key: Key press code.
        :param GuiControlParams params: GuiControlParams dataclass containing necessary parameters.
        :return: Tuple (bool, bool) - Whether to quit and whether to save the current image.
        """
        save_pkl_image = False

        if key in [ord('w'), ord('s')]:  # Single-step forward or backward
            self.current_image_index = self._navigate_images(key, params.max_images, step=1)
        elif key in [ord('d'), ord('a')]:  # Multistep forward or backward (e.g., 10 steps)
            self.current_image_index = self._navigate_images(key, params.max_images, step=10)
        elif key in [ord('j'), ord('l')]:  # Navigate pollution types
            self.current_pollution_type_index = self._navigate_pollution_types(key, params.pollution_types_count)
        elif key == ord('z'):  # Save image
            save_pkl_image = True
        elif key in [ord('q'), 27]:  # 'q' or ESC key to quit
            print("Quitting the program.")
            return True, save_pkl_image

        return False, save_pkl_image

    def _navigate_images(self, key: int, max_images: int, step: int) -> int:
        """
        Updates the current image index based on navigation keys.

        :param key: Key code for navigation.
        :param max_images: Maximum index of images for navigation.
        :param step: Number of images to step forward or backward.
        :return: Updated image index.
        """
        if key == ord('w'):  # Move forward by step
            new_index = self.current_image_index + step
        elif key == ord('s'):  # Move backward by step
            new_index = self.current_image_index - step
        elif key == ord('d'):  # Multistep forward
            new_index = self.current_image_index + step
        elif key == ord('a'):  # Multistep backward
            new_index = self.current_image_index - step
        else:
            new_index = self.current_image_index

        # Ensure new_index stays within bounds
        new_index = max(0, min(new_index, max_images - 1))

        if new_index == self.current_image_index:
            print("End of images.")

        return new_index

    def _navigate_pollution_types(self, key: int, max_pollutions: int) -> int:
        """
        Updates the current pollution type index based on key input.
        """
        new_index = self.current_pollution_type_index + (1 if key == ord('l') else -1)
        return (new_index + max_pollutions) % max_pollutions  # Wrap-around behavior

    def gui_control(self, params: GuiControlParams):
        """
        Display and control GUI for navigating images and labeling detected pollution.
        """
        concatenated_image = concatenate_images(params.base_image, params.results_image)
        self.display_info_text(concatenated_image, params.detected_pollutions_pixels_count)

        cv.imshow('window', concatenated_image)
        key = cv.waitKey(0)
        return self.handle_key_press(key, params)
