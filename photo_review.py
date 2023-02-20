import os
import cv2 as cv
import numpy as np
import csv
import json
import pickle
import tkinter as tk

from pkg_resources import add_activation_listener
# import OGXImage

pollution_name = "empty"

pollution_database =  [ "No pollution",
                        "Zielony",
                        "Niebieski",
                        "Czarny",
                        "Bialy",
                        "Szary",
                        "Czerwony",
                        "Zolty",
                        "Pomaranczowy" ]

def input_box():
    root = tk.Tk()
    canvas1 = tk.Canvas(root, width=200, height=60)
    canvas1.pack()

    var1 = tk.IntVar()
    var2 = tk.IntVar()
    var3 = tk.IntVar()
    var4 = tk.IntVar()
    var5 = tk.IntVar()
    var6 = tk.IntVar()
    var7 = tk.IntVar()
    var8 = tk.IntVar()
    var9 = tk.IntVar()

    R1 = tk.Checkbutton(root, text="False positive", variable=var1, onvalue=1, offvalue=0)
    R1.pack(anchor=tk.W)

    R2 = tk.Checkbutton(root, text="Zielony", variable=var2, onvalue=1, offvalue=0)
    R2.pack(anchor=tk.W)

    R3 = tk.Checkbutton(root, text="Niebieski", variable=var3, onvalue=1, offvalue=0)
    R3.pack(anchor=tk.W)

    R4 = tk.Checkbutton(root, text="Czarny", variable=var4, onvalue=1, offvalue=0)
    R4.pack(anchor=tk.W)

    R5 = tk.Checkbutton(root, text="Biały", variable=var5, onvalue=1, offvalue=0)
    R5.pack(anchor=tk.W)

    R6 = tk.Checkbutton(root, text="Szary", variable=var6, onvalue=1, offvalue=0)
    R6.pack(anchor=tk.W)

    R7 = tk.Checkbutton(root, text="Czerwony", variable=var7, onvalue=1, offvalue=0)
    R7.pack(anchor=tk.W)

    R8 = tk.Checkbutton(root, text="Żółty", variable=var8, onvalue=1, offvalue=0)
    R8.pack(anchor=tk.W)

    R9 = tk.Checkbutton(root, text="Pomarańczowy", variable=var9, onvalue=1, offvalue=0)
    R9.pack(anchor=tk.W)

    label = tk.Label(root)
    label.pack()

    def save_choice():
        dataBase = {
            "False positive": var1.get(),
            "Zielony": var2.get(),
            "Niebieski": var3.get(),
            "Czarny": var4.get(),
            "Biały": var5.get(),
            "Szary": var6.get(),
            "Czerwony": var7.get(),
            "Żółty": var8.get(),
            "Pomarańczowy": var9.get(),
        }
        for key, value in dataBase.items():
            if value is not 0:
                print(key)  # tą wartość (konkretny kolor) należy tutaj zpisać do pliku razem ze ścieżką
        label1 = tk.Label(root, text="Zapisano!")
        canvas1.create_window(100, 60, window=label1)  # output message box placement

    buttonLabel = tk.Button(text='Zapisz', command=save_choice)
    canvas1.create_window(70, 30, window=buttonLabel)  # button placement

    quitButton = tk.Button(text='Wyjdź', command=root.destroy)
    canvas1.create_window(130, 30, window=quitButton)  # button placement

    root.mainloop()


def changing_dir_meat(data_path_main, meat_name):  # zmienia ścieżkę w zależności od mięsa oraz zwraca ścieżkę wraz z nazwą mięsa
    if meat_name is None:
        meat_name = input('Podaj nazwe mięsa')
        meat_name = meat_name.strip()
    # path_main = 'C:\\Users\\Janki\\Projects\\agromaks\\data'  # początek ścieżki absolutnej
    path = os.path.join(data_path_main, meat_name, 'results')
    os.chdir(path)
    return path, meat_name

def get_series_path_list(data_path_main, meat_name):
    series_path_list = []
    if meat_name is None:
        meat_name = input('Podaj nazwe mięsa')
        meat_name = meat_name.strip()
    data_path_main = 'C:\\Users\\linnia1\\Desktop\\test_02_22\\'  # początek ścieżki absolutnej
    linia_path_main = os.path.join(data_path_main, meat_name, 'data')
    linia_paths = dir_list(linia_path_main)
    for linia_path in linia_paths:
        test_path_main = os.path.join(linia_path_main, linia_path, meat_name)
        test_paths = dir_list(test_path_main)
        for test_path in test_paths:
            series_path = os.path.join(test_path_main, test_path, '0', 'camera_series')
            results_path = os.path.join(data_path_main, meat_name, 'results', linia_path, meat_name, test_path, '0')
            series_path_list.append((series_path, results_path))
    return series_path_list

def dir_list(path):  # ma zwracać listę folderów w folderze
    list = os.listdir(path)
    return list


def dir_counter(path):  # liczy ilość foderów w ścieżce
    TotalDir = 0
    for dirs in os.listdir(path):
        if os.path.isdir(path):
            TotalDir += 1
    return TotalDir


def file_number_changer(image_number, path):  # zmienia ścieżkę do pliku ze zdjeciem
    image_name = 'base_image_'
    image_extension = '.jpg'
    image_name = f'{image_name}{image_number}{image_extension}'
    image_path = os.path.join(path, image_name)
    return image_path


def jsonpath(path):  # tworzy scieżke do jsona
    json_name = 'data.json'
    json_path = os.path.join(path, json_name)
    return json_path

def detected_is_inside_labelled_pollution(labelled_pollution, results_image):
    labelled_pollution_location_rectangle = labelled_pollution['location_rectangle'] 
    pollution_start_point = labelled_pollution_location_rectangle[0]
    pollution_end_point = labelled_pollution_location_rectangle[1]
    labelled_pollution_results_image = results_image[pollution_start_point[1]:pollution_end_point[1], 
                                                     pollution_start_point[0]:pollution_end_point[0]]
    values = np.where((labelled_pollution_results_image == (255,255,255)).all(axis=2))
    return len(values) > 0

def generate_detected_pollutions(image_size, detected_results, results_image):
    global labelled_pollutions
    detected_pollutions = []

    if len(labelled_pollutions) == 0 and detected_results == True:
        # False positive
        pollution_start_point = (0, 0)
        pollution_end_point = (image_size[0], image_size[1])
        pollution = {'type': pollution_database[0], #no pollution 
                    'location_rectangle': (pollution_start_point, pollution_end_point),
                    'confusion_value': "False positive"}
        detected_pollutions.append(pollution)
    elif len(labelled_pollutions) > 0 and detected_results == True:
        # True positive (and False negative)
        for labelled_pollution in labelled_pollutions:
            detected_pollution = labelled_pollution
            if detected_is_inside_labelled_pollution(labelled_pollution, results_image):
                detected_pollution['confusion_value'] = "True positive"
            else:
                detected_pollution['confusion_value'] = "False negative"
            detected_pollutions.append(detected_pollution)

    elif len(labelled_pollutions) == 0 and detected_results == False:
        # True negative
        pollution_start_point = (0, 0)
        pollution_end_point = (image_size[0], image_size[1])
        pollution = {'type': pollution_database[0], #no pollution 
                    'location_rectangle': (pollution_start_point, pollution_end_point),
                    'confusion_value': "True negative"}
        detected_pollutions.append(pollution)

    elif len(labelled_pollutions) > 0 and detected_results == False:
        # False negative
        for labelled_pollution in labelled_pollutions:
            detected_pollution = labelled_pollution
            detected_pollution['confusion_value'] = "False negative"
            detected_pollutions.append(detected_pollution)

    return detected_pollutions

def add_pollution(pollution_index, pollution_start_point, pollution_end_point):
    global labelled_pollutions
    
    if pollution_database[p] != "No pollution":
        pollution = {'type': pollution_database[pollution_index], 
                    'location_rectangle': (pollution_start_point, pollution_end_point),
                    'confusion_value': None}
        labelled_pollutions.append(pollution)

def generate_label_data(meat_type):
    global labelled_pollutions
    label_data = {'conveyor_type': 1,
                  'meat_type': meat_type,
                  'pollutions': labelled_pollutions}

    return label_data

def add_label_data(image_description, meat_type):
    label_data = generate_label_data(meat_type)
    image_description['label_data'] = label_data

def add_detected_pollutions(image_description, image_size, detected_results, results_image):
    detected_pollutions = generate_detected_pollutions(image_size, detected_results, results_image)
    image_description['detected_pollutions'] = detected_pollutions

# def review_data_from_pickles(meat_type):
#     series_path_list = get_series_path_list(meat_type)
#     for series_path in series_path_list:
#         series_metadata_file_path = os.path.join(series_path[0], 'series_metadata.json')
#         with open(series_metadata_file_path, 'r') as file:
#             series_description = json.load(file)
#         series_meta_data = series_description['meta_data']
#         series_image_data = series_meta_data['image_meta_data']
#         for i in range(0, len(series_image_data), 10):
#             image_key = 'ogx_image_' + str(i)
#             pickle_image_path = os.path.join(series_path[0], 'images', image_key + '.pkl')
#             if os.path.exists(pickle_image_path):
#                 with open(pickle_image_path, "rb") as image_file: #todo use OGXImage.from_pickle(pickle_image_path)  
#                     ogx_image = pickle.load(image_file) 
#                 #todo update pickle path in ogx_image
#                 image = ogx_image._image_data
#                 image_size = image.shape
#                 cv.imshow("iamge", cv.resize(image, (512, 512)) )
#                 results_image_path = os.path.join(series_path[1], str(i//10+1), 'result.jpg')
#                 print(pickle_image_path)
#                 print(results_image_path)
#                 results_image = cv.imread(results_image_path)
#                 cv.imshow("results_image", cv.resize(results_image, (512, 512)) )
#                 key = cv.waitKey(0)
#                 add_label_data(series_description['meta_data']['image_meta_data'][image_key], meat_type)
#                 add_detected_pollutions(series_description['meta_data']['image_meta_data'][image_key], image_size, detected_results)
#         # save labelled series json 
#         series_labelled_file_path = os.path.join(series_path[0], 'series_lebelled_metadata.json')
#         with open(series_labelled_file_path, 'w') as labelled_file:
#             json.dump(series_description, labelled_file, indent=4,sort_keys=True)

# mouse callback function
def mark_pollution(event,x,y,flags,param):
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

def gui_control(base_image, results_image, detected_results, max_i, max_p):
    detected_pollutions_color = (255, 0, 0)
    current_pollutions_color = (0, 255, 0)
    font = cv.FONT_HERSHEY_SIMPLEX

    global concaterated_image
    # cv.imshow("base_iamge", cv.resize(base_image, (512, 512)) )
    # cv.imshow("results_image", cv.resize(results_image, (512, 512)) )

    if results_image.shape[0] < base_image.shape[0] and results_image.shape[1] < base_image.shape[1]:
        value = [0, 0, 0]
        top = int((base_image.shape[0] - results_image.shape[0])/2)
        bottom = top
        left = int((base_image.shape[1] - results_image.shape[1])/2)
        right = left
        results_image = cv.copyMakeBorder(results_image, top, bottom, left, right, cv.BORDER_CONSTANT, None, value)
    concaterated_image = np.concatenate((base_image, results_image), axis=1)
    cv.namedWindow("window")#, cv.WND_PROP_FULLSCREEN)

    cv.setMouseCallback('window', mark_pollution)
    cv.putText(concaterated_image, f"Detected pollution : {detected_results}", (900, 20), font, 0.5, detected_pollutions_color, 1)
    global p 
    cv.putText(concaterated_image, f"Current pollution : {pollution_database[p]}", (900, 40), font, 0.5, current_pollutions_color, 1)
    
    global labelled_pollutions
    for lpi in range(0, len(labelled_pollutions)):
        previous_pollutions_color = (0, 255, 255)
        labelled_pollution = labelled_pollutions[lpi]
        cv.putText(concaterated_image, f"Labelled pollution : {labelled_pollution['type']}", (900, 60 + 20*lpi), font, 0.5, previous_pollutions_color, 1)
        labelled_pollution_location_rectangle = labelled_pollution['location_rectangle'] 
        pollution_start_point = labelled_pollution_location_rectangle[0]
        pollution_end_point = labelled_pollution_location_rectangle[1]
        cv.rectangle(concaterated_image, pollution_start_point, pollution_end_point, previous_pollutions_color, 2)
    
    cv.imshow('window', concaterated_image)

    key = cv.waitKey(0)

    global i

    if key == ord('j'):# choose pollution type
        p -= 1
        if p < 0:
            p = max_p - 1
    if key == ord('l'):# choose pollution type
        p += 1
        if p >= max_p:
            p = 0
    elif key == ord('d'):# choose image
        i += 10
        if i >= max_i:
            print("koniec zdjec")
            return True
    elif key == ord('a'):# choose image
        i -= 10
        if i < 0:
            i = 0
    elif key == 27:
        return True
    
    return False

def review_data_from_results(data_path_main, meat_type):
    series_path_list = get_series_path_list(data_path_main, meat_type)
    for series_path in series_path_list:
        series_metadata_file_path = os.path.join(series_path[0], 'series_metadata.json')
        with open(series_metadata_file_path, 'r') as file:
            series_description = json.load(file)
        
        series_labelled_metadata = {}

        series_meta_data = series_description['meta_data']
        series_image_data = series_meta_data['image_meta_data']

        global p # pollution index
        p = 0

        global i, prev_i # image index
        prev_i = -1
        i = 0
        max_i = (len(series_image_data)//10)*10
        while True:
        # for i in range(0, len(series_image_data), 10):
            global refPt, cropping
            refPt = []
            cropping = False

            image_key = 'ogx_image_' + str(i)
            pickle_image_path = os.path.join(series_path[0], 'images', image_key + '.pkl')
            print(pickle_image_path)
            series_description['meta_data']['image_meta_data'][image_key]['pickle_path'] = pickle_image_path #update pickle_path
            
            results_folder_number = i//10+1
            
            base_image_path = os.path.join(series_path[1], str(results_folder_number), 'base_image_0.jpg')          
            print(base_image_path)
            base_image = cv.imread(base_image_path) 

            results_image_path = os.path.join(series_path[1], str(results_folder_number), 'result_clean.jpg')
            print(results_image_path)
            results_image = cv.imread(results_image_path)

            detected_results_path = os.path.join(series_path[1], str(results_folder_number), 'data.json')  
            with open(detected_results_path) as detected_results_file:
                detected_results_data = json.load(detected_results_file)
            detected_results = detected_results_data["count"]
            
            global labelled_pollutions
            if prev_i != i:
                labelled_pollutions = []

            prev_i = i
            is_brake = gui_control(base_image, results_image, detected_results, max_i, len(pollution_database))
            
            #add new entry
            new_entry_name = 'result_' + str(results_folder_number)
            series_labelled_metadata[new_entry_name] = {}

            # add all base images wrt result to metadata info
            image_set_metadata = {}
            for j in range((prev_i//10)*10 + 0, (prev_i//10)*10 + 10):
                image_key_j = 'ogx_image_' + str(j)
                pickle_image_path_j = os.path.join(series_path[0], 'images', image_key_j + '.pkl')
                # print(pickle_image_path_j)
                image_set_metadata[image_key_j] = series_description['meta_data']['image_meta_data'][image_key_j]
            series_labelled_metadata[new_entry_name]['image_set_metadata'] = image_set_metadata

            image_size = base_image.shape
            add_label_data(series_labelled_metadata[new_entry_name], meat_type)
            add_detected_pollutions(series_labelled_metadata[new_entry_name], image_size, detected_results, results_image)
            print('added label data and detected pollutions')
            
            if is_brake:
                # save labelled series json 
                series_labelled_file_path = os.path.join(series_path[1], 'series_labelled_metadata.json')
                with open(series_labelled_file_path, 'w') as labelled_file:
                    json.dump(series_labelled_metadata, labelled_file, indent=4,sort_keys=True)
                    print('dumped results to ' + series_labelled_file_path)
                break

# def config_gui():
#     global refPt, cropping
#     refPt = []
#     cropping = False

def main():
    # config_gui()
    data_path_main = 'C:\\Users\\linnia1\\Desktop\\test_02_22'  # początek ścieżki absolutnej
    meat_type = 'Nerka wieprzowa'
    # review_data_from_pickles(meat_type)
    review_data_from_results(data_path_main, meat_type)
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
