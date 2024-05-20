import numpy as np
from shapes_dataset_generator.shapes_dataset_generator.consts import (
    Shape,
    DEFAULT_SAMPLE_SIZE,
    DEFAULT_SAMPLE_COLOR,
    DEFAULT_SAMPLE_SHAPE,
    DEFAULT_SAMPLE_X,
    DEFAULT_SAMPLE_Y,
)

DEFAULT_SAMPLE_VALUES = {
    'x' : DEFAULT_SAMPLE_X,
    'y' : DEFAULT_SAMPLE_Y,
    'size' : DEFAULT_SAMPLE_SIZE,
    'color' : DEFAULT_SAMPLE_COLOR,
    'shape' : DEFAULT_SAMPLE_SHAPE,
}

class SampleConfig:
    """
    This class represents a sample.
    It contains all the information needed to render the sample.
    """

    def __init__(self, x: float, y: float, size: float, shape: Shape, color: float):
        self.x: float = x
        self.shape: Shape = shape
        self.y: float = y
        self.color: float = color
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


class SampleConfigGenerator:
    def __init__(self, default_sample_config: dict):
        if default_sample_config is None:
            default_sample_config = {}
        self.default_sample_config = default_sample_config
        for key in DEFAULT_SAMPLE_VALUES:
            if key not in self.default_sample_config:
                self.default_sample_config[key] = DEFAULT_SAMPLE_VALUES[key]

    def generate(self, data: dict):
        data = data.copy()
        for key in self.default_sample_config:
            if key not in data:
                data[key] = self.default_sample_config[key]
        
        return SampleConfig(**data)
