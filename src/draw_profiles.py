from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Union, Any

from matplotlib import pyplot as plt
from numpy import ndarray, dtype, floating

from src.drawing.draw_linear_prog import DrawLinearProg
from src.drawing.draw_ose import DrawOSE

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


@dataclass
class DrawProfiles(DrawOSE, DrawLinearProg):
    """Class for plotting graphs after restoring profiles."""

    dataset_name: str = ("dataset_2_csv",)
    dir_profiles_name: str = "profiles_2"
    n_trials: int = 10

    def draw_ose_and_linprog(self, out_ose, out_linprog, folder_name: str) -> None:
        """Draw the profile reconstructed using OSE and LP."""
        path_out: Path = Path(Path.cwd().parent, "output", folder_name)
        path_out.mkdir(parents=True, exist_ok=True)
        for path_txt in path_out.glob("*.png"):
            try:
                path_txt.unlink()
            except OSError:
                ...
        plt.figure(figsize=(15, 12))
        for key in out_ose[0].keys():
            for k in range(2):
                plt.subplot(2, 2, k+1)
                h: ndarray[Any, dtype[floating]] = out_ose[k][key][0]
                out: tuple[
                    Union[ndarray[Any, dtype[floating]], Any]
                ] = out_ose[k][key][1]
                data_bars: tuple[list[float], list[float]] = out_ose[k][key][2]
                out_avg: ndarray[Any, dtype[floating]] = out_ose[k][key][3]
                out_er: ndarray[Any, dtype[floating]] = out_ose[k][key][4]
                sigma_1: float = out_ose[k][key][5]
                txt_path: Path = out_ose[k][key][6]
                name_height: dict[str, str] = out_ose[k][key][7]
                factor: float = out_ose[k][key][8]
                integral_mean: float = out_ose[k][key][9]
                integral_std: float = out_ose[k][key][10]
                integral_orig: float = out_ose[k][key][11]
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
                    label=f"ose:average restored n={self.n_trials}",
                )
                plt.axhline(y=50 * factor,
                            color='black',
                            linewidth=2,
                            label="priori profile")
                self.general_chart_settings(
                    info=[integral_mean, integral_std, integral_orig],
                    name_height=name_height,
                )
                print(f"ose:{txt_path.name}, {datetime.now()}")
            for k in range(2):
                plt.subplot(2, 2, k + 3)
                txt_path: Path = out_linprog[k][key][0]
                h: ndarray[Any, dtype[floating]] = out_linprog[k][key][1]
                out: tuple[
                    Union[ndarray[Any, dtype[floating]], Any]
                ] = out_linprog[k][key][2]
                out_avg: ndarray[Any, dtype[floating]] = out_linprog[k][key][3]
                out_er: ndarray[Any, dtype[floating]] = out_linprog[k][key][4]
                data_bars: tuple[list[float], list[float]] = out_linprog[k][key][5]
                sigma_1: float = out_linprog[k][key][6]
                num_max: int = out_linprog[k][key][7]
                name_height: dict[str, str] = out_linprog[k][key][8]
                integral_mean: float = out_linprog[k][key][9]
                integral_std: float = out_linprog[k][key][10]
                integral_orig: float = out_linprog[k][key][11]
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
            plt.figure(figsize=(15, 12))

    def calculate_pipeline(self, pipeline) -> None:
        for calc in pipeline:
            if (
                "sigma_2" in calc.keys()
                and self.dataset_name != "dataset_3_csv"
            ):
                folder_name: str = f"{self.dir_profiles_name},sigma_1={calc.get('sigma_1')},sigma_2={calc.get('sigma_2')}"
                self.draw_ose(
                    self.make_all_necessary_calculations_for_ose(
                        sigma_1=calc.get("sigma_1"),
                        sigma_2=calc.get("sigma_2"),
                    ),
                    folder_name=folder_name,
                )
            elif (
                "sigma_2" not in calc.keys()
                and self.dataset_name == "dataset_3_csv"
            ):
                folder_name: str = f"{self.dir_profiles_name},sigma_1={calc.get('sigma_1')},num_max={calc.get('num_max')}"
                self.draw_linear_prog(
                    self.make_all_necessary_calculations_for_linear_prog(
                        num_max=calc.get("num_max"),
                        sigma_1=calc.get("sigma_1"),
                    ),
                    folder_name=folder_name,
                )



    def calculate_pipeline_ose(self, pipeline):
        for calc in pipeline:
            folder_name: str = f"{self.dir_profiles_name},sigma_1={calc.get('sigma_1')},sigma_2={calc.get('sigma_2')}"
            out_results_1 = self.make_all_necessary_calculations_for_ose(sigma_1=calc.get("sigma_1"),
                                                                         sigma_2=calc.get("sigma_2"),
                                                                         h_0=50)
            out_results_2 = self.make_all_necessary_calculations_for_ose(sigma_1=calc.get("sigma_1"),
                                                                         sigma_2=calc.get("sigma_2"),
                                                                         h_0=200)
        return out_results_1, out_results_2, folder_name

    def calculate_pipeline_linprog(self, pipeline):
        for calc in pipeline:
            folder_name: str = f"{self.dir_profiles_name},sigma_1={calc.get('sigma_1')},sigma_2={calc.get('sigma_2')}"
            out_results_3 = self.make_all_necessary_calculations_for_linear_prog(num_max=1,
                                                                                 sigma_1=calc.get("sigma_1"))
            out_results_4 = self.make_all_necessary_calculations_for_linear_prog(num_max=2,
                                                                                 sigma_1=calc.get("sigma_1"))
        return out_results_3, out_results_4, folder_name


if __name__ == "__main__":
    n_trials = 13
    list_profiles_datasets = [
        # {"dataset_name": "dataset_3_csv", "dir_profiles_name": "profiles_1"},
        # {"dataset_name": "dataset_3_csv", "dir_profiles_name": "profiles_2"},
        # {"dataset_name": "dataset_2_csv", "dir_profiles_name": "profiles_1"},
        {"dataset_name": ["dataset_2_csv", "dataset_3_csv"], "dir_profiles_name": "profiles_2"},
    ]
    list_dictionary_of_calculations = [
        # {
        #     "sigma_1": 0,
        #     "sigma_2": 0,
        # },
        # {
        #     "sigma_1": 0.000001,
        #     "sigma_2": 0.000001,
        # },
        # {
        #     "sigma_1": 0.0001,
        #     "sigma_2": 0.0001,
        # },
        # {
        #     "sigma_1": 0.01,
        #     "sigma_2": 0.01,
        # },
        # {
        #     "sigma_1": 0.1,
        #     "sigma_2": 0.1,
        # },
        {
            "sigma_1": 0,
            "sigma_2": 0,
        }
        # {
        #     "sigma_1": 0.1,
        #     "num_max": 1,
        # },
        # {
        #     "sigma_1": 0.3,
        #     "num_max": 1,
        # },
        # {
        #     "sigma_1": 0.1,
        #     "num_max": 2,
        # },
        # {
        #     "sigma_1": 0.3,
        #     "num_max": 2,
        # },
    ]
    for p_d in list_profiles_datasets:
        obj = DrawProfiles(
            dataset_name=p_d["dataset_name"][0],
            dir_profiles_name=p_d["dir_profiles_name"],
            n_trials=n_trials,
        )
        out_results_1, out_results_2, folder_name = obj.calculate_pipeline_ose(pipeline=list_dictionary_of_calculations)
        obj = DrawProfiles(
            dataset_name=p_d["dataset_name"][1],
            dir_profiles_name=p_d["dir_profiles_name"],
            n_trials=n_trials,
        )
        out_results_3, out_results_4, folder_name = obj.calculate_pipeline_linprog(pipeline=list_dictionary_of_calculations)
        obj.draw_ose_and_linprog(out_ose=[out_results_1, out_results_2],
                                 out_linprog=[out_results_3, out_results_4],
                                 folder_name=folder_name)
