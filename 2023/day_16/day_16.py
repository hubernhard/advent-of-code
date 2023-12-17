"""Day 16: The Floor Will Be Lava"""

from collections import deque
from pathlib import Path
from typing import NamedTuple, Self

test_content = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return Point(self.x + other.x, self.y + other.y)


class Puzzle:
    def __init__(self, content: str):
        rows = content.strip().split("\n")
        self.nx = len(rows[0])
        self.ny = len(rows)
        self.mirrors = {}
        for y, row in enumerate(rows):
            for x, val in enumerate(row):
                if val != ".":
                    self.mirrors[Point(x, y)] = val

    def move(self, start: Point, direction: Point) -> int:
        queue = deque()
        # Store current position and direction in queue
        queue.append((start, direction))
        visited = set()
        beams = set()

        while queue:
            p, d = queue.popleft()
            if (p, d) in beams:
                continue
            beams.add((p, d))

            if 0 <= p.x < self.nx and 0 <= p.y < self.ny:
                visited.add(p)
                mirror = self.mirrors.get(p)
                if not mirror:
                    queue.append((p + d, d))
                else:
                    directions = []

                    match mirror:
                        case "/":
                            directions = [Point(-d.y, -d.x)]
                        case "\\":
                            directions = [Point(d.y, d.x)]
                        case "-":
                            if d.y == 0:
                                directions = [d]
                            else:
                                directions = [Point(-1, 0), Point(1, 0)]
                        case "|":
                            if d.x == 0:
                                directions = [d]
                            else:
                                directions = [Point(0, -1), Point(0, 1)]

                    for d in directions:
                        queue.append((p + d, d))

        return len(visited)

    def solve_part1(self) -> int:
        return self.move(Point(0, 0), Point(1, 0))

    def solve_part2(self) -> int:
        n_max = 0

        for x in range(self.nx):
            n_max = max(n_max, self.move(Point(x, 0), Point(0, 1)))
            n_max = max(n_max, self.move(Point(x, self.ny - 1), Point(0, -1)))

        for y in range(self.ny):
            n_max = max(n_max, self.move(Point(0, y), Point(1, 0)))
            n_max = max(n_max, self.move(Point(self.nx - 1, y), Point(-1, 0)))

        return n_max


if __name__ == "__main__":
    test_puzzle = Puzzle(test_content)
    assert test_puzzle.solve_part1() == 46
    assert test_puzzle.solve_part2() == 51

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = Puzzle(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2()}")
