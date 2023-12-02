from pathlib import Path

INPUT_FILE = Path(__file__).parent.parent / "inputs" / "day1.inp"

calibration_sum = 0

with INPUT_FILE.open("r") as f:
    lines = f.read().splitlines()
    for line in lines:
        numbers = list(filter(lambda c: c.isnumeric(), line))
        assert len(numbers) >= 1
        calibration_sum += int(numbers[0] + numbers[-1])
        
print(calibration_sum)