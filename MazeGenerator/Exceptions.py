class InputError(Exception):
    """
    An error for when the user doesn't choose the right number
    """
    pass


class Error42(Exception):
    """
    An error for when the entry or exit coordinates are inside the 42 pattern
    """
    pass


class MazeError(Exception):
    """
    Generic error for Maze operations
    """
    pass
