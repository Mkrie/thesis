import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Union

import matplotlib.pyplot as plt
import scipy
from scipy.optimize import linprog

from src.direct_measurements import DirectMeasurements


@dataclass
class ProfileRec:
    """Profile restoration using different methods."""

    profile: str
    profile_path: str
    dataset_name: str = "dataset_2_csv"

    @staticmethod
    def generate_restrictions(
        k: list[int], n: int
    ) -> list[list[tuple[int, ...]]]:
        restrictions = []
        if len(k) == 1:
            restrictions.append(
                [
                    tuple([0] + [0] * m + [1, -1] + [0] * (n - m - 2))
                    for m in range(k[0])
                ]
            )
            restrictions.append(
                [
                    tuple([0] + [0] * m + [-1, 1] + [0] * (n - m - 2))
                    for m in range(k[0], n - 1)
                ]
            )
        elif len(k) == 3:
            restrictions.append(
                [
                    tuple([0] + [0] * m + [1, -1] + [0] * (n - m - 2))
                    for m in range(k[0])
                ]
            )
            restrictions.append(
                [
                    tuple([0] + [0] * m + [-1, 1] + [0] * (n - m - 2))
                    for m in range(k[0], k[1] - 1)
                ]
            )
            restrictions.append(
                [
                    tuple([0] + [0] * m + [1, -1] + [0] * (n - m - 2))
                    for m in range(k[1], k[2] - 1)
                ]
            )
            restrictions.append(
                [
                    tuple([0] + [0] * m + [-1, 1] + [0] * (n - m - 2))
                    for m in range(k[2], n - 1)
                ]
            )
        return restrictions

    @staticmethod
    def solution_at_certain_maximum(
        xi: tuple[float],
        n: int,
        matrix_a: list[tuple[float]],
        obj: tuple[Union[int, Any], ...],
        bnd: tuple[tuple[int, float], ...],
        k: list[int],
    ) -> scipy.optimize.OptimizeResult:
        """Solution at a certain maximum."""
        l_restrictions = ProfileRec.generate_restrictions(k=k, n=n)
        lhs_ineq: list[list[Union[int, Any]]] = [
            [-1, *list(map(lambda x: -x, line))] for line in matrix_a
        ] + [[-1, *line] for line in matrix_a]
        sum_len: int = 0
        for restriction in l_restrictions:
            lhs_ineq += restriction
            sum_len += len(restriction)
        rhs_ineq: list[float] = [-x for x in xi] + list(xi) + [0] * sum_len
        return linprog(method="highs", c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq)

    def linear_programming(
        self, n_max: int, sigma: float, dir_meas_obj=None
    ) -> tuple[tuple[float, ...], list[Union[float, Any]], float]:
        """Solving a linear programming problem."""
        if dir_meas_obj is None:
            dir_meas = DirectMeasurements(
                profile=self.profile,
                sigma=sigma,
                dataset_name=self.dataset_name,
                dir_profiles_name=self.profile_path,
            )
            dir_meas_obj: tuple[
                tuple[float, float], ...
            ] = dir_meas.direct_measurements_for_profile()
        last: float = dir_meas_obj[-1][1]
        dir_meas_obj: tuple[tuple[float, float], ...] = tuple(
            (x[0], x[1] - last) for x in dir_meas_obj
        )
        xi: tuple[float, ...] = tuple(map(lambda x: x[1], dir_meas_obj))
        n: int = len(xi)
        make_data_out = self.make_data(n)
        heights: tuple[float, ...] = tuple(make_data_out[0])
        matrix_a: list[tuple[float]] = make_data_out[1]
        obj: tuple[Union[int, Any], ...] = tuple([1, *[0] * n])
        bnd: tuple[tuple[int, float], ...] = tuple(
            [(0, float("inf")) for _ in range(n + 1)]
        )
        z_min: float = 10**100
        k: list[int] = list()
        if n_max == 1:
            k: list[int] = [0]
        elif n_max == 2:
            k: list[int] = [0, 1, 2]
        opt_optimal: scipy.optimize.OptimizeResult = (
            self.solution_at_certain_maximum(
                xi=xi, n=n, matrix_a=matrix_a, obj=obj, bnd=bnd, k=k
            )
        )
        if n_max == 1:
            for k in range(1, n):
                opt: scipy.optimize.OptimizeResult = (
                    self.solution_at_certain_maximum(
                        xi=xi, n=n, matrix_a=matrix_a, obj=obj, bnd=bnd, k=[k]
                    )
                )
                if opt.success:
                    if tuple(opt.x)[0] < z_min:
                        opt_optimal = opt
                        z_min: float = tuple(opt.x)[0]
        elif n_max == 2:
            for k_1 in range(1, n):
                for k_2 in range(k_1, n):
                    for k_3 in range(k_2, n):
                        opt = self.solution_at_certain_maximum(
                            xi=xi,
                            n=n,
                            matrix_a=matrix_a,
                            obj=obj,
                            bnd=bnd,
                            k=[k_1, k_2, k_3],
                        )
                        if opt.success:
                            if tuple(opt.x)[0] < z_min:
                                opt_optimal = opt
                                z_min: float = tuple(opt.x)[0]

        return (
            heights,
            [
                1 / (heights[1] - heights[0]) * n_i
                for n_i in list(opt_optimal.x)[1:]
            ],
            z_min,
        )

    def make_data(
        self, n: int
    ) -> tuple[Union[tuple, tuple[Union[float, Any], ...]], list[tuple]]:
        path_to_dataset_csv = Path(
            Path(__file__).parents[1], "data", self.dataset_name
        )
        matrix_a: list[tuple] = list()
        heights: tuple = tuple()
        for txt_path in sorted(path_to_dataset_csv.glob("*.csv")):
            with open(txt_path, "r") as csv_file_1:
                reader_1 = csv.reader(csv_file_1)
                matrix_a.append(tuple(float(line[1]) for line in reader_1)[:n])
        for txt_path in sorted(path_to_dataset_csv.glob("*.csv")):
            with open(txt_path, "r") as csv_file_2:
                reader_2 = csv.reader(csv_file_2)
                heights: tuple[Union[float, Any], ...] = tuple(
                    float(line[0]) * 10**3 for line in reader_2
                )[:n]
            break
        return heights, matrix_a


if __name__ == "__main__":
    profile_name: str = "profile_07_05.csv"
    prof_recovery = ProfileRec(
        profile=profile_name,
        profile_path="profiles_1",
        dataset_name="dataset_3_csv",
    )
    for _ in range(20):
        rec = prof_recovery.linear_programming(n_max=1, sigma=1)
        for x in rec[1]:
            if x < 0:
                print("NEGATIIIVE!!!!!!!!!!")
        print(rec)
    plt.plot(rec[0], rec[1])
    path_to_profiles = Path(
        Path(__file__).parents[1], "data", "profiles_1", "csv"
    )
    with open(Path(path_to_profiles, profile_name), "r") as csv_file:
        reader = csv.reader(csv_file)
        tup_coords: tuple[tuple[str]] = tuple(reader)
        plt.minorticks_on()
        plt.grid(which="major", color="k", linewidth=1)
        plt.grid(which="minor", color="k", linestyle=":")
        plt.xlabel("h[m]")
        plt.ylabel(r"$n$ [$m^{-3}$]")
        plt.plot(
            tuple(float(x[0]) for x in tup_coords),
            tuple(float(x[1]) for x in tup_coords),
            linewidth=3,
        )
    plt.show()
