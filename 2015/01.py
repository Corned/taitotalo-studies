with open("./input/01.txt", "r") as file:
    text = file.read()
    floor = text.count("(") - text.count(")")

    print(floor)
