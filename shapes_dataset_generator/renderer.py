from PIL import Image, ImageDraw
from shapes_dataset_generator.shapes_dataset_generator.sample_config import SampleConfig
from shapes_dataset_generator.shapes_dataset_generator.consts import (
    DEFAULT_CANVAS_WIDTH,
    DEFAULT_CANVAS_HEIGHT,
    DEFAULT_CANVAS_BACKGROUND_COLOR,
    ANTIALIAS
)





class PILRenderer:
    """
    This class is responsible for rendering an image of a shape.
    """

    def __init__(
        self,
        canvas_width: int = DEFAULT_CANVAS_WIDTH,
        canvas_height: int = DEFAULT_CANVAS_HEIGHT,
        background_color: str = DEFAULT_CANVAS_BACKGROUND_COLOR,
        anti_alias: int = ANTIALIAS,
    ):
        self.enlarged_canvas_size: tuple = (
            canvas_width * anti_alias,
            canvas_height * anti_alias,
        )
        self.original_canvas_size: tuple = (canvas_width, canvas_height)
        self.background_color: str = background_color
        self.anti_alias: int = anti_alias

        # Reusable background
        self.canvas_background = Image.new(
            "RGB",
            self.enlarged_canvas_size,
            self.background_color,
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
                sample_config.x * self.enlarged_canvas_size[0],
                sample_config.y * self.enlarged_canvas_size[1],
                sample_config.size * self.anti_alias,
            ),
            sample_config.get_n_sides(),
            fill=sample_config.get_color(),
        )

        # Resize the image
        resize_canvas = self.canvas.resize(self.original_canvas_size, Image.LANCZOS)
        # Return the image
        return resize_canvas
