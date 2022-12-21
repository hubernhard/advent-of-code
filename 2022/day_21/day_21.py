"""Day 21: Monkey Math"""

import operator
import re
from pathlib import Path
from typing import Callable, NamedTuple

test_content = """
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""


class Operation(NamedTuple):
    a: str
    b: str
    op: Callable[[int, int], int | float]

    def apply(self, results: dict[str, int]) -> int | float | None:
        a = results.get(self.a, None)
        b = results.get(self.b, None)
        if a is None or b is None:
            return None
        else:
            return self.op(a, b)


class RootFinder:
    results: dict[str, int]
    operations: dict[str, Operation]

    def __init__(self, content: str):
        self.content = content.strip().split("\n")

    def _parse_input(self, humn: int | None = None) -> None:
        self.results = {}
        self.operations = {}
        for row in self.content:
            key, val = row.split(": ")
            if re.match(r"\d+", val):
                val = int(val) if humn is None or key != "humn" else humn
                self.results[key] = val
            else:
                a, op_, b = val.split(" ")
                if humn is not None and key == "root":
                    op = operator.sub  # Compute a - b
                else:
                    match op_:
                        case "+":
                            op = operator.add
                        case "-":
                            op = operator.sub
                        case "*":
                            op = operator.mul
                        case "/":
                            op = operator.truediv
                self.operations[key] = Operation(a, b, op)

    def root(self, humn: int | None = None) -> int | float:
        self._parse_input(humn=humn)
        while self.results.get("root", None) is None:
            for key, op in self.operations.copy().items():
                result = op.apply(self.results)
                if result is not None:
                    self.operations.pop(key)
                    self.results[key] = result
        return self.results["root"]

    @staticmethod
    def sign(x: int | float) -> int:
        return 1 if x >= 0 else -1

    def solve_part1(self) -> int:
        return int(self.root())

    def solve_part2(self) -> int:
        # We want to find the point humn, where root(humn) == 0.
        # To do that, we are going to apply the bisection method.

        # 1) Find feasible lower and upper limits:
        lower, upper = 1, 10  # initial guesses
        f_lower, f_upper = self.root(lower), self.root(upper)
        # Find upper value with sign(root(upper)) != sign(root(lower))
        while self.sign(f_lower) == self.sign(f_upper):
            upper *= 10
            f_upper = self.root(upper)

        # 2) Bisection
        while True:
            center = (lower + upper) // 2
            f_center = self.root(center)
            if abs(f_center) < 1e-6:
                # Root was found
                humn = center
                break
            # Update limits
            if self.sign(f_center) == self.sign(self.root(lower)):
                lower = center
            else:
                upper = center

        return humn


if __name__ == "__main__":
    test_puzzle = RootFinder(test_content)
    assert test_puzzle.solve_part1() == 152
    assert test_puzzle.solve_part2() == 301

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = RootFinder(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2()}")
