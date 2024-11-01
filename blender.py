import cv2 as cv


class Blender:
    """
    Handles image blending settings for multiple image pairs in the GUI.
    """

    def __init__(self):
        """
        Initializes blending factors and images for different image pairs and blending types.
        """
        # Initialize blending factors for two image pairs
        self.pair_0_diff_blend = 0.5
        self.pair_0_conv_blend = 0.0
        self.pair_0_pollution_blend = 1.0
        self.pair_1_diff_blend = 0.5
        self.pair_1_conv_blend = 0.0
        self.pair_1_pollution_blend = 1.0

        # Placeholders for images to blend
        self.pair_0_diff_image = None
        self.pair_0_conv_image = None
        self.pair_0_pollution_image = None
        self.pair_1_diff_image = None
        self.pair_1_conv_image = None
        self.pair_1_pollution_image = None
        self.conveyor_image_mask = None

    def setup_windows_and_trackbars(self):
        """
        Sets up GUI windows and trackbars for blending adjustments.
        """
        # Create windows for displaying images
        cv.namedWindow('pair_0_diff_channel_image')
        cv.namedWindow('pair_1_diff_channel_image')

        # Trackbars for blending control of pair 0
        cv.createTrackbar('pair_0_diff_blend', 'pair_0_diff_channel_image', int(self.pair_0_diff_blend * 100), 100,
                          self.on_change_pair_0_diff_blend)
        cv.createTrackbar('pair_0_conv_blend', 'pair_0_diff_channel_image', int(self.pair_0_conv_blend * 100), 100,
                          self.on_change_pair_0_conv_blend)
        cv.createTrackbar('pair_0_pollution_blend', 'pair_0_diff_channel_image', int(self.pair_0_pollution_blend * 100),
                          100, self.on_change_pair_0_pollution_blend)

        # Trackbars for blending control of pair 1
        cv.createTrackbar('pair_1_diff_blend', 'pair_1_diff_channel_image', int(self.pair_1_diff_blend * 100), 100,
                          self.on_change_pair_1_diff_blend)
        cv.createTrackbar('pair_1_conv_blend', 'pair_1_diff_channel_image', int(self.pair_1_conv_blend * 100), 100,
                          self.on_change_pair_1_conv_blend)
        cv.createTrackbar('pair_1_pollution_blend', 'pair_1_diff_channel_image', int(self.pair_1_pollution_blend * 100),
                          100, self.on_change_pair_1_pollution_blend)

    def set_images(self, pair_0_diff_image, pair_0_conv_image, pair_0_pollution_image,
                   pair_1_diff_image, pair_1_conv_image, pair_1_pollution_image, conveyor_image_mask):
        """
        Set images to be blended for both pairs.
        """
        self.pair_0_diff_image = pair_0_diff_image
        self.pair_0_conv_image = pair_0_conv_image
        self.pair_0_pollution_image = pair_0_pollution_image
        self.pair_1_diff_image = pair_1_diff_image
        self.pair_1_conv_image = pair_1_conv_image
        self.pair_1_pollution_image = pair_1_pollution_image
        self.conveyor_image_mask = conveyor_image_mask

    def show_blend(self, pair: int):
        """
        Displays a blended image based on specified blend settings for a given image pair.
        """
        if pair == 0 and self.pair_0_diff_image is not None:
            blend_img = cv.addWeighted(self.pair_0_diff_image, self.pair_0_diff_blend, self.conveyor_image_mask,
                                       self.pair_0_conv_blend, 0)
            if self.pair_0_pollution_image is not None:
                blend_img = cv.addWeighted(blend_img, 1.0, self.pair_0_pollution_image, self.pair_0_pollution_blend, 0)
            cv.imshow("pair_0_diff_channel_image", blend_img)
        elif pair == 1 and self.pair_1_diff_image is not None:
            blend_img = cv.addWeighted(self.pair_1_diff_image, self.pair_1_diff_blend, self.conveyor_image_mask,
                                       self.pair_1_conv_blend, 0)
            if self.pair_1_pollution_image is not None:
                blend_img = cv.addWeighted(blend_img, 1.0, self.pair_1_pollution_image, self.pair_1_pollution_blend, 0)
            cv.imshow("pair_1_diff_channel_image", blend_img)

    # Callback functions to update blend factors and refresh display
    def on_change_pair_0_diff_blend(self, value):
        self.pair_0_diff_blend = value / 100.0
        self.show_blend(0)

    def on_change_pair_0_conv_blend(self, value):
        self.pair_0_conv_blend = value / 100.0
        self.show_blend(0)

    def on_change_pair_0_pollution_blend(self, value):
        self.pair_0_pollution_blend = value / 100.0
        self.show_blend(0)

    def on_change_pair_1_diff_blend(self, value):
        self.pair_1_diff_blend = value / 100.0
        self.show_blend(1)

    def on_change_pair_1_conv_blend(self, value):
        self.pair_1_conv_blend = value / 100.0
        self.show_blend(1)

    def on_change_pair_1_pollution_blend(self, value):
        self.pair_1_pollution_blend = value / 100.0
        self.show_blend(1)
