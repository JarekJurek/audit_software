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

        if os.path.isdir(os.path.join(data_path_main, meat_type)):      
            
            meat_type_pollutions_summary = {}
            for pollution_type in pollution_database:
                meat_type_pollutions_summary[pollution_type] = {}
                meat_type_pollutions_summary[pollution_type]['True positive'] = 0
                meat_type_pollutions_summary[pollution_type]['True negative'] = 0
                meat_type_pollutions_summary[pollution_type]['False positive'] = 0
                meat_type_pollutions_summary[pollution_type]['False negative'] = 0

            series_path_list = get_series_path_list(meat_type, data_path_main)
            for series_path in series_path_list:
                series_labelled_file_path = os.path.join(series_path[1], 'series_labelled_metadata.json')
                if os.path.exists(series_labelled_file_path):
                    with open(series_labelled_file_path, 'r') as labelled_file:
                        series_labelled_metadata = json.load(labelled_file)
                    
                    for slm_index in range(1, len(series_labelled_metadata)+1):
                        slm_key = 'result_' + str(slm_index)
                        detected_pollutions = series_labelled_metadata[slm_key]["detected_pollutions"]
                        for detected_pollution in detected_pollutions:
                            convusion_value = detected_pollution['confusion_value']
                            pollution_type = detected_pollution['type']
                            meat_type_pollutions_summary[pollution_type][convusion_value] += 1
            
                    if meat_type in pollutions_summary:
                        for pollution_type in meat_type_pollutions_summary:
                            for convusion_value in pollution_type['confusion_value']:
                                pollutions_summary[meat_type][pollution_type][convusion_value] += meat_type_pollutions_summary[pollution_type][convusion_value]
                    else:
                        pollutions_summary[meat_type] = meat_type_pollutions_summary

    summary_file_path = os.path.join(data_path_main, 'series_labelled_metadata_summary.json')
    with open(summary_file_path, 'w') as summary_file:
        json.dump(pollutions_summary, summary_file, indent=4,sort_keys=True)
        print('dumped summary to ' + summary_file_path)

if __name__ == "__main__":
    main()