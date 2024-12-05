"""Day 14: Regolith Reservoir"""

from collections.abc import Callable
from pathlib import Path
from typing import NamedTuple

test_content = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""


class GridPoint(NamedTuple):
    x: int
    y: int


class ReservoirSimulator:
    origin: GridPoint
    blocked: dict[GridPoint, str]

    def __init__(self, content: str):
        self.content = content.strip().split("\n")
        self.origin = GridPoint(500, 0)

    def initialize_grid(self) -> None:
        self.blocked = {}
        for row in self.content:
            positions = [
                [int(v) for v in pair.split(",")] for pair in row.split(" -> ")
            ]
            for (x1, y1), (x2, y2) in zip(
                positions[:-1], positions[1:], strict=False
            ):
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    for y in range(min(y1, y2), max(y1, y2) + 1):
                        self.blocked[GridPoint(x, y)] = "#"

    def get_limits(self) -> tuple[int, int, int]:
        xmin = min(p.x for p in self.blocked.keys())
        xmax = max(p.x for p in self.blocked.keys())
        ymax = max(p.y for p in self.blocked.keys())
        return xmin, xmax, ymax

    def __str__(self) -> str:
        """Convert the grid into a string."""
        xmin, xmax, ymax = self.get_limits()
        grid = f"Grid size: {xmax - xmin + 1} x {ymax + 1}\n"
        for y in range(ymax + 1):
            for x in range(xmin, xmax + 1):
                grid += self.blocked.get(GridPoint(x, y), ".")
            grid += "\n"
        return grid

    def simulate(
        self,
        is_blocked: Callable[[GridPoint], bool],
        is_inside: Callable[[GridPoint], bool],
    ) -> int:
        counter = 0
        point = self.origin

        while point is not None and point not in self.blocked:
            px, py = old_point = point
            neighbors = [GridPoint(x, py + 1) for x in (px, px - 1, px + 1)]

            for new_point in neighbors:
                if is_blocked(new_point):
                    continue
                elif is_inside(new_point):
                    point = new_point
                    break
                else:
                    # Abyss reached
                    point = None

            if point == old_point:
                self.blocked[point] = "o"
                counter += 1
                point = self.origin

        self.blocked[self.origin] = "+"
        print(self)

        return counter

    def solve_part1(self) -> int:
        self.initialize_grid()
        xmin, xmax, ymax = self.get_limits()
        return self.simulate(
            is_blocked=lambda p: p in self.blocked,
            is_inside=lambda p: xmin <= p.x <= xmax and p.y <= ymax,
        )

    def solve_part2(self) -> int:
        self.initialize_grid()
        ymax = self.get_limits()[2]
        ymax += 2

        return self.simulate(
            is_blocked=lambda p: p in self.blocked or p.y == ymax,
            is_inside=lambda p: p.y <= ymax,
        )


if __name__ == "__main__":
    test_simulator = ReservoirSimulator(test_content)
    assert test_simulator.solve_part1() == 24
    assert test_simulator.solve_part2() == 93

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    simulator = ReservoirSimulator(content)
    print(f"Part 1: {simulator.solve_part1()}")
    print(f"Part 2: {simulator.solve_part2()}")
