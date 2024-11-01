import os
from pathlib import Path
from typing import List


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
