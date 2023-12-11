"""Day 11: Cosmic Expansion"""

from pathlib import Path
from typing import NamedTuple

test_content = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""


class Point(NamedTuple):
    x: int
    y: int


class Puzzle:
    def __init__(self, content: str):
        self.content = content.strip().split("\n")

    def init_galaxies(self, expansion: int = 2) -> list[Point]:
        empty_columns = [
            all(line[i] == "." for line in self.content)
            for i in range(len(self.content[0]))
        ]
        galaxies = []
        x, y = 0, 0

        for line in self.content:
            x = 0
            y += expansion if set(line) == {"."} else 1
            for i, element in enumerate(line):
                x += expansion if empty_columns[i] else 1
                if element == "#":
                    galaxies.append(Point(x, y))

        return galaxies

    @staticmethod
    def compute_total_dists(galaxies: list[Point]) -> int:
        total = 0
        for i, galaxy1 in enumerate(galaxies):
            for galaxy2 in galaxies[i + 1 :]:
                dist = abs(galaxy1.x - galaxy2.x) + abs(galaxy1.y - galaxy2.y)
                total += dist
        return total

    def solve_part1(self) -> int:
        galaxies = self.init_galaxies()
        return self.compute_total_dists(galaxies)

    def solve_part2(self, expansion: int) -> int:
        galaxies = self.init_galaxies(expansion=expansion)
        return self.compute_total_dists(galaxies)


if __name__ == "__main__":
    test_puzzle = Puzzle(test_content)
    assert test_puzzle.solve_part1() == 374
    assert test_puzzle.solve_part2(expansion=10) == 1030
    assert test_puzzle.solve_part2(expansion=100) == 8410

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = Puzzle(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2(expansion=1_000_000)}")
