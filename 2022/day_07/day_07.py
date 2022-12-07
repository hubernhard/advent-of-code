"""Day 7: No Space Left On Device"""

from pathlib import Path

test_content = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""


class FileNavigator:
    def __init__(self, content: str):
        self.terminal_history = content.strip().split("\n")
        self.dirs = self._get_dirs_and_sizes()

    def _get_dirs_and_sizes(self) -> dict[tuple[str, ...], int]:
        dirs = {}
        current_dir = ()

        for element in self.terminal_history:
            parts = element.split(" ")
            if element.startswith("$ cd"):
                if parts[2] == "..":
                    # Go up one level
                    current_dir = current_dir[:-1]
                else:
                    # Go down one level
                    current_dir += (parts[2],)
                # Initialize size of current dir (if it was not set already)
                dirs.setdefault(current_dir, 0)
            elif element.startswith(("$ ls", "dir")):
                continue
            else:
                # Element must be a file. Add file size to the current dir and
                # all dirs containing it.
                file_size = int(parts[0])
                for i in range(1, len(current_dir) + 1):
                    dirs[current_dir[:i]] += file_size

        return dirs

    def solve_part1(self) -> int:
        return sum(size for size in self.dirs.values() if size <= 100_000)

    def solve_part2(self) -> int:
        total_space = 70_000_000
        required_space = 30_000_000
        unused_space = total_space - self.dirs[("/",)]
        min_size = required_space - unused_space
        return min(size for size in self.dirs.values() if size >= min_size)


if __name__ == "__main__":
    test_navigator = FileNavigator(test_content)
    assert test_navigator.solve_part1() == 95_437
    assert test_navigator.solve_part2() == 24_933_642

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    navigator = FileNavigator(content)
    print(f"Part 1: {navigator.solve_part1()}")
    print(f"Part 2: {navigator.solve_part2()}")
