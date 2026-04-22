from typing import Optional


class Config():
    """
    Stores information from the config.txt file.
    """
    def __init__(self, config_dict: dict[str, str]) -> None:
        """
        Initializes the class
        """
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
        """
        Verifies if the width is negative.
        """
        if (int(width) <= 0):
            raise ValueError("Invalid width")
        return (int(width))

    @staticmethod
    def _validate_height(height: str) -> int:
        """
        Verifies if the height is negative.
        """
        if (int(height) <= 0):
            raise ValueError("Invalid height")
        return (int(height))

    @staticmethod
    def _validate_output_file_name(output_file_name: str) -> str:
        """
        Verifies if the output file name is a text extension.
        """
        if (not output_file_name.endswith(".txt")):
            raise ValueError("Invalid output file extension")
        return (output_file_name)

    @staticmethod
    def _validate_perfect(perfect_value: str) -> bool:
        """
        Verifies if it's True or False.
        """
        if (perfect_value.upper() not in ["TRUE", "FALSE"]):
            raise ValueError("Invalid perfect value")
        return (perfect_value.upper() == "TRUE")

    def _validate_entry(self, entry_coord: str) -> tuple[int, int]:
        """
        Verifies if the entry coordinates is out of bounds.
        """
        x, y = entry_coord.split(",")
        if (int(x) < 0 or int(y) < 0):
            raise ValueError("Invalid entry")
        elif (int(x) > self.width or int(y) > self.height):
            raise ValueError("Invalid entry")
        return (int(x), int(y))

    def _validate_exit(self, exit_coord: str) -> tuple[int, int]:
        """
        Verifies if the exit coordinates is out of bounds.
        """
        x, y = exit_coord.split(",")
        if (int(x) < 0 or int(y) < 0):
            raise ValueError("Invalid exit")
        elif (int(x) > self.width or int(y) > self.height):
            raise ValueError("Invalid exit")
        elif ((int(x), int(y)) == self.entry):
            raise ValueError("Invalid exit")
        return (int(x), int(y))
