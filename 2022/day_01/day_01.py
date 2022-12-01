"""Day 1: Calorie Counting"""

from pathlib import Path


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


if __name__ == "__main__":
    file = Path(__file__).parent / "input.txt"
    content = file.read_text()

    counter = CalorieCounter(content)
    print(counter.top())
    print(counter.top(3))
