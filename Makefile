.PHONY: run install build clean fclean remove venv

VENV=venv
PY=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

RESET=\033[0m
INFO=\033[0;34m[STEP]$(RESET)
SUCCESS=\033[0;32m[SUCCESS]$(RESET)
CLEAN=\033[0;33m[CLEAN]$(RESET)
REMOVE=\033[0;31m[REMOVE]$(RESET)

venv:
	@echo -e "$(INFO) Creating virtual environment..."
	@python3 -m venv $(VENV)
	@echo -e "$(SUCCESS) venv ready"

install: venv
	@echo -e "$(INFO) Installing dependencies..."
	@$(PIP) install -r requirements.txt
	@$(PIP) install pyinstaller
	@echo -e "$(SUCCESS) dependencies installed"

run: install
	@echo -e "$(INFO) Running To-Do Planner..."
	@$(PY) src/main.py

build: install
	@echo -e "$(INFO) Building executable..."
	@rm -rf build dist *.spec
	@$(PY) -m PyInstaller --onefile --name to-do-planner src/main.py
	@echo -e "$(SUCCESS) build complete"

clean:
	@echo -e "$(CLEAN) Cleaning project..."
	@rm -rf build dist src/__pycache__ *.spec
	@echo -e "$(SUCCESS) clean complete"

fclean: clean
	@echo -e "$(REMOVE) Removing venv..."
	@rm -rf venv
	@echo -e "$(SUCCESS) venv removed complete"

remove:
	@echo -e "$(REMOVE) Removing local data..."
	@rm -rf data
	@echo -e "$(SUCCESS) data removed"
