"""Day 3: Rucksack Reorganization"""

import string
from collections.abc import Iterator
from pathlib import Path

test_content = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""


class RucksackReorganizer:
    abc = string.ascii_lowercase + string.ascii_uppercase

    def __init__(self, content: str):
        self.rucksacks = content.strip().split("\n")

    def get_priority(self, item: str) -> int:
        return self.abc.index(item) + 1

    def solve_part1(self) -> int:
        total = 0
        for rucksack in self.rucksacks:
            n = len(rucksack) // 2
            a, b = set(rucksack[:n]), set(rucksack[n:])
            common_items = a.intersection(b)
            for item in common_items:
                total += self.get_priority(item)
        return total

    def groups(self) -> Iterator[list[str]]:
        for i in range(0, len(self.rucksacks), 3):
            yield self.rucksacks[i : i + 3]

    def solve_part2(self) -> int:
        total = 0
        for group in self.groups():
            common_items = set.intersection(*map(set, group))
            for item in common_items:
                total += self.get_priority(item)
        return total


if __name__ == "__main__":
    test_organizer = RucksackReorganizer(test_content)
    assert test_organizer.solve_part1() == 157
    assert test_organizer.solve_part2() == 70

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()

    organizer = RucksackReorganizer(content)
    print(f"Part 1: {organizer.solve_part1()}")
    print(f"Part 2: {organizer.solve_part2()}")
