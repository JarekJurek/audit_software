"""Application bootstrap code."""
from app import Reviewer


def main():
    """Module's main loop."""
    data_path_main = r'C:\Agromaks_tests\odbior_05_04_24'  # początek ścieżki absolutnej
    meat_type, test_name, results_folder_name = 'Nerka wolowa', 'test0', 'results_None_True'

    reviewer = Reviewer(
        data_path_main=data_path_main,
        meat_type=meat_type,
        test_name=test_name,
        results_folder_name=results_folder_name,
        start_folder=1,
        show_image_mask=True,
        show_pkl=True,
        show_blenders=True
    )

    reviewer.run()


if __name__ == "__main__":
    main()
