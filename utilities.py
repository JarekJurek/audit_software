import os

def dir_list(path):  # ma zwracać listę folderów w folderze
    list = os.listdir(path)
    return list
    
def get_series_path_list(meat_name):
    series_path_list = []
    if meat_name is None:
        meat_name = input('Podaj nazwe mięsa')
        meat_name = meat_name.strip()
    data_path_main = 'C:\\Users\\Janki\\Projects\\agromaks\\data'  # początek ścieżki absolutnej
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