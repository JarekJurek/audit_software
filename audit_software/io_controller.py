"""Input/output interaction module."""
import cv2 as cv

from audit_software.blender import Blender
from audit_software.enums import KeyAction


class IOController:
    """Controls the I/O signals from user."""

    def __init__(self, blender: Blender, start_folder: int):
        """
        Initializes IOController with instances of Blender and LabelManager.

        :param blender: Blender instance for handling image blending.
        """
        self.blender = blender
        self.current_image_index = self.set_start_image(start_folder)
        self.max_image_index = 0

    @staticmethod
    def set_start_image(start_folder: int) -> int:
        """Return the first image index in desired starting folder."""
        if start_folder == 0:
            print("ERROR: Folder indexing starts from one. Correct 'run.py'")
            exit(1)
        return start_folder * 10 - 1

    def handle_key_press(self, key: int, max_images: int) -> KeyAction:
        """
        Handles key presses for image navigation, pollution labeling, and quitting.

        :param int key: Key press code.
        :param int max_images: number of images in series.
        :return: KeyAction: action chosen by user.
        """
        if key in [ord('w'), ord('s')]:  # Single-step forward or backward
            self.current_image_index = self._navigate_images(key, max_images, step=1)
        elif key in [ord('d'), ord('a')]:  # Multistep forward or backward (e.g., 10 steps)
            self.current_image_index = self._navigate_images(key, max_images, step=8)
        elif key == ord('c'):
            return KeyAction.SAVE_IMAGE
        elif key == ord('u'):
            return KeyAction.CLEAR_LABELS
        elif key in [ord('q'), 27]:  # 'q' or ESC
            return KeyAction.QUIT

        return KeyAction.NONE

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

    def get_io_action(self, max_images: int) -> KeyAction:
        """
        Control IO for navigating images.
        """
        key = cv.waitKey(0)
        return self.handle_key_press(key, max_images)
