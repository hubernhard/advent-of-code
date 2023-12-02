"""Day 2: Cube Conundrum"""

import re
from math import prod
from pathlib import Path
from typing import NamedTuple, Self

test_content = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""


class Set(NamedTuple):
    red: int
    green: int
    blue: int

    def __le__(self, other: Self) -> bool:
        return all(
            [
                self.red <= other.red,
                self.green <= other.green,
                self.blue <= other.blue,
            ]
        )

    @classmethod
    def from_text(cls, text: str) -> Self:
        def _find(color: str) -> int:
            r = re.findall(f"(\\d+) {color}", text)
            return int(r[0]) if r else 0

        return cls(*(_find(color) for color in ("red", "green", "blue")))


class Puzzle:
    def __init__(self, content: str):
        self.games = {}
        for game in content.strip().split("\n"):
            name, sets = game.split(":")
            i = int(name.replace("Game", ""))
            self.games[i] = [Set.from_text(x) for x in sets.split(";")]

    def solve_part1(self) -> int:
        bag = Set(red=12, green=13, blue=14)
        total = 0
        for i, sets in self.games.items():
            if all(set_ <= bag for set_ in sets):
                total += i
        return total

    def solve_part2(self) -> int:
        total = 0
        for sets in self.games.values():
            total += prod(
                [
                    max(set_.red for set_ in sets),
                    max(set_.green for set_ in sets),
                    max(set_.blue for set_ in sets),
                ]
            )
        return total


if __name__ == "__main__":
    test_puzzle = Puzzle(test_content)
    assert test_puzzle.solve_part1() == 8
    assert test_puzzle.solve_part2() == 2286

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = Puzzle(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2()}")
