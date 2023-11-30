sources = .

.PHONY: lint
lint:
	ruff format --check $(sources)
	ruff check --show-source $(sources)

.PHONY: reformat
reformat:
	ruff format $(sources)
	ruff check --fix --show-fixes $(sources)
