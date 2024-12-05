# Advent of Code

My solutions to the [Advent of Code](https://adventofcode.com/) puzzles.

## Setup

Make sure [uv](https://docs.astral.sh/uv/) is installed on your system, clone
the repository and run:

```shell
uv sync --frozen
pre-commit install --install-hooks
```

## Initialize a new day using the template

```shell
uv run python -m aoc <YEAR> <DAY>
```
