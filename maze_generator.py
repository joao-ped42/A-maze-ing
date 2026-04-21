class Cell:

    def __init__(self, coords: tuple[int, int]) -> None:
        self.coordinates: tuple[int, int] = coords
        self.walls: dict[str, int] = {
            "north": 1,
            "east": 1,
            "south": 1,
            "west": 1
        }
        self.visited = False

    def destruct_wall(self, direction: str) -> None:
        self.walls.update({direction: 0})

    def build_wall(self, direction: str) -> None:
        self.walls.update({direction: 1})

    def get_hex(self) -> int:
        north = self.walls["north"]
        east = self.walls["east"]
        south = self.walls["south"]
        west = self.walls["west"]
        return north + 2 * east + 4 * south + 8 * west


class Config():

    def __init__(self, config_dict: dict[str, str]) -> None:

        if int(config_dict["WIDTH"]) <= 0:
            raise ValueError("Invalid width")
        self.width = int(config_dict["WIDTH"])

        if int(config_dict["HEIGHT"]) <= 0:
            raise ValueError("Invalid height")
        self.height = int(config_dict["HEIGHT"])

        x, y = config_dict["ENTRY"].split(",")
        if (int(x) < 0 or int(x) > self.width) or (int(y) < 0 or int(y) > self.height):
            raise ValueError("Invalid entry")
        self.entry: tuple[int, int] = int(x), int(y)

        x2, y2 = config_dict["EXIT"].split(",")
        if x == x2 and y == y2:
            raise ValueError("Entry must be different than exit")
        if (int(x) < 0 or int(x) > self.width) or (int(y) < 0 or int(y) > self.height):
            raise ValueError("Invalid exit")
        self.exit: tuple[int, int] = int(x2), int(y2)

        if not config_dict["OUTPUT_FILE"].endswith(".txt"):
            raise ValueError("Invalid output file extension")
        self.output_file: str = config_dict["OUTPUT_FILE"]

        if config_dict["PERFECT"].upper() not in ["TRUE", "FALSE"]:
            raise ValueError("Invalid perfect value")
        self.perfect: bool = config_dict["PERFECT"].upper() == "TRUE"
