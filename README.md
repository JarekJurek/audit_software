# Evaluation and Labelling Software

Project for displaying and creating labels on results images to evaluate the detection program.

The system supports interactive labeling, viewing, validation, and management of pollution labels, helping to identify and
address contamination issues.

## Project Description

### Main Modules

- **app.py**: Initializes and runs the `Reviewer` class to handle images and labels management.
- **validator.py**: Initializes and runs the `Validator` class to handle validating of the detection system.
- **label_manager.py**: Manages pollution labels, including adding, displaying, saving, and deleting labels for individual images.
- **io_controller.py**: Handles user input (key presses) for navigation, labeling actions, and deleting labels.
- **blender.py**: Manages blending and processing of multiple images for visualization.
- **image_loader.py**: Loads and preprocesses images for analysis and display.
- **path_manager.py**: Manages file paths and organizes image series for easy access.
- **utils.py**: Contains utility functions, including the callback function for drawing bounding boxes on images.

### Basic Functions

- **Displaying Images**: The program loads .pkl images from specified directories and displays them with existing labels overlaid.
- **Labeling Pollution**: Users can manually label areas of plastic pollution by drawing bounding boxes directly on the displayed image. Labels are saved in YOLO format for each image.
- **Clearing Labels**: Labels can be deleted from a displayed image, refreshing the view to show the image without any labels.
- **Validation**: Evaluates the detection system by:
  - Counting true positives, false positives, true negatives, and false negatives.
  - Generating a confusion matrix for results visualization.
  - Computing metrics like precision, recall, and F1 score.
  - Saving validation results to a file.

## Requirements

Install the dependencies listed in `requirements.txt`:
```commandline
pip install -r requirements.txt
```

For Linux systems, run the following command to install additional dependencies:
```commandline
sudo apt install python3-tk
```

Also, install the custom ogximg package from the Agromaks_ogx-image directory:

```commandline
python3 -m pip install -e .
```

## Usage

Labeling is possible on pkl_image. Blended images and image-mask pair are for evaluation.
The validation module starts when the labeling is done (labelling/reviewing program is closed).

In `run.py`, the following adjustable parameters allow you to customize the input data and program options:

```Python
data_path_main = '/home/gregory/agromaks/test_0'  # Path to the main data directory.
meat_type = 'Dorsz'  # Specifies the type of meat.
test_name = 'test0'  # Sets the test name for organizing data.
results_folder_name = 'results_None_True'  # Directory name for results.

validation_save_path = data_path_main  # Path for saving validation results.
save_validation_plot = False  # Boolean flag to save the confusion matrix plot.
validation_plot_name = "confusion_matrix"  # Confusion matrix file name

start_folder = 1  # Folder index to start the review process. The default is 1.
show_image_mask = True  # Boolean flag to display the image mask.
show_pkl = True  # Boolean flag to display the pkl_image.
show_blenders = False  # Boolean flag to display blended images.
```

Run the application with:

```commandline
python run.py
```

## Key User Controls

- **Navigation**:
  - **w**: Move forward by one image.
  - **s**: Move backward by one image.
  - **d**: Move forward by 10 images.
  - **a**: Move backward by 10 images.
  
- **Labeling and Deleting**:
  - **Left-click and drag on pkl_image**: Draw a bounding box on the image to label pollution.
  - **u**: Delete all labels for the currently displayed image and refresh the view.
  
- **Exit**:
  - **q** or **ESC**: Quit the application.

- **Validation**:
  - Validation is triggered automatically after closing the `Reviewer` process.
