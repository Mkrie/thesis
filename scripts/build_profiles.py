import csv
import json
from pathlib import Path
from math import fabs, sqrt
import numpy as np
import matplotlib.pyplot as plt

from profile_recovery import ProfileRec
from direct_measurements import DirectMeasurements

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


with open(Path(Path.cwd().parent,
               "data",
               "profiles_2",
               "profiles_2.json"), "r") as json_file:
    name_height = json.load(json_file)

font = {"family": "serif",
        "color": "red",
        "weight": "bold",
        "size": 12}

box = {"facecolor": "none",
       "edgecolor": "green",
       "boxstyle": "round"}

profiles_names = "threemod_1.csv"


class BuildProfiles(object):
    """Class for plotting graphs after restoring profiles."""



def build(
    sigma: float, number_of_trials: int, profiles: str, dataset: str, num_max: int, method: int = 1
) -> None:
    path_to_profiles = Path(Path(__file__).parents[1], "data", profiles, "csv")
    k: int = 1
    for txt_path in sorted(list(path_to_profiles.glob("*.csv"))):
        if txt_path.name == "profile_06_42.csv":
            continue
        if method == 1:
            prof_recovery = ProfileRec(profile=txt_path.name,
                                       profile_path=profiles,
                                       dataset_name=dataset)
            if num_max == 3:
                rec = prof_recovery.linear_programming_3(sigma=sigma)
            elif num_max == 1:
                rec = prof_recovery.linear_programming_1(sigma=sigma)
        rec_avg = [0] * len(rec[1])
        rec_list = []
        step = rec[0][1] - rec[0][0]

        dir_meas = DirectMeasurements(profile=txt_path.name,
                                      sigma=sigma,
                                      dataset_name=dataset,
                                      dir_profiles_name=profiles)
        dir_meas_obj = dir_meas.direct_measurements_for_profile()
        for _ in range(number_of_trials):
            if method == 1:
                if num_max == 3:
                    rec = prof_recovery.linear_programming_3(
                        sigma,
                        [
                            (x[0], x[1] + sigma * 10**13 * np.random.randn(1)[0])
                            for x in dir_meas_obj
                        ],
                    )
                else:
                    rec = prof_recovery.linear_programming_1(
                        sigma,
                        [
                            (x[0], x[1] + sigma * 10**13 * np.random.randn(1)[0])
                            for x in dir_meas_obj
                        ],
                    )
            elif method == 2:
                rec = prof_recovery.linear_programming_1(sigma)
            for i in range(len(rec[1])):
                rec_avg[i] += rec[1][i]
            rec_list.append(rec[1])
        for ext in [1, 2, 4, 6]:
            sp = plt.subplot(2, 2, k)
            rec_list_tmp = [
                tuple(sum(x[i : i + ext]) / ext for i in range(0, len(x), ext)) for x in rec_list
            ]
            tmp_error = [np.std([x[i] for x in rec_list_tmp]) for i in range(len(rec[1][::ext]))]
            tmp_bars = [
                sum(rec_avg[i : i + ext]) / number_of_trials / ext
                for i in range(0, len(rec_avg), ext)
            ]
            res_int = sum(tmp_bars) * ext * 0.5 * step
            plt.errorbar(
                [x + ext * 0.5 * step for x in rec[0][::ext]],
                tmp_bars,
                yerr=tmp_error,
                fmt="o",
                ecolor="black",
                elinewidth=2.5,
                capsize=4,
                color="black",
                label=f"average restored n={number_of_trials}",
            )
            list_discrepancy = list()
            step = rec[0][1] - rec[0][0]
            plt.bar(
                [h + ext * 0.5 * step for h in rec[0][::ext]],
                [sum(rec[1][i : i + ext]) / ext for i in range(0, len(rec[1]), ext)],
                width=step * ext,
                linewidth=1,
                edgecolor="black",
                alpha=0.5,
                color="red",
                linestyle="-",
                label="one restored profile",
            )
            with open(txt_path, "r") as csv_file:
                reader = csv.reader(csv_file)
                tup_coords: tuple[tuple[str]] = tuple(reader)
                plt.minorticks_on()
                plt.grid(which="major", color="k", linewidth=1)
                plt.grid(which="minor", color="k", linestyle=":")
                plt.xlabel("h[m]")
                plt.ylabel(r"$n$ [$cm^{-3}$]")
                list_text = txt_path.name.replace(".csv", "").split("_")
                if profiles == "profiles_1":
                    plt.xlim(0, 10**3)
                    plt.title(
                        f"""{dict_profile_time.get(tuple(list_text[1:]))}: {list_text[1]}:{list_text[2]}, averaging over {ext*50} m"""
                    )
                else:
                    plt.xlim(0, 1.0 * 10**3)
                    plt.title(name_height.get(txt_path.name))
                original_x = tuple(float(x[0]) for x in tup_coords)
                original_y = tuple(float(x[1]) for x in tup_coords)
                list_discrepancy.append((0, fabs(rec[1][0] - original_y[-1])))
                for res_i, res_h in enumerate(rec[0]):
                    for orig_i, orig_h in enumerate(original_x):
                        if res_h >= orig_h:
                            list_discrepancy.append(
                                (
                                    rec[0][res_i],
                                    sqrt((rec[1][res_i] - original_y[orig_i]) ** 2),
                                )
                            )
                            break
                data_bars = DirectMeasurements.generate_bars(rec[0][::ext], original_x, original_y)
                plt.bar(
                    [h + 0.5 * step * ext for h in data_bars[0]],
                    data_bars[1],
                    width=step * ext,
                    linewidth=1,
                    alpha=0.5,
                    edgecolor="darkblue",
                    color="turquoise",
                    linestyle="-",
                    label="original bar",
                )
                plt.errorbar(
                    original_x,
                    original_y,
                    linewidth=2,
                    label="original",
                )
                text = f"""int_original={0.5*step*ext*sum(data_bars[1]):4.3}\nint_av_res={res_int:4.3}\nint_av_res_er={sqrt(sum([x**2 for x in tmp_error])):4.3}\ns/n={0.5*step*ext*sum(data_bars[1])/sqrt(sum([x**2 for x in tmp_error])):4.3}"""
                plt.text(x=100, y=max(original_y) * 0.5, s=text, fontdict=font, bbox=box)
            plt.legend()
            k += 1
            plt.subplots_adjust(
                left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.35
            )
            # break
        k = 1
        plt.figure()
        print(txt_path.name)
        # break
    plt.show()


if __name__ == "__main__":
    build(
        sigma=0.1,
        number_of_trials=33,
        profiles="profiles_2",
        dataset="dataset_3_csv",
        num_max=3,
        method=1,
    )
