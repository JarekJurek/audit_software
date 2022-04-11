import os
import cv2 as cv
import numpy as np
import csv
import json
import tkinter as tk

pollution_name = "empty"




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
