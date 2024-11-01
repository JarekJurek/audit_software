import json
import os
from pathlib import Path
from typing import List

import cv2 as cv
import numpy as np
from ogximg import OGXImageSeries

from utilities import pollution_database


def get_series_path_list(data_path_main: str, meat_name: str = None, test_name: str = None,
                         results_folder_name: str = 'results') -> list:
    """
    Generate paths to acquisition image series and results directories.

    :param str data_path_main: Main directory where data is stored.
    :param str meat_name: Name of the meat type directory. If not provided, prompts for input.
    :param str test_name: Specific test series name to filter results; if None, includes all tests.
    :param str results_folder_name: Folder name for results within the main data path, defaults to 'results'.

    :return list of tuple:
        - series_path: Path to acquisition image series.
        - results_path: Corresponding path to results directory.
    """

    if meat_name is None:
        meat_name = input('Provide meat type: ').strip()

    series_path_list = []
    linia_path_main = Path(data_path_main) / meat_name / 'data'

    for linia_path in dir_list(linia_path_main):
        test_path_main = linia_path_main / linia_path / meat_name

        for test_path in dir_list(test_path_main):
            if test_name and test_path != test_name:
                continue  # Skip if test_name is specified and doesn't match

            series_path = test_path_main / test_path / '0' / 'camera_series'
            results_path = Path(
                data_path_main) / meat_name / results_folder_name / linia_path / meat_name / test_path / '0'

            series_path_list.append((str(series_path), str(results_path)))

    return series_path_list


def dir_list(path: Path) -> List[str]:
    """
    Return a list of directory names in the provided path.

    :param Path path: The path in which to look for directories.

    :return List[str]: A list of names of directories within the specified path.
    """
    try:
        # List all items and filter only directories
        folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        return folders
    except FileNotFoundError:
        print("The specified path does not exist.")
        return []
    except PermissionError:
        print("Permission denied: Unable to access the specified path.")
        return []


def load_series_labelled_metadata(series_path: tuple) -> dict:
    """
    Load labelled metadata from a JSON file in the specified series path.

    :param tuple series_path: Tuple with paths, where series_path[1] points to the directory with JSON files.
    :return dict: Parsed JSON data from the labelled series file, or None if no file is found.
    """
    files = [f for f in os.listdir(series_path[1]) if f.endswith(".json")]
    if files:
        series_labelled_file_path = os.path.join(series_path[1], files[0])
        with open(series_labelled_file_path, 'r') as labelled_file:
            series_labelled_metadata = json.load(labelled_file)
            print('Loaded series_labelled_metadata from', series_labelled_file_path)
            return series_labelled_metadata
    return None


def load_one_series_description(series_path: tuple) -> dict:
    """
    Load metadata description from series_metadata.json.

    :param tuple series_path: Tuple with paths, where series_path[0] points to the main series directory.
    :return dict: Parsed JSON data from series_metadata.json.
    """
    series_metadata_file_path = os.path.join(series_path[0], 'series_metadata.json')
    with open(series_metadata_file_path, 'r') as file:
        return json.load(file)


def load_one_series_metadata(series_description: dict) -> dict:
    """
    Extract metadata from a series description.

    :param dict series_description: JSON data containing series metadata.
    :return dict: Metadata from the series description.
    """
    return series_description.get('meta_data', {})


def load_one_series_image_data(series_meta_data: dict) -> dict:
    """
    Extract image metadata from series meta data.

    :param dict series_meta_data: Metadata containing image information.
    :return dict: Image metadata from the series meta data.
    """
    return series_meta_data.get('image_meta_data', {})


def load_image(image_name: str, series_path: tuple, results_folder_number: int) -> tuple:
    """
    Load an image from a series path with supported extensions.

    :param str image_name: Name of the image file without extension.
    :param tuple series_path: Tuple with paths, where series_path[1] points to the results directory.
    :param int results_folder_number: The folder number within the results directory.
    :return tuple: Loaded image as np.ndarray and the path to the image, or (None, None) if not found.
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


def init_global_indexes():
    """
    Initialize global indexes for pollution type and image navigation.
    """
    global p, i, prev_i
    p = 0
    prev_i = -1
    i = 0


def get_images_index_max(test_path: str) -> int:
    """
    Calculate the maximum index based on the number of results paths in a test path.

    :param str test_path: Path to the test folder.
    :return int: Number of result paths multiplied by 10 for index calculation.
    """
    results_paths = dir_list(test_path)
    return len(results_paths) * 10


def get_detected_pollutions_pixels_count(series_path: tuple, results_folder_number: int) -> int:
    """
    Load detected pollution pixel count from data.json.

    :param tuple series_path: Tuple with paths, where series_path[1] points to the results directory.
    :param int results_folder_number: Folder number within the results directory.
    :return int: Pixel count of detected pollutions, or None if not available.
    """
    detected_results_path = os.path.join(series_path[1], str(results_folder_number), 'data.json')
    if os.path.exists(detected_results_path):
        with open(detected_results_path) as detected_results_file:
            detected_results_data = json.load(detected_results_file)
            return detected_results_data.get("count")
    return None


def print_colors(x: int, y: int, image: np.ndarray):
    """
    Print the color of the pixel at a specified (x, y) location in BGR format.

    :param int x: X-coordinate of the pixel.
    :param int y: Y-coordinate of the pixel.
    :param np.ndarray image: Image array to fetch the pixel color.
    """
    colors = image[y, x]
    print("BGR Format:", colors)
    print("Coordinates of pixel: X:", x, "Y:", y)


def mouse_show_hsv_0(event, x, y, flags, param):
    """
    Show BGR color of pixel in pair_0_diff_channel_image on left-click.

    :param event: Mouse event type.
    :param x: X-coordinate of the click.
    :param y: Y-coordinate of the click.
    """
    if event == cv.EVENT_LBUTTONDOWN:
        print_colors(x, y, pair_0_diff_channel_image)


def mouse_show_hsv_1(event, x, y, flags, param):
    """
    Show BGR color of pixel in pair_1_diff_channel_image on left-click.

    :param event: Mouse event type.
    :param x: X-coordinate of the click.
    :param y: Y-coordinate of the click.
    """
    if event == cv.EVENT_LBUTTONDOWN:
        print_colors(x, y, pair_1_diff_channel_image)


def show_pair_0_blend():
    """
    Display a blended image for pair_0 based on blend settings.
    """
    if pair_0_diff_channel_image is None or conveyor_image_mask is None:
        return
    img = cv.addWeighted(pair_0_diff_channel_image, pair_0_diff_blend, conveyor_image_mask, pair_0_conv_blend, 0)
    if img is not None and pair_0_pollution_image_mask is not None:
        img = cv.addWeighted(img, 1.0, pair_0_pollution_image_mask, pair_0_pollution_blend, 0)
        cv.imshow(pair_0_window_name, img)


def show_pair_1_blend():
    """
    Display a blended image for pair_1 based on blend settings.
    """
    if pair_1_diff_channel_image is None or conveyor_image_mask is None:
        return
    img = cv.addWeighted(pair_1_diff_channel_image, pair_1_diff_blend, conveyor_image_mask, pair_1_conv_blend, 0)
    if img is not None and pair_1_pollution_image_mask is not None:
        img = cv.addWeighted(img, 1.0, pair_1_pollution_image_mask, pair_1_pollution_blend, 0)
        cv.imshow(pair_1_window_name, img)


def on_change_pair_0_diff_blend(value):
    """
    Update the diff blend value for pair_0 and refresh the display.

    :param int value: New value for the diff blend setting.
    """
    global pair_0_diff_blend
    pair_0_diff_blend = float(value) / 100.0
    show_pair_0_blend()


def on_change_pair_0_conv_blend(value):
    """
    Update the conv blend value for pair_0 and refresh the display.

    :param int value: New value for the conv blend setting.
    """
    global pair_0_conv_blend
    pair_0_conv_blend = float(value) / 100.0
    show_pair_0_blend()


def on_change_pair_0_pollution_blend(value):
    """
    Update the pollution blend value for pair_0 and refresh the display.

    :param int value: New value for the pollution blend setting.
    """
    global pair_0_pollution_blend
    pair_0_pollution_blend = float(value) / 100.0
    show_pair_0_blend()


def on_change_pair_1_diff_blend(value):
    """
    Update the diff blend value for pair_1 and refresh the display.

    :param int value: New value for the diff blend setting.
    """
    global pair_1_diff_blend
    pair_1_diff_blend = float(value) / 100.0
    show_pair_1_blend()


def on_change_pair_1_conv_blend(value):
    """
    Update the conv blend value for pair_1 and refresh the display.

    :param int value: New value for the conv blend setting.
    """
    global pair_1_conv_blend
    pair_1_conv_blend = float(value) / 100.0
    show_pair_1_blend()


def on_change_pair_1_pollution_blend(value):
    """
    Update the pollution blend value for pair_1 and refresh the display.

    :param int value: New value for the pollution blend setting.
    """
    global pair_1_pollution_blend
    pair_1_pollution_blend = float(value) / 100.0
    show_pair_1_blend()


def add_pollution(pollution_index: int, pollution_start_point: tuple, pollution_end_point: tuple):
    """
    Add a pollution annotation to the labelled_pollutions list.

    :param int pollution_index: Index of the pollution type.
    :param tuple pollution_start_point: Start point of the pollution rectangle.
    :param tuple pollution_end_point: End point of the pollution rectangle.
    """
    global labelled_pollutions
    if pollution_database[pollution_index] != "No pollution":
        pollution = {
            'type': pollution_database[pollution_index],
            'location_rectangle': (pollution_start_point, pollution_end_point),
            'confusion_value': None
        }
        labelled_pollutions.append(pollution)


def mark_pollution(event, x, y, flags, param):
    """
    Mark a pollution area based on mouse drag events and draw a rectangle.

    :param event: Mouse event type.
    :param x: X-coordinate of the event.
    :param y: Y-coordinate of the event.
    """
    global refPt, cropping, concaterated_image, p
    if event == cv.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True
    elif event == cv.EVENT_LBUTTONUP:
        refPt.append((x, y))
        cropping = False
        current_pollutions_color = (0, 255, 0)
        cv.rectangle(concaterated_image, refPt[0], refPt[1], current_pollutions_color, 2)
        add_pollution(p, refPt[0], refPt[1])
        cv.imshow('window', concaterated_image)

def show_labelled_results(data_path_main: str, meat_type: str, test_name: str, results_folder_name: str = 'results'):
    """
    Display labelled results for a given data path, meat type, and test series.

    :param str data_path_main: Main directory path containing data.
    :param str meat_type: The type of meat to filter data by.
    :param str test_name: The specific test series name to display.
    :param str results_folder_name: Folder where results are stored. Defaults to 'results'.
    """
    series_path_list = get_series_path_list(data_path_main, meat_type, test_name, results_folder_name=results_folder_name)

    for series_path in series_path_list:
        series_labelled_metadata = load_series_labelled_metadata(series_path)
        series_description = load_one_series_description(series_path)
        series_meta_data = load_one_series_metadata(series_description)
        series_image_data = load_one_series_image_data(series_meta_data)

        ogx_series = OGXImageSeries.from_pickle(series_path[0])

        # Initialize trackbars and blending values for image display
        global pair_0_diff_blend, pair_0_conv_blend, pair_0_pollution_blend, pair_0_window_name, pair_0_trackbars_added
        global pair_1_diff_blend, pair_1_conv_blend, pair_1_pollution_blend, pair_1_window_name, pair_1_trackbars_added
        pair_0_window_name = "pair_0_diff_channel_image"
        pair_1_window_name = "pair_1_diff_channel_image"
        pair_0_trackbars_added = False
        pair_1_trackbars_added = False
        pair_0_diff_blend = 0.5
        pair_0_conv_blend = 0.0
        pair_0_pollution_blend = 1.0
        pair_1_diff_blend = 0.5
        pair_1_conv_blend = 0.0
        pair_1_pollution_blend = 1.0

        global i
        init_global_indexes()

        max_i = get_images_index_max(series_path[1]) * 10

        while True:
            cv_img, _ = ogx_series.get_image(i)
            preview_size = (512, 512)
            pkl_image = cv.resize(cv_img, preview_size)
            cv.imshow('pkl_image', pkl_image)

            results_folder_number = i // 10 + 1

            # Load base and result images
            base_image, base_image_path = load_image('base_image_3', series_path, results_folder_number)
            results_image, results_image_path = load_image('result_clean', series_path, results_folder_number)

            # Load various mask images
            global pair_0_diff_channel_image, pair_1_diff_channel_image
            global gray_1_pollution_image_mask, pair_0_pollution_image_mask, pair_1_pollution_image_mask
            global conveyor_image_mask

            pair_0_diff_channel_image, _ = load_image('pair_0_diff_channel', series_path, results_folder_number)
            pair_1_diff_channel_image, _ = load_image('pair_1_diff_channel', series_path, results_folder_number)
            gray_1_pollution_image_mask, _ = load_image('gray_1_pollution_image_mask', series_path, results_folder_number)
            pair_0_pollution_image_mask, _ = load_image('pair_0_pollution_image_mask', series_path, results_folder_number)
            pair_1_pollution_image_mask, _ = load_image('pair_1_pollution_image_mask', series_path, results_folder_number)
            conveyor_image_mask, _ = load_image('pair_0_conveyor_mask', series_path, results_folder_number)

            if conveyor_image_mask is None:
                conveyor_image_mask, _ = load_image('pair_1_conveyor_mask', series_path, results_folder_number)

            detected_pollutions_pixels_count = get_detected_pollutions_pixels_count(series_path, results_folder_number)
            print('Folder:', results_folder_number)

            is_brake, save_pkl_image = gui_control(
                base_image, results_image, detected_pollutions_pixels_count, max_i, len(pollution_database), False
            )

            # Save image if requested
            if save_pkl_image and pkl_image is not None:
                pkl_folder_path = os.path.join('C:\\Users\\linnia1\\Pictures\\Saved Pictures\\', str(meat_type))
                if not os.path.exists(pkl_folder_path):
                    os.makedirs(pkl_folder_path)
                pkl_image_path = os.path.join(pkl_folder_path, f'pkl_image_{i}.png')
                cv.imwrite(pkl_image_path, cv_img)
                print('Saved pkl_image in', pkl_image_path)

            if is_brake:
                break


###########################  GUI  ####################################33

def gui_control(base_image, results_image, detected_results, max_i, max_p, record_labbeled=True):
    """
    Display and control GUI for navigating images and labeling detected pollution.

    :param np.ndarray base_image: The main image to be displayed.
    :param np.ndarray results_image: Image with detection results, overlaid onto base_image.
    :param int detected_results: Number of detected pollutions in the current image.
    :param int max_i: Maximum index of images for navigation.
    :param int max_p: Maximum index of pollution types for selection.
    :param bool record_labbeled: Whether to enable recording of labeled pollutions. Defaults to True.

    :return tuple: A tuple containing:
        - bool: Whether to exit the program.
        - bool: Whether to save the current image with labeled pollution as a pickle.
    """
    global refPt, prev_i, i, labelled_pollutions, p, concaterated_image, cropping

    initialize_globals(record_labbeled)
    add_trackbars()

    # Ensure results_image matches the size of base_image
    results_image = resize_results_image_if_needed(base_image, results_image)

    concaterated_image = np.concatenate((base_image, results_image), axis=1)
    set_mouse_callbacks(record_labbeled)
    display_info_text(concaterated_image, detected_results)

    cv.imshow('window', concaterated_image)
    key = cv.waitKey(0)

    return handle_key_press(key, max_i, max_p)


def resize_results_image_if_needed(base_image, results_image):
    """Resize results_image to match base_image if smaller in dimensions."""
    if results_image.shape[0] < base_image.shape[0] or results_image.shape[1] < base_image.shape[1]:
        top = int((base_image.shape[0] - results_image.shape[0]) / 2)
        bottom = top
        left = int((base_image.shape[1] - results_image.shape[1]) / 2)
        right = left
        value = [0, 0, 0]
        results_image = cv.copyMakeBorder(results_image, top, bottom, left, right, cv.BORDER_CONSTANT, None, value)
    return results_image


def initialize_globals(record_labbeled):
    """Initialize global variables for image labeling and navigation."""
    global refPt, prev_i, i, labelled_pollutions, cropping
    refPt = []
    cropping = False
    if prev_i != i and record_labbeled:
        labelled_pollutions = []
    prev_i = i


def add_trackbars():
    """Add trackbars to the GUI for blending adjustments."""
    global pair_0_trackbars_added, pair_1_trackbars_added

    show_pair_0_blend()
    if not pair_0_trackbars_added:
        cv.createTrackbar('pair_0_diff_blend', pair_0_window_name, 0, 100, on_change_pair_0_diff_blend)
        cv.createTrackbar('pair_0_conv_blend', pair_0_window_name, 0, 100, on_change_pair_0_conv_blend)
        cv.createTrackbar('pair_0_pollution_blend', pair_0_window_name, 0, 100, on_change_pair_0_pollution_blend)
        pair_0_trackbars_added = True

    show_pair_1_blend()
    if not pair_1_trackbars_added:
        cv.createTrackbar('pair_1_diff_blend', pair_1_window_name, 0, 100, on_change_pair_1_diff_blend)
        cv.createTrackbar('pair_1_conv_blend', pair_1_window_name, 0, 100, on_change_pair_1_conv_blend)
        cv.createTrackbar('pair_1_pollution_blend', pair_1_window_name, 0, 100, on_change_pair_1_pollution_blend)
        pair_1_trackbars_added = True


def resize_results_image_if_needed(base_image, results_image):
    """Resize results_image to match base_image if smaller in dimensions."""
    if results_image.shape[0] < base_image.shape[0] or results_image.shape[1] < base_image.shape[1]:
        top = int((base_image.shape[0] - results_image.shape[0]) / 2)
        bottom = top
        left = int((base_image.shape[1] - results_image.shape[1]) / 2)
        right = left
        value = [0, 0, 0]
        return cv.copyMakeBorder(results_image, top, bottom, left, right, cv.BORDER_CONSTANT, None, value)
    return results_image


def set_mouse_callbacks(record_labbeled):
    """Set mouse callbacks for interaction with the images."""
    cv.setMouseCallback('pair_0_diff_channel_image', mouse_show_hsv_0)
    cv.setMouseCallback('pair_1_diff_channel_image', mouse_show_hsv_1)
    if record_labbeled:
        cv.setMouseCallback('window', mark_pollution)


def display_info_text(image, detected_results):
    """Display detected and current pollution info on the concatenated image."""
    font = cv.FONT_HERSHEY_SIMPLEX
    detected_pollutions_color = (255, 0, 0)
    current_pollutions_color = (0, 255, 0)

    cv.putText(image, f"Detected pollution : {detected_results}", (900, 20), font, 0.5,
               detected_pollutions_color, 1)
    cv.putText(image, f"Current pollution : {pollution_database[p]}", (900, 40), font, 0.5,
               current_pollutions_color, 1)


def handle_key_press(key, max_i, max_p):
    """Handle key presses for navigation, labeling, and quitting."""
    global i, p
    save_pkl_image = False

    if key in [ord('w'), ord('s'), ord('d'), ord('a')]:
        i = navigate_images(key, max_i)
    elif key in [ord('j'), ord('l')]:
        p = navigate_pollution_types(key, max_p)
    elif key == ord('z'):
        save_pkl_image = True
    elif key in [ord('q'), 27]:  # 'q' or ESC key to quit
        print("Quitting the program.")
        return True, save_pkl_image

    return False, save_pkl_image


def navigate_images(key, max_i):
    """Navigate through images based on key press."""
    global i
    step = 1 if key in [ord('w'), ord('s')] else 10
    i = i + step if key in [ord('w'), ord('d')] else i - step
    if i >= max_i:
        print("End of images")
        i = max_i - 1
    elif i < 0:
        i = 0
    return i


def navigate_pollution_types(key, max_p):
    """Navigate through pollution types based on key press."""
    global p
    p = p - 1 if key == ord('j') else p + 1
    if p >= max_p:
        p = 0
    elif p < 0:
        p = max_p - 1
    return p


def main():
    data_path_main = '/home/gregory/agromaks/test_0'  # początek ścieżki absolutnej
    meat_type, test_name, results_folder_name = 'Dorsz', 'test0', 'results_None_True'

    # review_data_from_results(data_path_main, meat_type)
    show_labelled_results(data_path_main, meat_type, test_name, results_folder_name)
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
