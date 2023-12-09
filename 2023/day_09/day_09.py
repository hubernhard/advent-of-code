"""Day 9: Mirage Maintenance"""

from pathlib import Path

test_content = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""


class Puzzle:
    def __init__(self, content: str):
        content = content.strip().split("\n")
        self.arrays = [list(map(int, line.split())) for line in content]

    @staticmethod
    def diff(x: list[int]) -> list[int]:
        return [b - a for a, b in zip(x[:-1], x[1:])]

    def solve_part1(self) -> int:
        total = 0
        for array in self.arrays:
            x = array.copy()
            total += x[-1]
            while not all(v == 0 for v in x):
                x = self.diff(x)
                total += x[-1]
        return total

    def solve_part2(self) -> int:
        total = 0
        for array in self.arrays:
            x = array.copy()
            first_values = [x[0]]
            while not all(v == 0 for v in x):
                x = self.diff(x)
                first_values.append(x[0])

            first_values.reverse()
            old_value = 0
            for value in first_values[1:]:
                old_value = value - old_value
            total += old_value

        return total


if __name__ == "__main__":
    test_puzzle = Puzzle(test_content)
    assert test_puzzle.solve_part1() == 114
    assert test_puzzle.solve_part2() == 2

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = Puzzle(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2()}")
