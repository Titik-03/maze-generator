# main entry point
from maze.config import load_config, ConfigError
from maze.generator import MazeGenerator
from maze.model import validate_walls, Cell
from maze.solver import solve_shortest_path
from ascii_main import ascii_main
import curses
import sys


def cell_to_hex(cell: Cell) -> str:
    value = 0
    if cell.north:
        value |= 1
    if cell.east:
        value |= 2
    if cell.south:
        value |= 4
    if cell.west:
        value |= 8
    digits = "0123456789ABCDEF"
    return digits[value]


def path_to_directions(path: list[tuple[int, int]]) -> str:
    directions = ""
    for i in range(0, len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        if x2 == x1 + 1 and y2 == y1:
            directions += "E"
        elif x2 == x1 - 1 and y2 == y1:
            directions += "W"
        elif x2 == x1 and y2 == y1 + 1:
            directions += "S"
        elif x2 == x1 and y2 == y1 - 1:
            directions += "N"
    return directions


def main() -> None:
    """Entry point for the A-Maze-ing project (placeholder)."""
    if len(sys.argv) != 2:
        print("Error")
        return
    config_path = sys.argv[1]
    try:
        config = load_config(config_path)
    except ConfigError as e:
        print(f"Error: {e}")
        return
    print(f"loaded config: {config}")
    generator = MazeGenerator(
        config.width, config.height, seed=22, perfect=config.perfect
    )
    is_dfs = True
    maze = generator.generate(config.entry, config.exit, is_dfs)
    validate_walls(maze)
    path = solve_shortest_path(maze)
    with open(config.output_file, "w", encoding="utf-8") as f:
        for y in range(config.height):
            row_str = ""
            for x in range(config.width):
                cell = maze.cells[y][x]
                row_str += cell_to_hex(cell)
            f.write(row_str + "\n")
        f.write("\n")
        ex, ey = config.entry
        gx, gy = config.exit
        f.write(f"{ex},{ey}\n")
        f.write(f"{gx},{gy}\n")
        f.write(path_to_directions(path))
        f.write("\n")


if __name__ == "__main__":
    main()
    curses.wrapper(ascii_main)
