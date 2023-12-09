import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Union, Any

import numpy as np


@dataclass(frozen=True)
class DirectMeasurements:
    profile: str
    sigma: float
    dataset_name: str = "dataset_3_csv"
    dir_profiles_name: str = "profiles_2"

    @classmethod
    def integrate(cls, list_h: tuple[float], list_n: tuple[float]) -> float:
        """Averaging over an interval."""
        sum_n: float = 0
        for i in range(len(list_h) - 1):
            sum_n += (
                0.5 * (list_h[i] - list_h[i + 1]) * (list_n[i] + list_n[i + 1])
            )
        return sum_n / (list_h[0] - list_h[-1])

    @staticmethod
    def generate_bars(
        heights: tuple[Union[float, Any], ...],
        p_x: tuple[float],
        p_y: tuple[float],
    ) -> tuple[list[float], list[float]]:
        """Creating a histogram (averaging at 50m)."""
        fin_h: list[float] = []
        fin_n: list[float] = []
        dict_index: dict[float, float] = {0.0: len(p_y)}
        for h in heights:
            for i, x in enumerate(p_x):
                if h >= x:
                    dict_index[h] = i
                    break
        keys: list[float] = list(dict_index.keys())
        for h in range(len(keys) - 1):
            fin_h.append(keys[h])
            fin_n.append(
                DirectMeasurements.integrate(
                    list_h=p_x[dict_index[keys[h + 1]]: dict_index[keys[h]]],
                    list_n=p_y[dict_index[keys[h + 1]]: dict_index[keys[h]]],
                )
            )
        return fin_h, fin_n

    def integration(self, dataset: str) -> float:
        """Calculate direct measurement via integration."""
        path_to_dataset_csv: Path = Path(
            Path(__file__).parents[1], "data", self.dataset_name
        )

        with open(Path(path_to_dataset_csv, dataset)) as csv_file:
            reader: csv.reader = csv.reader(csv_file)
            msb_tup = tuple(
                map(lambda x: (float(x[0]) * 10**3, float(x[1])), reader)
            )

        path_to_profile_csv = Path(
            Path(__file__).parents[1], "data", self.dir_profiles_name, "csv"
        )
        with open(Path(path_to_profile_csv, self.profile)) as csv_file:
            reader: csv.reader = csv.reader(csv_file)
            tup_coords: tuple[tuple[str]] = tuple(reader)
            original_x: tuple[float] = tuple(float(x[0]) for x in tup_coords)
            original_y: tuple[float] = tuple(float(x[1]) for x in tup_coords)
            data_bars = self.generate_bars(
                heights=tuple(x[0] for x in msb_tup[:21]),
                p_x=original_x,
                p_y=original_y,
            )
        return (
            sum(tuple(msb_tup[i][1] * data_bars[1][i] * 50 for i in range(20)))
            + self.sigma * 10**13 * np.random.randn(1)[0]
        )

    def direct_measurements_for_profile(
        self,
    ) -> tuple[tuple[float, float], ...]:
        """Direct measurements for a specific profile."""
        # print(self.sigma)
        path_to_dataset_csv: Path = Path(
            Path(__file__).parents[1], "data", self.dataset_name
        )
        for_prof_calc: list[tuple[float, float]] = []
        for txt_path in path_to_dataset_csv.glob("*.csv"):
            for_prof_calc.append(
                (
                    float(
                        txt_path.name.replace("msbgraf_", "")
                        .replace(".csv", "")
                        .replace("_", ".")
                    ),
                    self.integration(txt_path.name),
                )
            )
        return tuple(sorted(for_prof_calc, key=lambda x: x[0]))


if __name__ == "__main__":
    dir_meas = DirectMeasurements("threemod_2.csv", 1)
    meas = dir_meas.direct_measurements_for_profile()
    print(meas)
    meas = dir_meas.direct_measurements_for_profile()
    print(meas)
