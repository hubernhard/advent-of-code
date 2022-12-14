"""Day 13: Distress Signal"""

from math import prod
from pathlib import Path

test_content = """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""


class Puzzle:
    def __init__(self, content: str):
        pairs = [pair.split("\n") for pair in content.strip().split("\n\n")]
        self.pairs = [[eval(x) for x in pair] for pair in pairs]

    def compare(self, left_: list, right_: list) -> bool | None:
        # print(f"Compare {left_} vs {right_}")
        iter_left = iter(left_)
        iter_right = iter(right_)

        while True:
            left = next(iter_left, None)
            right = next(iter_right, None)

            if left is None and right is None:
                # No items left in both sides.
                # Can only happen when called in a recursion.
                return None
            else:
                if left is None:
                    return True  # left side is smaller
                elif right is None:
                    return False  # right side is smaller

            if isinstance(left, int) and isinstance(right, int):
                if left < right:
                    return True  # right order
                elif left > right:
                    return False  # not right order
            else:
                if not isinstance(left, list):
                    left = [left]
                if not isinstance(right, list):
                    right = [right]

                if (right_order_ := self.compare(left, right)) is not None:
                    return right_order_

    def solve_part1(self) -> int:
        indexes = [
            i + 1 for i, pair in enumerate(self.pairs) if self.compare(*pair)
        ]
        return sum(indexes)

    def solve_part2(self) -> int:
        dividers = ([[2]], [[6]])
        # Get list of packets and dividers
        packets = list(dividers)
        for pair in self.pairs:
            packets += list(pair)
        # Sort packets
        n = len(packets)
        for i in range(n):
            for j in range(n - i - 1):
                # Swap elements if right element is 'smaller'
                if self.compare(packets[j + 1], packets[j]):
                    packets[j], packets[j + 1] = packets[j + 1], packets[j]

        return prod(packets.index(divider) + 1 for divider in dividers)


if __name__ == "__main__":
    test_puzzle = Puzzle(test_content)
    assert test_puzzle.solve_part1() == 13
    assert test_puzzle.solve_part2() == 140

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = Puzzle(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2()}")
