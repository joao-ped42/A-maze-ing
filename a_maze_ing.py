import sys
from maze_generator import Config


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
        raise KeyError(f"Error: {err}!")


def main(file_name: str) -> None:
    try:
        configs: Config = get_configs(file_name)
        print(configs.width)
        print(configs.height)
        print(configs.entry)
        print(configs.exit)
        print(configs.output_file)
        print(configs.perfect)
    except Exception as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Error: missing configuration file")
