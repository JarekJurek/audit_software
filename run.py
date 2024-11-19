"""Application bootstrap code."""
from pathlib import Path

from app import Reviewer
from path_manager import PathManager
from validator import Validator


def main():
    """Module's main loop."""
    data_path_main = r'/home/gregory/agromaks/test_0'  # To edit
    meat_type, test_name, results_folder_name = 'Dorsz', 'test0', 'results_None_True' # To edit

    validation_save_path = data_path_main  # To edit
    save_validation_plot = False  # To edit
    validation_plot_name = "confusion_matrix"  # To edit

    path_manager = PathManager(Path(data_path_main), meat_type, test_name, results_folder_name)

    reviewer = Reviewer(
        path_manager=path_manager,
        start_folder=1,  # To edit
        show_image_mask=True,  # To edit
        show_pkl=True,  # To edit
        show_blenders=True  # To edit
    )

    validator = Validator(
        path_manager=path_manager,
        save_results_path=Path(validation_save_path))

    reviewer.run()
    validator.run(save_validation_plot, validation_plot_name)


if __name__ == "__main__":
    main()
