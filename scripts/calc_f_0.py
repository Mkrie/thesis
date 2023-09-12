import csv
from pathlib import Path

import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt

from direct_measurements import DirectMeasurements


if __name__ == "__main__":
    summary = []
    dataset_name = "dataset_2_csv"
    dir_profiles_name = "profiles_1"
    path_to_profile_csv = Path(Path(__file__).parents[1], "data", dir_profiles_name, "csv")
    for txt_path in path_to_profile_csv.glob("*"):
        dir_meas = DirectMeasurements(txt_path.name, 0.3, dataset_name, dir_profiles_name)
        with open(Path(path_to_profile_csv, txt_path.name)) as csv_file:
            reader = csv.reader(csv_file)
            tup_coords: tuple[tuple[str]] = tuple(reader)
            original_x = tuple(float(x[0]) for x in tup_coords)
            original_y = tuple(float(x[1]) for x in tup_coords)
            data_bars = dir_meas.generate_bars([50 * i for i in range(21)], original_x, original_y)
        summary.append(data_bars[1])
    print(list(np.array(summary).mean(0)))
