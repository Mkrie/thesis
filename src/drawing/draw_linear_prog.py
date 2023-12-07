import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Union

import matplotlib.pyplot as plt
import numpy as np
from numpy import ndarray, dtype, floating

from src.drawing.common_drawing_methods import CommonDrawingMethods
from src.profile_recovery import ProfileRec

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
class DrawLinearProg(CommonDrawingMethods):
    """Class for plotting graphs after restoring profiles."""

    dataset_name: str = ("dataset_2_csv",)
    dir_profiles_name: str = "profiles_2"
    n_trials: int = 10

    def calculate_average_and_error_linear_prog(
        self, sigma_1: float, txt_path: Path, num_max: int
    ):
        """Calculate the average and error for linear programming."""
        out_sum = []
        for _ in range(self.n_trials):
            prof_recovery: ProfileRec = ProfileRec(
                profile=txt_path.name,
                profile_path=self.dir_profiles_name,
                dataset_name=self.dataset_name,
            )
            h, out, _ = prof_recovery.linear_programming(
                n_max=num_max, sigma=sigma_1
            )
            out_sum.append(tuple(out))
        # for const
        integrals: float = 50 * np.array(out_sum).sum(axis=1)
        return (
            h,
            out,
            np.array(out_sum).mean(axis=0),
            np.array(out_sum).std(axis=0),
            float(integrals.mean(axis=0)),
            float(integrals.std(axis=0)),
        )

    def make_all_necessary_calculations_for_linear_prog(
        self, num_max: int, sigma_1: float
    ):
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
            integral_orig: float = 50 * sum(data_bars[1])
            (
                h,
                out,
                out_avg,
                out_er,
                integral_mean,
                integral_std,
            ) = self.calculate_average_and_error_linear_prog(
                sigma_1=sigma_1, txt_path=txt_path, num_max=num_max
            )
            out_results[txt_path.name] = tuple(
                [
                    txt_path,
                    h,
                    out,
                    out_avg,
                    out_er,
                    data_bars,
                    sigma_1,
                    num_max,
                    name_height,
                    integral_mean,
                    integral_std,
                    integral_orig,
                ]
            )
            print(f"lin_prog:{txt_path.name}, {datetime.now()}")
            # break
        return out_results

    def draw_linear_prog(self, out_results, folder_name: str) -> None:
        """Draw the profile reconstructed using linear programming."""
        path_out: Path = Path(Path.cwd().parent, "output", folder_name)
        path_out.mkdir(parents=True, exist_ok=True)
        for path_txt in path_out.glob("*.png"):
            try:
                path_txt.unlink()
            except OSError:
                ...
        for key in out_results.keys():
            txt_path: Path = out_results[key][0]
            h: ndarray[Any, dtype[floating]] = out_results[key][1]
            out: tuple[
                Union[ndarray[Any, dtype[floating]], Any]
            ] = out_results[key][2]
            out_avg: ndarray[Any, dtype[floating]] = out_results[key][3]
            out_er: ndarray[Any, dtype[floating]] = out_results[key][4]
            data_bars: tuple[list[float], list[float]] = out_results[key][5]
            sigma_1: float = out_results[key][6]
            num_max: int = out_results[key][7]
            name_height: dict[str, str] = out_results[key][8]
            integral_mean: float = out_results[key][9]
            integral_std: float = out_results[key][10]
            integral_orig: float = out_results[key][11]
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
                label="original profile",
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
                label=f"linear prog:average restored n={self.n_trials}",
            )

            self.general_chart_settings(
                info=[integral_mean, integral_std, integral_orig],
                name_height=name_height,
            )
            plt.savefig(
                Path(path_out, f'{key.split(".")[0]}.png'), bbox_inches="tight"
            )
            plt.figure()


if __name__ == "__main__":
    obj = DrawLinearProg(
        dataset_name="dataset_3_csv",
        dir_profiles_name="profiles_1",
        n_trials=30,
    )
    # obj.draw_ose(obj.make_all_necessary_calculations_for_ose(sigma_1=0, sigma_2=0))
    obj.draw_linear_prog(
        obj.make_all_necessary_calculations_for_linear_prog(
            num_max=1, sigma_1=1
        )
    )
