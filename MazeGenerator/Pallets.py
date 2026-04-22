class Pallet:
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


class VSCode(Pallet):
    def __init__(self):
        super().__init__("\033[38;2;16;160;227m", "\033[48;237m", "\033[38;2;247;232;96m", "\033[48;78m", "\033[48;5;124m", "\033[48;5;214m")
