"""Module for validating the detection system based on ground truth labels."""

from pathlib import Path
from typing import Optional

from image_loader import load_detection_data
from label_manager import get_image_labels
from path_manager import PathManager
from utils import dir_list
import matplotlib.pyplot as plt


class SeriesResults:
    """Calculated results from one image series.

    Attributes:
        true_positive (int): Number of correctly identified positives.
        false_positive (int): Number of incorrectly identified positives.
        true_negative (int): Number of correctly identified negatives.
        false_negative (int): Number of incorrectly identified negatives.
    """
    def __init__(self):
        self.true_positive = 0
        self.false_positive = 0
        self.true_negative = 0
        self.false_negative = 0


class Validator:
    """
    Validates the detection system by comparing detection outcomes with ground truth labels.

    Attributes:
        path_manager (PathManager): Manages paths to input series data.
        save_results_path (Path): Optional path to save validation results.
        results (SeriesResults): Stores the validation results after processing.
    """
    def __init__(self, path_manager: PathManager, save_results_path: Path = Path(__file__).parent):
        self.path_manager: PathManager = path_manager
        self.save_results_path: Path = save_results_path

        self.results: Optional[SeriesResults] = None

    def validate_series(self) -> SeriesResults:
        """
        Validates the detection system for a series of images.

        Returns:
            SeriesResults: Results containing counts of true positives, false positives,
                           true negatives, and false negatives.
        """
        series_path_list = self.path_manager.get_series_paths()
        self.results = SeriesResults()

        for series_path in series_path_list:
            results_folders = dir_list(Path(series_path[1]))

            for results_folder_number in range(1, len(results_folders)):  # Folders from 1 to X
                pkl_image_idx = (results_folder_number * 10) - 1

                detection, pollution_size = load_detection_data(series_path, results_folder_number)

                pkl_image_path = Path(series_path[0]) / "images" / f"ogx_image_{pkl_image_idx}.txt"
                labels = get_image_labels(pkl_image_path)  # Ground truth labels

                # Update results based on detection and labels
                if len(labels) > 0 and detection:
                    self.results.true_positive += 1
                elif len(labels) == 0 and detection:
                    self.results.false_positive += 1
                elif len(labels) == 0 and not detection:
                    self.results.true_negative += 1
                elif len(labels) > 0 and not detection:
                    self.results.false_negative += 1

        return self.results

    def summarize_results(self):
        """Prints a summary of the validation results, including precision, recall, and F1 score."""
        if not self.results:
            print("Error: Series needs to be validated first.")
            return

        tp = self.results.true_positive
        fp = self.results.false_positive
        tn = self.results.true_negative
        fn = self.results.false_negative

        print(f"True Positives: {tp}\nFalse Positives: {fp}\nTrue Negatives: {tn}\nFalse Negatives: {fn}")

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        print(f"Summary of Results:\n"
              f"  Precision: {precision:.2f}\n"
              f"  Recall: {recall:.2f}\n"
              f"  F1 Score: {f1_score:.2f}")

    def save_results(self):
        """Saves the validation results to a text file."""
        if not self.results:
            print("Error: Series needs to be validated first.")
            return

        path = self.save_results_path / "series_results.txt"
        with open(path, "w") as file:
            file.write(f"True Positives: {self.results.true_positive}\n")
            file.write(f"False Positives: {self.results.false_positive}\n")
            file.write(f"True Negatives: {self.results.true_negative}\n")
            file.write(f"False Negatives: {self.results.false_negative}\n")

        print(f"Results saved to {path}")

    def plot_confusion_matrix(self, save_plot: bool = False, plot_name: str = "confusion_matrix"):
        """
        Plots the confusion matrix for the validation results.

        Args:
            save_plot (bool): Whether to save the plot as a file. Defaults to False.
            plot_name (str): Name for the saved plot.
        """
        if not self.results:
            print("Error: Series needs to be validated first.")
            return

        # Confusion matrix data
        data = [
            [self.results.true_positive, self.results.false_negative],
            [self.results.false_positive, self.results.true_negative]
        ]

        # Create the plot
        fig, ax = plt.subplots()
        cax = ax.matshow(data, cmap='Blues')
        plt.colorbar(cax)

        # Set axis ticks and labels
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(['Positive', 'Negative'])
        ax.set_yticklabels(['Positive', 'Negative'])
        plt.xlabel("Detected")
        plt.ylabel("Actual")
        plt.title("Confusion Matrix")

        # Overlay the values on the plot
        for i in range(2):
            for j in range(2):
                ax.text(j, i, str(data[i][j]), va='center', ha='center', color='black', fontsize=12)

        # Save or display the plot
        if save_plot and self.save_results_path:
            plot_path = self.save_results_path / f"{plot_name}.png"
            plt.savefig(plot_path)
            print(f"Confusion matrix saved to {plot_path}")
        else:
            plt.show()

    def run(self, save_plot: bool=False, plot_name: str ="confusion_matrix"):
        """Runs the entire validation process and outputs results."""
        self.validate_series()
        self.summarize_results()
        self.plot_confusion_matrix(save_plot=save_plot, plot_name=plot_name)
