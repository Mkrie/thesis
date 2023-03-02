import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DirectMeasurements:
    profile: str
    dataset_name: str = "dataset_1_csv"

    def integration(self, dataset: str) -> float:
        """Calculate direct measurement via integration."""
        path_to_dataset_csv = Path(Path(__file__).parents[1], "data", self.dataset_name)

        msb_tup: tuple[tuple[float]] = tuple()
        with open(Path(path_to_dataset_csv, dataset)) as csv_file:
            reader = csv.reader(csv_file)
            msb_tup = tuple(map(lambda x: (float(x[0]) * 1000, float(x[1])), reader))

        path_to_profile_csv = Path(
            Path(__file__).parents[1], "data", "profiles_1", "csv"
        )

        prof_tup: tuple[tuple[float]] = tuple()
        with open(Path(path_to_profile_csv, self.profile)) as csv_file:
            reader = csv.reader(csv_file)
            prof_tup = tuple(
                sorted(
                    list(map(lambda x: (float(x[0]), float(x[1])), reader)),
                    key=lambda y: y[0],
                )
            )

        max_h_prof_tup: float = max([i[0] for i in prof_tup])
        sum_X: float = 0
        # print(msb_tup)
        for i in range(len(msb_tup) - 1):
            if (msb_tup[i + 1][0] + msb_tup[i][0]) / 2 > max_h_prof_tup:
                break
            j: int = 0
            while (msb_tup[i + 1][0] + msb_tup[i][0]) / 2 > prof_tup[j][0]:
                j += 1
            sum_X += (
                (msb_tup[i + 1][0] - msb_tup[i][0])
                * (msb_tup[i + 1][1] + msb_tup[i][1])
                * prof_tup[j][1]
                / 2
            )
        return sum_X

    def direct_measurements_for_profile(self) -> list[tuple[float]]:
        """Direct measurements for a specific profile."""
        path_to_dataset_csv = Path(Path(__file__).parents[1], "data", self.dataset_name)
        for_prof_calc: list[tuple[float]] = []
        for txt_path in path_to_dataset_csv.glob("*.csv"):
            for_prof_calc.append(
                (
                    float(
                        txt_path.name.replace("msbgraf_", "")
                        .replace(".csv", "")
                        .replace("_", ".")
                    ),
                    self.integration(txt_path.name),
                )
            )
        return sorted(for_prof_calc, key=lambda x: x[0])


if __name__ == "__main__":
    dir_meas = DirectMeasurements("profile_07_05.csv")
    print(dir_meas.direct_measurements_for_profile())
