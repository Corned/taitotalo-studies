with open("./input/03.txt", "r") as file:
    directions = file.read().strip()

    x, y = 0, 0
    xr, yr = 0, 0
    loc = {}
    at_least_one_present = 0

    for index, dir in enumerate(directions):
        if index % 2 == 0:
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
        else:
            if dir == "v":
                yr += 1
            elif dir == "^":
                yr -= 1
            elif dir == "<":
                xr -= 1
            elif dir == ">":
                xr += 1

            if not loc.get(xr):
                loc[xr] = {}

            if not loc.get(xr).get(yr):
                loc[xr][yr] = 0
                at_least_one_present += 1

            loc[xr][yr] += 1

    print(at_least_one_present)
