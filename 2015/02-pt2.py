with open("./02-input.txt", "r") as file:
    presents = file.readlines()
    # "3x2x1 -> ['3', '2', '1']
    # split string into list
    presents = [present.strip().split("x") for present in presents]
    dimensions = []

    # ['3', '2', '1'] -> [1, 2, 3]
    # convert to int and sort
    for present in presents:
        dimensions.append(sorted(list(map(lambda s: int(s), present))))

    sum = 0
    for dimension in dimensions:
        x, y, z = dimension
        sum += (2 * x) + (2 * y) + (x * y * z)

    print(sum)
