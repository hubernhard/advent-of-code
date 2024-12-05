"""Day 9: Rope Bridge"""

from collections.abc import Iterator
from pathlib import Path
from typing import Self

test_content = """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""

test_content2 = """
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def add(self, x: int, y: int) -> Self:
        self.x += x
        self.y += y
        return self

    def move(self, direction: str) -> Self:
        directions = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}
        return self.add(*directions[direction])

    def follow(self, other: "Point") -> Self:
        # Get distance (in x and y) to other point
        dx = other.x - self.x
        dy = other.y - self.y
        # Tail needs to move if distance in at least one component is > 1
        if abs(dx) > 1 or abs(dy) > 1:
            # Move one step in direction of the other object if distance in
            # component is positive. Diagonal steps are handled automatically.
            x = bool(dx) * (-1 if dx < 0 else 1)
            y = bool(dy) * (-1 if dy < 0 else 1)
            self.add(x, y)
        return self

    @property
    def coordinates(self) -> tuple[int, int]:
        return self.x, self.y


class RopeSimulator:
    def __init__(self, content: str):
        self.actions = content.strip().split("\n")

    def iter_head_motions(self) -> Iterator[str]:
        for action in self.actions:
            direction, size = action.split()
            for _ in range(int(size)):
                yield direction

    def solve_part1(self) -> int:
        head = Point(0, 0)
        tail = Point(0, 0)
        visited = set()

        for direction in self.iter_head_motions():
            head.move(direction)
            tail.follow(head)
            visited.add(tail.coordinates)

        return len(visited)

    def solve_part2(self) -> int:
        points = [Point(0, 0) for _ in range(10)]
        visited = set()

        for direction in self.iter_head_motions():
            for i, point in enumerate(points):
                if i == 0:
                    point.move(direction)
                else:
                    point.follow(points[i - 1])
            visited.add(points[-1].coordinates)

        return len(visited)


if __name__ == "__main__":
    test_simulator = RopeSimulator(test_content)
    assert test_simulator.solve_part1() == 13
    assert test_simulator.solve_part2() == 1
    test_simulator2 = RopeSimulator(test_content2)
    assert test_simulator2.solve_part2() == 36

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    simulator = RopeSimulator(content)
    print(f"Part 1: {simulator.solve_part1()}")
    print(f"Part 2: {simulator.solve_part2()}")
