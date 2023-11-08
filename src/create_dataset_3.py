from pathlib import Path
import csv

if __name__ == "__main__":
    msb: list = []
    with open(
        Path(
            Path(__file__).parents[1],
            "data",
            "dataset_2_csv",
            "msbgraf_89_9.csv",
        )
    ) as csv_file:
        msb = tuple(csv.reader(csv_file))
        print(msb)
    for txt_path in sorted(
        Path(Path(__file__).parents[1], "data", "dataset_2_csv").glob("*")
    ):
        with open(txt_path, "r") as csv_read:
            reader: list[list[str]] = list(csv.reader(csv_read))
            new_values = []
            for i in range(len(msb)):
                new_values.append(
                    [reader[i][0], float(reader[i][1]) - float(msb[i][1])]
                )
            with open(
                Path(
                    Path(__file__).parents[1],
                    "data",
                    "dataset_3_csv",
                    txt_path.name,
                ),
                "w",
            ) as csv_write:
                writer = csv.writer(csv_write)
                writer.writerows(new_values)
            print(f"new = {new_values}")
