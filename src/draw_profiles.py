from dataclasses import dataclass

import matplotlib.pyplot as plt

from src.drawing.draw_ose import DrawOSE
from src.drawing.draw_linear_prog import DrawLinearProg

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


if __name__ == "__main__":
    obj = DrawProfiles(
        dataset_name="dataset_3_csv",
        dir_profiles_name="profiles_1",
        n_trials=30,
    )
    # obj.draw_ose(obj.make_all_necessary_calculations_for_ose(sigma_1=0, sigma_2=0))
    obj.draw_linear_prog(obj.make_all_necessary_calculations_for_linear_prog(num_max=1,
                                                                             sigma_1=1))
    # plt.show()
