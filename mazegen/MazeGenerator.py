from .Cell import Cell
from .Config import Config
from .Exceptions import Error42, MazeError
from random import choice
import sys


sys.setrecursionlimit(200000000)


class MazeGenerator:
    """
    MazeGenerator is responsible for creating, displaying, and solving mazes.
    """
    def __init__(self, configs: Config) -> None:
        """
        Initialize MazeGenerator with configuration data.

        Args:
            configs (Config): The configuration object with maze parameters.
        """
        self.configs: Config = configs
        self.grid: list[list[Cell]] = []
        self.show_path: bool = False

    def build_grid(self) -> None:
        """
        Create the initial grid of Cell objects for the maze.

        This method fills the grid with Cell instances, sets entry and exit
        points, and optionally inserts the '42' pattern if the maze is large
        enough.
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

    def display_maze(self) -> None:
        """
        Print the maze to the terminal.

        Raises:
            MazeError: If there is no maze to display.
        """
        if (not self.grid):
            raise MazeError("There's no maze to display.")
        ret: str = ""
        for y in range(self.configs.height):
            line_1: str = f"{self.configs.color.wall_h}"
            line_2: str = ""
            for x in range(self.configs.width):
                cell: Cell = self.grid[y][x]
                if cell.is_pattern:
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
                elif cell.is_path and self.show_path:
                    if cell.walls["north"] == 1:
                        line_1 += f"{self.configs.color.wall_v}\
{self.configs.color.wall_h}"
                    else:
                        if self.grid[y-1][x].is_path:
                            line_1 += f"{self.configs.color.path_v}\
{self.configs.color.wall_h}"
                        else:
                            line_1 += f"{self.configs.color.bg_v}\
{self.configs.color.wall_h}"
                    if cell.walls["west"] == 1:
                        line_2 += f"{self.configs.color.wall_h}"
                    else:
                        if self.grid[y][x-1].is_path:
                            line_2 += f"{self.configs.color.path_h}"
                        else:
                            line_2 += f"{self.configs.color.bg_h}"
                    if not cell.exit and not cell.entry:
                        line_2 += f"{self.configs.color.path_v}"
                    elif cell.entry:
                        line_2 += f"{self.configs.color.entry}"
                    else:
                        line_2 += f"{self.configs.color.exit}"

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

    def verified_neighbors(self, cell: Cell) -> dict[str, Cell]:
        """
        Get valid, unvisited neighboring cells for navigation.

        Args:
            cell (Cell): The cell whose neighbors are to be checked.

        Returns:
            dict[str, Cell]: Dictionary of direction to neighbor Cell.
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
        Recursively carve out a maze by breaking walls between cells.

        Args:
            current (Cell): The current cell being visited.
            path (list[Cell]): The path taken so far (used for backtracking).
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

    def _forms_open_3x3(self, x: int, y: int) -> bool:
        """
        Verifies if breaking a cell wall would create a 3x3 open cells.
        """
        for dy in [-2, -1, 0]:
            for dx in [-2, -1, 0]:
                cells: list[Cell] = []
                for iy in range(3):
                    for ix in range(3):
                        ny, nx = y + dy + iy, x + dx + ix
                        if (0 <= ny < self.configs.height and
                                0 <= nx < self.configs.width):
                            cells.append(self.grid[ny][nx])
                        else:
                            break
                if len(cells) == 9:
                    open_count: int = 0
                    for cell in cells:
                        if sum(cell.walls.values()) < 2:
                            open_count += 1
                    if open_count == 9:
                        return True
        return False

    def unperfectify(self) -> None:
        """
        Randomly break more walls to create multiple solution paths, but
        prevents forming 3x3 open blocks.
        """
        for lst in self.grid:
            for cell in lst:
                if (not cell.is_pattern):
                    cell.visited = False
        total_cells: list[Cell] = [c for lst in self.grid for c in lst]
        i: int = 0
        directions: list[str] = ["north", "east", "south", "west"]
        while (i < len(total_cells) * (40 / 100)):
            current_cell: Cell = choice(total_cells)
            if (len(self.verified_neighbors(current_cell)) > 1):
                if (not current_cell.is_pattern and not current_cell.visited):
                    direction = choice(directions)
                    x, y = current_cell.coordinates
                    if direction == "north" and y - 1 >= 0:
                        neighbor = self.grid[y-1][x]
                        if (current_cell.walls["north"] != 0 and
                                not neighbor.is_pattern and
                                not self._forms_open_3x3(x, y-1)):
                            current_cell.destruct_wall("north")
                            neighbor.destruct_wall("south")
                            current_cell.visited = True
                            i += 1
                    elif direction == "south" and y + 1 < self.configs.height:
                        neighbor = self.grid[y+1][x]
                        if (current_cell.walls["south"] != 0 and
                                not neighbor.is_pattern and
                                not self._forms_open_3x3(x, y+1)):
                            current_cell.destruct_wall("south")
                            neighbor.destruct_wall("north")
                            current_cell.visited = True
                            i += 1
                    elif direction == "east" and x + 1 < self.configs.width:
                        neighbor = self.grid[y][x+1]
                        if (current_cell.walls["east"] != 0 and
                                not neighbor.is_pattern and
                                not self._forms_open_3x3(x+1, y)):
                            current_cell.destruct_wall("east")
                            neighbor.destruct_wall("west")
                            current_cell.visited = True
                            i += 1
                    elif direction == "west" and x - 1 >= 0:
                        neighbor = self.grid[y][x-1]
                        if (current_cell.walls["west"] != 0 and
                                not neighbor.is_pattern and
                                not self._forms_open_3x3(x-1, y)):
                            current_cell.destruct_wall("west")
                            neighbor.destruct_wall("east")
                            current_cell.visited = True
                            i += 1
            i += 1

    def insert_42(self) -> None:
        """
        Insert a hardcoded '42' pattern at the center of the maze.

        Raises:
            Error42: If the entry or exit is inside the '42' pattern.
            MazeError: If the maze is too small for the pattern.
        """
        if (self.configs.width < 9 or self.configs.height < 6):
            raise MazeError("\nMaze too small to insert 42\n")
        x = int(self.configs.width / 2)
        y = int(self.configs.height / 2)

        if self.configs.width % 2 == 0:
            x -= 1

        self.grid[y][x-1].is_pattern = True
        self.grid[y][x-2].is_pattern = True
        self.grid[y][x-3].is_pattern = True
        self.grid[y-1][x-3].is_pattern = True
        self.grid[y-2][x-3].is_pattern = True
        self.grid[y+1][x-1].is_pattern = True
        self.grid[y+2][x-1].is_pattern = True

        if self.configs.width % 2 == 0:
            x += 1

        self.grid[y][x+1].is_pattern = True
        self.grid[y][x+2].is_pattern = True
        self.grid[y][x+3].is_pattern = True

        self.grid[y-1][x+3].is_pattern = True
        self.grid[y-2][x+3].is_pattern = True

        self.grid[y-2][x+2].is_pattern = True
        self.grid[y-2][x+1].is_pattern = True
        self.grid[y+1][x+1].is_pattern = True
        self.grid[y+2][x+1].is_pattern = True

        self.grid[y+2][x+2].is_pattern = True
        self.grid[y+2][x+3].is_pattern = True

        entry_x, entry_y = self.configs.entry
        exit_x, exit_y = self.configs.exit
        if (self.grid[entry_y][entry_x].is_pattern is True):
            raise Error42("Invalid entry: Inside 42")
        if (self.grid[exit_y][exit_x].is_pattern is True):
            raise Error42("Invalid exit: Inside 42")

        for lst in self.grid:
            for cell in lst:
                if cell.is_pattern:
                    directions: list[str] = ["north", "south", "east", "west"]
                    cell.visited = True
                    for direction in directions:
                        cell.build_wall(direction)

    def insert_67(self) -> None:
        """
        Insert a hardcoded '67' pattern at the center of the maze.

        Raises:
            Error42: If the entry or exit is inside the '67' pattern.
            MazeError: If the maze is too small for the pattern.
        """
        if (self.configs.width < 9 or self.configs.height < 6):
            raise MazeError("\nMaze too small to insert 67\n")
        if (not self.grid):
            print("No grid has been created yet")
            return
        x = int(self.configs.width / 2)
        y = int(self.configs.height / 2)

        if self.configs.width % 2 == 0:
            x -= 1

        self.grid[y][x-1].is_pattern = True
        self.grid[y][x-3].is_pattern = True
        self.grid[y][x-3].is_pattern = True
        self.grid[y+1][x-3].is_pattern = True
        self.grid[y+2][x-3].is_pattern = True
        self.grid[y+2][x-2].is_pattern = True
        self.grid[y-1][x-3].is_pattern = True
        self.grid[y-2][x-3].is_pattern = True
        self.grid[y+2][x-1].is_pattern = True
        self.grid[y+2][x].is_pattern = True
        self.grid[y+1][x].is_pattern = True
        self.grid[y][x].is_pattern = True

        if self.configs.width % 2 == 0:
            x += 1

        self.grid[y][x+3].is_pattern = True

        self.grid[y-1][x+3].is_pattern = True
        self.grid[y-2][x+3].is_pattern = True

        self.grid[y-2][x+2].is_pattern = True
        self.grid[y-2][x+1].is_pattern = True

        self.grid[y+2][x+3].is_pattern = True
        self.grid[y+1][x+3].is_pattern = True

        entry_x, entry_y = self.configs.entry
        exit_x, exit_y = self.configs.exit
        if (self.grid[entry_y][entry_x].is_pattern is True):
            raise Error42("Invalid entry: Inside 67")
        if (self.grid[exit_y][exit_x].is_pattern is True):
            raise Error42("Invalid exit: Inside 67")

        for lst in self.grid:
            for cell in lst:
                if cell.is_pattern:
                    cell.visited = True

        for lst in self.grid:
            for cell in lst:
                if cell.is_pattern:
                    directions: list[str] = ["north", "south", "east", "west"]
                    cell.visited = True
                    for direction in directions:
                        cell.build_wall(direction)

    def solve_maze(self) -> list[Cell]:
        """
        Find the shortest path from the maze entry to the exit using BFS.

        Returns:
            list[Cell]: List of cells representing the solution path.
        """
        def get_neighbor(direction: str, cell: Cell) -> Cell:
            """
            Get the neighboring cell in the specified direction.

            Args:
                direction (str): The direction to look for the neighbor.
                cell (Cell): The reference cell.

            Returns:
                Cell: The neighboring cell in the given direction.
            """
            x, y = cell.coordinates
            if direction == "north":
                y -= 1
            elif direction == "east":
                x += 1
            elif direction == "south":
                y += 1
            else:
                x -= 1
            neighbor = self.grid[y][x]
            return neighbor

        for lst in self.grid:
            for cell in lst:
                if cell.is_pattern is not True:
                    cell.visited = False
        entry_x, entry_y = self.configs.entry
        start = self.grid[entry_y][entry_x]

        end_x, end_y = self.configs.exit
        end: Cell = self.grid[end_y][end_x]

        queue: list[Cell] = []
        visited: list[Cell] = []
        parent: dict[tuple[int, int], tuple[int, int]] = {}

        queue.append(start)
        visited.append(start)

        while queue:
            cell = queue.pop(0)
            cell.visited = True
            if cell == end:
                break
            for direction, wall in cell.walls.items():
                if wall == 0:
                    neighbor = get_neighbor(direction, cell)
                    if neighbor not in visited:
                        visited.append(neighbor)
                        parent[neighbor.coordinates] = cell.coordinates
                        queue.append(neighbor)

        path: list[Cell] = []
        cur: Cell = end
        start.is_path = True
        while cur != start:
            cur.is_path = True
            path.append(cur)
            temp_x, temp_y = parent[cur.coordinates]
            cur = self.grid[temp_y][temp_x]
        path.append(start)
        path.reverse()
        return (path)

    def get_path(self) -> str:
        """
        Get the directions from entry to exit as a string (e.g., 'SENW').

        Returns:
            str: Directions to the exit using 'N', 'S', 'E', 'W'.
        """
        path: list[Cell] = self.solve_maze()
        ret: str = ""
        for i in range(len(path)):
            if (i + 1 < len(path)):
                x1, y1 = path[i].coordinates
                x2, y2 = path[i+1].coordinates
                if (x1 == x2):
                    if (y1 - y2 < 0):
                        ret += "S"
                    else:
                        ret += "N"
                else:
                    if (x1 - x2 < 0):
                        ret += "E"
                    else:
                        ret += "W"
        return (ret)

    def get_maze_hex(self) -> str:
        """
        Get the hexadecimal representation of the maze.

        Returns:
            str: The maze as a string of hexadecimal codes.
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
        Write the maze, entry/exit, and solution path to the output file.
        """
        with open(self.configs.output_file, "w") as file:
            file.write(self.get_maze_hex())
            entry_x, entry_y = self.configs.entry
            exit_x, exit_y = self.configs.exit
            file.write(f"\n{entry_x}, {entry_y}\n")
            file.write(f"{exit_x}, {exit_y}")
            file.write(f"\n{self.get_path()}\n")
