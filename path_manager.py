"""Module for managing files."""
from pathlib import Path
from typing import List, Tuple

from utils import dir_list


class PathManager:
    """Manages paths for acquisition image series and results directories."""

    def __init__(self, data_path_main: Path, meat_name: str, test_name: str = None,
                 results_folder_name: str = 'results'):
        """
        Initializes PathManager with paths and naming information.

        :param data_path_main: Main directory where data is stored.
        :param meat_name: Name of the meat type directory.
        :param test_name: Specific test series name to filter results, defaults to None.
        :param results_folder_name: Folder name for results within the main data path, defaults to 'results'.
        """
        self.data_path_main = data_path_main
        self.meat_name = meat_name
        self.test_name = test_name
        self.results_folder_name = results_folder_name

    def get_series_paths(self) -> List[Tuple[str, str]]:
        """
        Generate paths to acquisition image series and results directories.

        :return: List of tuples containing:
            - series_path: Path to acquisition image series.
            - results_path: Corresponding path to results directory.
        """
        series_path_list = []
        linia_path_main = Path(self.data_path_main) / self.meat_name / 'data'

        for linia_path in dir_list(linia_path_main):
            test_path_main = linia_path_main / linia_path / self.meat_name

            for test_path in dir_list(test_path_main):
                if self.test_name and test_path != self.test_name:
                    continue  # Skip if test_name is specified and doesn't match

                series_path = test_path_main / test_path / '0' / 'camera_series'
                results_path = Path(
                    self.data_path_main) / self.meat_name / self.results_folder_name / linia_path / self.meat_name / test_path / '0'

                series_path_list.append((str(series_path), str(results_path)))

        return series_path_list

    @staticmethod
    def get_max_images(series_path: Tuple[str, str]) -> int:
        """
        Calculate the maximum index for images in a series directory.

        :param series_path: Tuple where series_path[1] points to the results directory.
        :return: Maximum image index (number of results paths multiplied by 10).
        """
        return len(dir_list(Path(series_path[1]))) * 10
