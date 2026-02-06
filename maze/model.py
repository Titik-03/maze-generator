from dataclasses import dataclass


@dataclass
class Cell:
    north: bool = True
    east: bool = True
    south: bool = True
    west: bool = True
    on_solution_path: bool = False
    is_entry: bool = False
    is_exit: bool = False
    is_42_block: bool = False


@dataclass
class Maze:
    width: int
    height: int
    cells: list[list[Cell]]
    entry: tuple[int, int]
    exit: tuple[int, int]


def create_empty_maze(
    width: int,
    height: int,
    entry: tuple[int, int],
    exit_: tuple[int, int],
) -> Maze:
    cells: list[list[Cell]] = []
    for y in range(height):
        row: list[Cell] = []
        for x in range(width):
            row.append(Cell())
        cells.append(row)
    ex, ey = entry
    dx, dy = exit_
    cells[ey][ex].is_entry = True
    cells[dy][dx].is_exit = True
    return Maze(
        width=width,
        height=height,
        cells=cells,
        entry=entry,
        exit=exit_,
    )


class MazeError(Exception):
    pass


def validate_walls(maze: Maze) -> None:
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.cells[y][x]
            if x + 1 < maze.width:
                right = maze.cells[y][x + 1]
                if cell.east != right.west:
                    raise MazeError(
                        f"Inconsistent east/west walls at ({x}, {y})"
                    )
            if y + 1 < maze.height:
                down = maze.cells[y + 1][x]
                if cell.south != down.north:
                    raise MazeError(
                        f"Inconsistent south/north walls at ({x}, {y})"
                    )
