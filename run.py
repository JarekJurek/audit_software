"""Application bootstrap code."""
from app import Reviewer


def main():
    """Module's main loop."""
    data_path_main = '/home/gregory/agromaks/test_0'  # początek ścieżki absolutnej
    meat_type, test_name, results_folder_name = 'Dorsz', 'test0', 'results_None_True'

    reviewer = Reviewer(
        data_path_main=data_path_main,
        meat_type=meat_type,
        test_name=test_name,
        results_folder_name=results_folder_name,
        show_image_mask=True,
        show_pkl=True,
        show_blenders=True
    )

    reviewer.run()


if __name__ == "__main__":
    main()
