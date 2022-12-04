"""Day 4: Camp Cleanup"""

from pathlib import Path

test_content = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""


class CampCleaner:
    def __init__(self, content: str):
        pairs = content.strip().split("\n")
        self.pairs = [self._process_pair(pair) for pair in pairs]

    @staticmethod
    def _process_pair(pair: str) -> tuple[set[int], set[int]]:
        pair = [x.split("-") for x in pair.split(",")]
        a, b = [set(range(int(x[0]), int(x[1]) + 1)) for x in pair]
        return a, b

    def solve_part1(self) -> int:
        """Count number of pairs, where one range is fully contained in the
        other."""
        total = 0
        for a, b in self.pairs:
            if a.issubset(b) or a.issuperset(b):
                total += 1
        return total

    def solve_part2(self) -> int:
        """Count number of pairs that have overlapping ranges."""
        total = 0
        for a, b in self.pairs:
            if not a.isdisjoint(b):
                total += 1
        return total


if __name__ == "__main__":
    test_cleaner = CampCleaner(test_content)
    assert test_cleaner.solve_part1() == 2
    assert test_cleaner.solve_part2() == 4

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    cleaner = CampCleaner(content)
    print(f"Part 1: {cleaner.solve_part1()}")
    print(f"Part 2: {cleaner.solve_part2()}")
