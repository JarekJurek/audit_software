import os
import cv2 as cv
import numpy as np
import csv
import json
import tkinter as tk

pollution_name = "empty"




def input_box():
    root = tk.Tk()
    canvas1 = tk.Canvas(root, width=200, height=150)
    canvas1.pack()
    entry1 = tk.Entry(root)
    canvas1.create_window(100, 70, window=entry1)  # input box placement

    def get_pollution_name():
        global pollution_name
        pollution_name = entry1.get()
        if pollution_name != "empty":
            print("Nowe zanieczyszczenie: ", pollution_name)
            # tutaj zapis danej pollution_name do JSONa
        label1 = tk.Label(root, text="Zapisano!")
        canvas1.create_window(100, 130, window=label1)  # output message box placement

    buttonLabel = tk.Button(text='Zapisz', command=get_pollution_name)
    canvas1.create_window(70, 100, window=buttonLabel)  # button placement

    quitButton = tk.Button(text='Wyjdź', command=root.destroy)
    canvas1.create_window(130, 100, window=quitButton)  # button placement

    def sel():
        selection = "You selected the option " + str(var.get())
        label.config(text=selection)

    var = tk.IntVar()

    R1 = tk.Radiobutton(root, text="Czerwony", variable=var, value=1, command=sel)
    R1.pack(anchor=tk.W)

    R2 = tk.Radiobutton(root, text="Zielony", variable=var, value=2, command=sel)
    R2.pack(anchor=tk.W)

    R3 = tk.Radiobutton(root, text="Niebieski", variable=var, value=3, command=sel)
    R3.pack(anchor=tk.W)

    R4 = tk.Radiobutton(root, text="Czarny", variable=var, value=4, command=sel)
    R4.pack(anchor=tk.W)

    R5 = tk.Radiobutton(root, text="Biały", variable=var, value=5, command=sel)
    R5.pack(anchor=tk.W)

    label = tk.Label(root)
    label.pack()

    root.mainloop()


def changing_dir_meat():  # zmienia ścieżkę w zależności od mięsa oraz zwraca ścieżkę wraz z nazwą mięsa
    meat_name = input('Podaj nazwe mięsa')
    meat_name = meat_name.strip()
    path_main = 'E:\\dane\\'  # początek ścieżki absolutnej
    path = os.path.join(path_main, meat_name, 'results')
    os.chdir(path)
    return path, meat_name


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


def main():
    path, meat_name = changing_dir_meat()  # nazwa mięsa oraz
    pathog = path  # ścieżka główna, która się nie zmienia
    lines = dir_list(path)  # lista linii
    total_lines = dir_counter(path)  # liczba folderów z linią
    line = 0  # potrzebne do chodzenia po listach
    photo = 0
    test = 0
    color = (255, 0, 0)
    font = cv.FONT_HERSHEY_SIMPLEX
    while True:
        path = os.path.join(pathog, lines[line], meat_name)
        tests = dir_list(path)
        total_tests = dir_counter(path)
        path1 = path  # pomocnicza do cofania
        path = os.path.join(path, tests[test], '0')
        photos = dir_list(path)
        photos.sort(key=int)
        total_photo = dir_counter(path)
        result_name = os.path.join(path, photos[photo], 'result.jpg')
        with open(jsonpath(os.path.join(path, photos[photo]))) as file:
            results_data = json.load(file)
        if os.path.exists(file_number_changer(4, os.path.join(path, photos[photo]))):
            image_name0 = file_number_changer(4, os.path.join(path, photos[photo]))
        else:
            image_name0 = file_number_changer(2, os.path.join(path, photos[photo]))
        image0 = cv.imread(image_name0)
        result = cv.imread(result_name)
        Hori = np.concatenate((image0, result), axis=1)  # łączyobrazki
        results = results_data["count"]
        cv.namedWindow("window", cv.WND_PROP_FULLSCREEN)
        cv.setWindowProperty("window", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
        cv.putText(Hori, f"Pollution : {results}", (1000, 20), font, 0.5, color, 1)
        cv.imshow('window', Hori)

        key = cv.waitKey(1)

        if key == ord('p'):
            input_box()

        elif key == ord('d'):
            photo = photo + 1
            if photo == total_photo:
                photo = 0
                test += 1
            if test == total_tests:
                line += 1
                test = 0
            if line == total_lines:
                print("koniec zdjec")
                break
        elif key == ord('a'):
            photo = photo - 1
            if photo == -1:
                test = test - 1
                path1 = os.path.join(path1, tests[test], '0')
                total_photo = dir_counter(path1)
                photo = total_photo - 1
                if test == -1:
                    line = line - 1
                    if line == -1:
                        print("Koniec foteczek")
                        break
                    path2 = os.path.join(pathog, lines[line], meat_name)
                    total_tests = dir_counter(path2)
                    test = total_tests - 1
                    path3 = os.path.join(path2, tests[test], '0')
                    total_photo = dir_counter(path3)
                    photo = total_photo - 1

        elif key == 27:
            break

    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
