from pathlib import Path
from collections import defaultdict
import re

INPUT_FILE = Path(__file__).parent.parent / "inputs" / "day3.inp"

SYMBOLS: dict[tuple[int, int], str | None] = defaultdict(lambda: None)  # x, y -> symbol
SYMBOL_REGEX = re.compile(r"[^.\s\d]")
NUMBERS: list[tuple[int, int, int, int]] = []  # x, y, length, number
NUMBER_REGEX = re.compile(r"\d+")

with open(INPUT_FILE) as f:
    for y, line in enumerate(f.readlines()):
        # Find symbols
        symbol_matches = list(SYMBOL_REGEX.finditer(line))
        for symbol_match in symbol_matches:
            x, symbol = symbol_match.start(), symbol_match.group(0)
            SYMBOLS[(x, y)] = symbol

        # Find numbers
        number_matches = list(NUMBER_REGEX.finditer(line))
        for number_match in number_matches:
            x = number_match.start()
            length = number_match.end() - x
            number = int(number_match.group(0))
            NUMBERS.append((x, y, length, number))


PART_NUMBERS = []
for x, y, length, number in NUMBERS:
    # Find positions around number, including diagonally
    boundary = (
        (x + i + dx, y + dy)
        for dx in (-1, 0, 1)
        for dy in (-1, 0, 1)
        for i in range(length)
    )
    # Find if there's a symbol in the boundary
    for pos in boundary:
        if SYMBOLS[pos] is not None:
            PART_NUMBERS.append(number)
            break

print(sum(PART_NUMBERS))
