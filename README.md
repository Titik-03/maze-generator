*This project has been created as part of the 42 curriculum by maqlil, mgamal.*

# A-Maze-ing

## Description

This project generates and solves mazes from a text configuration file.
Given a config with width, height, entry and exit, the program:

- builds a maze grid of cells with walls,
- embeds a 42 pattern in the center made of fully closed cells,
- generates a maze (perfect or non-perfect),
- finds the shortest path from entry to exit,
- writes the maze and solution to a text file.

The output file contains:

1. One line per maze row, each a string of hex digits describing cell walls.
2. A blank line.
3. Entry coordinates `x,y`.
4. Exit coordinates `x,y`.
5. Shortest path as a string of `N/E/S/W`.

## Instructions

### Run

From the project root:

```bash
make run
```
Debug with:

```bash
make debug
```

### Lint / Type-check:

```bash
make install
make lint
make lint-strict
```

### Clean:

```bash
make clean
```

### ASCII Visualizer (optional)

We also have a curses-based ASCII visualizer (extra feature) that can:

- show the maze generation in real time,
- toggle between DFS and Prim’s algorithms,
- show/hide the solution path.

You can run it separately (for example):

```bash
python3 ascii_main.py
```

### Config File

Example config.txt:
```txt
WIDTH=7
HEIGHT=7
ENTRY=0,0
EXIT=6,6
OUTPUT_FILE=maze.txt
PERFECT=True
```

Keys:
. WIDTH, HEIGHT: positive integers.
. ENTRY, EXIT: x,y inside the grid , ENTRY != EXIT.
. OUTPUT_FILE: path to output file.
. PERFECT: True or False.

Blank lines and lines starting with `#`, `'''` or `//` are ignored.

## Maze Generation Algorithm
The generator uses:

. **DFS(depth-first search)**:
	. Start from one cell.
	. Randomly visit unvisited neighbors, opening walls between cells.
	. Backtrack when stuck.
	. This produces a perfect maze in the area outside 42 cells.

. **Prim’s algorithm (randomized)**:

	. Start from one cell and mark it visited.
	. Maintain a list of “frontier” edges between visited and unvisited neighbors.
	. Repeatedly pick a random frontier edge, carve it, and add its neighbors to the frontier.
		Also produces a perfect maze, but with a different corridor style than DFS.

. `if PERFECT=False`:
	. After Dfs, a second phase opens a few extra walls between neighboring cells.
	. This adds cycles and makes the maze non-perfect.

**The "42" is fixed 7*5 pattern in the center**:

	. Certain cells are marked is_42_block.
	. DFS and extra openings skip those cells.
	. At the end, all walls on 42 cells and the matching walls on neighbors are forced closed.

## Solver Algorithm
The solver uses Breadth-First Search (BFS):

	. Treats each cell as a node.
	. Edges connect neighboring cells where the wall between them is open in both cells.
	. BFS starts at the entry, explores in waves until it reaches the exit.
	. A parent grid remembers how each cell was reached.
	. The path is reconstructed from exit back to entry using parent, then reversed.

	The direction string (N/E/S/W) is built by comparing each consecutive pair coordinates in the path.

## Reusable Code (mazegen_42)
The library lives in the mazegen package and is build as mazegen_42-1.0.0-py3-none-any.whl

```bash
install it with:
	pip install ./mazegen_42-1.0.0-py3-none-any.whl
```

```code
Use it like:
from mazegen import MazeGenerator, solve_shortest_path
generator = MazeGenerator(
	config.width, config.height, seed=22, perfect=config.perfect
)
maze = generator.generate(config.entry, config.exit)
validate_walls(maze)
path = solve_shortest_path(maze)
```

## Team And Project Management
. group project by **maqlil** and **mgamal**
. **maqlil** phases:
	. config parsing.
	. DFS generator.
	. BFS solver and output writer.
	. 42 pattern
. **mgamal** phases:
	. Renderer_ascii
	. Cli
	. Prim’s generator
. Tools:
	Python, flake8, mypy, build/setuptools/wheel, Makefile.

## Resources && AI Usage
. DFS maze generation (recursive backtracker):
	<https://weblog.jamisbuck.org/2011/2/7/maze-generation-recursive-backtracking>
. BFS shortest path:
	<https://en.wikipedia.org/wiki/Breadth-first_search>
. Python docs:
	<https://docs.python.org/3/>

we used an AI assistant to:

Help clarify algorithm choices and other algorithms concepts.
