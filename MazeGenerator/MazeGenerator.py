from .Cell import Cell
from .Config import Config
from .Exceptions import Error42, MazeError
from random import choice
import sys


sys.setrecursionlimit(200000000)


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
        self.show_path: bool = False

    @staticmethod
    def get_configs(file_name: str) -> Config:
        """
        The function receives the file name, gets the configuration parameter
        pairs in it and then creates a dictionary with its values.
        The file name NEEDS to be in the root for it to work.
        """

        config_dict: dict[str, str] = {}

        try:
            with open(file_name, "r") as file:
                for line in file:
                    if not line.startswith("#"):
                        key = line.split("=")[0]
                        value = line.strip().split("=")[1]
                        config_dict.update({key: value})

        except FileNotFoundError:
            raise FileNotFoundError("Error: Invalid file!")

        except KeyError:
            raise KeyError(f"Error: Invalid configurations in {file_name}!")

        try:
            return Config(config_dict)

        except (KeyError, ValueError, TypeError) as err:
            raise KeyError(f"{err}")

    def display_maze(self) -> None:
        """
        Prints the maze on the terminal if there's any.
        """
        if (not self.grid):
            raise MazeError("There's no maze to display.")
        ret: str = ""
        for y in range(self.configs.height):
            line_1: str = f"{self.configs.color.wall_h}"
            line_2: str = ""
            for x in range(self.configs.width):
                cell: Cell = self.grid[y][x]
                if cell.is_42:
                    if cell.walls["north"] == 1:
                        line_1 += f"{self.configs.color.wall_v}\
{self.configs.color.wall_h}"
                    else:
                        line_1 += f"{self.configs.color.fourty_two_v}\
{self.configs.color.wall_h}"
                    if cell.walls["west"] == 1:
                        line_2 += f"{self.configs.color.wall_h}"
                    else:
                        line_2 += f"{self.configs.color.fourty_two_h}"
                    line_2 += f"{self.configs.color.fourty_two_v}"
                else:
                    if (cell.walls["north"] == 1):
                        line_1 += f"{self.configs.color.wall_v}"
                    else:
                        line_1 += f"{self.configs.color.bg_v}"
                    if (cell.walls["west"] == 1):
                        line_2 += f"{self.configs.color.wall_h}"
                    else:
                        line_2 += f"{self.configs.color.bg_h}"
                    if (cell.exit):
                        line_2 += f"{self.configs.color.exit}"
                    elif (cell.entry):
                        line_2 += f"{self.configs.color.entry}"
                    else:
                        line_2 += f"{self.configs.color.bg_v}"
                    line_1 += f"{self.configs.color.wall_h}"
            line_2 += f"{self.configs.color.wall_h}"
            ret = ret + line_1 + "\n" + line_2 + "\n"
        bottom_line: str = ""
        for x in range(self.configs.width):
            bottom_line += f"{self.configs.color.wall_v}\
{self.configs.color.wall_h}"
        bottom_line += f"{self.configs.color.wall_h}"
        ret += bottom_line
        print(ret)

    def build_grid(self) -> None:
        """
        Creates the maze by inserting the Cells in the MazeGenerator.grid.
        It's still not the real maze, just a grid.
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
        entry_x, entry_y = self.configs.entry
        exit_x, exit_y = self.configs.exit
        self.grid[entry_y][entry_x].entry = True
        self.grid[exit_y][exit_x].exit = True
        if (self.configs.width >= 9 and
                self.configs.height >= 6):
            self.insert_42()

    def verified_neighbors(self, cell: Cell) -> dict[str, Cell]:
        """
        Returns a dictionary with which of the cell's neighbors are valid
        for naviagtion
        """
        visitable_neighbors: dict[str, Cell] = {}
        cell_x, cell_y = cell.coordinates
        top: int = 0
        bottom: int = self.configs.height
        right: int = self.configs.width
        left: int = 0
        if (cell_x + 1 < right and
                not self.grid[cell_y][cell_x + 1].visited):
            visitable_neighbors.update({"east":
                                        self.grid[cell_y][cell_x+1]})
        if (cell_y - 1 >= top and
                not self.grid[cell_y-1][cell_x].visited):
            visitable_neighbors.update({"north":
                                        self.grid[cell_y-1][cell_x]})
        if (cell_y + 1 < bottom and
                not self.grid[cell_y+1][cell_x].visited):
            visitable_neighbors.update({"south":
                                        self.grid[cell_y+1][cell_x]})
        if (cell_x - 1 >= left and
                not self.grid[cell_y][cell_x - 1].visited):
            visitable_neighbors.update({"west":
                                        self.grid[cell_y][cell_x-1]})
        return (visitable_neighbors)

    def make_maze(self, current: Cell, path: list[Cell]) -> None:
        """
        Breaks walls from start to finish randomly, making the maze paths.
        Needs to be called after build_grid and after the insert_42 if you want
        the 42 at the center of the maze
        """
        current.visited = True
        while True:
            visitable_neighbors: dict[str, Cell] = {}
            visitable_neighbors = self.verified_neighbors(current)
            if (not visitable_neighbors):
                if path:
                    current = path.pop()
                    self.make_maze(current, path)
                return
            direction: str = choice(list(visitable_neighbors.keys()))
            neighbor: Cell = visitable_neighbors[direction]
            if (direction == "north"):
                current.destruct_wall("north")
                neighbor.destruct_wall("south")
            elif (direction == "south"):
                current.destruct_wall("south")
                neighbor.destruct_wall("north")
            elif (direction == "east"):
                current.destruct_wall("east")
                neighbor.destruct_wall("west")
            else:
                current.destruct_wall("west")
                neighbor.destruct_wall("east")
            path.append(current)
            self.make_maze(neighbor, path)

    def unperfectify(self) -> None:
        """
        Makes more solution paths for the maze.
        Needs to be called after make_maze
        """
        for lst in self.grid:
            for cell in lst:
                if (not cell.is_42):
                    cell.visited = False
        total_cells: list[Cell] = [c for lst in self.grid for c in lst]
        i: int = 0
        directions: list[str] = ["north", "east", "south", "west"]
        while (i < len(total_cells) * (20 / 100)):
            current_cell: Cell = choice(total_cells)
            if (not current_cell.is_42 and not current_cell.visited):
                direction = choice(directions)
                if (current_cell.walls[direction] != 0 and
                        direction in self.verified_neighbors(current_cell)):
                    current_cell.destruct_wall(direction)
                    current_cell.visited = True
                    i += 1

    def insert_42(self) -> None:
        """
        Hardcodes the 42 at the center of the maze.
        Needs to be called after build_grid and before make_maze
        """
        x = int(self.configs.width / 2)
        y = int(self.configs.height / 2)

        if self.configs.width % 2 == 0:
            x -= 1

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

        if self.configs.width % 2 == 0:
            x += 1

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

        entry_x, entry_y = self.configs.entry
        exit_x, exit_y = self.configs.exit
        if (self.grid[entry_y][entry_x].is_42 is True):
            raise Error42("Invalid entry")
        if (self.grid[exit_y][exit_x].is_42 is True):
            raise Error42("Invalid exit")

        for lst in self.grid:
            for cell in lst:
                if cell.is_42:
                    cell.visited = True

    def solve_maze(self, current: Cell) -> list[Cell]:
        """
        Returns a list with the fastest path from the entry to the exit
        """
        if (not self.grid):
            raise MazeError("No maze to solve")
        for lst in self.grid:
            for cell in lst:
                if (not cell.is_42):
                    cell.visited = False
        #

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
