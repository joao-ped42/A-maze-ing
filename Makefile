NAME = a_maze_ing.py
CONFIG = config.txt
REQUIREMENTS = "requirements.txt"
MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
VENV_NAME = venv
PYTHON = $(VENV_NAME)/bin/python
PIP = $(VENV_NAME)/bin/pip

venv_create:
	test -d $(VENV_NAME) || python3 -m venv $(VENV_NAME)

install: venv_create
	$(PIP) install -r $(REQUIREMENTS)

run:
	$(PYTHON) $(NAME) $(CONFIG)


debug:
	$(PYTHON) -m pdb $(NAME) $(CONFIG)


clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

lint:
	-$(PYTHON) -m flake8 --exclude $(VENV_NAME)
	-$(PYTHON) -m mypy . $(MYPY_FLAGS)

lint-strict:
	-$(PYTHON) -m flake8 . --exclude $(VENV_NAME)
	-$(PYTHON) -m mypy . --strict

.PHONY: install run clean lint lint-strict