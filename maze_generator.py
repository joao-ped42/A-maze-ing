from typing import Optional, IO


class Config():
    """
    Stores information from the config.txt file
    """
    def __init__(self, config_dict: dict[str, str]) -> None:

        self.width: int = self._validate_width(config_dict["WIDTH"])
        self.height: int = self._validate_height(config_dict["HEIGHT"])
        self.entry: tuple[int, int] = self._validate_entry(
            config_dict["ENTRY"])
        self.exit: tuple[int, int] = self._validate_exit(config_dict["EXIT"])
        self.output_file: str = self._validate_output_file_name(
            config_dict["OUTPUT_FILE"])
        self.perfect: bool = self._validate_perfect(config_dict["PERFECT"])
        self.seed: Optional[int] = None
        if ("SEED" in config_dict):
            self.seed = int(config_dict["SEED"])

    @staticmethod
    def _validate_width(width: str) -> int:
        if (int(width) <= 0):
            raise ValueError("Invalid width")
        return (int(width))

    @staticmethod
    def _validate_height(height: str) -> int:
        if (int(height) <= 0):
            raise ValueError("Invalid height")
        return (int(height))

    @staticmethod
    def _validate_output_file_name(output_file_name: str) -> str:
        if (not output_file_name.endswith(".txt")):
            raise ValueError("Invalid output file extension")
        return (output_file_name)

    @staticmethod
    def _validate_perfect(perfect_value: str) -> bool:
        if (perfect_value.upper() not in ["TRUE", "FALSE"]):
            raise ValueError("Invalid perfect value")
        return (perfect_value.upper() == "TRUE")

    def _validate_entry(self, entry_coord: str) -> tuple[int, int]:
        x, y = entry_coord.split(",")
        if (int(x) < 0 or int(y) < 0):
            raise ValueError("Invalid entry")
        elif (int(x) > self.width or int(y) > self.height):
            raise ValueError("Invalid entry")
        return (int(x), int(y))

    def _validate_exit(self, exit_coord: str) -> tuple[int, int]:
        x, y = exit_coord.split(",")
        if (int(x) < 0 or int(y) < 0):
            raise ValueError("Invalid exit")
        elif (int(x) > self.width or int(y) > self.height):
            raise ValueError("Invalid exit")
        elif ((int(x), int(y)) == self.entry):
            raise ValueError("Invalid exit")
        return (int(x), int(y))


class Cell:
    """
    Represents each square in the maze.
    Each Cell has 4 wall directions, 1 means closed, 0 means open.
    When created, all walls are closed.
    """
    def __init__(self, coords: tuple[int, int]) -> None:
        self.coordinates: tuple[int, int] = coords
        self.walls: dict[str, int] = {
            "north": 1,
            "east": 1,
            "south": 1,
            "west": 1
        }
        self.visited = False
        self.is_42 = False
        if self.is_42:
            self.visited = True

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

    @staticmethod
    def put_horizontal() -> None:
        print("████", end="")

    @staticmethod
    def put_vertical() -> None:
        print("█  █", end="")


class MazeGenerator:
    """
    Handles the management of the maze, from it's generation to it's output.
    """
    def __init__(self, configs: Config) -> None:
        self.configs: Config = configs
        self.grid: list[list[Cell]] = []

    def display_maze(self) -> None:
        ret: str = ""
        for y in range(self.configs.height):
            line_1: str = "█"
            line_2: str = ""
            for x in range(self.configs.width):
                cell: Cell = self.grid[y][x]
                empty: str = "  "
                if cell.is_42:
                    if cell.walls["north"] == 1:
                        line_1 += "███"
                    else:
                        line_1 += "\033[31m██\033[0m█"
                    if cell.walls["west"] == 1:
                        line_2 += "█"
                    else:
                        line_2 += "\033[31m█\033[0m"
                    line_2 += "\033[31m██\033[0m"
                else:
                    if (cell.walls["north"] == 1):
                        line_1 += "██"
                    else:
                        line_1 += empty
                    if (cell.walls["west"] == 1):
                        line_2 += "█"
                    else:
                        line_2 += " "
                    line_2 += empty
                    line_1 += "█"
            line_2 += "█"
            ret = ret + line_1 + "\n" + line_2 + "\n"
        bottom_line: str = ""
        for x in range(self.configs.width):
            bottom_line += "███"
        bottom_line += "█"
        ret += bottom_line
        print(ret)

    def build_grid(self) -> None:
        width = self.configs.width
        height = self.configs.height

        for y in range(height):
            row: list[Cell] = []
            for x in range(width):
                row.append(Cell((x, y)))
            self.grid.append(row)

    def insert_42(self) -> None:
        x = int(self.configs.width / 2)
        y = int(self.configs.height / 2)

        # 4 format
        # self.grid[x-1][y].is_42 = True
        # self.grid[x-2][y].is_42 = True
        # self.grid[x-3][y].is_42 = True
        # self.grid[x-3][y-1].is_42 = True
        # self.grid[x-3][y-2].is_42 = True
        # self.grid[x-1][y+1].is_42 = True
        # self.grid[x-1][y+2].is_42 = True
        self.grid[y][x-1].is_42 = True
        self.grid[y][x-1].walls.update({"west": 0})
        self.grid[y][x-2].is_42 = True
        self.grid[y][x-2].walls.update({"west": 0})
        self.grid[y][x-3].is_42 = True
        self.grid[y][x-3].walls.update({"north": 0})
        self.grid[y-1][x-3].is_42 = True
        self.grid[y-1][x-3].walls.update({"north": 0})
        self.grid[y-2][x-3].is_42 = True
        self.grid[y+1][x-1].is_42 = True
        self.grid[y+1][x-1].walls.update({"north": 0})
        self.grid[y+2][x-1].is_42 = True
        self.grid[y+2][x-1].walls.update({"north": 0})

        # 2 format
        self.grid[y][x+1].is_42 = True
        self.grid[y][x+2].is_42 = True
        self.grid[y][x+2].walls.update({"west": 0})
        self.grid[y][x+3].is_42 = True
        self.grid[y][x+3].walls.update({"north": 0})
        self.grid[y][x+3].walls.update({"west": 0})
        
        self.grid[y-1][x+3].is_42 = True
        self.grid[y-1][x+3].walls.update({"north": 0})
        self.grid[y-2][x+3].is_42 = True
        self.grid[y-2][x+3].walls.update({"west": 0})

        self.grid[y-2][x+2].is_42 = True
        self.grid[y-2][x+2].walls.update({"west": 0})
        self.grid[y-2][x+1].is_42 = True
        self.grid[y+1][x+1].is_42 = True
        self.grid[y+1][x+1].walls.update({"north": 0})
        self.grid[y+2][x+1].is_42 = True
        self.grid[y+2][x+1].walls.update({"north": 0})
        
        self.grid[y+2][x+2].is_42 = True
        self.grid[y+2][x+2].walls.update({"west": 0})
        self.grid[y+2][x+3].is_42 = True
        self.grid[y+2][x+3].walls.update({"west": 0})

    def get_maze_hex(self, file: IO) -> None:
        ret: str = ""
        for lst in self.grid:
            for cell in lst:
                ret_hex: str = hex(cell.get_hex()).upper()
                ret += ret_hex[2:]
            ret += "\n"
        file.write(ret)

    def get_output_file(self) -> None:
        with open(self.configs.output_file, "w") as file:
            self.get_maze_hex(file)
            entry_x, entry_y = self.configs.entry
            exit_x, exit_y = self.configs.exit
            file.write(f"\n{entry_x}, {entry_y}\n")
            file.write(f"{exit_x}, {exit_y}")
