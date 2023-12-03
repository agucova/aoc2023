from pathlib import Path
import regex as re

INPUT_FILE = Path(__file__).parent.parent / "inputs" / "day2.inp"
COLOR_REGEX = re.compile(r"(\d+) red|(\d+) green|(\d+) blue")

bag = (12, 13, 14)  # R, G, B


def get_bag(round_line: str) -> tuple[int, int, int]:
    """
    Returns the (R, G, B) representation
    of the bag for this round string.
    """
    matches = COLOR_REGEX.findall(round_line)
    bag = [0, 0, 0]
    for match in matches:
        for i, color in enumerate(match):
            if color:
                bag[i] = int(color)

    return (bag[0], bag[1], bag[2])


id_sum = 0
with open(INPUT_FILE) as f:
    for game_line in f.readlines():
        prefix, body = game_line.split(":")
        game_id = int(prefix.strip("Game "))
        bag_samples = (get_bag(round_line) for round_line in body.split("; "))
        if all(
            (sampled_color <= max_color)
            for sample in bag_samples
            for sampled_color, max_color in zip(sample, bag)
        ):
            id_sum += game_id


print(id_sum)
