import csv
from dataclasses import dataclass
from direct_measurements import DirectMeasurements
from pathlib import Path
from scipy.optimize import linprog


@dataclass
class ProfileRecovery:
    profile: str
    dataset_name: str = "dataset_1_csv"

    def linear_programming(self):
        """Solving a linear programming problem."""
        dir_meas = DirectMeasurements(self.profile)
        xi = tuple(map(lambda x: x[1], dir_meas.direct_measurements_for_profile()))
        heights, matrix_a = self.make_data(len(dir_meas.direct_measurements_for_profile()))
        obj = [1, *[0] * len(dir_meas.direct_measurements_for_profile())]
        lhs_ineq = [[-1, *list(map(lambda x: -x, line))] for line in matrix_a] + [
            [-1, *line] for line in matrix_a
        ]
        rhs_ineq = [-x for x in xi] + list(xi)
        opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq)
        return heights, tuple(opt.x)[1:]

    def make_data(self, n: int = 10):
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
                heights = tuple(float(line[0])*1000 for line in reader)[:n]
            break
        return heights, matrix_a


if __name__ == "__main__":
    prof_recovery = ProfileRecovery("profile_17_17.csv")
    print(prof_recovery.linear_programming())
