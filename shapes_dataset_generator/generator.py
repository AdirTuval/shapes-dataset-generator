import numpy as np
from typing import Union
import torch
from torch.distributions.beta import Beta

from shapes_dataset_generator.shapes_dataset_generator.sample_config import SampleConfig
from shapes_dataset_generator.shapes_dataset_generator.renderer import PILRenderer


class ShapesDatasetGenerator:
    """
    This class is responsible for generating a dataset of shapes.
    """

    def __init__(
        self,
        random_seed: int = 42,
        render_config: Union[dict, None] = None,
    ):
        self.latents: np.array = None
        self.samples: np.array = None
        self.renderer = PILRenderer(render_config)
        # self.sampler = Sampler(dist_config)

        # Set random seed
        np.random.seed(random_seed)
        torch.manual_seed(random_seed)

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

    def generate_latents(self, n_samples: int = 1):
        """
        Generate latent vectors for the dataset.
        """
        dist = Beta(torch.tensor([2.0]), torch.tensor([5.0]))
        return dist.sample((n_samples, 2)).numpy().reshape((n_samples, 2))

    def generate_samples(self):
        """
        Generate samples for the dataset.
        """
        samples = map(lambda l: SampleConfig(*l), self.latents)
        samples = map(self.renderer.render, samples)
        samples = map(np.array, samples)
        return np.array(list(samples))
