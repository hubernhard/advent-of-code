"""Day 8: Treetop Tree House"""

from pathlib import Path
from typing import Iterator

test_content = """
30373
25512
65332
33549
35390
"""


class TreeFinder:
    def __init__(self, content: str):
        self.array = [[*line] for line in content.strip().split("\n")]
        self.n_rows = len(self.array[0])
        self.n_cols = len(self.array)

    def interior(self) -> Iterator[tuple[str, int, int]]:
        """Iterate over the interior of the array."""
        for i in range(1, self.n_rows - 1):
            for j in range(1, self.n_cols - 1):
                yield self.array[i][j], i, j

    def get_neighbors_list(self, i: int, j: int) -> list[list[str]]:
        """Get lists of neighbors in each direction (ordered by distance)."""
        neighbors = [
            self.array[i][:j][::-1],  # left (reversed order)
            self.array[i][j + 1 :],  # right
            [x[j] for x in self.array[:i]][::-1],  # top (reversed order)
            [x[j] for x in self.array[i + 1 :]],  # bottom
        ]
        return neighbors

    def solve_part1(self) -> int:
        # Count trees around the edge of the grid
        visible = 2 * (self.n_rows + self.n_cols - 2)

        for x, i, j in self.interior():
            neighbors_list = self.get_neighbors_list(i, j)
            # Check if tree is visible from any of the directions
            if any(max(neighbors) < x for neighbors in neighbors_list):
                visible += 1

        return visible

    def solve_part2(self) -> int:
        max_score = 0

        for x, i, j in self.interior():
            neighbors_list = self.get_neighbors_list(i, j)
            score = 1

            # Iterate over all directions
            for neighbors in neighbors_list:
                # Compute viewing distance
                n_trees = 0
                for tree in neighbors:
                    n_trees += 1
                    if tree >= x:
                        break
                # Update score
                score *= n_trees

            if score > max_score:
                max_score = score

        return max_score


if __name__ == "__main__":
    test_tree_finder = TreeFinder(test_content)
    assert test_tree_finder.solve_part1() == 21
    assert test_tree_finder.solve_part2() == 8

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    tree_finder = TreeFinder(content)
    print(f"Part 1: {tree_finder.solve_part1()}")
    print(f"Part 2: {tree_finder.solve_part2()}")
