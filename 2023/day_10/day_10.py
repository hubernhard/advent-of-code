"""Day 10: Pipe Maze"""

from collections import deque
from pathlib import Path
from typing import NamedTuple, Self

test_content = """
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return Point(self.x + other.x, self.y + other.y)


UP = Point(0, -1)
DOWN = Point(0, 1)
LEFT = Point(-1, 0)
RIGHT = Point(1, 0)

DIRECTIONS = {
    "|": (UP, DOWN),
    "-": (LEFT, RIGHT),
    "L": (UP, RIGHT),
    "J": (UP, LEFT),
    "7": (DOWN, LEFT),
    "F": (DOWN, RIGHT),
    "S": (UP, DOWN, LEFT, RIGHT),
}


class Puzzle:
    def __init__(self, content: str):
        self.points = {}
        for y, line in enumerate(content.strip().split("\n")):
            for x, type_ in enumerate(line):
                point = Point(x, y)
                if type_ != ".":
                    self.points[point] = type_
                if type_ == "S":
                    self.start = point

    def solve_part1(self) -> int:
        queue = deque()
        queue.append((self.start, 0))
        # Store visited points and the smallest number of steps to reach them
        visited = {self.start: 0}

        while queue:
            p0, n = queue.popleft()
            n += 1
            for direction in DIRECTIONS[self.points[p0]]:
                p1 = p0 + direction
                if p1 not in visited:
                    type_ = self.points.get(p1)
                    if type_ is not None:
                        # Check if we can go back to p0 from p1
                        neighbors = [p1 + d for d in DIRECTIONS[type_]]
                        if p0 in neighbors:
                            queue.append((p1, n))
                            visited[p1] = n

        return max(visited.values())

    def solve_part2(self) -> int:
        return 2


if __name__ == "__main__":
    test_puzzle = Puzzle(test_content)
    assert test_puzzle.solve_part1() == 8
    assert test_puzzle.solve_part2() == 2

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = Puzzle(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2()}")
