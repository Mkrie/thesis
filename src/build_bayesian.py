import csv
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt

from src.bayesian import Bayesian
from src.direct_measurements import DirectMeasurements


def plot(
    dataset_name: str = "dataset_2_csv",
    dir_profiles_name: str = "profiles_2",
    sigma_1: float = 0,
    sigma_2: float = 0,
    n: int = 10,
) -> None:
    path_to_profile_csv: Path = Path(
        Path.cwd().parent, "data", dir_profiles_name, "csv"
    )
    with open(
        Path(Path.cwd().parent, "data", "profiles_2", "profiles_2.json"), "r"
    ) as json_file:
        name_height: dict = json.load(json_file)
    plt.rcParams["font.size"] = "18"
    for txt_path in path_to_profile_csv.glob("*"):
        val = name_height.get(txt_path.name).split()
        factor = 0.5 * float(val[1][6:9]) * float(val[2][4:].split("*")[0])
        dir_meas = DirectMeasurements(
            txt_path.name, 0, dataset_name, dir_profiles_name
        )
        with open(Path(path_to_profile_csv, txt_path.name)) as csv_file:
            reader = csv.reader(csv_file)
            tup_coords: tuple[tuple[str]] = tuple(reader)
            original_x = tuple(float(x[0]) for x in tup_coords)
            original_y = tuple(float(x[1]) for x in tup_coords)
            data_bars = dir_meas.generate_bars(
                tuple(50 * i for i in range(21)), original_x, original_y
            )
        out_sum = []
        for _ in range(n):
            b = Bayesian(txt_path.name, dir_profiles_name)
            h, out = b.assessment(
                sigma_1=sigma_1,
                n=21,
                sigma_2=sigma_2,
                factor=factor,
            )
            out_sum.append(out)
        out_avg = np.array(out_sum).mean(0)
        out_er = [
            np.std([0.02 * x[i] for x in out_sum])
            for i in range(len(out_sum[0]))
        ]
        plt.bar(
            x=[x + 25 for x in h],
            height=[factor * 10**10 * 0.02],
            width=45,
            linewidth=3,
            edgecolor="black",
            alpha=0.3,
            color="green",
            linestyle="-",
            label="prior profile",
        )
        plt.bar(
            x=[x + 25 for x in h],
            height=[0.02 * x for x in out],
            width=45,
            linewidth=1,
            edgecolor="black",
            alpha=0.5,
            color="red",
            linestyle="-",
            label="one restored profile",
        )
        plt.errorbar(
            x=[x + 25 for x in h],
            y=[0.02 * x for x in out_avg],
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
        plt.minorticks_on()
        plt.grid(which="major", color="k", linewidth=1)
        plt.grid(which="minor", color="k", linestyle=":")
        plt.xlim(0, 1000)
        plt.xlabel("h[m]")
        plt.ylabel(r"$n$ [$cm^{-3}$]")
        if dir_profiles_name == "profiles_2":
            plt.title(
                f"error = {sigma_1}*10^15, {name_height.get(txt_path.name)}"
            )
        else:
            plt.title(str(txt_path).split("/")[-1])
        plt.figure()
        # break
    plt.rcParams["font.size"] = "16"
    plt.show()
