from dataclasses import dataclass
import random
from typing import Optional
from collections.abc import Callable
from maze.model import Maze, create_empty_maze


Visualizer = Callable[[Maze], None]


@dataclass
class MazeGenerator:
    width: int
    height: int
    seed: Optional[int] = None
    perfect: bool = True

    def __post_init__(self) -> None:
        self.rng = random.Random(self.seed)

    def dfs(self, maze: Maze, visualizer: Visualizer | None = None) -> None:
        visited: list[list[bool]] = []
        for y in range(maze.height):
            row: list[bool] = []
            for x in range(maze.width):
                row.append(False)
            visited.append(row)
        start_x = 0
        start_y = 0
        visited[start_y][start_x] = True
        stack = [(start_x, start_y)]
        while stack:
            x, y = stack[-1]
            neighbors = self.unvisited_neighbors(maze, x, y, visited)
            if not neighbors:
                stack.pop()
                continue
            else:
                nx, ny = self.rng.choice(neighbors)
                self.open_wall_between(maze, x, y, nx, ny)
                visited[ny][nx] = True
                stack.append((nx, ny))
            if visualizer:
                visualizer(maze)

    def _get_neighbors(
        self, x: int, y: int, maze: Maze
    ) -> list[tuple[int, int]]:
        neighbors = []
        if x - 1 >= 0 and not maze.cells[y][x - 1].is_42_block:
            neighbors.append((x - 1, y))
        if x + 1 < self.width and not maze.cells[y][x + 1].is_42_block:
            neighbors.append((x + 1, y))
        if y - 1 >= 0 and not maze.cells[y - 1][x].is_42_block:
            neighbors.append((x, y - 1))
        if y + 1 < self.height and not maze.cells[y + 1][x].is_42_block:
            neighbors.append((x, y + 1))
        return neighbors

    def prims(self, maze: Maze, visualizer: Visualizer | None = None) -> None:
        visited = []
        for y in range(maze.height):
            row = []
            for x in range(maze.width):
                row.append(False)
            visited.append(row)
        start_x = 0
        start_y = 0
        visited[start_y][start_x] = True
        frontier = []
        for nx, ny in self._get_neighbors(start_x, start_y, maze):
            if not visited[ny][nx]:
                frontier.append((start_x, start_y, nx, ny))
        while frontier:
            wall_index = self.rng.randint(0, len(frontier) - 1)
            x, y, nx, ny = frontier[wall_index]
            frontier.pop(wall_index)

            if not visited[ny][nx]:
                self.open_wall_between(maze, x, y, nx, ny)
                visited[ny][nx] = True

                for nnx, nny in self._get_neighbors(nx, ny, maze):
                    if not visited[nny][nnx]:
                        frontier.append((nx, ny, nnx, nny))
                if visualizer:
                    visualizer(maze)

    def generate(
        self,
        entry: tuple[int, int],
        exit_: tuple[int, int],
        is_dfs: bool,
        visualizer: Visualizer | None = None,
    ) -> Maze:
        maze = create_empty_maze(self.width, self.height, entry, exit_)
        should_i = True
        pattern_width = 7
        pattern_height = 5
        if self.width < pattern_width or self.height < pattern_height:
            should_i = False
        start_x_42 = (self.width - pattern_width) // 2
        start_y_42 = (self.height - pattern_height) // 2
        if should_i:
            coords_4 = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (2, 4)]
            for col, row in coords_4:
                x = start_x_42 + col
                y = start_y_42 + row
                maze.cells[y][x].is_42_block = True
            coords_2 = [
                (0, 0),
                (1, 0),
                (2, 0),
                (2, 1),
                (0, 2),
                (1, 2),
                (2, 2),
                (0, 3),
                (0, 4),
                (1, 4),
                (2, 4),
            ]
            for col, row in coords_2:
                x = start_x_42 + 4 + col
                y = start_y_42 + row
                maze.cells[y][x].is_42_block = True
        if is_dfs:
            self.dfs(maze, visualizer)
        else:
            self.prims(maze, visualizer)
        if not self.perfect:
            for _ in range(6):
                x = self.rng.choice(range(self.width))
                y = self.rng.choice(range(self.height))
                random_dir = self.rng.choice(["N", "E", "S", "W"])
                if random_dir == "N":
                    nx, ny = x, y - 1
                elif random_dir == "E":
                    nx, ny = x + 1, y
                elif random_dir == "S":
                    nx, ny = x, y + 1
                elif random_dir == "W":
                    nx, ny = x - 1, y
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if random_dir == "N":
                        cell = maze.cells[y][x]
                        neighbor = maze.cells[ny][nx]
                        if (
                            neighbor.south
                            and cell.north
                            and not cell.is_42_block
                            and not neighbor.is_42_block
                        ):
                            self.open_wall_between(maze, x, y, nx, ny)
                        else:
                            continue
                    elif random_dir == "E":
                        cell = maze.cells[y][x]
                        neighbor = maze.cells[ny][nx]
                        if (
                            neighbor.west
                            and cell.east
                            and not cell.is_42_block
                            and not neighbor.is_42_block
                        ):
                            self.open_wall_between(maze, x, y, nx, ny)
                        else:
                            continue
                    elif random_dir == "S":
                        cell = maze.cells[y][x]
                        neighbor = maze.cells[ny][nx]
                        if (
                            neighbor.north
                            and cell.south
                            and not cell.is_42_block
                            and not neighbor.is_42_block
                        ):
                            self.open_wall_between(maze, x, y, nx, ny)
                        else:
                            continue
                    elif random_dir == "W":
                        cell = maze.cells[y][x]
                        neighbor = maze.cells[ny][nx]
                        if (
                            neighbor.east
                            and cell.west
                            and not cell.is_42_block
                            and not neighbor.is_42_block
                        ):
                            self.open_wall_between(maze, x, y, nx, ny)
                        else:
                            continue
        if should_i:
            for y in range(self.height):
                for x in range(self.width):
                    c = maze.cells[y][x]
                    if c.is_42_block:
                        c.north = True
                        c.east = True
                        c.south = True
                        c.west = True
                        if x - 1 >= 0:
                            maze.cells[y][x - 1].east = True
                        if x + 1 < self.width:
                            maze.cells[y][x + 1].west = True
                        if y - 1 >= 0:
                            maze.cells[y - 1][x].south = True
                        if y + 1 < self.height:
                            maze.cells[y + 1][x].north = True
        return maze

    def unvisited_neighbors(
        self,
        maze: Maze,
        x: int,
        y: int,
        visited: list[list[bool]],
    ) -> list[tuple[int, int]]:
        neighbors: list[tuple[int, int]] = []
        if (
            x - 1 >= 0
            and not visited[y][x - 1]
            and not maze.cells[y][x - 1].is_42_block
        ):
            neighbors.append((x - 1, y))
        if (
            x + 1 < self.width
            and not visited[y][x + 1]
            and not maze.cells[y][x + 1].is_42_block
        ):
            neighbors.append((x + 1, y))
        if (
            y - 1 >= 0
            and not visited[y - 1][x]
            and not maze.cells[y - 1][x].is_42_block
        ):
            neighbors.append((x, y - 1))
        if (
            y + 1 < self.height
            and not visited[y + 1][x]
            and not maze.cells[y + 1][x].is_42_block
        ):
            neighbors.append((x, y + 1))
        return neighbors

    def open_wall_between(
        self, maze: Maze, x1: int, y1: int, x2: int, y2: int
    ) -> None:
        if x2 == x1 + 1 and y2 == y1:
            maze.cells[y1][x1].east = False
            maze.cells[y2][x2].west = False
        elif x2 == x1 - 1 and y2 == y1:
            maze.cells[y1][x1].west = False
            maze.cells[y2][x2].east = False
        elif x2 == x1 and y2 == y1 + 1:
            maze.cells[y1][x1].south = False
            maze.cells[y2][x2].north = False
        elif x2 == x1 and y2 == y1 - 1:
            maze.cells[y1][x1].north = False
            maze.cells[y2][x2].south = False
