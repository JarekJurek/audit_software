import os
from pathlib import Path
from typing import List

import cv2 as cv
import numpy as np


def dir_list(path: Path) -> List[str]:
    """
    Return a list of directory names in the provided path.

    :param path: The path in which to look for directories.
    :return: A list of names of directories within the specified path.
    """
    try:
        return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    except FileNotFoundError:
        print("The specified path does not exist.")
    except PermissionError:
        print("Permission denied: Unable to access the specified path.")
    return []


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


def display_info_text(image, detected_results: int):
    """
    Displays pollution detection and current pollution information on the image.

    :param image: The image on which to overlay text information.
    :param detected_results: The number of detected pollutions in the current image.
    """
    font = cv.FONT_HERSHEY_SIMPLEX
    detected_pollutions_color = (0, 255, 0)

    text = f'Detected pollution size: {detected_results}'
    cv.putText(image, text, (900, 20), font, 0.5, detected_pollutions_color, 1)


def print_colors(x: int, y: int, image: np.ndarray):
    """
    Print the color of the pixel at a specified (x, y) location in BGR format.

    :param int x: X-coordinate of the pixel.
    :param int y: Y-coordinate of the pixel.
    :param np.ndarray image: Image array to fetch the pixel color.
    """
    colors = image[y, x]
    print(f"BGR: {str(colors):<15} X:{x:<4} Y:{y:<4}")
