"""Day 25: Full of Hot Air"""

from pathlib import Path

test_content = """
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
"""


class SNAFUConverter:
    def __init__(self, content: str):
        self.snafu_numbers = content.strip().split("\n")

    @staticmethod
    def snafu_to_decimal(snafu: str) -> int:
        decimal = 0
        for i, x in enumerate(reversed(snafu)):
            x = x.replace("-", "-1").replace("=", "-2")
            decimal += 5**i * int(x)
        return decimal

    @staticmethod
    def decimal_to_snafu(decimal: int) -> str:
        snafu = ""
        x = decimal
        while x > 0:
            remainder = x % 5
            snafu += str(remainder).replace("3", "=").replace("4", "-")
            x = x // 5 + (1 if remainder >= 3 else 0)
        return snafu[::-1]

    def solve_part1(self) -> str:
        s = sum(self.snafu_to_decimal(snafu) for snafu in self.snafu_numbers)
        return self.decimal_to_snafu(s)


if __name__ == "__main__":
    test_puzzle = SNAFUConverter(test_content)
    assert test_puzzle.solve_part1() == "2=-1=0"

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = SNAFUConverter(content)
    print(f"Part 1: {puzzle.solve_part1()}")
