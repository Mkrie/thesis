import csv
from pathlib import Path

with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "unimod_1.csv"), "w"
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 0 <= h <= 100:
            writer.writerow((h, 6 * 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1

with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "unimod_2.csv"), "w"
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 300 <= h <= 400:
            writer.writerow((h, 6 * 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1

with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "unimod_3.csv"),
    "w",
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 800 <= h <= 900:
            writer.writerow((h, 6 * 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1


with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "unimod_4.csv"), "w"
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 0 <= h <= 200:
            writer.writerow((h, 3 * 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1

with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "unimod_5.csv"), "w"
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 300 <= h <= 500:
            writer.writerow((h, 3 * 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1

with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "unimod_6.csv"),
    "w",
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 800 <= h <= 1000:
            writer.writerow((h, 3 * 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1

with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "unimod_1_1.csv"), "w"
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 0 <= h <= 100:
            writer.writerow((h, 60 * 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1

with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "unimod_2_1.csv"), "w"
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 300 <= h <= 400:
            writer.writerow((h, 60 * 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1

with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "unimod_3_1.csv"),
    "w",
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 800 <= h <= 900:
            writer.writerow((h, 60 * 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1


with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "unimod_4_1.csv"), "w"
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 0 <= h <= 200:
            writer.writerow((h, 30 * 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1

with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "unimod_5_1.csv"), "w"
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 300 <= h <= 500:
            writer.writerow((h, 30 * 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1

with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "unimod_6_1.csv"),
    "w",
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 800 <= h <= 1000:
            writer.writerow((h, 30 * 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1

with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "threemod_1.csv"),
    "w",
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 0 <= h <= 100 or 200 <= h <= 300:
            writer.writerow((h, 6 * 10**11))
        elif 100 < h < 200:
            writer.writerow((h, 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1

with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "threemod_2.csv"),
    "w",
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 600 <= h <= 700 or 800 <= h <= 900:
            writer.writerow((h, 6 * 10**11))
        elif 700 < h < 800:
            writer.writerow((h, 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1

with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "threemod_3.csv"),
    "w",
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 0 <= h <= 200 or 400 <= h <= 600:
            writer.writerow((h, 3 * 10**11))
        elif 200 < h < 400:
            writer.writerow((h, 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1

with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "threemod_4.csv"),
    "w",
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 600 <= h <= 800 or 1000 <= h <= 1200:
            writer.writerow((h, 3 * 10**11))
        elif 800 < h < 1000:
            writer.writerow((h, 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1

with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "threemod_1_1.csv"),
    "w",
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 0 <= h <= 100 or 200 <= h <= 300:
            writer.writerow((h, 60 * 10**11))
        elif 100 < h < 200:
            writer.writerow((h, 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1

with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "threemod_2_1.csv"),
    "w",
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 600 <= h <= 700 or 800 <= h <= 900:
            writer.writerow((h, 60 * 10**11))
        elif 700 < h < 800:
            writer.writerow((h, 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1

with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "threemod_3_1.csv"),
    "w",
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 0 <= h <= 200 or 400 <= h <= 600:
            writer.writerow((h, 30 * 10**11))
        elif 200 < h < 400:
            writer.writerow((h, 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1

with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "threemod_4_1.csv"),
    "w",
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 600 <= h <= 800 or 1000 <= h <= 1200:
            writer.writerow((h, 30 * 10**11))
        elif 800 < h < 1000:
            writer.writerow((h, 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1

with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "unimod500big_1.csv"),
    "w",
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 0 <= h <= 500:
            writer.writerow((h, 1.2 * 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1

with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "unimod500big_2.csv"),
    "w",
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 200 <= h <= 700:
            writer.writerow((h, 1.2 * 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1

with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "unimod500big_3.csv"),
    "w",
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 500 <= h <= 1000:
            writer.writerow((h, 1.2 * 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1

with open(
    Path(
        Path(__file__).parents[1], "data", "profiles_2", "csv", "unimod500big_1_1.csv"
    ),
    "w",
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 0 <= h <= 500:
            writer.writerow((h, 12 * 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1

with open(
    Path(
        Path(__file__).parents[1], "data", "profiles_2", "csv", "unimod500big_2_1.csv"
    ),
    "w",
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 200 <= h <= 700:
            writer.writerow((h, 12 * 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1

with open(
    Path(
        Path(__file__).parents[1], "data", "profiles_2", "csv", "unimod500big_3_1.csv"
    ),
    "w",
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 500 <= h <= 1000:
            writer.writerow((h, 12 * 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1

with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "unimod1000big_1.csv"),
    "w",
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 0 <= h <= 1000:
            writer.writerow((h, 6 * 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1

with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "unimod1000big_2.csv"),
    "w",
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 200 <= h <= 1200:
            writer.writerow((h, 6 * 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1

with open(
    Path(Path(__file__).parents[1], "data", "profiles_2", "csv", "unimod1000big_3.csv"),
    "w",
) as csv_file:
    writer = csv.writer(csv_file)
    h: int = 1500
    while h >= 0:
        if 500 <= h <= 1500:
            writer.writerow((h, 6 * 10**11))
        else:
            writer.writerow((h, 0.5 * 10**11))
        h -= 1
