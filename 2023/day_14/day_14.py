"""Day 14: Parabolic Reflector Dish"""

from pathlib import Path

test_content = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

StringTuple = tuple[str, ...]


def transpose(x: StringTuple) -> StringTuple:
    return tuple("".join(line[i] for line in x) for i in range(len(x[0])))


def flip(x: StringTuple) -> StringTuple:
    return tuple(line[::-1] for line in x)


def move(x: StringTuple) -> StringTuple:
    lines = []
    for line in x:
        old_line = ""
        while line != old_line:
            old_line = line
            line = line.replace(".O", "O.")
        lines.append(line)
    return tuple(lines)


def cycle(rows: StringTuple) -> StringTuple:
    # Tilt north
    cols = transpose(rows)
    cols = move(cols)
    # Tilt west
    rows = transpose(cols)
    rows = move(rows)
    # Tilt south
    cols = flip(transpose(rows))
    cols = flip(move(cols))
    # Tilt east
    rows = flip(transpose(cols))
    rows = flip(move(rows))
    return rows


def get_load(cols: StringTuple) -> int:
    total = 0
    for col in cols:
        count = 0
        for x in col[::-1]:
            count += 1
            if x == "O":
                total += count
    return total


class Puzzle:
    def __init__(self, content: str):
        self.rows = tuple(content.strip().split("\n"))

    def solve_part1(self) -> int:
        cols = transpose(self.rows)
        cols = move(cols)
        return get_load(cols)

    def solve_part2(self) -> int:
        n_cycles = 1_000_000_000
        rows = self.rows
        seen = {}
        i = 0

        while True:
            i += 1
            rows = cycle(rows)
            if rows in seen:
                start = seen[rows]
                diff = i - start
                n_missing = (n_cycles - start) % diff
                break
            seen[rows] = i

        for _ in range(n_missing):
            rows = cycle(rows)

        return get_load(transpose(rows))


if __name__ == "__main__":
    test_puzzle = Puzzle(test_content)
    assert test_puzzle.solve_part1() == 136
    assert test_puzzle.solve_part2() == 64

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = Puzzle(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2()}")
