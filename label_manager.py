import cv2 as cv


class LabelManager:
    """
    Manages labeling of detected pollution regions in images.
    """

    def __init__(self, pollution_database):
        """
        Initializes LabelManager with a pollution database.

        :param pollution_database: List of pollution types.
        """
        self.pollution_database = pollution_database
        self.labelled_pollutions = []
        self.ref_point = []  # Replaces global refPt
        self.cropping = False  # Replaces global cropping

    def add_pollution(self, pollution_index: int, start_point: tuple, end_point: tuple):
        """
        Add a pollution annotation to the labelled_pollutions list.

        :param pollution_index: Index of the pollution type.
        :param start_point: Start point of the pollution rectangle.
        :param end_point: End point of the pollution rectangle.
        """
        if self.pollution_database[pollution_index] != "No pollution":
            pollution = {
                'type': self.pollution_database[pollution_index],
                'location_rectangle': (start_point, end_point),
                'confusion_value': None
            }
            self.labelled_pollutions.append(pollution)

    def mark_pollution(self, event, x, y, current_pollution_index: int, image):
        """
        Mark a pollution area based on mouse drag events and draw a rectangle.

        :param event: Mouse event type.
        :param x: X-coordinate of the event.
        :param y: Y-coordinate of the event.
        :param current_pollution_index: Index of the current pollution type.
        :param image: The image on which the pollution rectangle is drawn.
        """
        if event == cv.EVENT_LBUTTONDOWN:
            self.ref_point = [(x, y)]
            self.cropping = True
        elif event == cv.EVENT_LBUTTONUP:
            self.ref_point.append((x, y))
            self.cropping = False
            current_pollutions_color = (0, 255, 0)
            cv.rectangle(image, self.ref_point[0], self.ref_point[1], current_pollutions_color, 2)
            self.add_pollution(current_pollution_index, self.ref_point[0], self.ref_point[1])
            cv.imshow('window', image)
