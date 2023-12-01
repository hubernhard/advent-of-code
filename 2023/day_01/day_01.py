"""Day 1: Trebuchet?!"""

import re
from pathlib import Path

test_content = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

test_content2 = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""


class Puzzle:
    def __init__(self, content: str):
        self.content = content.strip().split("\n")

    def solve_part1(self) -> int:
        total = 0
        for line in self.content:
            digits = re.findall(r"\d", line)
            total += int(digits[0] + digits[-1])
        return total

    def solve_part2(self) -> int:
        numbers = [
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
        ]

        def _index(number: str) -> int:
            return numbers.index(number) + 1

        pattern1 = "^[a-z]*?(" + "|".join(numbers) + ")"
        # Here *? does not work, as we have an or-condition and would need to
        # search the string right-to-left. So we gradually increase the number
        # of letters allowed on the right side.
        pattern2 = "(" + "|".join(numbers) + ")[a-z]{,%d}$"
        total = 0

        for line in self.content:
            digits = re.findall(r"\d", line)

            start = re.findall(pattern1, line)
            # We need to find the rightmost "text-number"
            for n in range(len(line)):
                end = re.findall(pattern2 % n, line)
                if end:
                    break

            n1 = _index(start[0]) if start else digits[0]
            n2 = _index(end[0]) if end else digits[-1]
            total += int(f"{n1}{n2}")

        return total


if __name__ == "__main__":
    test_puzzle = Puzzle(test_content)
    assert test_puzzle.solve_part1() == 142
    test_puzzle = Puzzle(test_content2)
    assert test_puzzle.solve_part2() == 281

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = Puzzle(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2()}")
