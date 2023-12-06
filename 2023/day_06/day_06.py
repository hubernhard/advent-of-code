"""Day 6: Wait For It"""

from pathlib import Path

test_content = """
Time:      7  15   30
Distance:  9  40  200
"""


class Puzzle:
    def __init__(self, content: str):
        lines = content.strip().split("\n")
        lines = [line.split(":")[1].strip() for line in lines]
        self.max_times = list(map(int, lines[0].split()))
        self.max_distances = list(map(int, lines[1].split()))

    def solve_part1(self) -> int:
        result = 1
        for max_time, max_distance in zip(self.max_times, self.max_distances):
            total = 0
            for speed in range(max_time):
                # Speed is equal to the time spent holding the button
                remaining_time = max_time - speed
                distance = speed * remaining_time
                if distance > max_distance:
                    total += 1
            result *= total

        return result

    def solve_part2(self) -> int:
        max_time = int("".join(str(i) for i in self.max_times))
        max_distance = int("".join(str(i) for i in self.max_distances))
        total = 0
        for speed in range(max_time):
            # Speed is equal to the time spent holding the button
            remaining_time = max_time - speed
            distance = speed * remaining_time
            if distance > max_distance:
                total += 1
        return total


if __name__ == "__main__":
    test_puzzle = Puzzle(test_content)
    assert test_puzzle.solve_part1() == 288
    assert test_puzzle.solve_part2() == 71503

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = Puzzle(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2()}")
