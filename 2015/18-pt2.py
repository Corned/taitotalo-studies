import math
import time

"""conway's game of life"""

WIDTH = 100
HEIGHT = 100
STEPS = 100

STR_ON = "#"
STR_OFF = " "

PERMANENTLY_ON = [(0, 0), (0, WIDTH - 1), (HEIGHT - 1, 0), (WIDTH - 1, HEIGHT - 1)]


def parse(lines: list[str]) -> list[int]:
    data = []
    for line in lines:
        for char in line.strip():
            data.append(1 if char == "#" else -1)

    return data


def iterate(old_state: list[int]) -> list[int]:
    """
    A light which is on stays on when 2 or 3 neighbors are on, and turns off otherwise.
    A light which is off turns on if exactly 3 neighbors are on, and stays off otherwise.
    """
    new_state = [*old_state]

    for index, value in enumerate(old_state):
        x = index % WIDTH
        y = math.floor(index / WIDTH)

        if (x, y) in PERMANENTLY_ON:
            continue

        neighbors_on = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                new_x = x + dx
                new_y = y + dy

                if not (0 <= new_x < WIDTH):
                    continue

                if not (0 <= new_y < HEIGHT):
                    continue

                neighbor_state = old_state[new_x + new_y * WIDTH]
                neighbor_is_permanently_on = (new_x, new_y) in PERMANENTLY_ON

                if neighbor_state == 1 or neighbor_is_permanently_on:
                    neighbors_on += 1

        if value == 1:
            if neighbors_on == 2 or neighbors_on == 3:
                new_state[index] = 1
            else:
                new_state[index] = -1

        if value == -1:
            if neighbors_on == 3:
                new_state[index] = 1

    return new_state


def print_state(state: list[int]):
    state_string = ""
    for index, value in enumerate(state):
        x = index % WIDTH
        y = math.floor(index / WIDTH)
        if (x, y) in PERMANENTLY_ON:
            state_string += STR_ON
        else:
            state_string += STR_ON if value == 1 else STR_OFF
        if index % WIDTH == WIDTH - 1:
            state_string += "\n"

    print(state_string.strip())


with open("input/18.txt", "r") as file:
    lines = file.readlines()
    state = parse(lines)

    for x, y in PERMANENTLY_ON:
        state[x + y * WIDTH] = 1

    print_state(state)

    for iteration in range(STEPS):
        state = iterate(state)
        print(f"\n\niter {iteration}")
        print_state(state)
        # time.sleep(0.05)

    print(f"Answer: {state.count(1)}")


"""
Initial state:
.#.#.#
...##.
#....#
..#...
#.#..#
####..

After 1 step:
..##..
..##.#
...##.
......
#.....
#.##..
"""
