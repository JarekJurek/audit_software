"""Application bootstrap code."""
from app import Reviewer
from path_manager import PathManager


def main():
    """Module's main loop."""
    data_path_main = r'/home/gregory/agromaks/test_0'  # początek ścieżki absolutnej
    meat_type, test_name, results_folder_name = 'Dorsz', 'test0', 'results_None_True'

    path_manager = PathManager(data_path_main, meat_type, test_name, results_folder_name)

    reviewer = Reviewer(
        path_manager=path_manager,
        start_folder=1,
        show_image_mask=True,
        show_pkl=True,
        show_blenders=True
    )

    reviewer.run()


if __name__ == "__main__":
    main()
