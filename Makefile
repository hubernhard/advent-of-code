# Make sure that correct Python version is used on Windows
ifeq ($(OS),Windows_NT)
	POETRY_CMD = py -3.11 -m poetry
else
	POETRY_CMD = poetry
endif

.PHONY: lint
lint:
	$(POETRY_CMD) run flake8 --max-line-length 79 --ignore E203 .
	$(POETRY_CMD) run isort --check-only --df .
	$(POETRY_CMD) run black --check --diff .

.PHONY: reformat
reformat:
	$(POETRY_CMD) run isort .
	$(POETRY_CMD) run black .
