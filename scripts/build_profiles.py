import csv
from pathlib import Path

import matplotlib.pyplot as plt

from profile_recovery import ProfileRec

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

path_to_profiles = Path(Path(__file__).parents[1], "data", "profiles_1", "csv")
k: int = 1
for txt_path in path_to_profiles.glob("*.csv"):
    sp = plt.subplot(2,2,k)
    prof_recovery = ProfileRec(txt_path.name)
    rec = prof_recovery.linear_programming(0.3)
    plt.plot(rec[0], rec[1], linewidth=3, label="restored")
    with open(txt_path, "r") as csv_file:
        reader = csv.reader(csv_file)
        tup_coords: tuple[tuple[str]] = tuple(reader)
        plt.minorticks_on()
        plt.grid(which="major", color="k", linewidth=1)
        plt.grid(which="minor", color="k", linestyle=":")
        plt.xlim(0, 1000)
        # plt.ylim(0, 6*10**7)
        plt.xlabel("h[m]")
        plt.ylabel(r"$n$ [$m^{-3}$]")
        list_text = txt_path.name.replace(".csv", "").split("_")
        plt.title(f"{dict_profile_time.get(tuple(list_text[1:]))}: {list_text[1]}:{list_text[2]}")
        plt.plot(
            tuple(float(x[0]) for x in tup_coords),
            tuple(float(x[1]) for x in tup_coords),
            linewidth=3,
            label="original",
        )
    plt.legend()
    k += 1
    if k > 4:
        k = 1
        plt.figure()
plt.show()
# var1 = [1, 2, 3, 4, 5, 6]
# var2 = [7, 13, 16, 18, 25, 19]
# var3 = [29, 25, 20, 25, 20, 18]
#
# # define grid of plots
# fig, axs = plt.subplots(nrows=3, ncols=2)
#
# # add title
# fig.suptitle('Plots Stacked Vertically')
#
# # add data to plots
# axs[0][0].plot(var1, var2)
# axs[1][0].plot(var1, var3)
# axs[2][0].plot(var2, var3)
# plt.show()
