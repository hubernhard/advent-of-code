"""Day 2: Rock Paper Scissors"""

from pathlib import Path

test_content = """
A Y
B X
C Z
"""


class RockPaperScissors:
    # Key wins against value (A=Rock, B=Paper, C=Scissors)
    win = {"A": "C", "C": "B", "B": "A"}
    # Base points awarded to Player 2
    base_points = {"A": 1, "B": 2, "C": 3}

    def __init__(self, play: str):
        self.rounds = [x.split() for x in play.strip().split("\n")]

    def get_points(self, p1: str, p2: str) -> int:
        total = self.base_points[p2]
        if p1 == p2:
            total += 3
        elif p1 == self.win[p2]:
            total += 6
        return total

    def solve_part1(self) -> int:
        total = 0
        for p1, p2 in self.rounds:
            p2 = {"X": "A", "Y": "B", "Z": "C"}[p2]
            total += self.get_points(p1, p2)
        return total

    def solve_part2(self) -> int:
        lose = {val: key for key, val in self.win.items()}
        total = 0

        for p1, p2 in self.rounds:
            if p2 == "X":
                p2 = self.win[p1]
            elif p2 == "Y":
                p2 = p1
            else:
                p2 = lose[p1]
            total += self.get_points(p1, p2)

        return total


if __name__ == "__main__":
    test_game = RockPaperScissors(test_content)
    assert test_game.solve_part1() == 15
    assert test_game.solve_part2() == 12

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    game = RockPaperScissors(content)
    print(f"Part 1: {game.solve_part1()}")
    print(f"Part 2: {game.solve_part2()}")
