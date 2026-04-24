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

        self.wall_h = wall + "█\033[0m"
        self.wall_v = wall + "██\033[0m"
        self.bg_h = bg + "█\033[0m"
        self.bg_v = bg + "██\033[0m"
        self.fourty_two_h = fourty_two + "█\033[0m"
        self.fourty_two_v = fourty_two + "██\033[0m"
        self.entry = entry + "██\033[0m"
        self.exit = exit + "██\033[0m"
        self.path = path + "██\033[0m"


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


class CandyStore(Pallet):
    def __init__(self) -> None:
        super().__init__("\033[38;2;173;19;19m",
                         "\033[38;2;247;229;156m",
                         "\033[38;2;89;158;82m",
                         "\033[38;2;49;94;176m",
                         "\033[38;2;22;23;33m",
                         "\033[38;2;245;188;227m")


class Quaquaval(Pallet):
    def __init__(self) -> None:
        super().__init__("\033[38;2;54;79;160m",
                         "\033[38;2;138;209;223m",
                         "\033[38;2;237;248;251m",
                         "\033[38;2;246;181;85m",
                         "\033[38;2;224;74;22m",
                         "\033[38;2;228;116;47m")


class SSalazzle(Pallet):
    def __init__(self) -> None:
        super().__init__("\033[38;2;255;255;255m",
                         "\033[38;2;120;117;145m",
                         "\033[38;2;242;88;133m",
                         "\033[38;2;177;162;213m",
                         "\033[38;2;0;0;0m",
                         "\033[38;2;215;217;255m")


class Brits(Pallet):
    def __init__(self) -> None:
        super().__init__("\033[38;2;181;118;246m",
                         "\033[38;2;34;3;65m",
                         "\033[38;2;65;247;236m",
                         "\033[38;2;210;43;232m",
                         "\033[38;2;255;255;255m",
                         "\033[38;2;240;166;250m")


class HomemDeFerro(Pallet):
    def __init__(self) -> None:
        super().__init__("\033[38;2;212;8;8m",
                         "\033[38;2;206;161;63m",
                         "\033[38;2;34;234;245m",
                         "\033[38;2;230;252;255m",
                         "\033[38;2;42;2;11m",
                         "\033[38;2;0;104;121m")
