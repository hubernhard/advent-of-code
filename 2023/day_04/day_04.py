"""Day 4: Scratchcards"""

import re
from pathlib import Path

test_content = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""


class Puzzle:
    def __init__(self, content: str):
        content = re.sub(r"Card \d+: ", "", content)
        cards = content.strip().split("\n")
        self.cards = {
            i + 1: tuple(x.strip().split() for x in card.split(" | "))
            for i, card in enumerate(cards)
        }

    def solve_part1(self) -> int:
        total = 0
        for winning, your_numbers in self.cards.values():
            numbers = [x for x in your_numbers if x in winning]
            if numbers:
                total += 2 ** (len(numbers) - 1)
        return total

    def solve_part2(self) -> int:
        counts = {i: 1 for i in self.cards.keys()}
        total = 0
        for i, (winning, your_numbers) in self.cards.items():
            matching_numbers = [x for x in your_numbers if x in winning]
            for j in range(i + 1, i + len(matching_numbers) + 1):
                if j <= max(counts.keys()):
                    counts[j] += counts[i]
            total += counts[i]
        return total


if __name__ == "__main__":
    test_puzzle = Puzzle(test_content)
    assert test_puzzle.solve_part1() == 13
    assert test_puzzle.solve_part2() == 30

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = Puzzle(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2()}")
