import re


def set_(grid, x, y, value):
    if not grid.get(x):
        grid[x] = {}

    if not grid.get(x).get(y):
        grid[x][y] = 0

    if value is None:
        grid[x][y] = 1 if grid[x][y] == 0 else 0
    else:
        grid[x][y] = value


with open("./input/06.txt", "r") as file:
    directions = file.readlines()
    grid = {}
    lights_on = 0

    for line in directions:
        match = re.match(r"^(\D*) (\d+),(\d+) \D* (\d+),(\d+)$", line.strip())
        if match:
            cmd = match.group(1)
            x1 = int(match.group(2))
            y1 = int(match.group(3))
            x2 = int(match.group(4))
            y2 = int(match.group(5))

            # print(f'cmd="{cmd}" x1={x1} y1={y1} x2={x2} y2={y2}')

            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    if cmd == "turn on":
                        set_(grid, x, y, 1)
                    elif cmd == "turn off":
                        set_(grid, x, y, 0)
                    elif cmd == "toggle":
                        set_(grid, x, y, None)

    count = 0
    for x in range(1000):
        for y in range(1000):
            try:
                if grid[x][y]:
                    count += 1
            except KeyError:
                pass

    print(count)
