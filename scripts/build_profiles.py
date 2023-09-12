import csv
from pathlib import Path
from math import fabs, sqrt
import numpy as np
import matplotlib.pyplot as plt

from profile_recovery import ProfileRec
from direct_measurements import DirectMeasurements
from bayesan import Bayesan

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
    "unimod_1.csv": "left=0m, width=100m, val=6*10^11",
    "unimod_2.csv": "left=300m, width=100m, val=6*10^11",
    "unimod_3.csv": "left=800m, width=100m, val=6*10^11",
    "unimod_4.csv": "left=0m, width=200m, val=3*10^11",
    "unimod_5.csv": "left=300m, width=200m, val=3*10^11",
    "unimod_6.csv": "left=800m, width=200m, val=3*10^11",
    "unimod_1_1.csv": "left=0m, width=100m, val=60*10^11",
    "unimod_2_1.csv": "left=300m, width=100m, val=60*10^11",
    "unimod_3_1.csv": "left=800m, width=100m, val=60*10^11",
    "unimod_4_1.csv": "left=0m, width=200m, val=30*10^11",
    "unimod_5_1.csv": "left=300m, width=200m, val=30*10^11",
    "unimod_6_1.csv": "left=800m, width=200m, val=30*10^11",
    "threemod_1.csv": "left=0m, width=100m, val=6*10^11",
    "threemod_2.csv": "left=600m, width=100m, val=6*10^11",
    "threemod_3.csv": "left=0m, width=200m, val=3*10^11",
    "threemod_4.csv": "left=600m, width=200m, val=3*10^11",
    "threemod_1_1.csv": "left=0m, width=100m, val=60*10^11",
    "threemod_2_1.csv": "left=600m, width=100m, val=60*10^11",
    "threemod_3_1.csv": "left=0m, width=200m, val=30*10^11",
    "threemod_4_1.csv": "left=600m, width=200m, val=30*10^11",
    "unimod500big_1.csv": "left=0m, width=500m, val=1.2*10^11",
    "unimod500big_2.csv": "left=200m, width=500m, val=1.2*10^11",
    "unimod500big_3.csv": "left=500m, width=500m, val=1.2*10^11",
    "unimod500big_1_1.csv": "left=0m, width=500m, val=12*10^11",
    "unimod500big_2_1.csv": "left=200m, width=500m, val=12*10^11",
    "unimod500big_3_1.csv": "left=500m, width=500m, val=12*10^11",
    "unimod1000big_1.csv": "left=0m, width=1000m, val=50*10^11",
    "unimod1000big_2.csv": "left=200m, width=1000m, val=50*10^11",
    "unimod1000big_3.csv": "left=500m, width=1000m, val=50*10^11",
}

font = {"family": "serif", "color": "red", "weight": "bold", "size": 12}

box = {"facecolor": "none", "edgecolor": "green", "boxstyle": "round"}


def generate_bars(heights, p_x, p_y):
    def integrate(list_h, list_n):
        sum_n = 0
        for i in range(len(list_h) - 1):
            sum_n += 0.5 * (list_h[i] - list_h[i + 1]) * (list_n[i] + list_n[i + 1])
        return sum_n / (list_h[0] - list_h[-1])

    # print(heights, p_x, p_y)
    fin_h = []
    fin_n = []
    dict_index = {0.0: len(p_y)}
    for h in heights:
        for i, x in enumerate(p_x):
            if h >= x:
                dict_index[h] = i
                break
    keys = list(dict_index.keys())
    for h in range(len(keys) - 1):
        fin_h.append(keys[h])
        fin_n.append(
            integrate(
                p_x[dict_index[keys[h + 1]] : dict_index[keys[h]]],
                p_y[dict_index[keys[h + 1]] : dict_index[keys[h]]],
            )
        )
    return fin_h, fin_n


def build(
    sigma: float, number_of_trials: int, profiles: str, dataset: str, num_max: int, method: int = 1
) -> None:
    path_to_profiles = Path(Path(__file__).parents[1], "data", profiles, "csv")
    k: int = 1
    for txt_path in sorted(list(path_to_profiles.glob("*.csv"))):
        if txt_path.name == "profile_06_42.csv":
            continue
        if method == 1:
            prof_recovery = ProfileRec(txt_path.name, profiles, dataset)
            if num_max == 3:
                rec = prof_recovery.linear_programming_3(sigma)
                # print(rec)
            else:
                rec = prof_recovery.linear_programming(sigma)
        elif method == 2:
            prof_recovery = Bayesan(txt_path.name, profiles, dataset)
            rec = prof_recovery.assessment(sigma, n=21)
        rec_avg = [0] * len(rec[1])
        rec_list = []
        step = rec[0][1] - rec[0][0]
        dir_meas = DirectMeasurements(txt_path.name, sigma, dataset, profiles)
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
                    rec = prof_recovery.linear_programming(
                        sigma,
                        [
                            (x[0], x[1] + sigma * 10**13 * np.random.randn(1)[0])
                            for x in dir_meas_obj
                        ],
                    )
            elif method == 2:
                rec = prof_recovery.linear_programming(sigma)
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
                data_bars = generate_bars(rec[0][::ext], original_x, original_y)
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
                plt.text(x=600, y=max(original_y) * 0.5, s=text, fontdict=font, bbox=box)
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
        sigma=0.3,
        number_of_trials=3,
        profiles="profiles_1",
        dataset="dataset_3_csv",
        num_max=1,
        method=2,
    )
