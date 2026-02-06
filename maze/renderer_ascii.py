import curses
import random
from typing import Any


def setup_colors() -> None:
    curses.start_color()
    curses.use_default_colors()
    if curses.COLORS == 256:
        color = random.sample([i for i in range(255)], 7)
    else:
        color = random.sample([i for i in range(7)], 7)
    curses.init_pair(1, color[0], color[1])
    curses.init_pair(2, color[0], color[2])
    curses.init_pair(3, color[0], color[3])
    curses.init_pair(4, color[4], color[0])
    curses.init_pair(5, color[5], color[0])
    curses.init_pair(6, color[0], -1)
    curses.init_pair(7, color[5], color[0])
    curses.init_pair(8, color[4], color[0])
    curses.init_pair(9, color[4], color[1])
    curses.init_pair(10, color[5], color[1])
    curses.init_pair(11, color[4], color[2])
    curses.init_pair(12, color[5], color[2])


def draw_cell(
    stdscr: Any,
    cell: Any,
    x: int,
    y: int,
    should_i: bool,
    cell_below_on_path: bool = False
) -> None:
    sy = y * 2 + 1
    sx = x * 4 + 1
    wall = 1
    path = 2
    patern = 3
    if should_i:
        c = wall
    else:
        c = path
    if x == 0:
        stdscr.addstr(sy, sx - 1, "█", curses.color_pair(c))
        stdscr.addstr(sy + 1, sx - 1, "█", curses.color_pair(c))
    if y == 0:
        if cell.east:
            stdscr.addstr(sy - 1, sx, "▄▄▄▄", curses.color_pair(6))
        else:
            stdscr.addstr(sy - 1, sx, "▄▄▄▄", curses.color_pair(6))
    if x == 0 and y == 0:
        stdscr.addstr(sy - 1, sx - 1, "▄", curses.color_pair(6))
    stdscr.addstr(sy, sx, "   ", curses.color_pair(c))
    if cell.east:
        stdscr.addstr(sy, sx + 3, "█", curses.color_pair(c))
    else:
        stdscr.addstr(sy, sx + 3, " ", curses.color_pair(c))
    if cell.south:
        stdscr.addstr(sy + 1, sx, "▄▄▄", curses.color_pair(c))
    else:
        stdscr.addstr(sy + 1, sx, "   ", curses.color_pair(c))
    if cell.east:
        stdscr.addstr("█", curses.color_pair(c))
    else:
        stdscr.addstr("▄", curses.color_pair(c))
    if cell.is_entry:
        stdscr.addstr(sy,     sx, "███", curses.color_pair(4))
        if cell.south:
            stdscr.addstr(sy + 1,     sx, "▀▀▀", curses.color_pair(8))
        elif cell_below_on_path:
            stdscr.addstr(sy + 1,     sx, "▀▀▀", curses.color_pair(11))
        else:
            stdscr.addstr(sy + 1,     sx, "▀▀▀", curses.color_pair(9))
    if cell.is_exit:
        stdscr.addstr(sy,     sx, "███", curses.color_pair(5))
        if cell.south:
            stdscr.addstr(sy + 1,     sx, "▀▀▀", curses.color_pair(7))
        elif cell_below_on_path:
            stdscr.addstr(sy + 1,     sx, "▀▀▀", curses.color_pair(12))
        else:
            stdscr.addstr(sy + 1,     sx, "▀▀▀", curses.color_pair(10))
    if should_i:
        if cell.is_42_block:
            stdscr.addstr(sy,     sx, "   ", curses.color_pair(patern))
            stdscr.addstr(sy,     sx + 3, "█", curses.color_pair(patern))
            stdscr.addstr(sy + 1, sx, "▄▄▄█", curses.color_pair(patern))


def draw_maze(stdscr: Any, maze: Any) -> None:
    curses.curs_set(0)
    for y in range(maze.height):
        for x in range(maze.width):

            cell = maze.cells[y][x]
            draw_cell(stdscr, cell, x, y, True)
    x = 0
    stdscr.addstr(y * 2 + 5, x, "\n")
    if maze.width < 7 + 1 or maze.height < 5 + 1:
        stdscr.addstr("width or height is too SMALL for 42 pattern\n")
    stdscr.addstr("Choose your option: \n\n", curses.color_pair(6))
    stdscr.addstr("¤ - Generate new maze ----------------(g)\n")
    stdscr.addstr("¤ - Animate maze generation ----------(m)\n")
    stdscr.addstr("¤ - Draw path BFS --------------------(p)\n")
    stdscr.addstr("¤ - Animate path generation ----------(l)\n")
    stdscr.addstr("¤ - Re-generate colors ---------------(c)\n")
    stdscr.addstr("¤ - Hide path ------------------------(h)\n")
    stdscr.addstr("¤ - Switch algorithm -----------------(a)\n")
    stdscr.addstr("¤ - Save maze seed -------------------(s)\n")
    stdscr.addstr("¤ - Quit -----------------------------(q)\n")
    stdscr.refresh()


def draw_path(stdscr: Any, maze: Any) -> None:
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.cells[y][x]
            if cell.on_solution_path:
                cell_below_on_path = (
                    y + 1 < maze.height and
                    maze.cells[y + 1][x].on_solution_path
                )
                draw_cell(stdscr, cell, x, y, False, cell_below_on_path)

    stdscr.refresh()
