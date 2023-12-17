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

    @staticmethod
    def _ndiff(a: str, b: str) -> int:
        return sum(x != y for x, y in zip(a, b, strict=True))

    def _find_reflection(self, x: list[str], max_ndiff: int = 0) -> int | None:
        for i in range(1, len(x[0])):
            max_ndiff_ = max_ndiff
            for row in x:
                a, b = row[:i], row[i:]
                n = min(len(a), len(b))
                a, b = a[-n:], b[:n][::-1]
                diff = self._ndiff(a, b)
                if diff > max_ndiff_:
                    break
                if diff == max_ndiff_ > 0:
                    max_ndiff_ = 0
            else:
                # Loop did not break, so i could be the right index:
                #   max_ndiff == 0 -> i is the right index
                #   max_ndiff != max_ndiff_ -> there was exactly one smudge ->
                #     i is the right index
                if max_ndiff == 0 or max_ndiff != max_ndiff_:
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
        total = 0
        for pattern in self.patterns:
            i = self._find_reflection(pattern.rows, max_ndiff=1)
            if i is not None:
                total += i
            else:
                total += 100 * self._find_reflection(pattern.cols, max_ndiff=1)
        return total


if __name__ == "__main__":
    test_puzzle = Puzzle(test_content)
    assert test_puzzle.solve_part1() == 405
    assert test_puzzle.solve_part2() == 400

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = Puzzle(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2()}")
