from dataclasses import dataclass

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


if __name__ == "__main__":
    n_trials = 13
    list_profiles_datasets = [
        {"dataset_name": "dataset_3_csv", "dir_profiles_name": "profiles_1"},
        {"dataset_name": "dataset_3_csv", "dir_profiles_name": "profiles_2"},
        {"dataset_name": "dataset_2_csv", "dir_profiles_name": "profiles_1"},
        {"dataset_name": "dataset_2_csv", "dir_profiles_name": "profiles_2"},
    ]
    list_dictionary_of_calculations = [
        {
            "sigma_1": 0,
            "sigma_2": 0,
        },
        {
            "sigma_1": 0.000001,
            "sigma_2": 0.000001,
        },
        {
            "sigma_1": 0.0001,
            "sigma_2": 0.0001,
        },
        {
            "sigma_1": 0.01,
            "sigma_2": 0.01,
        },
        {
            "sigma_1": 0.1,
            "sigma_2": 0.1,
        },
        {
            "sigma_1": 0.1,
            "num_max": 1,
        },
        {
            "sigma_1": 0.3,
            "num_max": 1,
        },
        {
            "sigma_1": 0.1,
            "num_max": 2,
        },
        {
            "sigma_1": 0.3,
            "num_max": 2,
        },
    ]
    for p_d in list_profiles_datasets:
        obj = DrawProfiles(
            dataset_name=p_d["dataset_name"],
            dir_profiles_name=p_d["dir_profiles_name"],
            n_trials=n_trials,
        )
        obj.calculate_pipeline(pipeline=list_dictionary_of_calculations)
