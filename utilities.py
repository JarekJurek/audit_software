import os

# Dla Nerka wieprzowa:
# pollution_database =  [ "No pollution",
#                         "Z/9 - kaptur foliowy niebieski cienki",
#                         "Z/10 - kaptur foliowy niebieski średni",
#                         "Z/11 - kaptur foliowy niebieski gruby",
#                         "Z/19 - plastik  żółty",
#                         "Z/31 - rękawica niebieska bardzo cienka",
#                         "Z/32 - rękawica niebieska cienka",
#                         "Z/33 - rękawica niebieska gruba",
#                         "Z/20 - przekładka piankowa biała",
#                         "Z/29 - rękawica materiałowo gumowa niebiesko czarna",
#                         "Z/1 - drewno z palety jasne",
#                         "Z/2 - drzazgi z palety",
#                         "Z/6 - folia stretch transparentna",
#                         "Z/39 - papier / etykieta" ]

# Dla Sledziona wieprzowa:
pollution_database =  [ "No pollution",
                        "Z/9 - kaptur foliowy niebieski cienki",
                        "Z/10 - kaptur foliowy niebieski średni",
                        "Z/11 - kaptur foliowy niebieski gruby",
                        "Z/31 - rękawica niebieska bardzo cienka",
                        "Z/32 - rękawica niebieska cienka",
                        "Z/33 - rękawica niebieska gruba",
                        "Z/14 - plastik czerwony ciemne",
                        "Z/15 - plastik czerwony jasny",
                        "Z/19 - plastik  żółty",
                        "Z/12 - plastik  biały" ]


def dir_list(path):  # ma zwracać listę folderów w folderze
    list = os.listdir(path)
    return list

def get_series_path_list(meat_name, data_path_main):
    series_path_list = []
    if meat_name is None:
        meat_name = input('Podaj nazwe mięsa')
        meat_name = meat_name.strip()
    if data_path_main is None:
        data_path_main = input('Podaj sciezke do katalogu z danymi')
        data_path_main = data_path_main.strip()
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