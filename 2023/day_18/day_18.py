"""Day 18: Lavaduct Lagoon"""

import re
from collections import deque
from pathlib import Path
from typing import NamedTuple, Self

test_content = """
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, other: int) -> Self:
        return Point(self.x * other, self.y * other)

    def neighbors(self) -> set[Self]:
        neighbors = {Point(self.x + d, self.y) for d in (-1, 1)}
        neighbors |= {Point(self.x, self.y + d) for d in (-1, 1)}
        return neighbors


DIRECTIONS = {
    "U": Point(0, -1),
    "D": Point(0, 1),
    "L": Point(-1, 0),
    "R": Point(1, 0),
}


def flood_fill(border: set[Point]) -> set[Point]:
    xs = range(min(p.x for p in border) - 1, max(p.x for p in border) + 2)
    ys = range(min(p.y for p in border) - 1, max(p.y for p in border) + 2)
    points = {Point(x, y) for x in xs for y in ys}
    start = Point(xs.start, ys.start)

    queue = deque()
    queue.append(start)
    outside = set()

    while queue:
        p = queue.popleft()
        outside.add(p)
        neighbors = p.neighbors()
        neighbors.difference_update(queue)
        for pn in neighbors:
            if pn in points and pn not in border and pn not in outside:
                queue.append(pn)

    interior = {p for p in points if p not in outside}
    return interior


class Puzzle:
    def __init__(self, content: str):
        self.instructions = re.findall(r"([A-Z]) (\d+) \(#(\w{6})\)", content)

    def solve_part1(self) -> int:
        point = Point(0, 0)
        border = {point}
        for direction, distance, _ in self.instructions:
            for _ in range(int(distance)):
                point += DIRECTIONS[direction]
                border.add(point)
        interior = flood_fill(border)
        return len(interior)

    def solve_part2(self) -> int:
        point = Point(0, 0)
        vertices = [point]
        border_length = 0
        for _, _, hexcode in self.instructions:
            direction = DIRECTIONS["RDLU"[int(hexcode[-1])]]
            distance = int(hexcode[:-1], 16)
            point += direction * distance
            vertices.append(point)
            border_length += distance

        # Use Trapezoid formula to compute polygon area:
        # https://en.wikipedia.org/wiki/Shoelace_formula
        total = 0
        for p1, p2 in zip(vertices[:-1], vertices[1:], strict=False):
            total += (p1.y + p2.y) * (p1.x - p2.x)
        interior = abs(total // 2)

        # Use Pick's theorem to compute area:
        # https://en.wikipedia.org/wiki/Pick%27s_theorem
        return interior + border_length // 2 + 1


if __name__ == "__main__":
    test_puzzle = Puzzle(test_content)
    assert test_puzzle.solve_part1() == 62
    assert test_puzzle.solve_part2() == 952_408_144_115

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = Puzzle(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2()}")
