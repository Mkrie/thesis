import json
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Union

import matplotlib.pyplot as plt
import numpy as np
from numpy import ndarray, dtype, floating

from src.bayesian import Bayesian
from src.drawing.common_drawing_methods import CommonDrawingMethods


@dataclass
class DrawOSE(CommonDrawingMethods):
    """Class for plotting graphs after OSE restoring profiles."""

    dataset_name: str = ("dataset_2_csv",)
    dir_profiles_name: str = "profiles_2"
    n_trials: int = 10

    @staticmethod
    def calculate_factor(data_bars: tuple[list[float], list[float]]) -> float:
        """Calculate factor for priore profile"""
        integral = sum(data_bars[1]) * (data_bars[0][1] - data_bars[0][0])
        return integral / (max(data_bars[0]) - min(data_bars[0]))

    def draw_ose(self, out_results, folder_name: str) -> None:
        """Draw the profile reconstructed using optimal statistical estimation."""
        path_out: Path = Path(Path.cwd().parent, "output", folder_name)
        path_out.mkdir(parents=True, exist_ok=True)
        for path_txt in path_out.glob("*.png"):
            try:
                path_txt.unlink()
            except OSError:
                ...
        for key in out_results.keys():
            h: ndarray[Any, dtype[floating]] = out_results[key][0]
            out: tuple[
                Union[ndarray[Any, dtype[floating]], Any]
            ] = out_results[key][1]
            data_bars: tuple[list[float], list[float]] = out_results[key][2]
            out_avg: ndarray[Any, dtype[floating]] = out_results[key][3]
            out_er: ndarray[Any, dtype[floating]] = out_results[key][4]
            sigma_1: float = out_results[key][5]
            txt_path: Path = out_results[key][6]
            name_height: dict[str, str] = out_results[key][7]
            factor: float = out_results[key][8]
            integral_mean: float = out_results[key][9]
            integral_std: float = out_results[key][10]
            integral_orig: float = out_results[key][11]
            plt.bar(
                x=[x_i + 25 for x_i in h],
                height=[h_i/50 for h_i in out[0]],
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
                y=[y_i/50 for y_i in out_avg],
                yerr=[yerr_i for yerr_i in out_er],
                fmt="o",
                ecolor="black",
                elinewidth=2.5,
                capsize=4,
                color="black",
                label=f"ose:average restored n={self.n_trials}",
            )
            plt.axhline(
                y= factor,
                color="black",
                linewidth=2,
                label="priori profile",
            )
            # plt.bar(
            #     x=[x_i + 25 for x_i in h],
            #     height=len(h) * [factor * 50],
            #     width=45,
            #     linewidth=3,
            #     edgecolor="black",
            #     alpha=0.3,
            #     color="green",
            #     linestyle="-",
            #     label="ose:prior profile",
            # )
            self.general_chart_settings(
                info=[integral_mean, integral_std, integral_orig],
                name_height=name_height,
            )
            print(f"ose:{txt_path.name}, {datetime.now()}")
            plt.savefig(
                Path(path_out, f'{key.split(".")[0]}.png'), bbox_inches="tight"
            )
            plt.figure()
        # plt.rcParams["font.size"] = "16"
        # plt.show()

    def calculate_average_and_error_ose(
        self,
        sigma_1: float,
        sigma_2: float,
        h_0: int,
        factor: float,
        txt_path: Path,
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
                sigma_1=sigma_1, n=21, sigma_2=sigma_2, factor=factor, h_0=h_0
            )
            out_sum.append(tuple(out[0]))
            # for const
            integrals: float = 50 * np.array(out_sum).sum(axis=1)
        theoretical_error = b.calculate_theoretical_error(sigma_1=sigma_1,
                                                          n=21,
                                                          sigma_2=sigma_2,
                                                          factor=10**13)
        # print(*out_sum, sep='\n')
        # sys.exit()
        return (
            h,
            out,
            np.array(out_sum).mean(0),
            np.array(out_sum).std(0),
            float(integrals.mean(axis=0)),
            float(integrals.std(axis=0)),
        )

    def make_all_necessary_calculations_for_ose(
        self, sigma_1: float, sigma_2: float, h_0: int
    ):
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
            needed_profiles = [
                "threemod_1.csv",
                "threemod_1_1.csv",
                "threemod_2.csv",
                "threemod_2_1.csv",
            ]
            if txt_path.name not in needed_profiles:
                continue
            data_bars = self.get_data_for_original_profile(
                path_to_profile_csv=path_to_profile_csv,
                txt_path_name=txt_path.name,
                sigma_1=sigma_1,
            )
            factor: float = DrawOSE.calculate_factor(data_bars)
            integral_orig: float = 50 * sum(data_bars[1])
            (
                h,
                out,
                out_avg,
                out_er,
                integral_mean,
                integral_std,
            ) = self.calculate_average_and_error_ose(
                sigma_1=sigma_1,
                sigma_2=sigma_2,
                h_0=h_0,
                factor=factor,
                txt_path=txt_path,
            )
            out_results[txt_path.name] = tuple(
                [
                    h,
                    out,
                    data_bars,
                    out_avg,
                    out_er,
                    sigma_1,
                    txt_path,
                    name_height,
                    factor,
                    integral_mean,
                    integral_std,
                    integral_orig,
                    h_0,
                    sigma_2
                ]
            )
            # break
        return out_results


if __name__ == "__main__":
    obj = DrawOSE(
        dataset_name="dataset_2_csv",
        dir_profiles_name="profiles_1",
        n_trials=30,
    )
    obj.draw_ose(
        obj.make_all_necessary_calculations_for_ose(sigma_1=0, sigma_2=0)
    )
