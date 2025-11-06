import re

LITER_TARGET = 150


def parse(lines):
    data = []
    for line in lines:
        data.append(int(line.strip()))
    return list(sorted(data))


def iterate(remaining_containers: list[int] = [], current_containers: list[int] = []):
    if sum(current_containers) > LITER_TARGET:
        return 0

    if sum(current_containers) == LITER_TARGET:
        return 1

    counter = 0
    while remaining_containers:
        container = remaining_containers.pop()

        counter += iterate([*remaining_containers], [container, *current_containers])

    return counter


with open("input/17.txt", "r") as file:
    lines = file.readlines()
    containers = parse(lines)

    solution = iterate(containers)

    print("Solution:", solution)
