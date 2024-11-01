from reviewer import Reviewer


def main():
    data_path_main = '/home/gregory/agromaks/test_0'  # początek ścieżki absolutnej
    meat_type, test_name, results_folder_name = 'Dorsz', 'test0', 'results_None_True'
    pollution_database = ["No pollution",
                          "Zielony",
                          "Niebieski",
                          "Czarny",
                          "Bialy",
                          "Szary",
                          "Czerwony",
                          "Zolty",
                          "Pomaranczowy"]

    reviewer = Reviewer(
        data_path_main=data_path_main,
        meat_type=meat_type,
        test_name=test_name,
        results_folder_name=results_folder_name,
        pollution_database=pollution_database
    )

    reviewer.run()


if __name__ == "__main__":
    main()
