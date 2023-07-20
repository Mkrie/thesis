import sys
import csv
import matplotlib.pyplot as plt
from pathlib import Path

from direct_measurements import DirectMeasurements

dict_profile_time = {("06", "42"): "PM004A",
                     ("07", "05"): "PM004D",
                     ("07", "37"): "PM005A",
                     ("08", "08"): "PM005D",
                     ("09", "42"): "PM006A",
                     ("10", "13"): "PM006D",
                     ("11", "01"): "PM007A",
                     ("11", "27"): "PM007D",
                     ("13", "06"): "PM008A",
                     ("13", "23"): "PM008D",
                     ("16", "54"): "PM010A",
                     ("17", "17"): "PM010D",
                     ("17", "46"): "PM011A",
                     ("18", "04"): "PM011D"}

plt.figure(figsize=(15, 10))
plt.rc('font', size= 15 )
for txt_path in Path(Path.cwd().parent,
                     "data", "profiles_1",
                     "csv").glob("*.csv"):
    with open(txt_path, "r") as csv_file:
        reader = csv.reader(csv_file)
        tup_coords: tuple[tuple[str]] = tuple(reader)
        plt.minorticks_on()
        plt.grid(which='major', color = 'k', linewidth = 1)
        plt.grid(which='minor', color = 'k', linestyle = ':')
        plt.xlim(0, 90)
        plt.ylim(0, 3*10**17)
        plt.xlabel("angle, °")
        plt.ylabel(r"$\xi$ [$cm^{-2}$]")
        #plt.title(r'$NO_2 \, profiles$')
        dir_meas = DirectMeasurements(txt_path.name, 0, "dataset_2_csv", "profiles_1")
        tup_dir_meas = dir_meas.direct_measurements_for_profile()
        list_text = txt_path.name.replace(".csv", "").split("_")
        plt.plot(tuple(float(x[0]) for x in tup_dir_meas),
                 tuple(float(x[1]) * 100 for x in tup_dir_meas),
                 "-o",
                 linewidth=3,
                 label=f"{dict_profile_time.get(tuple(list_text[1:]))}: {list_text[1]}:{list_text[2]}",)
        plt.legend()
plt.show()