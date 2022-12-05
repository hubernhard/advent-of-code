"""Day 5: Supply Stacks"""

from pathlib import Path

test_content = """
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""  # noqa: W291


class CargoCrane:
    stacks: dict[str, str]

    def __init__(self, content: str):
        stack_rows, actions = content.strip("\n").split("\n\n")
        self.initial_states = self._get_initial_states(stack_rows)
        self.actions = actions.split("\n")

    @staticmethod
    def _get_initial_states(stack_rows: str) -> dict[str, str]:
        # Reverse the input
        stack_rows = stack_rows.split("\n")
        stack_rows.reverse()
        # The contents of the crates (letters A-Z) in the different stacks are
        # always separated by 4 characters
        s = slice(1, len(stack_rows[0]), 4)
        # Create dictionary of stacks where each stack can be accessed by its
        # number
        stacks = {i: "" for i in stack_rows[0][s]}
        for row in stack_rows[1:]:
            for i, item in zip(stacks.keys(), row[s]):
                stacks[i] += item.strip()  # remove whitespace before appending
        return stacks

    def apply_actions(self, one_by_one: bool = True) -> None:
        """Move crates between stacks according to the actions in the input."""
        # Reset stacks to their initial states
        self.stacks = self.initial_states.copy()

        for action in self.actions:
            _, n, _, a, _, b = action.split(" ")
            n = int(n)
            # Remove top-n elements from stack A
            self.stacks[a], top = self.stacks[a][:-n], self.stacks[a][-n:]
            # Add new crates on top of stack B (reverse order of top crates if
            # one_by_one is True, i.e. if crane can only move one crate at a
            # time)
            self.stacks[b] += top[::-1] if one_by_one else top

    def get_top_elements(self) -> str:
        top_elements = [stack[-1] for stack in self.stacks.values()]
        return "".join(top_elements)

    def solve_part1(self) -> str:
        self.apply_actions(one_by_one=True)
        return self.get_top_elements()

    def solve_part2(self) -> str:
        self.apply_actions(one_by_one=False)
        return self.get_top_elements()


if __name__ == "__main__":
    test_crane = CargoCrane(test_content)
    assert test_crane.solve_part1() == "CMZ"
    assert test_crane.solve_part2() == "MCD"

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    crane = CargoCrane(content)
    print(f"Part 1: {crane.solve_part1()}")
    print(f"Part 2: {crane.solve_part2()}")
