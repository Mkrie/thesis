import csv
import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt
from pathlib import Path


@dataclass
class DirectMeasurements:
    profile: str
    sigma: float
    dataset_name: str = "dataset_3_csv"
    dir_profiles_name: str = "profiles_1"

    @staticmethod
    def generate_bars(heights, p_x, p_y):
        def integrate(list_h, list_n):
            sum_n = 0
            for i in range(len(list_h) - 1):
                sum_n += 0.5 * (list_h[i] - list_h[i + 1]) * (list_n[i] + list_n[i + 1])
            return sum_n / (list_h[0] - list_h[-1])

        fin_h = []
        fin_n = []
        dict_index = {0.0: len(p_y)}
        for h in heights:
            for i, x in enumerate(p_x):
                if h >= x:
                    dict_index[h] = i
                    break
        keys = list(dict_index.keys())
        for h in range(len(keys) - 1):
            fin_h.append(keys[h])
            fin_n.append(
                integrate(
                    p_x[dict_index[keys[h + 1]] : dict_index[keys[h]]],
                    p_y[dict_index[keys[h + 1]] : dict_index[keys[h]]],
                )
            )
        return fin_h, fin_n

    def integration(self, dataset: str) -> float:
        """Calculate direct measurement via integration."""
        path_to_dataset_csv = Path(Path(__file__).parents[1], "data", self.dataset_name)

        msb_tup: tuple[tuple[float]] = tuple()
        with open(Path(path_to_dataset_csv, dataset)) as csv_file:
            reader = csv.reader(csv_file)
            msb_tup = tuple(map(lambda x: (float(x[0]) * 10**3, float(x[1])), reader))
        path_to_profile_csv = Path(Path(__file__).parents[1], "data", self.dir_profiles_name, "csv")
        with open(Path(path_to_profile_csv, self.profile)) as csv_file:
            reader = csv.reader(csv_file)
            tup_coords: tuple[tuple[str]] = tuple(reader)
            original_x = tuple(float(x[0]) for x in tup_coords)
            original_y = tuple(float(x[1]) for x in tup_coords)
            data_bars = self.generate_bars([x[0] for x in msb_tup[:21]], original_x, original_y)
        # print(data_bars)
        return (
            sum([msb_tup[i][1] * data_bars[1][i] * 50 for i in range(20)])
            + self.sigma * 10**13 * np.random.randn(1)[0]
        )

    def direct_measurements_for_profile(self) -> list[tuple[float]]:
        """Direct measurements for a specific profile."""
        path_to_dataset_csv = Path(Path(__file__).parents[1], "data", self.dataset_name)
        for_prof_calc: list[tuple[float]] = []
        for txt_path in path_to_dataset_csv.glob("*.csv"):
            for_prof_calc.append(
                (
                    float(
                        txt_path.name.replace("msbgraf_", "").replace(".csv", "").replace("_", ".")
                    ),
                    self.integration(txt_path.name),
                )
            )
        return sorted(for_prof_calc, key=lambda x: x[0])


if __name__ == "__main__":
    dir_meas = DirectMeasurements("threemod_2.csv", 0.3)
    meas = dir_meas.direct_measurements_for_profile()
    print(meas)
    # plt.plot(list(map(lambda x: x[0], meas)), list(map(lambda x: x[1], meas)))
    # plt.show()
