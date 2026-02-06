from collections import deque
from typing import Optional
from .model import MazeError, Maze


def solve_shortest_path(
    maze: Maze,
) -> list[tuple[int, int]]:
    visited: list[list[bool]] = []
    for y in range(maze.height):
        row: list[bool] = []
        for x in range(maze.width):
            row.append(False)
        visited.append(row)
    parent: list[list[Optional[tuple[int, int]]]] = []
    for y in range(maze.height):
        cell: list[Optional[tuple[int, int]]] = []
        for x in range(maze.width):
            cell.append(None)
        parent.append(cell)
    queue: deque[tuple[int, int]] = deque()
    start_x, start_y = maze.entry
    goal_x, goal_y = maze.exit
    visited[start_y][start_x] = True
    queue.append((start_x, start_y))
    while queue:
        x, y = queue.popleft()
        if (x, y) == (goal_x, goal_y):
            break
        neighbors = []
        if (
            x - 1 >= 0
            and not visited[y][x - 1]
            and not maze.cells[y][x - 1].east
            and not maze.cells[y][x].west
        ):
            neighbors.append((x - 1, y))
        if (
            x + 1 < maze.width
            and not visited[y][x + 1]
            and not maze.cells[y][x + 1].west
            and not maze.cells[y][x].east
        ):
            neighbors.append((x + 1, y))
        if (
            y - 1 >= 0
            and not visited[y - 1][x]
            and not maze.cells[y - 1][x].south
            and not maze.cells[y][x].north
        ):
            neighbors.append((x, y - 1))
        if (
            y + 1 < maze.height
            and not visited[y + 1][x]
            and not maze.cells[y + 1][x].north
            and not maze.cells[y][x].south
        ):
            neighbors.append((x, y + 1))
        for neighbor in neighbors:
            nx, ny = neighbor
            visited[ny][nx] = True
            parent[ny][nx] = (x, y)
            queue.append((nx, ny))
    if not visited[goal_y][goal_x]:
        raise MazeError("no solution")
    path = []
    current: tuple[int, int] | None = (goal_x, goal_y)
    while current is not None and current != (start_x, start_y):
        path.append(current)
        cx, cy = current
        preview_cell = parent[cy][cx]
        current = preview_cell
    path.append((start_x, start_y))
    path.reverse()
    return path
