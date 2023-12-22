"""Day 17: Clumsy Crucible"""

from pathlib import Path
from queue import PriorityQueue
from typing import NamedTuple, Self

test_content = """
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return Point(self.x + other.x, self.y + other.y)


class State(NamedTuple):
    position: Point
    direction: Point
    count: int


DIRECTIONS = {
    Point(1, 0): (Point(1, 0), Point(0, 1), Point(0, -1)),
    Point(-1, 0): (Point(-1, 0), Point(0, 1), Point(0, -1)),
    Point(0, 1): (Point(0, 1), Point(1, 0), Point(-1, 0)),
    Point(0, -1): (Point(0, -1), Point(1, 0), Point(-1, 0)),
}


class Puzzle:
    def __init__(self, content: str):
        rows = content.strip().split("\n")
        self.points = {}
        for y, row in enumerate(rows):
            for x, val in enumerate(row):
                self.points[Point(x, y)] = int(val)
        self.xmax = max(p.x for p in self.points)
        self.ymax = max(p.y for p in self.points)

    def solve_part1(self) -> int:
        start_pos = Point(0, 0)
        end_pos = Point(self.xmax, self.ymax)
        queue = PriorityQueue()
        queue.put((0, State(start_pos, Point(0, 1), 0)))
        queue.put((0, State(start_pos, Point(1, 0), 0)))
        seen = set()

        min_heat_loss = 0

        while not queue.empty():
            heat_loss, state = queue.get()
            if state in seen:
                continue
            seen.add(state)

            if state.position == end_pos:
                min_heat_loss = heat_loss
                break

            for direction in DIRECTIONS[state.direction]:
                count = state.count + 1 if direction == state.direction else 1
                if count > 3:
                    continue
                new_pos = state.position + direction
                if 0 <= new_pos.x <= self.xmax and 0 <= new_pos.y <= self.ymax:
                    new_state = State(new_pos, direction, count)
                    new_heat_loss = heat_loss + self.points[new_pos]
                    queue.put((new_heat_loss, new_state))

        return min_heat_loss

    def solve_part2(self) -> int:
        start_pos = Point(0, 0)
        end_pos = Point(self.xmax, self.ymax)
        queue = PriorityQueue()
        queue.put((0, State(start_pos, Point(0, 1), 0)))
        queue.put((0, State(start_pos, Point(1, 0), 0)))
        seen = set()

        min_heat_loss = 0

        while not queue.empty():
            heat_loss, state = queue.get()
            # print((heat_loss, state))
            if state in seen:
                continue
            seen.add(state)

            if state.position == end_pos:
                min_heat_loss = heat_loss
                break

            for direction in DIRECTIONS[state.direction]:
                if direction != state.direction and state.count < 4:
                    continue
                count = state.count + 1 if direction == state.direction else 1
                if count > 10:
                    continue

                new_pos = state.position + direction
                if 0 <= new_pos.x <= self.xmax and 0 <= new_pos.y <= self.ymax:
                    new_state = State(new_pos, direction, count)
                    new_heat_loss = heat_loss + self.points[new_pos]
                    queue.put((new_heat_loss, new_state))

        return min_heat_loss


if __name__ == "__main__":
    test_puzzle = Puzzle(test_content)
    assert test_puzzle.solve_part1() == 102
    assert test_puzzle.solve_part2() == 94

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = Puzzle(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2()}")
