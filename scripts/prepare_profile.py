import shutil
import csv
import matplotlib.pyplot as plt
from pathlib import Path
from dataclasses import dataclass
from PIL import Image, ImageDraw


@dataclass
class PrepareProfile:
    profiles_name: str

    def cleaning(self, profile_name: str) -> list[tuple[float]]:
        """Noise removal and image output."""
        list_coords: list[tuple[float]] = []
        path_to_profiles = Path(Path(__file__).parents[1], "data", self.profiles_name)
        image = Image.open(Path(path_to_profiles, profile_name))
        draw = ImageDraw.Draw(image)
        width: int = image.size[0]
        height: int = image.size[1]
        pix = image.load()

        for i in range(height):
            for j in range(width):
                a: int = pix[j, i][0]
                b: int = pix[j, i][1]
                c: int = pix[j, i][2]
                if a + b + c > 531:
                    draw.point((j, i), (255, 255, 255))
                else:
                    draw.point((j, i), (0, 0, 0))
                    list_coords.append((1000 - (i * 1000 / height), j * 30 / width))
                    for k in range(j + 1, width):
                        draw.point((k, i), (255, 255, 255))
                    break

        path_to_clean_profile = Path(path_to_profiles, "clean")
        if path_to_clean_profile.is_dir():
            shutil.rmtree(str(path_to_clean_profile), ignore_errors=True)
        path_to_clean_profile.mkdir()
        image.save(Path(path_to_clean_profile, profile_name))

        path_to_csv_profile = Path(path_to_profiles, "csv")
        if path_to_csv_profile.is_dir():
            shutil.rmtree(str(path_to_csv_profile), ignore_errors=True)
        path_to_csv_profile.mkdir()
        with open(Path(path_to_csv_profile, profile_name.replace("png", "csv")), "w") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(list_coords)
        del draw
        return list_coords


if __name__ == "__main__":
    profile_1 = PrepareProfile("profiles_1")
    list_coords: list[tuple[float]] = profile_1.cleaning("profile_06_42.png")
    plt.plot(tuple(x[0] for x in list_coords), tuple(x[1] for x in list_coords))
    plt.show()