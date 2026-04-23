class Cell:
    """
    Represents each square in the maze.
    Each Cell has 4 wall directions, 1 means closed, 0 means open.
    When created, all walls are closed.
    """
    def __init__(self, coords: tuple[int, int]) -> None:
        """
        Initializes the class
        """
        self.coordinates: tuple[int, int] = coords
        self.walls: dict[str, int] = {
            "north": 1,
            "east": 1,
            "south": 1,
            "west": 1
        }
        self.is_42 = False
        self.visited = False
        self.entry = False
        self.exit = False

        self.color = "\033[97m██\033[0m"

    def destruct_wall(self, direction: str) -> None:
        """
        Kills a wall out of the existence by changing one of the Cell.walls
        value to 0
        """
        self.walls.update({direction: 0})

    def build_wall(self, direction: str) -> None:
        """
        Brings a wall to life by changing one of the Cell.walls
        value to 0
        """
        self.walls.update({direction: 1})

    def get_hex(self) -> int:
        """
        Gets the Cell's hexadecimal code
        """
        north = self.walls["north"]
        east = self.walls["east"]
        south = self.walls["south"]
        west = self.walls["west"]
        return north + 2 * east + 4 * south + 8 * west
