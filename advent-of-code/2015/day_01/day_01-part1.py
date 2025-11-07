with open("input.txt", "r") as file:
    text = file.read()
    floor = text.count("(") - text.count(")")

    print(floor)
