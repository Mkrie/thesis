import csv
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from dataclasses import dataclass


@dataclass
class Bayesan:
    """Class for optimal statistical estimation"""

    profile: str
    profile_type: str
    dataset_name: str

    def get_data(self):
        """Get matrix M, direct measurements xi"""
        ...


if __name__ == "__main__":
    ...
