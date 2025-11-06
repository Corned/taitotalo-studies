import re

LITER_TARGET = 150


def parse(lines):
    data = []
    for line in lines:
        data.append(int(line.strip()))
    return list(sorted(data))


def iterate(
    remaining_containers: list[int] = [],
    current_containers: list[int] = [],
    solution_data: dict[int, int] = {},
):
    if sum(current_containers) > LITER_TARGET:
        return 0, solution_data

    if sum(current_containers) == LITER_TARGET:
        key = len(current_containers)
        if not solution_data.get(key):
            solution_data[key] = 0

        solution_data[key] += 1
        return 1, solution_data

    counter = 0
    while remaining_containers:
        container = remaining_containers.pop()

        new_counter, solution_data = iterate(
            [*remaining_containers], [container, *current_containers], solution_data
        )

        counter += new_counter

    return counter, solution_data


with open("input/17.txt", "r") as file:
    lines = file.readlines()
    containers = parse(lines)

    solution, solution_data = iterate(containers)

    print("Solution:", solution, solution_data)
