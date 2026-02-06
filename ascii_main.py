from maze.generator import MazeGenerator
from maze.renderer_ascii import draw_maze, draw_path, setup_colors
import random
import time
from maze.config import load_config
from maze.solver import solve_shortest_path
from typing import Any
config = load_config("config.txt")


def ascii_main(stdscr: Any) -> None:
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
            draw_maze(stdscr, m)
            if animation:
                time.sleep(0.03)
        maze = generator.generate(
            e, exit_pos, is_dfs, visualizer=animation_step
        )
        return maze

    current = gen(seed_maze)
    while True:
        c = stdscr.getch()
        if c == ord('g'):
            animation = False
            seed_maze = random.randint(0, 500000)
            current = gen(seed_maze)
        if c == ord('p'):
            path = solve_shortest_path(current)
            for px, py in path:
                current.cells[py][px].on_solution_path = True
            draw_path(stdscr, current)
            stdscr.refresh()
        if c == ord('c'):
            setup_colors()
            draw_maze(stdscr, current)
            draw_path(stdscr, current)
        if c == ord('a'):
            is_dfs = not is_dfs
            current = gen(seed_maze)
        if c == ord('m'):
            animation = True
            current = gen(seed_maze)
        if c == ord('l'):
            path = solve_shortest_path(current)
            for px, py in path:
                current.cells[py][px].on_solution_path = True
                draw_path(stdscr, current)
                stdscr.refresh()
                time.sleep(0.05)
        if c == ord('h'):
            for row in current.cells:
                for cell in row:
                    cell.on_solution_path = False
            draw_maze(stdscr, current)
        if c == ord('s'):
            with open("maze_seeds", 'a') as f:
                f.write(f"{seed_maze}\n")
        if c == ord('q'):
            break
