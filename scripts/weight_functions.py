import matplotlib.pyplot as plt
import csv
from pathlib import Path


plt.figure(figsize=(15, 10))
plt.rc("font", size=15)
for txt_path in sorted(Path(Path.cwd().parent, "data", "dataset_2_csv").glob("*.csv")):
    with open(txt_path, "r") as csv_file:
        reader = csv.reader(csv_file)
        tup_coords: tuple[tuple[str]] = tuple(reader)
        plt.minorticks_on()
        plt.grid(which="major", color="k", linewidth=1)
        plt.grid(which="minor", color="k", linestyle=":")
        plt.xlim(0, 1000)
        plt.ylim(0, 70)
        plt.xlabel("h[m]")
        plt.ylabel("$m[]$")
        # plt.title(txt_path.name.replace(".csv", "").replace("_", " "))
        label = txt_path.name.replace(".csv", "").replace("_", " ").split()[1:]
        print(label)
        if len(label) == 1:
            label = f"{float(label[0])}°"
        else:
            label = f"{round((int(label[0]) + 0.1 * int(label[1])), 2)}°"
        plt.plot(
            [float(x[0]) * 1000 for x in tup_coords],
            [float(x[1]) for x in tup_coords],
            "-o",
            linewidth=3,
            label=label,
        )

plt.legend()
plt.show()
