import sys
from MazeGenerator import Config, MazeGenerator, InputError, Pallets
from os import system
from typing import Generator


def get_configs(file_name: str) -> Config:
    """
    The function receives the file name, gets the configuration parameter pairs
    in it and then creates a dictionary with its values.
    """

    config_dict: dict[str, str] = {}

    try:
        with open(file_name, "r") as file:
            for line in file:
                if not line.startswith("#"):
                    key = line.split("=")[0]
                    value = line.strip().split("=")[1]
                    config_dict.update({key: value})

    except FileNotFoundError:
        raise FileNotFoundError("Error: Invalid file!")

    except KeyError:
        raise KeyError(f"Error: Invalid configurations in {file_name}!")

    try:
        return Config(config_dict)

    except (KeyError, ValueError, TypeError) as err:
        raise KeyError(f"{err}")


def display_config(config: Config) -> None:
    print(config.width)
    print(config.height)
    print(config.entry)
    print(config.exit)
    print(config.output_file)
    print(config.perfect)
    print(config.seed)


def clearify() -> None:
    """
    Clears the terminal
    """
    system("clear")


def display_options() -> str:
    print("\n==A-Maze-In==")
    print("1. Re-generate a new maze")
    print("2. Show/Hide path from entry to exit")
    print("3. Rotate colors")
    print("4. Quit")
    try:
        answer: str = input("Choice? (1-4): ")
        if (answer in "1234"):
            return (answer)
        raise InputError("Choose a number 1-4!")
    except InputError as e:
        print(e)
        return (display_options())


def choose_color() -> Generator[Pallets.Pallet, None, None]:
    colors: list[Pallets.Pallet] = [Pallets.VSCode()]
    while True:
        for color in colors:
            yield (color)


def display_interface(maze_generator: MazeGenerator) -> None:
    maze_generator.build_grid()
    color = choose_color()
    if (maze_generator.configs.width >= 9 and
            maze_generator.configs.height >= 6):
        maze_generator.insert_42()
        # se as cordenadas do entry ou do exit estiverem numa Cell que is_42 ==
        # True
        #   raise error
    else:
        print("42 unprintable :(")
    maze_generator.get_output_file()
    maze_generator.display_maze(next(color))
    answer: str = display_options()
    match answer:
        case "1":
            system(f"rm -rf {maze_generator.configs.output_file}")
            clearify()
            display_interface(maze_generator)
        case "2":
            pass
        case "3":
            pass
        case "4":
            return


def main(file_name: str) -> None:
    """
    Runs the main program.
    """
    try:
        configs: Config = get_configs(file_name)
        generator = MazeGenerator(configs)
        display_interface(generator)
    except Exception as err:
        print(f"{err}")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Error: missing configuration file")
