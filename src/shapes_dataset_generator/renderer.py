from typing import Union
import numpy as np
from PIL import Image, ImageDraw, ImageColor
from shapes_dataset_generator.sample_config import SampleConfig
from shapes_dataset_generator.consts import (
    DEFAULT_CANVAS_SIZE,
    DEFAULT_CANVAS_BACKGROUND_COLOR,
    DEFAULT_SAMPLE_COLOR_1,
    DEFAULT_SAMPLE_COLOR_2,
    ANTIALIAS,
    SIZE_HIGH,
    SIZE_LOW,
)

CANVAS_SIZE = "canvas_size"
BACKGROUND_COLOR = "background_color"
ANTI_ALIAS = "anti_alias"
SAMPLE_COLOR = "sample_color"
SAMPLE_COLOR_2 = "sample_color_2"


class PILRenderer:
    """
    This class is responsible for rendering an image of a shape.
    """

    def __init__(self, config: Union[dict, None] = None):
        self.config = self.fill_in_missing_default_values(config)
        self.convert_colors_to_rgb()

        # Set the configuration
        self.enlarged_canvas_size: tuple = (
            self.config[CANVAS_SIZE] * self.config[ANTI_ALIAS],
            self.config[CANVAS_SIZE] * self.config[ANTI_ALIAS],
        )
        self.original_canvas_size: tuple = (
            self.config[CANVAS_SIZE],
            self.config[CANVAS_SIZE],
        )
        
        # Reusable background
        self.canvas_background = Image.new(
            "RGB",
            self.enlarged_canvas_size,
            self.config[BACKGROUND_COLOR],
        )

        # Active canvas
        self.canvas = Image.new("RGB", self.enlarged_canvas_size)
        self.draw = ImageDraw.Draw(self.canvas)

    def render(self, sample_config: SampleConfig) -> Image:
        """
        Render an image of a shape.

        Args:
        - sample_config: A SampleConfig object.

        Returns:
        - image: A PIL Image object.
        """
        # Reset the canvas
        self.canvas.paste(self.canvas_background)

        # Draw the shape
        self.draw.regular_polygon(
            (
                *self.convert_sample_coordinates_to_image_coordinates(sample_config),
                self.get_sample_radius(sample_config.size),
            ),
            sample_config.get_n_sides(),
            fill=self.get_sample_color(sample_config.color),
        )

        # Resize the image
        resize_canvas = self.canvas.resize(self.original_canvas_size, Image.LANCZOS)
        # Return the image
        return resize_canvas

    def convert_colors_to_rgb(self):
        self.config[SAMPLE_COLOR] = ImageColor.getrgb(self.config[SAMPLE_COLOR])
        self.config[SAMPLE_COLOR_2] = ImageColor.getrgb(self.config[SAMPLE_COLOR_2])

    def fill_in_missing_default_values(self, config: dict) -> dict:
        """
        Validate the configuration, and fill in the missing values with the default values.

        Args:
        - config: A dictionary.
        """
        if type(config) is not dict:
            return self.get_default_config()
        
        default_dict = self.get_default_config()
        for key, value in default_dict.items():
            if key not in config:
                config[key] = value
        return config

    def get_sample_radius(self, size: float) -> float:
        """
        Get the radius of the sample.

        Args:
        - size: A float.

        Returns:
        - radius: A float.
        """
        diameter = self.get_sample_width(size) * (2 ** 0.5)
        return diameter / 2
    
    def get_sample_width(self, size: float) -> float:
        """
        width is in range [0.15, 0.35] of the canvas' width.
        """
        interpolated_size = SIZE_LOW + (SIZE_HIGH - SIZE_LOW) * size
        width_f = interpolated_size ** 0.5
        width = width_f * self.enlarged_canvas_size[0]
        return width
    
    def get_sample_color(self, color_val : float):
        high_color = np.array(self.config[SAMPLE_COLOR])
        low_color = np.array(self.config[SAMPLE_COLOR_2])
        interpolated_color = high_color * color_val + (1 - color_val) * low_color
        return tuple(interpolated_color.astype(int))

    def convert_sample_coordinates_to_image_coordinates(self, sample_config : SampleConfig) -> tuple:
        """
        Convert the sample coordinates to image coordinates.
        """
        x, y, size = sample_config.x, sample_config.y, sample_config.size
        offset = self.get_max_offset()
        effective_canvas_width_and_height = self.enlarged_canvas_size[0] - (offset * 2)
        x_coord = effective_canvas_width_and_height * x + offset
        y_coord = effective_canvas_width_and_height * y + offset
        return x_coord, y_coord

    def get_max_offset(self):
        return self.get_sample_width(1.0) / 2

    @staticmethod
    def get_default_config() -> dict:
        """
        Get the default configuration for the renderer.

        Returns:
        - config: A dictionary.
        """
        return {
            CANVAS_SIZE: DEFAULT_CANVAS_SIZE,
            BACKGROUND_COLOR: DEFAULT_CANVAS_BACKGROUND_COLOR,
            ANTI_ALIAS: ANTIALIAS,
            SAMPLE_COLOR: DEFAULT_SAMPLE_COLOR_1,
            SAMPLE_COLOR_2: DEFAULT_SAMPLE_COLOR_2,
        }
