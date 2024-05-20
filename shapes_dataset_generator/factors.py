ALLOWED_FACTORS = ['x', 'y', 'color', 'size']

class Factors:
    """
    This class is responsible for managing the factors of variation in the dataset.
    """

    def __init__(self, factors: list):
        self.factors = []
        allowed_factors_cpy = ALLOWED_FACTORS.copy()
        for factor in factors:
            if factor not in ALLOWED_FACTORS:
                raise ValueError(f"Factor {factor} is not allowed.")
            if factor not in allowed_factors_cpy:
                raise ValueError(f"Factor {factor} is duplicated.")
            
            allowed_factors_cpy.remove(factor)
            self.factors.append(factor)
    
    def __len__(self):
        return len(self.factors)

    def from_list(self, l: list):
        """
        Convert a list of factors into a dictionary.
        """
        return dict(zip(self.factors, l))