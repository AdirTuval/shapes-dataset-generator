from typing import Union
from torch.distributions import Uniform, Beta

DISTRIBUTIONS_DICT = {
    "uniform": Uniform,
    "beta": Beta
}

class Sampler:
    def __init__(self, config: Union[dict, None] = None):
        dist_fn = DISTRIBUTIONS_DICT[config["type"]]
        self.dist = dist_fn(*config["params"])
        
    def sample(self, sample_shape):
        return self.dist.sample(sample_shape)