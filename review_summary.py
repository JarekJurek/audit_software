import os
import cv2 as cv
import numpy as np
import json

from utilities import get_series_path_list

def main():
    meat_type = 'nerka_wieprzowa'
    series_path_list = get_series_path_list(meat_type)
    for series_path in series_path_list:
        series_labelled_file_path = os.path.join(series_path[1], 'series_labelled_metadata.json')
        with open(series_labelled_file_path, 'r') as labelled_file:
            series_labelled_metadata = json.load(labelled_file)
        print(series_labelled_metadata)

if __name__ == "__main__":
    main()