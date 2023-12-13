"""Day 12: Hot Springs"""

import re
from pathlib import Path

test_content = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""


def distinct_permutations(iterable):
    # More efficient alternative to `set(permutations(iterable))`
    # Taken from https://github.com/more-itertools/more-itertools/blob/10b69b34b6619876c835559312a7b5346ccfcd86/more_itertools/more.py#L649
    items = sorted(iterable)
    size = len(items)

    # Algorithm: https://w.wiki/Qai
    while True:
        # Yield the permutation we have
        yield tuple(items)

        # Find the largest index i such that A[i] < A[i + 1]
        for i in range(size - 2, -1, -1):
            if items[i] < items[i + 1]:
                break
        #  If no such index exists, this permutation is the last one
        else:
            return

        # Find the largest index j greater than j such that A[i] < A[j]
        for j in range(size - 1, i, -1):
            if items[i] < items[j]:
                break

        # Swap the value of A[i] with that of A[j], then reverse the
        # sequence from A[i + 1] to form the new permutation
        items[i], items[j] = items[j], items[i]
        items[i + 1 :] = items[: i - size : -1]  # A[i + 1:][::-1]


class Puzzle:
    def __init__(self, content: str):
        self.conditions = []
        for line in content.strip().split("\n"):
            pattern, counts = line.split()
            counts = list(map(int, counts.split(",")))
            self.conditions.append((pattern, counts))

    def solve_part1(self) -> int:
        total = 0

        for condition in self.conditions:
            pattern, counts = condition
            regex = r"^\.*"
            regex += r"\.+".join(f"#{{{count}}}" for count in counts)
            regex += r"\.*$"

            n_missing = pattern.count("?")
            n_damaged = sum(counts) - pattern.count("#")
            set_ = "#" * n_damaged + "." * (n_missing - n_damaged)

            for permutation in distinct_permutations(set_):
                x = pattern
                for char in permutation:
                    x = x.replace("?", char, 1)
                if re.match(regex, x):
                    total += 1

        return total

    def solve_part2(self) -> int:
        return 2


if __name__ == "__main__":
    test_puzzle = Puzzle(test_content)
    assert test_puzzle.solve_part1() == 21
    assert test_puzzle.solve_part2() == 2

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = Puzzle(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2()}")
