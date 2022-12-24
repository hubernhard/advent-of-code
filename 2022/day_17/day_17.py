"""Day 17: Pyroclastic Flow"""

from dataclasses import dataclass
from itertools import cycle
from pathlib import Path
from typing import Iterator, NamedTuple

ROCK_SHAPES = """
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
"""


class GridPoint(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "GridPoint") -> "GridPoint":
        return GridPoint(self.x + other.x, self.y + other.y)


@dataclass
class Rock:
    points: set[GridPoint]

    @property
    def height(self) -> int:
        return max(point.y for point in self.points)

    @property
    def y(self) -> int:
        return min(point.y for point in self.points)

    @property
    def columns(self) -> dict[int, int]:
        x_vals = {p.x for p in self.points}
        return {x: max(p.y for p in self.points if p.x == x) for x in x_vals}

    @classmethod
    def from_shape(cls, shape: str) -> "Rock":
        points = set()
        rows = shape.strip().split("\n")
        for y, row in enumerate(reversed(rows)):
            for x, val in enumerate(row):
                if val == "#":
                    points.add(GridPoint(x, y))
        return cls(points=points)

    def __add__(self, other: GridPoint) -> "Rock":
        return Rock(points={point + other for point in self.points})

    def push(self, pattern: str) -> "Rock":
        return self + GridPoint(1 if pattern == ">" else -1, 0)


class State(NamedTuple):
    rock_idx: int
    pattern_idx: int
    height: int
    column_heights: tuple[int, ...]


class RockFall:
    width: int = 7

    def __init__(self, content: str):
        self._patterns = content.strip()
        self._rocks = self._initialize_rocks()

    def _initialize_rocks(self) -> list[Rock]:
        shapes = ROCK_SHAPES.strip().split("\n\n")
        return [Rock.from_shape(shape) for shape in shapes]

    def stack(self) -> Iterator[State]:
        pile = {GridPoint(x, 0) for x in range(self.width)}
        rocks = enumerate(cycle(self._rocks))
        patterns = enumerate(cycle(self._patterns))
        column_heights = tuple(0 for _ in range(self.width))
        height = 0

        while True:
            rock_idx, rock = next(rocks)
            rock += GridPoint(2, height + 4)

            pattern_counter = 0
            while True:
                # Push rock sideways
                pattern_idx, pattern = next(patterns)
                new_rock = rock.push(pattern)
                pattern_counter += 1
                if all(
                    0 <= p.x <= self.width - 1 for p in new_rock.points
                ) and (
                    new_rock.y > height or new_rock.points.isdisjoint(pile)
                ):
                    rock = new_rock
                # Move rock downward
                new_rock = rock + GridPoint(0, -1)
                if new_rock.y <= height and not new_rock.points.isdisjoint(
                    pile
                ):
                    break
                rock = new_rock

            # Update height
            height = max(rock.height, height)
            # Update heights of each column in pile
            column_heights = tuple(
                max(y, rock.columns.get(x, y))
                for x, y in enumerate(column_heights)
            )
            # Normalize column heights by subtracting the current height
            normalized_column_heights = tuple(
                y - height for y in column_heights
            )
            # Add rock to pile
            pile.update(rock.points)

            yield State(
                rock_idx=rock_idx,
                pattern_idx=pattern_idx,
                height=height,
                column_heights=normalized_column_heights,
            )

    def solve_part1(self) -> int:
        simulation = self.stack()
        for _ in range(2022):
            height = next(simulation).height
        return height

    def solve_part2(self) -> int:
        n_rocks = 1_000_000_000_000
        history = {}
        simulation = self.stack()

        while True:
            state = next(simulation)
            key = (
                state.rock_idx % len(self._rocks),
                state.pattern_idx % len(self._patterns),
                state.column_heights,
            )
            if key in history:
                old_state = history[key]
                # Number of rocks between current and old state
                step_size = state.rock_idx - old_state.rock_idx
                # Number of steps that can be skipped
                steps = (n_rocks - old_state.rock_idx) // step_size - 1
                # Number of missing steps to fully cover n_rocks
                missing = n_rocks % (steps * step_size) - state.rock_idx - 1
                for _ in range(missing):
                    height = next(simulation).height
                return height + steps * (state.height - old_state.height)
            else:
                history[key] = state


if __name__ == "__main__":
    test_puzzle = RockFall(">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>")
    assert test_puzzle.solve_part1() == 3068
    assert test_puzzle.solve_part2() == 1_514_285_714_288

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = RockFall(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2()}")
