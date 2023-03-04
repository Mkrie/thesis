import csv
from pathlib import Path
from math import fabs
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

sigma = 0.6
number_of_trials: int = 33
path_to_profiles = Path(Path(__file__).parents[1], "data", "profiles_1", "csv")
k: int = 1
for txt_path in path_to_profiles.glob("*.csv"):
    sp = plt.subplot(2, 2, k)
    prof_recovery = ProfileRec(txt_path.name)
    rec = prof_recovery.linear_programming(sigma)
    rec_min_max = [[x, x] for x in rec[1]]
    for _ in range(number_of_trials):
        rec = prof_recovery.linear_programming(sigma)
        for i, x in enumerate(rec[1]):
            if rec[1][i] < rec_min_max[i][0]:
                rec_min_max[i][0] = rec[1][i]
            if rec[1][i] > rec_min_max[i][1]:
                rec_min_max[i][1] = rec[1][i]
    plt.errorbar(rec[0], tuple(0.5 * (x[1] + x[0]) for x in rec_min_max),
                 yerr=tuple(0.5 * (x[1] - x[0]) for x in rec_min_max),
                 fmt="o",
                 linestyle="None",
                 ecolor='black',
                 elinewidth=2,
                 capsize=3,
                 color="black")
    list_discrepancy = list()
    plt.errorbar(
        rec[0],
        rec[1],
        linewidth=4,
        color="red",
        label="restored",
    )
    with open(txt_path, "r") as csv_file:
        reader = csv.reader(csv_file)
        tup_coords: tuple[tuple[str]] = tuple(reader)
        plt.minorticks_on()
        plt.grid(which="major", color="k", linewidth=1)
        plt.grid(which="minor", color="k", linestyle=":")
        plt.xlim(0, 1000)
        #plt.ylim(0, 6*10**14)
        plt.xlabel("h[m]")
        plt.ylabel(r"$n$ [$m^{-3}$]")
        list_text = txt_path.name.replace(".csv", "").split("_")
        plt.title(
            f"{dict_profile_time.get(tuple(list_text[1:]))}: {list_text[1]}:{list_text[2]}"
        )
        original_x = tuple(float(x[0]) for x in tup_coords)
        original_y = tuple(float(x[1]) for x in tup_coords)
        list_discrepancy.append((0, fabs(rec[1][0] - original_y[-1])))
        for res_i, res_h in enumerate(rec[0]):
            for orig_i, orig_h in enumerate(original_x):
                if res_h >= orig_h:
                    list_discrepancy.append(
                        (rec[0][res_i], fabs(rec[1][res_i] - original_y[orig_i]))
                    )
                    break
        plt.errorbar(
            original_x,
            original_y,
            linewidth=4,
            label="original",
        )
    plt.plot(
        tuple(x[0] for x in list_discrepancy),
        tuple(x[1] for x in list_discrepancy),
        linewidth=2,
        linestyle="--",
        label="modulo error",
        color="purple"
    )
    plt.legend()
    k += 1
    if k > 4:
        k = 1
        # break
        plt.figure()
plt.show()
