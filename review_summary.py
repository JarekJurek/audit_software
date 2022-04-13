import os
import cv2 as cv
import numpy as np
import json

from utilities import get_series_path_list, dir_list, pollution_database

def main():
    
    data_path_main = 'C:\\Users\\Janki\\Projects\\agromaks\\data'  # początek ścieżki absolutnej

    pollutions_summary = {}
    
    meat_types = dir_list(data_path_main)
    for meat_type in meat_types:
        
        meat_type_pollutions_summary = {}
        for pollution_type in pollution_database:
            meat_type_pollutions_summary[pollution_type] = 0

        series_path_list = get_series_path_list(meat_type, data_path_main)
        for series_path in series_path_list:
            series_labelled_file_path = os.path.join(series_path[1], 'series_labelled_metadata.json')
            with open(series_labelled_file_path, 'r') as labelled_file:
                series_labelled_metadata = json.load(labelled_file)
            
            for slm_index in range(1, len(series_labelled_metadata)+1):
                slm_key = 'result_' + str(slm_index)
                detected_pollutions = series_labelled_metadata[slm_key]["detected_pollutions"]
                for detected_pollution in detected_pollutions:
                    meat_type_pollutions_summary[detected_pollution['type']] += 1
        
        if meat_type in pollutions_summary:
            for pollution_type in meat_type_pollutions_summary:
                pollutions_summary[meat_type][pollution_type] += meat_type_pollutions_summary[pollution_type]
        else:
            pollutions_summary[meat_type] = meat_type_pollutions_summary

    summary_file_path = os.path.join(data_path_main, 'series_labelled_metadata_summary.json')
    with open(summary_file_path, 'w') as summary_file:
        json.dump(pollutions_summary, summary_file, indent=4,sort_keys=True)
        print('dumped summary to ' + summary_file_path)

if __name__ == "__main__":
    main()