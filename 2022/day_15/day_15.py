"""Day 15: Beacon Exclusion Zone"""

import re
from collections.abc import Iterator
from pathlib import Path
from typing import NamedTuple

test_content = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""


class GridPoint(NamedTuple):
    x: int
    y: int

    def dist(self, other: "GridPoint") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def ball_slice(self, other: "GridPoint", y: int) -> Iterator["GridPoint"]:
        radius = self.dist(other)
        if min(self.y, other.y) - radius <= y <= max(self.y, other.y) + radius:
            dy = abs(self.y - y)
            for dx in range(radius + 1 - dy):
                for sign in (-1, 1):
                    point = GridPoint(self.x + sign * dx, y)
                    if point not in (self, other):
                        yield point


class Limits(NamedTuple):
    xmin: int
    xmax: int
    ymin: int
    ymax: int


class BeaconFinder:
    sensors: list[GridPoint]
    beacons: list[GridPoint]

    def __init__(self, content: str):
        self._process_input(content)

    def _process_input(self, content: str) -> None:
        self.sensors = []
        self.beacons = []

        for row in content.strip().split("\n"):
            x1, y1, x2, y2 = map(int, re.findall("[-|0-9]+", row))
            self.sensors.append(GridPoint(x1, y1))
            self.beacons.append(GridPoint(x2, y2))

    def solve_part1(self, y: int) -> int:
        blocked = set()
        for sensor, beacon in zip(self.sensors, self.beacons, strict=False):
            for point in sensor.ball_slice(beacon, y):
                blocked.add(point)
        return len(blocked)

    def solve_part2(self, limits: Limits) -> int:
        dists = [
            s.dist(b) for s, b in zip(self.sensors, self.beacons, strict=False)
        ]
        x, y = limits.xmin, limits.ymin

        while y <= limits.ymax:
            for sensor, radius in zip(self.sensors, dists, strict=False):
                if sensor.dist(GridPoint(x, y)) <= radius:
                    # Move x to the right side of the current sensor's ball
                    x = sensor.x + radius - abs(sensor.y - y) + 1
                    if x > limits.xmax:
                        x = limits.xmin
                        y += 1
                    break
            else:
                print(f"Distress beacon found at {(x, y)}")
                return x * 4_000_000 + y


if __name__ == "__main__":
    test_finder = BeaconFinder(test_content)
    assert test_finder.solve_part1(y=10) == 26
    assert test_finder.solve_part2(Limits(0, 20, 0, 20)) == 56_000_011

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    finder = BeaconFinder(content)
    print(f"Part 1: {finder.solve_part1(y=2_000_000)}")
    print(f"Part 2: {finder.solve_part2(Limits(0, 4_000_000, 0, 4_000_000))}")
