class Pallet:
    """
    Colors
    """
    def __init__(self,
                 wall: str,
                 bg: str,
                 fourty_two: str,
                 entry: str,
                 exit: str,
                 path: str) -> None:

        self.wall = wall
        self.bg = bg
        self.fourty_two = fourty_two
        self.entry = entry
        self.exit = exit
        self.path = path


class Default(Pallet):
    def __init__(self) -> None:
        super().__init__("\033[38;2;255;255;255m",
                         "\033[38;2;0;0;0m",
                         "\033[38;2;6;170;189m",
                         "\033[38;2;6;189;79m",
                         "\033[38;2;194;37;58m",
                         "\033[38;2;255;196;246m")


class VSCode(Pallet):
    def __init__(self) -> None:
        super().__init__("\033[38;2;16;160;227m",
                         "\033[38;2;25;55;69m",
                         "\033[38;2;247;232;96m",
                         "\033[38;2;19;191;99m",
                         "\033[38;2;138;74;128m",
                         "\033[38;2;252;133;73m")
