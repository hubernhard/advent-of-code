"""Day 12: Hill Climbing Algorithm"""

import math
import string
from collections import deque
from pathlib import Path
from typing import NamedTuple

test_content = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""


class GridPoint(NamedTuple):
    i: int
    j: int
    val: str

    def diff(self, other: "GridPoint") -> int:
        letters = string.ascii_lowercase
        return letters.index(other.val) - letters.index(self.val)


class Grid:
    grid: list[list[GridPoint]]
    start_point: GridPoint
    end_point: GridPoint

    def __init__(self, content: str):
        self._initialize_grid(content)
        self.n_rows = len(self.grid)
        self.n_cols = len(self.grid[0])

    def _initialize_grid(self, content: str) -> None:
        content = content.strip().split("\n")
        self.grid = []
        for i, row in enumerate(content):
            self.grid.append([])
            for j, val in enumerate(row):
                x = GridPoint(i, j, val.replace("S", "a").replace("E", "z"))
                if val == "S":
                    self.start_point = x
                if val == "E":
                    self.end_point = x
                self.grid[i].append(x)

    def neighbors(self, x: GridPoint) -> set[GridPoint]:
        neighbors = {
            self.grid[x.i][max(x.j - 1, 0)],  # west
            self.grid[x.i][min(x.j + 1, self.n_cols - 1)],  # east
            self.grid[max(x.i - 1, 0)][x.j],  # north
            self.grid[min(x.i + 1, self.n_rows - 1)][x.j],  # south
        }
        neighbors.discard(x)
        return neighbors

    def climb(self) -> int:
        queue = deque()
        queue.append((self.start_point, 0))
        # Store visited points and the smallest number of steps to reach them
        visited = {self.start_point: 0, self.end_point: math.inf}

        while queue:
            x, n = queue.popleft()
            n += 1
            for neighbor in self.neighbors(x):
                if x.diff(neighbor) <= 1:
                    if neighbor not in visited.keys():
                        queue.append((neighbor, n))

                    visited.setdefault(neighbor, n)
                    if n < visited[neighbor]:
                        visited[neighbor] = n

        return visited[self.end_point]

    def solve_part1(self) -> int:
        return self.climb()

    def solve_part2(self) -> int:
        min_steps = math.inf
        for row in self.grid:
            for x in row:
                if x.val == "a":
                    self.start_point = x
                    if (n := self.climb()) < min_steps:
                        min_steps = n
        return min_steps


if __name__ == "__main__":
    test_puzzle = Grid(test_content)
    assert test_puzzle.solve_part1() == 31
    assert test_puzzle.solve_part2() == 29

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = Grid(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2()}")
