from pathlib import Path
from bst import BinarySearchTree
import re

INPUT_FILE = Path(__file__).parent.parent / "inputs" / "day5.inp"

MAP_REGEX = re.compile(r"(\w+)-to-(\w+) map:\n((?:\d+ \d+ \d+\n)+)", re.MULTILINE)
with open(INPUT_FILE) as f:
    seeds = [int(seed) for seed in f.readline().lstrip("seeds: ").split(" ")]
    mappings: dict[tuple[str, str], BinarySearchTree] = {}

    # Find each block with a mapping
    mapping_blocks = list(m.groups() for m in MAP_REGEX.finditer(f.read()))
    for match in mapping_blocks:
        source, target, mapping = match
        intervals = [
            (
                range(int(source_start), int(source_start) + int(range_length)),
                range(int(dest_start), int(dest_start) + int(range_length)),
            )
            for dest_start, source_start, range_length in (
                line.split(" ") for line in mapping.split("\n") if line
            )
        ]
        mapping = BinarySearchTree()
        for source_interval, target_interval in intervals:
            mapping.insert(source_interval, target_interval)

        mappings[(source, target)] = mapping

    # Find the shortest path through the mappings
    # that gets us from a seed number to a location number
    available_mappings = set(mappings.keys())
    initial_mapping = [m for m in available_mappings if m[1] == "location"][0]
    available_mappings.remove(initial_mapping)
    path = [initial_mapping]
    while available_mappings:
        for mapping in available_mappings:
            if mapping[0] == path[-1][1]:
                path.append(mapping)
                available_mappings.remove(mapping)
                break
            elif mapping[1] == path[0][0]:
                path.insert(0, mapping)
                available_mappings.remove(mapping)
                break
        else:
            raise ValueError("No path found through the mappings")

    # Apply the mappings to the seeds iteratively
    # to get the locations
    for source, target in path:
        mapping = mappings[(source, target)]
        seeds = [mapping.map(seed) for seed in seeds]

    print(min(seeds))
