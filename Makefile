CONFIG ?= config.txt
PYTHON ?= python3

install:
	$(PYTHON) -m pip install -r requirements.txt
run:
	$(PYTHON) a_maze_ing.py $(CONFIG)
build:
	$(PYTHON) -m build
	cp dist/mazegen_42-1.0.0-py3-none-any.whl .
debug:
	$(PYTHON) -m pdb a_maze_ing.py $(CONFIG)
clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache build dist *.egg-info
	find . -name '__pycache__' -type d -exec rm -rf {} +
lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
lint-strict:
	flake8 .
	mypy . --strict
