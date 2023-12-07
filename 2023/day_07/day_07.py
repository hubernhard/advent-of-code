"""Day 7: Camel Cards"""

from collections import Counter
from pathlib import Path
from typing import NamedTuple, Self

test_content = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

CARDS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]


class Hand(NamedTuple):
    cards: str
    bid: int

    @classmethod
    def from_text(cls, text: str) -> Self:
        cards, bid = text.split()
        return cls(cards, int(bid))

    @staticmethod
    def _get_type_rank(counts: Counter) -> int:
        if counts[5]:
            return 7
        if counts[4]:
            return 6
        if counts[3] and counts[2]:
            return 5
        if counts[3]:
            return 4
        if counts[2] == 2:
            return 3
        if counts[2]:
            return 2
        if counts[1] == 5:
            return 1

    def __lt__(self, other: Self) -> bool:
        # Get counters for types
        t1 = Counter(Counter(self.cards).values())
        t2 = Counter(Counter(other.cards).values())

        # Handle same types
        if t1 == t2:
            for c1, c2 in zip(self.cards, other.cards):
                i1 = CARDS.index(c1)
                i2 = CARDS.index(c2)
                # Lower index is better
                if i1 < i2:
                    return True
                if i1 > i2:
                    return False

        return self._get_type_rank(t1) > self._get_type_rank(t2)


class Puzzle:
    def __init__(self, content: str):
        self.hands = [Hand.from_text(x) for x in content.strip().split("\n")]

    def solve_part1(self) -> int:
        total = 0
        for rank, hand in enumerate(sorted(self.hands, reverse=True)):
            total += (rank + 1) * hand.bid
        return total

    def solve_part2(self) -> int:
        return 2


if __name__ == "__main__":
    test_puzzle = Puzzle(test_content)
    assert test_puzzle.solve_part1() == 6440
    assert test_puzzle.solve_part2() == 2

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = Puzzle(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2()}")
