"""Day 13: Point of Incidence"""

from dataclasses import dataclass
from pathlib import Path

test_content = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""


@dataclass
class Pattern:
    rows: list[str]

    @property
    def cols(self) -> list[str]:
        ncols = len(self.rows[0])
        return ["".join(r[i] for r in self.rows) for i in range(ncols)]


class Puzzle:
    def __init__(self, content: str):
        patterns = content.strip().split("\n\n")
        self.patterns = [Pattern(p.split("\n")) for p in patterns]

    def _find_reflection(self, x: list[str]) -> int | None:
        for i in range(1, len(x[0])):
            for row in x:
                a, b = row[:i], row[i:]
                n = min(len(a), len(b))
                a, b = a[-n:], b[:n][::-1]
                if a != b:
                    break
            else:
                # Loop did not break, so i must be the right index
                return i
        return None

    def solve_part1(self) -> int:
        total = 0
        for pattern in self.patterns:
            i = self._find_reflection(pattern.rows)
            if i is not None:
                total += i
            else:
                total += 100 * self._find_reflection(pattern.cols)
        return total

    def solve_part2(self) -> int:
        return 2


if __name__ == "__main__":
    test_puzzle = Puzzle(test_content)
    assert test_puzzle.solve_part1() == 405
    assert test_puzzle.solve_part2() == 2

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = Puzzle(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2()}")
