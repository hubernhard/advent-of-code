"""Day 6: Tuning Trouble"""

from pathlib import Path


class SignalTuner:
    def __init__(self, content: str):
        self.datastream = content.strip()

    def find_marker(self, n_characters: int = 4) -> tuple[int, str]:
        """Find first unique sequence of length n_characters in datastream."""
        for idx in range(n_characters, len(self.datastream)):
            marker = self.datastream[idx - n_characters : idx]
            if len(set(marker)) == n_characters:
                return idx, marker

    def solve_part1(self) -> int:
        idx, _ = self.find_marker()
        return idx

    def solve_part2(self) -> int:
        idx, _ = self.find_marker(n_characters=14)
        return idx


if __name__ == "__main__":
    assert SignalTuner("mjqjpqmgbljsphdztnvjfqwrcgsmlb").find_marker() == (
        7,
        "jpqm",
    )

    assert SignalTuner("bvwbjplbgvbhsrlpgdmjqwftvncz").solve_part1() == 5
    assert SignalTuner("nppdvjthqldpwncqszvftbrmjlhg").solve_part1() == 6
    assert SignalTuner("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg").solve_part1() == 10
    assert SignalTuner("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw").solve_part1() == 11

    assert SignalTuner("mjqjpqmgbljsphdztnvjfqwrcgsmlb").solve_part2() == 19
    assert SignalTuner("bvwbjplbgvbhsrlpgdmjqwftvncz").solve_part2() == 23
    assert SignalTuner("nppdvjthqldpwncqszvftbrmjlhg").solve_part2() == 23
    assert SignalTuner("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg").solve_part2() == 29
    assert SignalTuner("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw").solve_part2() == 26

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    tuner = SignalTuner(content)
    print(f"Part 1: {tuner.solve_part1()}")
    print(f"Part 2: {tuner.solve_part2()}")
