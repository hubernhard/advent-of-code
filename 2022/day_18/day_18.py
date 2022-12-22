"""Day 18: Boiling Boulders"""

from collections import deque
from pathlib import Path
from typing import Iterator, NamedTuple

test_content = """
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""


class Cube(NamedTuple):
    x: int
    y: int
    z: int

    def neighbors(self) -> set["Cube"]:
        x, y, z = self
        neighbors = {Cube(x + d, y, z) for d in (-1, 1)}
        neighbors.update({Cube(x, y + d, z) for d in (-1, 1)})
        neighbors.update({Cube(x, y, z + d) for d in (-1, 1)})
        return neighbors


class LavaDroplet:
    def __init__(self, content: str):
        self.lava = self._process_input(content)

    def _process_input(self, content: str) -> set[Cube]:
        content = content.strip().split("\n")
        return {Cube(*eval(row)) for row in content}

    @staticmethod
    def get_surface_area(cubes: set[Cube]) -> int:
        total_surface = 0
        for cube in cubes:
            neighbors = cube.neighbors()
            total_surface += len(neighbors.difference(cubes))
        return total_surface

    def solve_part1(self) -> int:
        return self.get_surface_area(self.lava)

    def solve_part2(self) -> int:
        cubes = self.flodd_fill()
        return self.get_surface_area(cubes)

    def _get_ranges(self) -> list[Iterator[int]]:
        components = [[cube[i] for cube in self.lava] for i in range(3)]
        return [range(min(vals) - 1, max(vals) + 2) for vals in components]

    def flodd_fill(self) -> set[Cube]:
        """Find all exterior cubes starting at a point outside the droplet."""
        x_vals, y_vals, z_vals = self._get_ranges()
        cubes = {Cube(x, y, z) for x in x_vals for y in y_vals for z in z_vals}

        queue = deque()
        # Start at minimum cube (which is always on the outside of the droplet)
        queue.append(min(cubes))
        # Mark all lava cubes as already visited
        visited = self.lava.copy()

        while queue:
            cube = queue.popleft()
            # Mark current cube as visited
            visited.add(cube)
            # Get neighbors (inside the limits)
            neighbors = cube.neighbors().intersection(cubes)
            # Remove already visited points from neighbors
            neighbors.difference_update(visited)
            # Add neighbors (that are not already in the queue) to queue
            queue.extend(neighbors.difference(queue))

        interior_points = {cube for cube in cubes if cube not in visited}

        return self.lava.union(interior_points)


if __name__ == "__main__":
    test_puzzle = LavaDroplet(test_content)
    assert test_puzzle.solve_part1() == 64
    assert test_puzzle.solve_part2() == 58

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = LavaDroplet(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2()}")
