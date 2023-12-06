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
        out_results
    ) -> None:
        """Draw the profile reconstructed using optimal statistical estimation."""
        for key in out_results.keys():
            h: ndarray[Any, dtype[floating]] = out_results[key][0]
            out: tuple[Union[ndarray[Any, dtype[floating]], Any]] = out_results[key][1]
            data_bars: tuple[list[float], list[float]] = out_results[key][2]
            out_avg: ndarray[Any, dtype[floating]] = out_results[key][3]
            out_er: ndarray[Any, dtype[floating]] = out_results[key][4]
            sigma_1: float = out_results[key][5]
            txt_path: Path = out_results[key][6]
            name_height: dict[str, str] = out_results[key][7]
            factor: float = out_results[key][8]
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
        plt.rcParams["font.size"] = "16"
        plt.show()

    def calculate_average_and_error_ose(
        self, sigma_1: float, sigma_2: float, factor: float, txt_path: Path
    ) -> tuple[
        ndarray[Any, dtype[floating]],
        tuple[Union[ndarray[Any, dtype[floating]], Any]],
        Any,
        Any,
    ]:
        """Calculate the average and error for OSE."""
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
        out_results = dict()
        for txt_path in path_to_profile_csv.glob("*"):
            val: list[str] = name_height.get(txt_path.name).split()
            data_bars = self.get_data_for_original_profile(
                path_to_profile_csv=path_to_profile_csv,
                txt_path_name=txt_path.name,
                sigma_1=sigma_1,
            )
            factor: float = DrawProfiles.calculate_factor(data_bars)
            h, out, out_avg, out_er = self.calculate_average_and_error_ose(
                sigma_1=sigma_1,
                sigma_2=sigma_2,
                factor=factor,
                txt_path=txt_path,
            )
            out_results[txt_path.name] = tuple([h,
                                                out,
                                                data_bars,
                                                out_avg,
                                                out_er,
                                                sigma_1,
                                                txt_path,
                                                name_height,
                                                factor])
            # break
        return out_results

    def calculate_average_and_error_linear_prog(self, sigma_1: float,
                                                txt_path: Path,
                                                num_max: int):
        """Calculate the average and error for linear programming."""
        out_sum = []
        for _ in range(self.n_trials):
            prof_recovery: ProfileRec = ProfileRec(
                profile=txt_path.name,
                profile_path=self.dir_profiles_name,
                dataset_name=self.dataset_name,
            )
            h, out, _ = prof_recovery.linear_programming(n_max=num_max,
                                                         sigma=sigma_1)
            out_sum.append(tuple(out))
        return h, out, np.array(out_sum).mean(0), np.array(out_sum).std(0)

    def make_all_necessary_calculations_for_linear_prog(self,
                                                        num_max: int,
                                                        sigma_1: float):
        """Make all the necessary calculations for recovery using linear programming."""
        path_to_profile_csv: Path = Path(
            Path.cwd().parent, "data", self.dir_profiles_name, "csv"
        )
        with open(
            Path(Path.cwd().parent, "data", "profiles_2", "profiles_2.json"),
            "r",
        ) as json_file_1:
            name_height: dict[str, str] = json.load(json_file_1)
        out_results = dict()
        for txt_path in path_to_profile_csv.glob("*"):
            if txt_path.name == "profile_06_42.csv":
                continue
            data_bars = self.get_data_for_original_profile(
                path_to_profile_csv=path_to_profile_csv,
                txt_path_name=txt_path.name,
                sigma_1=sigma_1,
            )
            h, out, out_avg, out_er = self.calculate_average_and_error_linear_prog(sigma_1=sigma_1,
                                                                                   txt_path=txt_path,
                                                                                   num_max=num_max)
            out_results[txt_path.name] = tuple([txt_path,
                                                h,
                                                out,
                                                out_avg,
                                                out_er,
                                                data_bars,
                                                sigma_1,
                                                num_max,
                                                name_height])
            break
        return out_results

    def draw_linear_prog(self, out_results):
        """Draw the profile reconstructed using linear programming."""
        for key in out_results.keys():
            txt_path: Path = out_results[key][0]
            h: ndarray[Any, dtype[floating]] = out_results[key][1]
            out: tuple[Union[ndarray[Any, dtype[floating]], Any]] = out_results[key][2]
            out_avg: ndarray[Any, dtype[floating]] = out_results[key][3]
            out_er: ndarray[Any, dtype[floating]] = out_results[key][4]
            data_bars: tuple[list[float], list[float]] = out_results[key][5]
            sigma_1: float = out_results[key][6]
            num_max: int = out_results[key][7]
            name_height: dict[str, str] = out_results[key][8]
            plt.bar(
                x=[x_i + 25 for x_i in h],
                height=[h_i for h_i in out],
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
                height=[h_i for h_i in data_bars[1]],
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

            self.general_chart_settings(
                sigma_1=sigma_1, txt_path=txt_path, name_height=name_height
            )
            plt.figure()
        plt.rcParams["font.size"] = "16"
        plt.show()


if __name__ == "__main__":
    obj = DrawProfiles(
        dataset_name="dataset_3_csv",
        dir_profiles_name="profiles_1",
        n_trials=3,
    )
    # obj.draw_ose(obj.make_all_necessary_calculations_for_ose(sigma_1=0, sigma_2=0))
    obj.draw_linear_prog(obj.make_all_necessary_calculations_for_linear_prog(num_max=1,
                                                                             sigma_1=0))
