from maze.generator import MazeGenerator
from maze.renderer_ascii import draw_maze, draw_path, setup_colors
import random
import time
import sys
from maze.config import load_config
from maze.solver import solve_shortest_path
from typing import Any


def ascii_main(stdscr: Any) -> None:
    """Curses-based ASCII visualizer for the maze generator.

    Uses the current config (size, entry/exit, PERFECT) to generate mazes with
    DFS or Prim's and display them in the terminal. Supports key bindings to:

    - 'g': generate a new maze (no path shown)
    - 'm': animate maze generation
    - 'p': draw the shortest path once
    - 'l': animate drawing of the shortest path
    - 'c': re-generate colors and redraw maze + path
    - 'a': switch between DFS and Prim's algorithms
    - 'h': hide/clear the path rendering
    - 's': append the current seed to a "maze_seeds" file
    - 'q': quit

    Args:
        stdscr: The curses screen/window passed by curses.wrapper.
    """
    config_path = sys.argv[1]
    config = load_config(config_path)
    setup_colors()
    stdscr.clear()
    seed_maze = random.randint(0, 500000)
    is_dfs = True
    animation = False
    h = config.height
    w = config.width
    e = config.entry
    exit_pos = config.exit
    perfect = config.perfect

    def gen(seed: int) -> Any:
        generator = MazeGenerator(h, w, seed, perfect)

        def animation_step(m: Any) -> None:
            if animation:
                draw_maze(stdscr, m)
                time.sleep(0.003)

        maze = generator.generate(
            e, exit_pos, is_dfs, visualizer=animation_step
        )
        draw_maze(stdscr, maze)
        return maze

    current = gen(seed_maze)
    while True:
        c = stdscr.getch()
        if c == ord("g"):
            animation = False
            seed_maze = random.randint(0, 500000)
            current = gen(seed_maze)
        if c == ord("p"):
            path = solve_shortest_path(current)
            for px, py in path:
                current.cells[py][px].on_solution_path = True
            draw_path(stdscr, current)
            stdscr.refresh()
        if c == ord("c"):
            setup_colors()
            draw_maze(stdscr, current)
            draw_path(stdscr, current)
        if c == ord("a"):
            is_dfs = not is_dfs
            current = gen(seed_maze)
        if c == ord("m"):
            animation = True
            current = gen(seed_maze)
        if c == ord("l"):
            path = solve_shortest_path(current)
            for px, py in path:
                current.cells[py][px].on_solution_path = True
                draw_path(stdscr, current)
                stdscr.refresh()
                time.sleep(0.05)
        if c == ord("h"):
            for row in current.cells:
                for cell in row:
                    cell.on_solution_path = False
            draw_maze(stdscr, current)
        if c == ord("s"):
            with open("maze_seeds", "a") as f:
                f.write(f"{seed_maze}\n")
        if c == ord("q"):
            break
