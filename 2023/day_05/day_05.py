"""Day 5: You Give A Seed A Fertilizer"""

import math
from pathlib import Path

test_content = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""


class Puzzle:
    def __init__(self, content: str):
        content = content.strip().split("\n\n")

        seeds = content[0].replace("seeds: ", "")
        self.seeds = list(map(int, seeds.split()))

        mappings = [mapping.split(":\n")[1] for mapping in content[1:]]
        self.mappings = [self._parse_map(mapping) for mapping in mappings]

    def _parse_map(self, mapping_input: str) -> dict[range, range]:
        mapping = {}
        for line in mapping_input.strip().split("\n"):
            dest_start, source_start, length = map(int, line.split())
            dest_range = range(dest_start, dest_start + length)
            source_range = range(source_start, source_start + length)
            mapping[source_range] = dest_range
        return mapping

    def _get_location(self, seed: int) -> tuple[int, int]:
        item = seed
        next_change = math.inf
        for mapping in self.mappings:
            found_in_range = False

            for source, dest in mapping.items():
                if item in source:
                    next_change = min(next_change, source.stop - item)
                    item = dest[source.index(item)]
                    found_in_range = True
                    break

            if not found_in_range:
                closest = math.inf
                for source in mapping.keys():
                    if source.start > item:
                        closest = min(closest, source.start - item)
                next_change = min(next_change, closest)

        return item, next_change

    def solve_part1(self) -> int:
        locations = [self._get_location(seed)[0] for seed in self.seeds]
        return min(locations)

    def solve_part2(self) -> int:
        seed_ranges = [
            range(a, a + b)
            for a, b in zip(self.seeds[0::2], self.seeds[1::2], strict=False)
        ]
        locations = []

        for seed_range in seed_ranges:
            seed = seed_range.start
            while seed <= seed_range.stop:
                location, next_change = self._get_location(seed)
                locations.append(location)
                seed += next_change

        return min(locations)


if __name__ == "__main__":
    test_puzzle = Puzzle(test_content)
    assert test_puzzle.solve_part1() == 35
    assert test_puzzle.solve_part2() == 46

    file = Path(__file__).parent / "input.txt"
    content = file.read_text()
    puzzle = Puzzle(content)
    print(f"Part 1: {puzzle.solve_part1()}")
    print(f"Part 2: {puzzle.solve_part2()}")
