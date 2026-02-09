from dataclasses import dataclass
from typing import Dict


@dataclass
class Config:
    """Configuration options for maze generation.

    Attributes:
        width: Maze width in number of cells.
        height: Maze height in number of cells.
        entry: (x, y) coordinates of the entry cell.
        exit: (x, y) coordinates of the exit cell.
        output_file: Path to the output file that will be written.
        perfect: If True, generate a perfect maze (no loops); if False,
         allow loops.
    """

    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool


class ConfigError(Exception):
    """Raised when the configuration file is missing, invalid,
    or inconsistent."""

    pass


def load_config(path: str) -> Config:
    """Load and validate maze configuration from a text file.

    The file must contain one `KEY=VALUE` pair per line. Required keys are:
    WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT.

    Comments (lines starting with `#`, `'''`, or `//`)
    and blank lines are ignored.

    Args:
        path: Path to the config file.

    Returns:
        A populated `Config` instance with validated values.

    Raises:
        ConfigError: If the file cannot be read, has bad syntax
        , is missing keys,
        or contains invalid WIDTH/HEIGHT/ENTRY/EXIT/PERFECT values.
    """
    raw: Dict[str, str] = {}
    try:
        with open(path, "r") as f:
            for row in f:
                line = row.strip()
                if not line:
                    continue
                if line.startswith(("#", "'''", "//")):
                    continue
                try:
                    key, value = line.split("=", 1)
                except ValueError:
                    raise ConfigError("Bad syntax: expected KEY=VALUE")
                raw[key.strip()] = value.strip()
            required_keys = {
                "WIDTH",
                "HEIGHT",
                "ENTRY",
                "EXIT",
                "OUTPUT_FILE",
                "PERFECT",
            }
            missing = required_keys - raw.keys()
            if missing:
                missing_str = ", ".join(missing)
                raise ConfigError(f"Missing config: {missing_str}")
    except FileNotFoundError:
        raise ConfigError("File not found")
    except PermissionError:
        raise ConfigError("File Permission Error")
    except ConfigError:
        raise
    except OSError:
        raise ConfigError("Cannot read config file")
    try:
        width = int(raw["WIDTH"])
    except ValueError:
        raise ConfigError("WIDTH must be an integer")
    try:
        height = int(raw["HEIGHT"])
    except ValueError:
        raise ConfigError("HEIGHT must be an integer")
    if width <= 0 or height <= 0:
        raise ConfigError("WIDTH and HEIGHT must be positive")
    try:
        entry_x_str, entry_y_str = raw["ENTRY"].split(",", 1)
        entry_x_str = entry_x_str.strip()
        entry_y_str = entry_y_str.strip()
        exit_x_str, exit_y_str = raw["EXIT"].split(",", 1)
        exit_x_str = exit_x_str.strip()
        exit_y_str = exit_y_str.strip()
        entry = (int(entry_x_str), int(entry_y_str))
        exit_coord = (int(exit_x_str), int(exit_y_str))
    except ValueError:
        raise ConfigError('ENTRY/EXIT must be "x,y" with integers')
    ex, ey = entry
    if not (0 <= ex < width and 0 <= ey < height):
        raise ConfigError("ENTRY outside maze bounds")
    dx, dy = exit_coord
    if not (0 <= dx < width and 0 <= dy < height):
        raise ConfigError("EXIT outside maze bounds")
    if entry == exit_coord:
        raise ConfigError("ENTRY and EXIT must be different")
    perfect_str = raw["PERFECT"].strip().lower()
    if perfect_str == "true":
        perfect = True
    elif perfect_str == "false":
        perfect = False
    else:
        raise ConfigError("PERFECT must be True or False")
    output_file = raw["OUTPUT_FILE"].strip()
    return Config(
        width=width,
        height=height,
        entry=entry,
        exit=exit_coord,
        output_file=output_file,
        perfect=perfect,
    )
