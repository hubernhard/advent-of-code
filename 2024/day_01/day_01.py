"""Day 1: Historian Hysteria"""

from pathlib import Path

test_content = """
3   4
4   3
2   5
1   3
3   9
3   3
"""


class Puzzle:
    def __init__(self, content: str):
        content = content.strip().split("\n")
        content = [list(map(int, line.split())) for line in content]
        self.lists = list(zip(*content, strict=False))

    def solve_part1(self) -> int:
        a = sorted(self.lists[0])
        b = sorted(self.lists[1])
        return sum(abs(x - y) for x, y in zip(a, b, strict=True))

    def solve_part2(self) -> int:
        a = sorted(self.lists[0])
        b = self.lists[1]
        return sum(x * b.count(x) for x in a)


if __name__ == "__main__":
    test_puzzle = Puzzle(test_content)
    assert test_puzzle.solve_part1() == 11
    assert test_puzzle.solve_part2() == 31

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = Puzzle(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2()}")
