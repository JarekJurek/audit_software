"""Utility functions module."""
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
        print(f"The specified path does not exist: {path}.")
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


def display_info_text(image, detection: bool, pollution_size: int):
    """
    Displays pollution detection and pollution size information below the image.

    :param image: The main image to be displayed.
    :param detection: Boolean indicating if pollution was detected.
    :param pollution_size: Pixel size of the detected pollution.
    """
    extra_space_height = 30
    combined_image = cv.copyMakeBorder(image, 0, extra_space_height, 0, 0, cv.BORDER_CONSTANT, value=[0, 0, 0])

    font = cv.FONT_HERSHEY_SIMPLEX
    text_color = (0, 255, 0)

    text = f'Detection: {detection}'

    if detection:
        text = f'{text}     Size: {pollution_size} px'

    cv.putText(combined_image, text, (10, image.shape[0] + 20), font, 0.5, text_color, 1)

    return combined_image


def print_colors(x: int, y: int, image: np.ndarray):
    """
    Print the color of the pixel at a specified (x, y) location in BGR format.

    :param int x: X-coordinate of the pixel.
    :param int y: Y-coordinate of the pixel.
    :param np.ndarray image: Image array to fetch the pixel color.
    """
    colors = image[y, x]
    print(f"Hue:{str(colors[0]):<4} X:{x:<4} Y:{y:<4}")


def resize_image(image, resize_fraction=0.4):
    height, width = image.shape[:2]
    new_width = int(width * resize_fraction)
    new_height = int(height * resize_fraction)
    return cv.resize(image, (new_width, new_height))
