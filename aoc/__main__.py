import sys
from pathlib import Path

TEMPLATE = '''"""Day %d: TODO: CHANGE TITLE"""

from pathlib import Path

test_content = """
YOUR TEST CONTENT
"""


class Puzzle:
    def __init__(self, content: str):
        self.content = content.strip().split("\\n")

    def solve_part1(self) -> int:
        return 1

    def solve_part2(self) -> int:
        return 2


if __name__ == "__main__":
    test_puzzle = Puzzle(test_content)
    assert test_puzzle.solve_part1() == 1
    assert test_puzzle.solve_part2() == 2

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = Puzzle(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2()}")
'''


def _add_day(year: int, day: int) -> None:
    day_ = f"day_{day:02d}"
    path = Path(str(year)) / day_
    path.mkdir(exist_ok=True, parents=True)

    file = path / f"{day_}.py"
    if file.exists():
        raise FileExistsError(f"File '{file}' already exists!")
    file.write_text(TEMPLATE % day)


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        raise ValueError("Please pass YEAR and DAY as command-line arguments.")
    _add_day(int(args[1]), int(args[2]))
