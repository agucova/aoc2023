from pathlib import Path
import re
from itertools import batched
from bst import BinarySearchTree

INPUT_FILE = Path(__file__).parent.parent / "inputs" / "day5.inp"


def find_shortest_path(
    mappings: dict[tuple[str, str], BinarySearchTree]
) -> list[tuple[str, str]]:
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
    return path


def find_interval_gaps(main_range: range, subintervals: list[range]) -> list[range]:
    # Find the gaps subintervals in the main range which are not covered
    # by any of the given intervals
    if len(subintervals) == 0:
        return [main_range]
    sorted_subintervals = sorted(subintervals, key=lambda x: x.start)
    gaps = []
    # Initial gap
    if sorted_subintervals[0].start > main_range.start:
        gaps.append(
            range(main_range.start, min(sorted_subintervals[0].start, main_range.stop))
        )
    # Gaps between subintervals
    for i in range(len(sorted_subintervals) - 1):
        if sorted_subintervals[i].stop < sorted_subintervals[i + 1].start:
            gaps.append(
                range(
                    sorted_subintervals[i].stop,
                    min(sorted_subintervals[i + 1].start, main_range.stop),
                )
            )

    # Final gap
    if sorted_subintervals[-1].stop < main_range.stop:
        gaps.append(
            range(max(sorted_subintervals[-1].stop, main_range.start), main_range.stop)
        )

    return gaps


def map_interval(interval: range, mapping: BinarySearchTree) -> list[range]:
    # Map a single interval through a mapping
    # including identity mappings for any gaps
    mapping_result = mapping.find_maps(interval)
    identity_mappings = [
        (gap, gap)
        for gap in find_interval_gaps(interval, [m[0] for m in mapping_result])
    ]
    # Calculate the target intervals for each mapping, within the bounds of the interval
    return [target_interval for _, target_interval in identity_mappings] + [
        (
            range(
                target_interval.start + max(interval.start - source_interval.start, 0),
                target_interval.stop - max(source_interval.stop - interval.stop, 0),
            )
        )
        for source_interval, target_interval in mapping_result
    ]


def map_interval_through_path(
    interval: range,
    mappings: dict[tuple[str, str], BinarySearchTree],
    path: list[tuple[str, str]],
) -> list[range]:
    intervals = [interval]
    for source, target in path:
        print(f"Mapping {intervals} through {source} to {target}")
        intervals = [
            target_interval
            for source_interval in intervals
            for target_interval in map_interval(
                source_interval, mappings[(source, target)]
            )
        ]

    return intervals


MAP_REGEX = re.compile(r"(\w+)-to-(\w+) map:\n((?:\d+ \d+ \d+\n)+)", re.MULTILINE)


def extract_mappings(text: str) -> dict[tuple[str, str], BinarySearchTree]:
    mappings: dict[tuple[str, str], BinarySearchTree] = {}
    mapping_blocks = list(m.groups() for m in MAP_REGEX.finditer(text))

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

    return mappings


if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        seed_entries = [int(seed) for seed in f.readline().lstrip("seeds: ").split(" ")]
        seed_ranges = [
            range(start, start + length) for start, length in batched(seed_entries, 2)
        ]

        # Find each block with a mapping
        mappings = extract_mappings(f.read())

        found = False
        for path in find_shortest_path(mappings):
            print(f"Trying path {path}")
            intervals = map_interval_through_path(
                range(0, 100), mappings, find_shortest_path(mappings)
            )
            if all(seed in intervals for seed in seed_ranges):
                print(f"Found path {path}")
                found = True
                break
