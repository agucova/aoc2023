from pathlib import Path
import re

INPUT_FILE = Path(__file__).parent.parent / "inputs" / "day4.inp"
NUMBERS_REGEX = re.compile("\d+")

points = []
with open(INPUT_FILE) as f:
    for line in f.readlines():
        winning_line, numbers_in_card = line.split("|")
        winning_line = winning_line.split(": ")[1]
        winning_numbers = len(set(NUMBERS_REGEX.findall(winning_line)) & set(NUMBERS_REGEX.findall(numbers_in_card)))
        points.append(2**(winning_numbers - 1) if winning_numbers >= 1 else 0)

print(sum(points))

