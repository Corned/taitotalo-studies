with open("./input/03.txt", "r") as file:
    directions = file.read().strip()

    x, y = 0, 0
    loc = {}
    at_least_one_present = 0

    for dir in directions:
        if dir == "v":
            y += 1
        elif dir == "^":
            y -= 1
        elif dir == "<":
            x -= 1
        elif dir == ">":
            x += 1

        if not loc.get(x):
            loc[x] = {}

        if not loc.get(x).get(y):
            loc[x][y] = 0
            at_least_one_present += 1

        loc[x][y] += 1

    print(at_least_one_present)
