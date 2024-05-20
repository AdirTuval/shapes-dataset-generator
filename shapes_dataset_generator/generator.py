import numpy as np
from typing import Union

from shapes_dataset_generator.shapes_dataset_generator.sample_config import SampleConfigGenerator
from shapes_dataset_generator.shapes_dataset_generator.renderer import PILRenderer
from shapes_dataset_generator.shapes_dataset_generator.distribution import Distribution
from shapes_dataset_generator.shapes_dataset_generator.factors import Factors


class ShapesDatasetGenerator:
    """
    This class is responsible for generating a dataset of shapes.
    """

    def __init__(
        self,
        factors: list,
        render_config: Union[dict, None] = None,
        distribution_config: Union[dict, None] = None,
        sample_config: Union[dict, None] = None,
    ):
        self.latents: np.array = None
        self.samples: np.array = None

        self.factors = Factors(factors)
        self.renderer = PILRenderer(render_config)
        self.distribution = Distribution(distribution_config)
        self.sample_config_generator = SampleConfigGenerator(sample_config)

    def generate(self, n_samples: int = 1):
        """
        Main method for generating the dataset.

        Returns:
        - samples: A list of images of shapes.
        - latents: A list of corresponding latent vectors.
        """
        self.latents = self.generate_latents(n_samples)
        self.samples = self.generate_samples()
        return self.samples, self.latents

    def set_latents(self, latents: np.array):
        """
        Set the latent vectors for the dataset.

        Args:
        - latents: A list of latent vectors.
        """
        self.latents = latents
        return self

    def generate_latents(self, n_samples: int = 1):
        """
        Generate latent vectors for the dataset.
        """
        d = len(self.factors)
        return self.distribution.sample((n_samples, d)).numpy().reshape((n_samples, d))

    def generate_samples(self):
        """
        Generate samples for the dataset.
        """
        samples = map(
            lambda l: self.sample_config_generator.generate(self.factors.from_list(l)),
            self.latents,
        )
        samples = map(self.renderer.render, samples)
        samples = map(np.array, samples)
        return np.array(list(samples))
