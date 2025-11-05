with open("./input/02.txt", "r") as file:
    presents = file.readlines()

    # "3x2x1 -> ['3', '2', '1']
    presents: list[list[str]] = [present.strip().split("x") for present in presents]
    dimensions: list[list[int]] = []

    # ['3', '2', '1'] -> [1, 2, 3]
    # convert to int and sort
    for present in presents:
        dimensions.append(sorted([int(n) for n in present]))

    sum = 0
    for dimension in dimensions:
        x, y, z = dimension
        sum += (2 * x) + (2 * y) + (x * y * z)

    print(sum)
