import csv
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt

from src.direct_measurements import DirectMeasurements


@dataclass
class CommonDrawingMethods(object):
    """Class with common drawing methods for restoring profiles."""

    dataset_name: str = "dataset_2_csv"
    dir_profiles_name: str = "profiles_2"
    n_trials: int = 10

    def general_chart_settings(
        self, info: list[float], name_height: dict[str, str]
    ) -> None:
        plt.legend()
        plt.minorticks_on()
        plt.grid(which="major", color="k", linewidth=1)
        plt.grid(which="minor", color="k", linestyle=":")
        plt.xlim(0, 1000)
        plt.xlabel("h[m]")
        plt.ylabel(r"$n$ [$cm^{-3}$]")
        plt.title(
            f"int_mean={info[0]:4.4e},int_std={info[1]:4.4e},int_orig={info[2]:4.4e}"
        )

    def get_data_for_original_profile(
        self, path_to_profile_csv: Path, txt_path_name: str, sigma_1: float
    ) -> tuple[list[float], list[float]]:
        """Get data for the original profile."""
        with open(Path(path_to_profile_csv, txt_path_name)) as csv_file:
            reader = csv.reader(csv_file)
            tup_coords: tuple[tuple[str]] = tuple(reader)
            dir_meas: DirectMeasurements = DirectMeasurements(
                profile=txt_path_name,
                sigma=sigma_1,
                dataset_name=self.dataset_name,
                dir_profiles_name=self.dir_profiles_name,
            )
            data_bars: tuple[
                list[float], list[float]
            ] = dir_meas.generate_bars(
                heights=tuple(50 * i for i in range(21)),
                p_x=tuple(float(x[0]) for x in tup_coords),
                p_y=tuple(float(x[1]) for x in tup_coords),
            )
        return data_bars
