"""Application bootstrap code."""
from pathlib import Path

from audit_software import Reviewer, PathManager, Validator


def main():
    """Module's main loop."""
    data_path_main = r'C:\Agromaks_tests\odbior_05_04_24'  # Editable
    meat_type, test_name, results_folder_name = 'Nerka wolowa', 'test0', 'results_None_True'  # Editable

    validation_save_path = Path(data_path_main) / meat_type  # Editable
    save_validation_plot = False  # Editable
    validation_plot_name = "confusion_matrix"  # Editable

    png_save_path = Path(data_path_main) / 'png_images' / meat_type  # Editable

    path_manager = PathManager(Path(data_path_main), meat_type, test_name, results_folder_name)

    reviewer = Reviewer(
        path_manager=path_manager,
        start_folder=1,  # Editable
        show_image_mask=True,  # Editable
        show_pkl=True,  # Editable
        show_blenders=True,  # Editable
        save_path = png_save_path
    )

    validator = Validator(
        path_manager=path_manager,
        save_results_path=Path(validation_save_path))

    reviewer.run()
    validator.run(save_validation_plot, validation_plot_name)


if __name__ == "__main__":
    main()
