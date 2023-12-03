"""Day 3: Gear Ratios"""

import re
from itertools import product
from math import prod
from pathlib import Path
from typing import NamedTuple, Self

test_content = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


class Point(NamedTuple):
    x: int
    y: int

    def neighbors(self) -> set[Self]:
        x, y = self
        neighbors = {
            Point(x + dx, y + dy) for dx, dy in product((-1, 0, 1), repeat=2)
        }
        return neighbors


class Puzzle:
    def __init__(self, content: str):
        self.content = content.strip().split("\n")
        self.symbols = {}
        for y, line in enumerate(self.content):
            symbols = list(re.finditer(r"[^\d\.]", line))
            for symbol in symbols:
                x = symbol.start()
                self.symbols[Point(x, y)] = symbol.group()

    def solve_part1(self) -> int:
        total = 0
        for y, line in enumerate(self.content):
            numbers = list(re.finditer(r"\d+", line))
            for number in numbers:
                xs = range(*number.span())
                neighbors = set.union(*(Point(x, y).neighbors() for x in xs))
                if not neighbors.isdisjoint(self.symbols):
                    value = int(number.group())
                    total += value
        return total

    def solve_part2(self) -> int:
        stars = {p: [] for p, value in self.symbols.items() if value == "*"}

        for y, line in enumerate(self.content):
            numbers = list(re.finditer(r"\d+", line))
            for number in numbers:
                xs = range(*number.span())
                neighbors = set.union(*(Point(x, y).neighbors() for x in xs))
                neighbors.intersection_update(stars)
                for neighbor in neighbors:
                    value = int(number.group())
                    stars[neighbor].append(value)

        total = 0
        for values in stars.values():
            if len(values) == 2:
                total += prod(values)

        return total


if __name__ == "__main__":
    test_puzzle = Puzzle(test_content)
    assert test_puzzle.solve_part1() == 4361
    assert test_puzzle.solve_part2() == 467835

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = Puzzle(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2()}")
