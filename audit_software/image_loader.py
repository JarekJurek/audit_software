"""Image loading module."""
import json
import os
from typing import Tuple, Optional

import cv2 as cv
import numpy as np


def load_image(image_name: str, series_path: tuple, results_folder_number: int) -> Tuple[
    Optional[np.ndarray], Optional[str]]:
    """
    Load an image from a series path with supported extensions.

    :param image_name: Name of the image file without extension.
    :param series_path: Tuple with paths, where series_path[1] points to the results directory.
    :param results_folder_number: The folder number within the results directory.
    :return: Loaded image as np.ndarray and the path to the image, or (None, None) if not found.
    """
    extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']
    for ext in extensions:
        image_path = os.path.join(series_path[1], str(results_folder_number), f"{image_name}{ext}")
        if os.path.exists(image_path):
            image = cv.imread(image_path)
            if image is not None:
                return image, image_path
    print(f"Warning: Could not load image for {image_name} with any of the extensions {extensions}")
    return None, None


def load_detection_data(series_path: tuple, results_folder_number: int) -> Tuple[Optional[bool], Optional[int]]:
    """
    Load detected pollution information from data.json.

    :param series_path: Tuple with paths, where series_path[1] points to the results directory.
    :param results_folder_number: Folder number within the results' directory.
    :return: Tuple of pollution detection boolean and pollution pixel count.
    """
    detected_results_path = os.path.join(series_path[1], str(results_folder_number), 'data.json')

    if os.path.exists(detected_results_path):
        with open(detected_results_path) as detected_results_file:
            detected_results_data = json.load(detected_results_file)
            pollution_detected = detected_results_data.get("pollution_detected")
            pollution_count = detected_results_data.get("count")
            return pollution_detected, pollution_count

    return None, None
