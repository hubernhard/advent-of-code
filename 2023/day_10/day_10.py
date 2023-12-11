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

test_content2 = """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""

test_content3 = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
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
    ".": (),
}


class Puzzle:
    def __init__(self, content: str):
        content = content.strip().split("\n")
        self.nx = len(content[0])
        self.ny = len(content)
        self.points = {}
        for y, line in enumerate(content):
            for x, type_ in enumerate(line):
                point = Point(x, y)
                self.points[point] = type_
                if type_ == "S":
                    self.start = point

    def visit_all(self) -> dict[Point, int]:
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
                    if type_ is not None and type_ != ".":
                        # Check if we can go back to p0 from p1
                        neighbors = [p1 + d for d in DIRECTIONS[type_]]
                        if p0 in neighbors:
                            queue.append((p1, n))
                            visited[p1] = n

        return visited

    def solve_part1(self) -> int:
        visited = self.visit_all()
        return max(visited.values())

    def solve_part2(self) -> int:
        visited = self.visit_all()
        total = 0

        for y in range(self.ny):
            inside = False
            for x in range(self.nx - 1):
                p = Point(x, y)
                type_ = self.points.get(p)
                if p in visited and type_ in ("|", "J", "L"):
                    inside = not inside
                if inside and p not in visited:
                    total += 1

        return total


if __name__ == "__main__":
    assert Puzzle(test_content).solve_part1() == 8
    assert Puzzle(test_content2).solve_part2() == 8
    assert Puzzle(test_content3).solve_part2() == 10

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = Puzzle(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2()}")
