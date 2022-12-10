"""Day 1: Calorie Counting"""

from pathlib import Path

test_content = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""


class CalorieCounter:
    def __init__(self, calories: str):
        # Remove whitespace
        calories = calories.strip()
        # Split data and convert strings to integer
        self.elves = [x.split("\n") for x in calories.split("\n\n")]
        self.elves = [[int(x) for x in elf] for elf in self.elves]
        # Compute sum for each elf
        self.sums = [sum(x) for x in self.elves]

    def top(self, n: int = 1) -> int:
        """Return the sum of the top n calorie counts across all elves."""
        return sum(sorted(self.sums)[-n:])

    def solve_part1(self) -> int:
        return self.top(1)

    def solve_part2(self) -> int:
        return self.top(3)


if __name__ == "__main__":
    test_counter = CalorieCounter(test_content)
    assert test_counter.solve_part1() == 24000
    assert test_counter.solve_part2() == 45000

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    counter = CalorieCounter(content)
    print(f"Part 1: {counter.solve_part1()}")
    print(f"Part 2: {counter.solve_part2()}")
