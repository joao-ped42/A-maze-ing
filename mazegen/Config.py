from typing import Optional
from .Pallets import Pallet, Default


class Config():
    """
    Stores information from the config.txt file.
    """
    def __init__(self,
                 width: int,
                 height: int,
                 entry_coord: tuple[int, int],
                 exit_coord: tuple[int, int],
                 output_file: str,
                 perfect: bool,
                 seed: Optional[int] = None,
                 color: Pallet = Default()) -> None:
        """
        Initializes the configuration for the maze.

        Args:
            width (int): Maze width.
            height (int): Maze height.
            entry_coord (tuple[int, int]): Entry coordinates.
            exit_coord (tuple[int, int]): Exit coordinates.
            output_file (str): Output file name.
            perfect (bool): Whether the maze is perfect.
            seed (Optional[int]): Random seed.
            color (Pallet): Color pallet.
        """
        self.width: int = self._validate_width(width)
        self.height: int = self._validate_height(height)
        self.entry: tuple[int, int] = self._validate_entry(entry_coord)
        self.exit: tuple[int, int] = self._validate_exit(exit_coord)
        self.output_file: str = self._validate_output_file_name(output_file)
        self.perfect: bool = perfect
        self.seed: Optional[int] = seed
        self.color: Pallet = color

    @staticmethod
    def _validate_width(width: int) -> int:
        """
        Checks if the width is valid.

        Args:
            width (int): Maze width.
        Returns:
            int: Validated width.
        Raises:
            ValueError: If the width is invalid.
        """
        if (width <= 0):
            raise ValueError("Invalid width")
        return (width)

    @staticmethod
    def _validate_height(height: int) -> int:
        """
        Checks if the height is valid.

        Args:
            height (int): Maze height.
        Returns:
            int: Validated height.
        Raises:
            ValueError: If the height is invalid.
        """
        if (height <= 0):
            raise ValueError("Invalid height")
        return (height)

    @staticmethod
    def _validate_output_file_name(output_file_name: str) -> str:
        """
        Checks if the output file name has a valid text extension.

        Args:
            output_file_name (str): Output file name.
        Returns:
            str: Validated name.
        Raises:
            ValueError: If the extension is invalid.
        """
        if (not output_file_name.endswith(".txt")):
            raise ValueError("Invalid output file extension")
        return (output_file_name)

    def _validate_entry(self, entry_coord: tuple[int, int]) -> tuple[int, int]:
        """
        Checks if the entry coordinates are within bounds.

        Args:
            entry_coord (tuple[int, int]): Entry coordinates.
        Returns:
            tuple[int, int]: Validated coordinates.
        Raises:
            ValueError: If the coordinates are invalid.
        """
        x, y = entry_coord
        if (x < 0 or y < 0):
            raise ValueError("Invalid entry")
        elif (x > self.width or y > self.height):
            raise ValueError("Invalid entry")
        return (x, y)

    def _validate_exit(self, exit_coord: tuple[int, int]) -> tuple[int, int]:
        """
        Checks if the exit coordinates are within bounds.

        Args:
            exit_coord (tuple[int, int]): Exit coordinates.
        Returns:
            tuple[int, int]: Validated coordinates.
        Raises:
            ValueError: If the coordinates are invalid.
        """
        x, y = exit_coord
        if (x < 0 or y < 0):
            raise ValueError("Invalid exit")
        elif (x > self.width or y > self.height):
            raise ValueError("Invalid exit")
        elif ((x, y) == self.entry):
            raise ValueError("Invalid exit")
        return (x, y)
