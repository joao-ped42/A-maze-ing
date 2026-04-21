import sys
from maze_generator import Config, MazeGenerator


# class Ideias:
    # generator.display_cells2()
    # for _ in range(generator.configs.width):
    #     Cell.put_horizontal()
    # print()
    # for _ in range(generator.configs.height):
    #     for _ in range(generator.configs.width):
    #         Cell.put_vertical()
    #     print()
    #     for _ in range(generator.configs.width):
    #         Cell.put_horizontal()
    #     print()
    # Cell.put_horizontal()


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


def main(file_name: str) -> None:
    """
    Runs the main program.
    """
    try:
        configs: Config = get_configs(file_name)
        generator = MazeGenerator(configs)
        # display_config(generator.configs)
        # print("============================================\n")
        generator.build_grid()
        generator.display_maze()
        generator.get_output_file()
    except Exception as err:
        print(f"{err}")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Error: missing configuration file")
