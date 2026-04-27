class Cell:
    """
    Represents each square in the maze.
    Each Cell has 4 wall directions, 1 means closed, 0 means open.
    When created, all walls are closed.
    """

    def __init__(self, coords: tuple[int, int]) -> None:
        """
        Initializes the cell with coordinates and closed walls.

        Args:
            coords (tuple[int, int]): Cell coordinates.
        """
        self.coordinates: tuple[int, int] = coords
        self.walls: dict[str, int] = {
            "north": 1,
            "east": 1,
            "south": 1,
            "west": 1
        }
        self.is_pattern: bool = False
        self.is_path: bool = False
        self.visited: bool = False
        self.entry: bool = False
        self.exit: bool = False

    def destruct_wall(self, direction: str) -> None:
        """
        Breaks a wall of the cell, making it open.

        Args:
            direction (str): Direction of the wall to break.
        """
        self.walls.update({direction: 0})

    def build_wall(self, direction: str) -> None:
        """
        Builds a wall of the cell, making it closed.

        Args:
            direction (str): Direction of the wall to build.
        """
        self.walls.update({direction: 1})

    def get_hex(self) -> int:
        """
        Returns the hexadecimal code of the cell based on its walls.

        Returns:
            int: Hexadecimal code of the cell.
        """
        north = self.walls["north"]
        east = self.walls["east"]
        south = self.walls["south"]
        west = self.walls["west"]
        return north + 2 * east + 4 * south + 8 * west
