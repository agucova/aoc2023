from pathlib import Path
from collections import defaultdict
import re

INPUT_FILE = Path(__file__).parent.parent / "inputs" / "day3.inp"

ASTERISKS: list[tuple[int, int]] = []  # [(x, y)]
ASTERISK_REGEX = re.compile(r"\*")

NUMBERS: list[int] = []
NUMBER_REFS: dict[tuple[int, int], int] = defaultdict(lambda: None)  # x, y -> id
NUMBER_REGEX = re.compile(r"\d+")

with open(INPUT_FILE) as f:
    for y, line in enumerate(f.readlines()):
        # Find symbols
        asterisk_matches = list(ASTERISK_REGEX.finditer(line))
        for asterisk_match in asterisk_matches:
            boundary_x = asterisk_match.start()
            ASTERISKS.append((boundary_x, y))

        # Find numbers
        number_matches = list(NUMBER_REGEX.finditer(line))
        for number_match in number_matches:
            # Save the number so it can be looked up later by index
            NUMBERS.append(int(number_match.group(0)))
            for offset_x in range(number_match.start(), number_match.end()):
                # Store the ID of the number in every coordinate of its span
                NUMBER_REFS[(offset_x, y)] = len(NUMBERS) - 1


GEAR_RATIOS = []

for x, y in ASTERISKS:
    # Find positions around the asterisk, including diagonally
    boundary = (
        (x + dx, y + dy)
        for dx in (-1, 0, 1)
        for dy in (-1, 0, 1)
        if not (dx == dy == 0)
    )
    # Find if there's a number in its boundary
    part_ids = set()
    for bx, by in boundary:
        if (bx, by) in NUMBER_REFS:
            part_ids.add(NUMBER_REFS[(bx, by)])

    if len(part_ids) == 2:
        # Gear found, store its gear ratio
        part_1, part_2 = [NUMBERS[part_id] for part_id in part_ids]
        GEAR_RATIOS.append(part_1 * part_2)

print(sum(GEAR_RATIOS))
