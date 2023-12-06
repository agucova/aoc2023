from pathlib import Path
import re

INPUT_FILE = Path(__file__).parent.parent / "inputs" / "day4.inp"
NUMBERS_REGEX = re.compile("\d+")

with open(INPUT_FILE) as f:
    lines = f.readlines()
    n_cards = int(NUMBERS_REGEX.findall(lines[-1].split(":")[0])[0])
    card_counts = [1 for i in range(0, n_cards)]
    for i, line in enumerate(lines):
        if not line.strip():
            continue

        winning_line, numbers_in_card = line.split("|")
        winning_line = winning_line.split(": ")[1]
        winning_numbers = len(
            set(NUMBERS_REGEX.findall(winning_line))
            & set(NUMBERS_REGEX.findall(numbers_in_card))
        )
        for i_copied_card in range(i + 1, i + 1 + winning_numbers):
            card_counts[i_copied_card] += card_counts[i]


print(sum(card_counts))
