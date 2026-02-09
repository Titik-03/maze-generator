from dataclasses import dataclass


@dataclass
class Cell:
    """One cell of the maze grid, with walls and flags.

    Attributes:
        north: True if the north wall is closed.
        east: True if the east wall is closed.
        south: True if the south wall is closed.
        west: True if the west wall is closed.
        on_solution_path: True if this cell is part of the solution path.
        is_entry: True if this cell is the maze entry.
        is_exit: True if this cell is the maze exit.
        is_42_block: True if this cell is part of the solid 42 pattern.
    """

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
    """Maze structure containing the grid and entry/exit coordinates.

    Attributes:
        width: Maze width in number of cells.
        height: Maze height in number of cells.
        cells: 2D list of Cell instances, indexed as cells[y][x].
        entry: (x, y) coordinates of the entry cell.
        exit: (x, y) coordinates of the exit cell.
    """

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
    """Create a new maze with all walls closed and entry/exit marked.

    Args:
        width: Maze width in number of cells.
        height: Maze height in number of cells.
        entry: (x, y) coordinates of the entry cell.
        exit_: (x, y) coordinates of the exit cell.

    Returns:
        A Maze instance where every Cell has all four walls closed, and
        entry/exit flags set on the corresponding cells.
    """
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
    """Raised when the maze structure is inconsistent
    (e.g., mismatched walls)."""

    pass


def validate_walls(maze: Maze) -> None:
    """Validate that neighboring cells have consistent shared walls.

    Checks that:
    - For each pair of horizontal neighbors, cell.east == right.west.
    - For each pair of vertical neighbors, cell.south == down.north.

    Args:
        maze: The maze to validate.

    Raises:
        MazeError: If any pair of neighboring cells has mismatched walls.
    """
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
