import csv
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
from scipy.optimize import linprog

from direct_measurements import DirectMeasurements


@dataclass
class ProfileRec:
    profile: str
    dataset_name: str = "dataset_1_csv"

    def solution_at_certain_maximum(
        self, xi: tuple[float], n: int, matrix_a: list[tuple[float]], obj, bnd, k
    ):
        """solution at a certain maximum"""
        restriction_1 = [
            tuple([0] + [0] * m + [1, -1] + [0] * (n - m - 2)) for m in range(k)
        ]
        restriction_2 = [
            tuple([0] + [0] * m + [-1, 1] + [0] * (n - m - 2)) for m in range(k, n - 1)
        ]
        lhs_ineq = (
            [[-1, *list(map(lambda x: -x, line))] for line in matrix_a]
            + [[-1, *line] for line in matrix_a]
            + restriction_1
            + restriction_2
        )
        rhs_ineq = (
            [-x for x in xi]
            + list(xi)
            + [0] * (len(restriction_1) + len(restriction_2))
        )
        return linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq, bounds=bnd)

    def linear_programming(self, sigma: float):
        """Solving a linear programming problem."""
        dir_meas = DirectMeasurements(self.profile, sigma)
        dir_meas_obj = dir_meas.direct_measurements_for_profile()
        xi = tuple(map(lambda x: x[1], dir_meas_obj))
        n: int = len(xi)
        heights, matrix_a = self.make_data(n)
        obj: list[int] = [1, *[0] * n]
        bnd = [(0, float("inf")) for _ in range(n + 1)]
        z_min: float = 10**50
        opt_optimal = self.solution_at_certain_maximum(xi, n, matrix_a, obj, bnd, 0)
        for k in range(1, n):
            opt = self.solution_at_certain_maximum(xi, n, matrix_a, obj, bnd, k)
            if opt.success:
                if tuple(opt.x)[0] < z_min:
                    opt_optimal = opt
                    z_min = tuple(opt.x)[0]
        return heights, [0.01 * n_i for n_i in list(opt_optimal.x)[1:]], z_min

    def make_data(self, n: int):
        path_to_dataset_csv = Path(Path(__file__).parents[1], "data", self.dataset_name)
        matrix_a: list(tuple) = list()
        heights: list(float) = tuple()
        for txt_path in sorted(path_to_dataset_csv.glob("*.csv")):
            with open(txt_path, "r") as csv_file:
                reader = csv.reader(csv_file)
                matrix_a.append(tuple(float(line[1]) for line in reader)[:n])
        for txt_path in sorted(path_to_dataset_csv.glob("*.csv")):
            with open(txt_path, "r") as csv_file:
                reader = csv.reader(csv_file)
                heights = tuple(float(line[0]) * 1000 for line in reader)[:n]
            break
        return heights, matrix_a


if __name__ == "__main__":
    profile_name = "unimod_three.csv"
    prof_recovery = ProfileRec(profile_name)
    rec = prof_recovery.linear_programming(0)
    plt.plot(rec[0], rec[1])
    path_to_profiles = Path(Path(__file__).parents[1], "data", "profiles_2", "csv")
    with open(Path(path_to_profiles, profile_name), "r") as csv_file:
        reader = csv.reader(csv_file)
        tup_coords: tuple[tuple[str]] = tuple(reader)
        plt.minorticks_on()
        plt.grid(which="major", color="k", linewidth=1)
        plt.grid(which="minor", color="k", linestyle=":")
        # plt.xlim(0, 1000)
        # plt.ylim(0, 6*10**7)
        plt.xlabel("h[m]")
        plt.ylabel(r"$n$ [$m^{-3}$]")
        # plt.title("profile_17_46.csv")
        # list_text = txt_path.name.replace(".csv", "").split("_")
        plt.plot(
            tuple(float(x[0]) for x in tup_coords),
            tuple(float(x[1]) for x in tup_coords),
            linewidth=3,
        )
    plt.show()
