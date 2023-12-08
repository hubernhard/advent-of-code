"""Day 8: Haunted Wasteland"""

import math
import re
from itertools import cycle
from pathlib import Path

test_content = """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

test_content2 = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""


class Puzzle:
    def __init__(self, content: str):
        self.instructions, nodes = content.strip().split("\n\n")
        self.nodes = {}
        pattern = r"(\w{3}) = \((\w{3}), (\w{3})\)"
        for label, left, right in re.findall(pattern, nodes):
            self.nodes[label] = (left, right)

    def solve_part1(self) -> int:
        instructions = cycle(self.instructions)
        count = 0
        position = "AAA"
        while position != "ZZZ":
            instruction = next(instructions)
            position = self.nodes[position][instruction == "R"]
            count += 1
        return count

    def _follow_path(self, position: str) -> int:
        count = 0
        instructions = cycle(self.instructions)
        while not position.endswith("Z"):
            instruction = next(instructions)
            position = self.nodes[position][instruction == "R"]
            count += 1
        return count

    def solve_part2(self) -> int:
        positions = [p for p in self.nodes.keys() if p.endswith("A")]
        counts = [self._follow_path(p) for p in positions]
        return math.lcm(*counts)


if __name__ == "__main__":
    test_puzzle = Puzzle(test_content)
    assert test_puzzle.solve_part1() == 2
    test_puzzle = Puzzle(test_content2)
    assert test_puzzle.solve_part2() == 6

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = Puzzle(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2()}")
