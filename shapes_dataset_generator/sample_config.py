import numpy as np
from shapes_dataset_generator.shapes_dataset_generator.consts import (
    Shape,
    Color,
    DEFAULT_SAMPLE_SIZE,
    DEFAULT_SAMPLE_COLOR,
    DEFAULT_SAMPLE_SHAPE,
)


class SampleConfig:
    """
    This class represents a sample.
    It contains all the information needed to render the sample.
    """

    def __init__(
        self,
        x: float,
        y: float,
        size: float = DEFAULT_SAMPLE_SIZE,
        shape: Shape = DEFAULT_SAMPLE_SHAPE,
        color: Color = DEFAULT_SAMPLE_COLOR,
    ):
        self.x: float = x
        self.shape: Shape = shape
        self.y: float = y
        self.color: Color = color
        self.size: float = size

    def get_n_sides(self) -> int:
        """
        Get the number of sides of the shape.

        Returns:
        - side_num: An integer.
        """
        return self.shape.value

    def get_color(self) -> str:
        """
        Get the color of the shape.

        Returns:
        - color: A string.
        """
        return self.color.value
