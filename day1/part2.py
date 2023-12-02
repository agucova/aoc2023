from pathlib import Path
import regex as re

INPUT_FILE = Path(__file__).parent.parent / "inputs" / "day1.inp"
DIGIT_MAP = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
# Regex for matching either literal digits or spelled-out digits
DIGIT_REGEX = re.compile(r"(\d)|(" + "|".join(DIGIT_MAP) + r")")

calibration_sum = 0


def handle_digit(match: tuple[str, str]) -> int:
    if match[0]:  # First capture group (numeric digit)
        return int(match[0])
    else:  # Second capture group (spelled-out digit)
        return DIGIT_MAP.index(match[1]) + 1


with INPUT_FILE.open("r") as f:
    lines = f.read().splitlines()
    for line in lines:
        numeric_matches = DIGIT_REGEX.findall(line, overlapped=True)
        assert len(numeric_matches) >= 1
        x, y = handle_digit(numeric_matches[0]), handle_digit(numeric_matches[-1])
        calibration_sum += 10 * x + y


print(calibration_sum)
