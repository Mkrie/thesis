import csv
from pathlib import Path

with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "unimod_one.csv"), "w"
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 0
    while h <= 1500:
        if 0 <= h <= 100:
            writer.writerow((h, 6 * 10**14))
        else:
            writer.writerow((h, 0.5 * 10 ** 14))
        h += 1

with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "unimod_two.csv"), "w"
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 0
    while h <= 1500:
        if 300 <= h <= 400:
            writer.writerow((h, 6 * 10**14))
        else:
            writer.writerow((h, 0.5 * 10 ** 14))
        h += 1

with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "unimod_three.csv"), "w"
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 0
    while h <= 1500:
        if 800 <= h <= 900:
            writer.writerow((h, 6 * 10**14))
        else:
            writer.writerow((h, 0.5 * 10 ** 14))
        h += 1
