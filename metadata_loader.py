import json
import os
from typing import Tuple, Optional, Dict


def load_series_labelled_metadata(series_path: Tuple[str, str]) -> Optional[Dict]:
    """
    Load labelled metadata from a JSON file in the specified series path.

    :param series_path: Tuple with paths, where series_path[1] points to the directory with JSON files.
    :return: Parsed JSON data from the labelled series file, or None if no file is found.
    """
    files = [f for f in os.listdir(series_path[1]) if f.endswith(".json")]
    if files:
        series_labelled_file_path = os.path.join(series_path[1], files[0])
        with open(series_labelled_file_path, 'r') as labelled_file:
            series_labelled_metadata = json.load(labelled_file)
            print(f'Loaded series_labelled_metadata from {series_labelled_file_path}')
            return series_labelled_metadata
    return None


def load_one_series_description(series_path: Tuple[str, str]) -> Optional[Dict]:
    """
    Load metadata description from series_metadata.json.

    :param series_path: Tuple with paths, where series_path[0] points to the main series directory.
    :return: Parsed JSON data from series_metadata.json, or None if file is not found.
    """
    series_metadata_file_path = os.path.join(series_path[0], 'series_metadata.json')
    if os.path.exists(series_metadata_file_path):
        with open(series_metadata_file_path, 'r') as file:
            return json.load(file)
    print(f"Warning: series_metadata.json not found at {series_metadata_file_path}")
    return None


def load_one_series_metadata(series_description: Dict) -> Dict:
    """
    Extract metadata from a series description.

    :param series_description: JSON data containing series metadata.
    :return: Metadata from the series description.
    """
    return series_description.get('meta_data', {})
