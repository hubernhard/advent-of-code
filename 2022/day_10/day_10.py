"""Day 10: Cathode-Ray Tube"""

from pathlib import Path

test_image = """
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
"""


class CathodeRayTube:
    def __init__(self, content: str):
        self.instructions = content.strip().split("\n")
        self.x_values = [1]  # initial value for X
        self._run_instructions()
        self._screen_size = (40, 6)

    def _run_instructions(self) -> None:
        """Run all instructions and collect X values for each cycle."""
        for instruction in self.instructions:
            x_old = self.x_values[-1]
            self.x_values.append(x_old)
            if instruction.startswith("addx"):
                _, val = instruction.split()
                self.x_values.append(x_old + int(val))

    def render_image(self) -> str:
        image = ""
        width, height = self._screen_size
        for cycle, x in enumerate(self.x_values[: width * height]):
            image += "#" if cycle % width in (x - 1, x, x + 1) else "."
            if (cycle + 1) % width == 0:
                image += "\n"
        return image

    def solve_part1(self) -> int:
        cycles = range(20, 221, 40)
        x_values = [self.x_values[i - 1] for i in cycles]
        return sum(cycle * x for cycle, x in zip(cycles, x_values))

    def solve_part2(self) -> str:
        return self.render_image()


if __name__ == "__main__":
    file = Path(__file__).parent / "example.txt"
    test_content = file.read_text()
    test_crt = CathodeRayTube(test_content)
    assert test_crt.solve_part1() == 13140
    assert test_crt.solve_part2().strip() == test_image.strip()

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    crt = CathodeRayTube(content)
    print(f"Part 1: {crt.solve_part1()}")
    print(f"Part 2:\n{crt.solve_part2()}")
