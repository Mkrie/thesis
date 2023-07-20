import csv
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from profile_recovery import ProfileRec

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

name_height = {
    "unimod_1.csv": 0,
    "unimod_2.csv": 300,
    "unimod_3.csv": 800,
    "threemod_1.csv": 100,
    "threemod_2.csv": 600,
}

number_of_trials: int = 10
step: float = 0.05
path_to_profiles = Path(Path(__file__).parents[1], "data", "profiles_1", "csv")
for txt_path in sorted(list(path_to_profiles.glob("*.csv"))):
    if txt_path.name == "profile_06_42.csv":
        continue
    sp = plt.subplot(1, 2, 1)
    prof_recovery = ProfileRec(txt_path.name, "profiles_1", "dataset_1_csv")
    sigma: float = 0
    step_list = []
    error_list = []
    while sigma <= 1.05:
        step_list.append(sigma)
        error = []
        for _ in range(number_of_trials):
            error.append(prof_recovery.linear_programming(sigma)[2])
        error_list.append((np.array(error).mean(), np.array(error).std()))
        sigma += step
    plt.minorticks_on()
    plt.grid(which="major", color="k", linewidth=1)
    plt.grid(which="minor", color="k", linestyle=":")
    plt.xlabel(r"$\sigma$ $10^{15}$ [cm^{-2}$]")
    plt.ylabel(r"$n$ [$cm^{-2}$]")
    plt.xlim(0, 1)
    plt.ylim(0, np.array([x[0] * 10 for x in error_list]).max())
    plt.title(f"n = {number_of_trials}")
    plt.errorbar(
        step_list,
        [x[0] * 10 for x in error_list],
        yerr=[x[1] for x in error_list],
        linewidth=4,
        label="original",
        ecolor="black",
        elinewidth=2.5,
        capsize=4,
        color="indigo",
    )
    print(step_list, error_list)
    sp = plt.subplot(1, 2, 2)
    with open(txt_path, "r") as csv_file:
        reader = csv.reader(csv_file)
        tup_coords: tuple[tuple[str]] = tuple(reader)
        plt.minorticks_on()
        plt.grid(which="major", color="k", linewidth=1)
        plt.grid(which="minor", color="k", linestyle=":")
        plt.xlabel("h[m]")
        plt.ylabel(r"$n$ [$cm^{-3}$]")
        plt.xlim(0, 10**3)
        # list_text = txt_path.name.replace(".csv", "").split("_")
        # plt.title(
        #     f"{dict_profile_time.get(tuple(list_text[1:]))}: {list_text[1]}:{list_text[2]}"
        # )
        plt.title(
            f"{txt_path.name.split('.')[0]}, {'min' if txt_path.name[0] == 't' else 'max'}:{name_height.get(txt_path.name)}"
        )
        original_x = tuple(float(x[0]) for x in tup_coords)
        original_y = tuple(float(x[1]) for x in tup_coords)
        plt.errorbar(
            original_x,
            original_y,
            linewidth=4,
            label="original",
        )
    plt.legend()
    k = 1
    plt.figure()
plt.show()
