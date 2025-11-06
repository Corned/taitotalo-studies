with open("./input/01.txt", "r") as file:
    text = file.read().strip()

    floor = 0
    for index, char in enumerate(text):
        floor += 1 if char == "(" else -1

        if floor < -1:
            print(index)
            break
