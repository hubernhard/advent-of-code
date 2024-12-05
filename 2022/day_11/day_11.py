"""Day 11: Monkey in the Middle"""

import math
import re
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Monkey:
    items: list[int]
    operation: Callable[[int], int]
    mod: int
    true: int
    false: int
    counter: int = 0


class MonkeyInTheMiddle:
    def __init__(self, content: str):
        self.content = content.strip().split("\n\n")

    def parse_input(self) -> list[Monkey]:
        monkeys = []
        for x in self.content:
            items = re.search("Starting items: (.*?)\n", x).group(1)
            operation = re.search("Operation: new = (.*?)\n", x).group(1)
            mod = re.search("Test: divisible by (\\d+)\n", x).group(1)
            true = re.search("If true: throw to monkey (\\d+)\n", x).group(1)
            false = re.search("If false: throw to monkey (\\d+)$", x).group(1)

            monkey = Monkey(
                # Append a comma to items to make sure that items is always a
                # tuple after running eval()
                items=list(eval(items + ",")),
                # Convert operation to lambda
                operation=eval(f"lambda old: {operation}"),
                mod=int(mod),
                true=int(true),
                false=int(false),
            )
            monkeys.append(monkey)

        return monkeys

    def play(self, n_rounds: int, relief_factor: int) -> int:
        monkeys = self.parse_input()
        mod_lcm = math.lcm(*(monkey.mod for monkey in monkeys))

        for _ in range(n_rounds):
            for monkey in monkeys:
                for item in monkey.items:
                    item = (monkey.operation(item) // relief_factor) % mod_lcm
                    i = monkey.true if item % monkey.mod == 0 else monkey.false
                    monkeys[i].items.append(item)
                    monkey.counter += 1
                monkey.items = []

        counts = sorted(monkey.counter for monkey in monkeys)
        return counts[-1] * counts[-2]

    def solve_part1(self) -> int:
        return self.play(n_rounds=20, relief_factor=3)

    def solve_part2(self) -> int:
        return self.play(n_rounds=10_000, relief_factor=1)


if __name__ == "__main__":
    file = Path(__file__).parent / "example.txt"
    test_content = file.read_text()
    test_game = MonkeyInTheMiddle(test_content)
    assert test_game.solve_part1() == 10_605
    assert test_game.solve_part2() == 2_713_310_158

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    game = MonkeyInTheMiddle(content)
    print(f"Part 1: {game.solve_part1()}")
    print(f"Part 2: {game.solve_part2()}")
