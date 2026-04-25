import sys
from MazeGenerator import Config, MazeGenerator, InputError, Pallets, Cell
from os import system
from typing import Generator
import random


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


def display_options(generator: MazeGenerator,
                    color: Generator[Pallets.Pallet, None, None]) -> None:
    print("\n==A-Maze-In==")
    print("1. Re-generate a new maze")
    print("2. Show/Hide path from entry to exit")
    print("3. Rotate colors")
    print("4. Quit")
    try:
        answer: str = input("Choice? (1-4): ")
        if (answer in "1234"):
            match answer:
                case "1":
                    system(f"rm -rf {generator.configs.output_file}")
                    clearify()
                    display_interface(generator, color)
                case "2":
                    clearify()
                    if generator.show_path:
                        generator.show_path = False
                    else:
                        generator.show_path = True
                    generator.display_maze()
                    display_options(generator, color)
                case "3":
                    generator.configs.color = next(color)
                    clearify()
                    generator.display_maze()
                    display_options(generator, color)
                case "4":
                    exit(0)
        raise InputError("Choose a number 1-4!")
    except InputError as e:
        print(e)
        display_options(generator, color)


def choose_color() -> Generator[Pallets.Pallet, None, None]:
    colors: list[Pallets.Pallet] = [Pallets.VSCode(),
                                    Pallets.CandyStore(),
                                    Pallets.Quaquaval(),
                                    Pallets.SSalazzle(),
                                    Pallets.Brits(),
                                    Pallets.HomemDeFerro(),
                                    Pallets.Default()]
    while True:
        for color in colors:
            yield (color)


def display_interface(maze_generator: MazeGenerator, color:
                      Generator[Pallets.Pallet, None, None]) -> None:
    maze_generator.build_grid()
    start: Cell = maze_generator.grid[0][0]
    path: list[Cell] = []
    random.seed(maze_generator.configs.seed)
    maze_generator.make_maze(start, path)
    if (not maze_generator.configs.perfect):
        maze_generator.unperfectify()
    maze_generator.get_output_file()
    maze_generator.display_maze()
    print(maze_generator.grid[1][0].walls)
    print(maze_generator.grid[2][1].walls)
    print(maze_generator.grid[1][2].walls)
    display_options(maze_generator, color)


def main(file_name: str) -> None:
    """
    Runs the main program.
    """
    try:
        configs: Config = MazeGenerator.get_configs(file_name)
        generator = MazeGenerator(configs)
        colors = choose_color()
        display_interface(generator, colors)
    except Exception as err:
        print(f"{err}")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Error: missing configuration file")
