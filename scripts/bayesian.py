import csv
import numpy as np
import matplotlib.pyplot as plt
import json
from pathlib import Path
from dataclasses import dataclass
import math

from direct_measurements import DirectMeasurements
from profile_recovery import ProfileRec


@dataclass(frozen=True)
class Bayesian:
    """Class for solving inverse problems using the optimal statistical estimation method"""
    profile: str
    profile_path: str
    dataset_name: str = "dataset_2_csv"

    def assessment(self, sigma, n, s, sigma_2, y_max, factor):
        """Calculation of the optimal statistical estimate."""
        # get data: xi == \xi, M == M(matrix(21x21)), h == heights
        xi, m, h = self.get_data(sigma=sigma, n=n)
        h_0 = 200
        f_0 = np.array([factor * 10**12] * 21)
        f = np.array(
            [
                [
                    0.25 * f_0[j] * f_0[i] * (math.e ** (-((h[i] - h[j]) ** 2) / h_0))
                    for j in range(n)
                ]
                for i in range(n)
            ]
        )
        out = f @ m.T @ np.linalg.inv(m @ f @ m.T + (sigma_2 * 10**15) ** 2 * np.eye(n)) @ (xi - m @ f_0) + f_0,
        return h, out

    def get_data(self, sigma, n=21):
        """Get data: xi == \\xi, M == M(matrix(21x21)), h == heights."""
        dir_meas = DirectMeasurements(self.profile, sigma, self.dataset_name, self.profile_path)
        prof_recovery = ProfileRec(self.profile, self.profile_path, self.dataset_name)
        data = prof_recovery.make_data(n)
        return (
            np.array([x[1] for x in dir_meas.direct_measurements_for_profile()]),
            np.array(data[1]),
            np.array(data[0]),
        )


def plot(dataset_name="dataset_2_csv",
         dir_profiles_name="profiles_2",
         sigma=0,
         sigma_2=0,
         n=10):
    path_to_profile_csv = Path(Path.cwd().parent,
                               "data",
                               dir_profiles_name,
                               "csv")
    with open(Path(Path.cwd().parent,
                   "data",
                   "profiles_2",
                   "profiles_2.json"), "r") as json_file:
        name_height = json.load(json_file)
    plt.rcParams["font.size"] = "18"
    for txt_path in path_to_profile_csv.glob("*"):
        val = name_height.get(txt_path.name).split()
        factor = 0.5 * float(val[1][6:9]) * float(val[2][4:].split("*")[0])
        print(factor)
        dir_meas = DirectMeasurements(txt_path.name, 0, dataset_name, dir_profiles_name)
        y_max = 0
        with open(Path(path_to_profile_csv, txt_path.name)) as csv_file:
            reader = csv.reader(csv_file)
            tup_coords: tuple[tuple[str]] = tuple(reader)
            original_x = tuple(float(x[0]) for x in tup_coords)
            original_y = tuple(float(x[1]) for x in tup_coords)
            data_bars = dir_meas.generate_bars([50 * i for i in range(21)], original_x, original_y)
        out_sum = []
        for _ in range(n):
            b = Bayesian(txt_path.name, dir_profiles_name)
            h, out = b.assessment(
                sigma=sigma, n=21, s=30, sigma_2=sigma_2, y_max=max(original_y), factor=factor
            )
            out_sum.append(out)
        # print(out_sum)
        out_avg = np.array(out_sum).mean(0)
        # print(out_avg)
        out_er = [np.std([0.02 * x[i] for x in out_sum]) for i in range(len(out_sum[0]))]
        plt.bar(
            [x + 25 for x in h],
            [factor * 10**10 * 0.02],
            width=45,
            linewidth=3,
            edgecolor="black",
            alpha=0.3,
            color="green",
            linestyle="-",
            label="prior profile",
        )
        plt.bar(
            [x + 25 for x in h],
            [0.02 * x for x in out],
            width=45,
            linewidth=1,
            edgecolor="black",
            alpha=0.5,
            color="red",
            linestyle="-",
            label="one restored profile",
        )
        plt.errorbar(
            [x + 25 for x in h],
            [0.02 * x for x in out_avg],
            yerr=[x for x in out_er],
            fmt="o",
            ecolor="black",
            elinewidth=2.5,
            capsize=4,
            color="black",
            label=f"average restored n={n}",
        )
        plt.bar(
            [x + 25 for x in data_bars[0]],
            [x * 50 * 0.02 for x in data_bars[1]],
            width=45,
            linewidth=1,
            edgecolor="black",
            alpha=0.5,
            color="blue",
            linestyle="-",
            label="original profile",
        )
        plt.legend()
        if dir_profiles_name == "profiles_2":
            plt.title(f"error = {sigma}*10^15, {name_height.get(txt_path.name)}")
        else:
            plt.title(str(txt_path).split("/")[-1])
        plt.minorticks_on()
        plt.grid(which="major", color="k", linewidth=1)
        plt.grid(which="minor", color="k", linestyle=":")
        plt.xlim(0, 1000)
        plt.xlabel("h[m]")
        plt.ylabel(r"$n$ [$cm^{-3}$]")
        plt.figure()
        # break
    plt.rcParams["font.size"] = "16"
    plt.show()


if __name__ == "__main__":
    plot(
        dataset_name="dataset_2_csv",
        dir_profiles_name="profiles_2",
        sigma=0.3,
        sigma_2=0.3,
        n=33,
    )
