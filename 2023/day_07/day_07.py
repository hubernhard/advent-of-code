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


class Hand(NamedTuple):
    cards: str
    bid: int

    @classmethod
    def from_text(cls, text: str) -> Self:
        cards, bid = text.split()
        return cls(cards, int(bid))

    @property
    def replaced_cards(self) -> str:
        cards = self.cards.replace("J", "")
        # Get most common card that is not J
        if len(cards) == 0:
            most_common = "A"  # We can pick any card
        else:
            most_common = Counter(cards).most_common(1)[0][0]
        return self.cards.replace("J", most_common)

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

    def _compare(
        self, other: Self, card_order: str, replace_joker: bool = False
    ) -> bool:
        cards1 = self.cards if not replace_joker else self.replaced_cards
        cards2 = other.cards if not replace_joker else other.replaced_cards
        # Get counters for types
        t1 = Counter(Counter(cards1).values())
        t2 = Counter(Counter(cards2).values())

        # Handle same types
        if t1 == t2:
            for c1, c2 in zip(self.cards, other.cards):
                i1 = card_order.index(c1)
                i2 = card_order.index(c2)
                # Lower index means stronger card
                if i1 > i2:
                    return True
                if i1 < i2:
                    return False

        return self._get_type_rank(t1) < self._get_type_rank(t2)

    def __lt__(self, other: Self) -> bool:
        return self._compare(other, card_order="AKQJT98765432")


class Hand2(Hand):
    def __lt__(self, other: Self) -> bool:
        return self._compare(
            other, card_order="AKQT98765432J", replace_joker=True
        )


class Puzzle:
    def __init__(self, content: str):
        self.content = content.strip().split("\n")
        self.hands = [Hand.from_text(x) for x in self.content]

    def solve_part1(self) -> int:
        total = 0
        for rank, hand in enumerate(sorted(self.hands)):
            total += (rank + 1) * hand.bid
        return total

    def solve_part2(self) -> int:
        hands = [Hand2.from_text(x) for x in self.content]
        total = 0
        for rank, hand in enumerate(sorted(hands)):
            total += (rank + 1) * hand.bid
        return total


if __name__ == "__main__":
    test_puzzle = Puzzle(test_content)
    assert test_puzzle.solve_part1() == 6440
    assert test_puzzle.solve_part2() == 5905

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = Puzzle(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2()}")
