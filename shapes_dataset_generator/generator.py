import numpy as np
import torch
from torch.distributions.beta import Beta

from shapes_dataset_generator.shapes_dataset_generator.sample_config import SampleConfig
from shapes_dataset_generator.shapes_dataset_generator.renderer import PILRenderer


class ShapesDatasetGenerator:
    """
    This class is responsible for generating a dataset of shapes.
    """

    def __init__(self, n_samples: int = 1, random_seed: int = 42):
        self.n_samples : int = n_samples
        self.latents : np.array = None
        self.samples : np.array = None
        self.renderer = PILRenderer()

        # Set random seed
        np.random.seed(random_seed)
        torch.manual_seed(random_seed)

    def generate(self):
        """
        Main method for generating the dataset.

        Returns:
        - samples: A list of images of shapes.
        - latents: A list of corresponding latent vectors.
        """
        self.generate_latents()
        self.generate_samples()
        return self.samples, self.latents

    def generate_latents(self):
        """
        Generate latent vectors for the dataset.
        """
        # dist = Beta(torch.tensor([2.]), torch.tensor([5.]))
        # self.latents = dist.sample((self.n_samples, 2)).numpy().reshape((self.n_samples, 2))
        self.latents = np.array([
            [0.1, 0.1],
            [0.3, 0.3],
            [0.5, 0.5],
            [0.7, 0.7],
            [0.9, 0.9],
        ])
        
    def generate_samples(self):
        """
        Generate samples for the dataset.
        """
        samples_objects = [SampleConfig(x=x, y=y) for x, y in self.latents]
        self.samples = [self.renderer.render(sample) for sample in samples_objects]