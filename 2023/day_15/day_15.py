"""Day 15: Lens Library"""

from pathlib import Path
from typing import NamedTuple

test_content = """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""


class Lens(NamedTuple):
    label: str
    focal_length: int


class Puzzle:
    def __init__(self, content: str):
        self.strings = content.strip().split(",")

    @staticmethod
    def _get_hash(string: str) -> int:
        current = 0
        for x in string:
            current += ord(x)
            current *= 17
            current %= 256
        return current

    def solve_part1(self) -> int:
        total = 0
        for string in self.strings:
            total += self._get_hash(string)
        return total

    def solve_part2(self) -> int:
        boxes = [[] for _ in range(256)]

        for string in self.strings:
            if "-" in string:
                label = string.removesuffix("-")
                box_number = self._get_hash(label)
                for lens in (box := boxes[box_number]):
                    if lens.label == label:
                        box.remove(lens)
                        break
            else:
                label, focal_length = string.split("=")
                box_number = self._get_hash(label)
                new_lens = Lens(label, int(focal_length))
                for i, lens in enumerate(boxes[box_number]):
                    if lens.label == label:
                        boxes[box_number][i] = new_lens
                        break
                else:
                    boxes[box_number].append(new_lens)

        total = 0
        for i, box in enumerate(boxes):
            for slot, lens in enumerate(box):
                total += (i + 1) * (slot + 1) * lens.focal_length

        return total


if __name__ == "__main__":
    test_puzzle = Puzzle(test_content)
    assert test_puzzle.solve_part1() == 1320
    assert test_puzzle.solve_part2() == 145

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = Puzzle(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2()}")
