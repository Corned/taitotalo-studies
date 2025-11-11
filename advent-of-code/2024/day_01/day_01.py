from pathlib import Path


def part1(data):
    safe_reports = 0

    for datum in data:
        should_increase = datum[0] < datum[1]
        unsafe_report = False
        for index in range(len(datum) - 1):
            a, b = datum[index], datum[index + 1]
            diff = abs(a - b)
            is_increasing = a < b

            if not (should_increase == is_increasing):
                unsafe_report = True
                break

            if diff > 3 or diff == 0:
                unsafe_report = True
                break

        if not unsafe_report:
            safe_reports += 1

    return safe_reports


def part2(data):
    safe_reports = 0

    for datum in data:
        for index_ignore in range(0, len(datum)):
            new_datum = [*datum[:index_ignore], *datum[index_ignore + 1 :]]

            is_safe = not not part1([new_datum])
            if is_safe:
                safe_reports += 1
                break

    return safe_reports


BASEDIR = Path(__file__).parent
with open(BASEDIR / "input.txt", "r") as file:
    lines = [line.strip().split(" ") for line in file.readlines()]
    data = [tuple(map(int, line)) for line in lines]


if __name__ == "__main__":
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
