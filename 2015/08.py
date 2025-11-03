with open("./input/08.txt", "r") as file:
    lines = file.readlines()

    code_characters = sum([len(line.strip()) for line in lines])
    memory_characters = sum([len(eval(line.strip())) for line in lines])

    print(code_characters, memory_characters)
    print("answer:", code_characters - memory_characters)
