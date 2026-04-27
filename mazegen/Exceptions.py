class InputError(Exception):
    """
    Exception for when the user does not choose the correct number.
    """

    pass


class Error42(Exception):
    """
    Exception for when the entry or exit coordinates are inside the 42 pattern.
    """

    pass


class MazeError(Exception):
    """
    Generic exception for Maze operations.
    """

    pass
