import csv
import json
from typing import Any, Union
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from numpy import ndarray, dtype, floating
import matplotlib.pyplot as plt

from src.profile_recovery import ProfileRec
from src.direct_measurements import DirectMeasurements
from src.bayesian import Bayesian

dict_profile_time = {
    ("06", "42"): "PM004A",
    ("07", "05"): "PM004D",
    ("07", "37"): "PM005A",
    ("08", "08"): "PM005D",
    ("09", "42"): "PM006A",
    ("10", "13"): "PM006D",
    ("11", "01"): "PM007A",
    ("11", "27"): "PM007D",
    ("13", "06"): "PM008A",
    ("13", "23"): "PM008D",
    ("16", "54"): "PM010A",
    ("17", "17"): "PM010D",
    ("17", "46"): "PM011A",
    ("18", "04"): "PM011D",
}


font = {"family": "serif", "color": "red", "weight": "bold", "size": 12}

box = {"facecolor": "none", "edgecolor": "green", "boxstyle": "round"}

profiles_names = "threemod_1.csv"


@dataclass
class DrawProfiles(object):
    """Class for plotting graphs after restoring profiles."""

    dataset_name: str = ("dataset_2_csv",)
    dir_profiles_name: str = "profiles_2"
    n_trials: int = 10

    @staticmethod
    def calculate_factor(data_bars: tuple[list[float], list[float]]) -> float:
        """Calculate factor for priore profile"""
        integral = sum(data_bars[1]) * (data_bars[0][1] - data_bars[0][0])
        print(integral)
        return integral / (max(data_bars[0]) - min(data_bars[0]))

    def general_chart_settings(
        self, sigma_1: float, txt_path: Path, name_height: dict[str, str]
    ) -> None:
        plt.legend()
        plt.minorticks_on()
        plt.grid(which="major", color="k", linewidth=1)
        plt.grid(which="minor", color="k", linestyle=":")
        plt.xlim(0, 1000)
        plt.xlabel("h[m]")
        plt.ylabel(r"$n$ [$cm^{-3}$]")
        if self.dir_profiles_name == "profiles_2":
            plt.title(
                f"error = {sigma_1}*10^15, {name_height.get(txt_path.name)}"
            )
        else:
            plt.title(str(txt_path).split("/")[-1])

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

    def draw_ose(
        self,
        h: ndarray[Any, dtype[floating]],
        out: tuple[Union[ndarray[Any, dtype[floating]], Any]],
        data_bars: tuple[list[float], list[float]],
        out_avg: ndarray[Any, dtype[floating]],
        out_er: ndarray[Any, dtype[floating]],
        sigma_1: float,
        txt_path: Path,
        name_height: dict[str, str],
        factor: float,
    ) -> None:
        """Draw the profile reconstructed using optimal statistical estimation."""
        plt.bar(
            x=[x_i + 25 for x_i in h],
            height=[h_i for h_i in out[0]],
            width=45,
            linewidth=1,
            edgecolor="black",
            alpha=0.5,
            color="red",
            linestyle="-",
            label="ose:one restored profile",
        )
        plt.bar(
            x=[x_i + 25 for x_i in data_bars[0]],
            height=[h_i * 50 for h_i in data_bars[1]],
            width=45,
            linewidth=1,
            edgecolor="black",
            alpha=0.5,
            color="blue",
            linestyle="-",
            label="ose:original profile",
        )
        plt.errorbar(
            x=[x_i + 25 for x_i in h],
            y=[y_i for y_i in out_avg],
            yerr=[yerr_i for yerr_i in out_er],
            fmt="o",
            ecolor="black",
            elinewidth=2.5,
            capsize=4,
            color="black",
            label=f"ose:average restored n={self.n_trials}",
        )
        plt.bar(
            x=[x_i + 25 for x_i in h],
            height=len(h) * [factor * 50],
            width=45,
            linewidth=3,
            edgecolor="black",
            alpha=0.3,
            color="green",
            linestyle="-",
            label="ose:prior profile",
        )
        self.general_chart_settings(
            sigma_1=sigma_1, txt_path=txt_path, name_height=name_height
        )
        plt.figure()

    def calculate_average_and_error(
        self, sigma_1: float, sigma_2: float, factor: float, txt_path: Path
    ) -> tuple[
        ndarray[Any, dtype[floating]],
        tuple[Union[ndarray[Any, dtype[floating]], Any]],
        Any,
        Any,
    ]:
        """Calculate the average and error."""
        out_sum = []
        for _ in range(self.n_trials):
            b: Bayesian = Bayesian(
                profile=txt_path.name,
                profile_path=self.dir_profiles_name,
                dataset_name="dataset_2_csv",
            )
            h, out = b.assessment(
                sigma_1=sigma_1,
                n=21,
                sigma_2=sigma_2,
                factor=factor,
            )
            # print(out)
            out_sum.append(tuple(out[0]))
        return h, out, np.array(out_sum).mean(0), np.array(out_sum).std(0)

    def make_all_necessary_calculations_for_ose(
        self, sigma_1: float, sigma_2: float
    ) -> None:
        path_to_profile_csv: Path = Path(
            Path.cwd().parent, "data", self.dir_profiles_name, "csv"
        )
        """Make all the necessary calculations for OSE."""
        with open(
            Path(Path.cwd().parent, "data", "profiles_2", "profiles_2.json"),
            "r",
        ) as json_file_1:
            name_height: dict[str, str] = json.load(json_file_1)

        for txt_path in path_to_profile_csv.glob("*"):
            val: list[str] = name_height.get(txt_path.name).split()
            data_bars = self.get_data_for_original_profile(
                path_to_profile_csv=path_to_profile_csv,
                txt_path_name=txt_path.name,
                sigma_1=sigma_1,
            )
            factor: float = DrawProfiles.calculate_factor(data_bars)
            h, out, out_avg, out_er = self.calculate_average_and_error(
                sigma_1=sigma_1,
                sigma_2=sigma_2,
                factor=factor,
                txt_path=txt_path,
            )
            self.draw_ose(
                h=h,
                out=out,
                data_bars=data_bars,
                out_avg=out_avg,
                out_er=out_er,
                sigma_1=sigma_1,
                txt_path=txt_path,
                name_height=name_height,
                factor=factor,
            )
            break
        plt.rcParams["font.size"] = "16"
        plt.show()
        

if __name__ == "__main__":
    # build(
    #     sigma=0.1,
    #     number_of_trials=33,
    #     profiles="profiles_2",
    #     dataset="dataset_3_csv",
    #     num_max=1,
    #     method=1,
    # )
    obj = DrawProfiles(
        dataset_name="dataset_2_csv",
        dir_profiles_name="profiles_2",
        n_trials=3,
    )
    obj.make_all_necessary_calculations_for_ose(sigma_1=0, sigma_2=0)
