import sys
from pathlib import Path

folder = Path(__file__).parent


def part1():
    with open(folder / "input.txt", "r") as file:
        text = file.read()

    floor = text.count("(") - text.count(")")
    return floor


def part2():
    with open(folder / "input.txt", "r") as file:
        text = file.read().strip()

    floor = 0
    for index, char in enumerate(text):
        floor += 1 if char == "(" else -1

        if floor == -1:
            return index + 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python day_01.py <part>")
        sys.exit(1)

    try:
        part = int(sys.argv[1])
    except ValueError:
        print(f"Invalid part value '{sys.argv[1]}', should be an Integer.")
        sys.exit(1)

    answer = None
    if part == 1:
        answer = part1()
    elif part == 2:
        answer = part2()
    else:
        print(f"Invalid part {part}, should be 1 or 2.")
        sys.exit(1)

    print(f"Answer: {answer}")
