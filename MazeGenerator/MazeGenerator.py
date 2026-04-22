from .Cell import Cell
from .Config import Config


class MazeGenerator:
    """
    Handles the management of the maze, from it's generation to it's output.
    It recieves a Config object with the maze specs.
    """
    def __init__(self, configs: Config) -> None:
        """
        Initializes the class
        """
        self.configs: Config = configs
        self.grid: list[list[Cell]] = []

    def display_maze(self) -> None:
        """
        Prints the maze on the terminal.
        """
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
        """
        Creates the maze by inserting the Cells in the MazeGenerator.grid
        """
        width = self.configs.width
        height = self.configs.height
        if (len(self.grid) > 0):
            self.grid.clear()
        for y in range(height):
            row: list[Cell] = []
            for x in range(width):
                row.append(Cell((x, y)))
            self.grid.append(row)

    def insert_42(self) -> None:
        """
        Hardcodes the 42 at the center of the maze
        """
        x = int(self.configs.width / 2)
        y = int(self.configs.height / 2)

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

    def get_maze_hex(self) -> str:
        """
        Returns a string with the full hexadecimal code of the maze
        """
        ret: str = ""
        for lst in self.grid:
            for cell in lst:
                ret_hex: str = hex(cell.get_hex()).upper()
                ret += ret_hex[2:]
            ret += "\n"
        return (ret)

    def get_output_file(self) -> None:
        """
        Creates the output file with all the needed information
        """
        with open(self.configs.output_file, "w") as file:
            file.write(self.get_maze_hex())
            entry_x, entry_y = self.configs.entry
            exit_x, exit_y = self.configs.exit
            file.write(f"\n{entry_x}, {entry_y}\n")
            file.write(f"{exit_x}, {exit_y}")
