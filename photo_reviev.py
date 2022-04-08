import os
import cv2 as cv
import numpy as np
import csv
import json

def changing_dir_meat(): #zmienia ścieżkę w zależności od mięsa oraz zwraca ścieżkę wraz z nazwą mięsa
    meat_name=input('Podaj nazwe mięsa')
    meat_name=meat_name.strip()
    path_main='D:\\praca\\'  #początek ścieżki absolutnej
    path=os.path.join(path_main, meat_name, 'wyniki')
    os.chdir(path)
    #print(path)
    return path, meat_name


def dir_list(path): #ma zwracać listę folderów w folderze
    list = os.listdir(path)
    return list


def dir_counter(path): #liczy ilość foderów w ścieżce
    TotalDir=0
    for dirs in os.listdir(path):
        if os.path.isdir(path):
            TotalDir += 1
    return TotalDir

def file_number_changer(image_number, path): #zmienia ścieżkę do pliku ze zdjeciem
    image_name='base_image_'
    image_extension='.jpg'
    image_name=f'{image_name}{image_number}{image_extension}'
    image_path=os.path.join(path,image_name)
    #print(image_name)
    #eturn image_name
    return image_path


def jsonpath(path): #tworzy scieżke do jsona
    json_name='data.json'
    json_path=os.path.join(path, json_name)
    return json_path


def main():
    path, meat_name = changing_dir_meat() #nazwa mięsa oraz
    pathog=path #ścieżka główna, która się nie zmienia
    lines = dir_list(path) #lista linii
    total_lines = dir_counter(path) #liczba folderów z linią
    #print(total_lines)
    line = 0  # potrzebne do chodzenia po listach
    photo = 0
    test = 0
    color = (255, 0, 0)
    font = cv.FONT_HERSHEY_SIMPLEX
    #print(lines, tests, photos)
    while True:
        path = os.path.join(pathog, lines[line], meat_name)
        #print(path)
        tests = dir_list(path)
        total_tests = dir_counter(path)
        #print(total_tests)
        path = os.path.join(path, tests[test], '0')
        photos = dir_list(path)
        photos.sort(key=int)
        total_photo = dir_counter(path)
        result_name = os.path.join(path, photos[photo], 'result.jpg')
        with open(jsonpath(os.path.join(path, photos[photo]))) as file:
            results_data = json.load(file)
        with open(jsonpath(os.path.join(path, photos[photo]))) as file:
            results_data = json.load(file)
        #print(os.path.join(path, photos[photo]))
        if os.path.exists(file_number_changer(4, os.path.join(path, photos[photo]))):
            image_name0 = file_number_changer(4, os.path.join(path, photos[photo]))
        else :
            image_name0 = file_number_changer(2, os.path.join(path, photos[photo]))
        image0 = cv.imread(image_name0)
        result = cv.imread(result_name)
        Hori = np.concatenate((image0,result), axis=1) #łączyobrazki
        results = results_data["count"]
        #print(results)
        cv.namedWindow("window", cv.WND_PROP_FULLSCREEN)
        cv.setWindowProperty("window", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
        cv.putText(Hori,f"Pollution : {results}",[1100,20],font,0.5,color,1)
        cv.imshow('window',Hori)
        key = cv.waitKey(1)
        if key == ord('d'):
            photo = photo + 1
            if photo == total_photo:
                photo = 0
                test += 1
            if test == total_tests:
                line += 1
                test = 0
                # print(line)
            if line == total_lines:
                    break
        elif key == ord('a'):
            if photo == 0:
                if test == 0:
                    if line == 0:
                        print("koniec foteczek")
                        break
                    else:
                        line = line - 1
                else:
                    test = test - 1
            else:
             photo = photo - 1

        elif key == 27:
            break

    cv.destroyAllWindows()







if __name__ == "__main__":
    main()
