import sys
# from typing import Any


def get_configs(file_name: str) -> dict[str, str]:

    config_dict: dict[str, str] = {}

    try:
        with open(file_name, "r") as file:
            for line in file:
                key = line.split("=")[0]
                value = line.strip().split("=")[1]
                config_dict.update({key: value})

    except FileNotFoundError:
        raise FileNotFoundError("Error: Invalid file!")

    except KeyError:
        raise KeyError(f"Error: Invalid configurations in {file_name}!")

    return config_dict


def main(file_name: str) -> None:
    try:
        config_dict: dict[str, str] = get_configs(file_name)
        print(config_dict)
    except Exception as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Error: missing configuration file")
