import matplotlib.pyplot as plt
import csv
from profile_recovery import ProfileRec
from pathlib import Path

name_height = {
    "unimod_1.csv": 0,
    "unimod_2.csv": 300,
    "unimod_3.csv": 800,
    "threemod_1.csv": 100,
    "threemod_2.csv": 600,
}

if __name__ == "__main__":
    path_to_profiles = Path(Path(__file__).parents[1], "data", "profiles_2", "csv")
    sigma: float = 0.1
    k: int = 1
    number_of_trials: int = 20
    for txt_path in sorted(list(path_to_profiles.glob("*"))):
        if txt_path.name == "unimod_1.csv":
            plt.figure()
            k = 1
        prof_recovery = ProfileRec(txt_path.name, "profiles_2", "dataset_2_csv")
        rec = prof_recovery.linear_programming(sigma)
        sp = plt.subplot(2, 2, k)
        # plt.ylim(0, 10**15)
        rec_min_max = [[x, x] for x in rec[1]]
        for _ in range(number_of_trials):
            rec = prof_recovery.linear_programming(sigma)
            for i, x in enumerate(rec[1]):
                if rec[1][i] < rec_min_max[i][0]:
                    rec_min_max[i][0] = rec[1][i]
                if rec[1][i] > rec_min_max[i][1]:
                    rec_min_max[i][1] = rec[1][i]
        plt.errorbar(
            rec[0],
            tuple(0.5 * (x[1] + x[0]) for x in rec_min_max),
            yerr=tuple(0.5 * (x[1] - x[0]) for x in rec_min_max),
            linestyle="None",
            ecolor="black",
            elinewidth=2.5,
            capsize=4,
            color="black",
        )
        plt.errorbar(
            rec[0], rec[1], fmt="-o", linewidth=4, color="red", label="restored"
        )
        with open(Path(path_to_profiles, txt_path.name), "r") as csv_file:
            reader = csv.reader(csv_file)
            tup_coords: tuple[tuple[str]] = tuple(reader)
            plt.minorticks_on()
            plt.grid(which="major", color="k", linewidth=1)
            plt.grid(which="minor", color="k", linestyle=":")
            plt.xlim(0, 1000)
            plt.xlabel("h[m]")
            plt.ylabel(r"$n$ [$cm^{-3}$]")
            plt.title(
                f"{txt_path.name.split('.')[0]}, {'min' if txt_path.name[0]=='t' else 'max'}:{name_height.get(txt_path.name)}"
            )
            plt.plot(
                tuple(float(x[0]) for x in tup_coords),
                tuple(float(x[1]) for x in tup_coords),
                linewidth=3,
            )
        k += 1
        if k == 4:
            k = 1
            plt.figure()
plt.show()
