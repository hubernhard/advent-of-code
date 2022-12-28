.PHONY: lint
lint:
	poetry run flake8 --max-line-length 79 --ignore E203 .
	poetry run isort --check-only --df .
	poetry run black --check --diff .

.PHONY: reformat
reformat:
	poetry run isort .
	poetry run black .
