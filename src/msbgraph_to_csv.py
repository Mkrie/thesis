import csv
import shutil
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Msbgraph:
    """Converts data to csv."""

    dataset_name: str
    begin_f: int = 42
    end_f: int = 137

    def convert_all_files_to_csv(self) -> None:
        """Convert all files in dataset to csv."""
        path_to_data = Path(Path(__file__).parents[1], "data")
        path_to_csv = Path(path_to_data, f"{self.dataset_name}_csv")
        if path_to_csv.is_dir():
            shutil.rmtree(str(path_to_csv), ignore_errors=True)
        path_to_csv.mkdir()
        for txt_path in Path(path_to_data, self.dataset_name).glob("*.txt"):
            with open(txt_path, "r") as file:
                with open(
                    Path(path_to_csv, txt_path.name.replace("txt", "csv")), "w"
                ) as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows(
                        tuple(
                            tuple(line.split("\t")[:2])
                            for line in file.readlines()[self.begin_f : self.end_f]
                        )
                    )


if __name__ == "__main__":
    dataset_1 = Msbgraph("dataset_2")
    dataset_1.convert_all_files_to_csv()
