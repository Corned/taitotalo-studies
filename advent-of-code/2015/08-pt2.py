with open("./input/08.txt", "r") as file:
    lines = file.readlines()  # ['""', '"abc"', r'"aaa\"aaa"', r'"\x27"']
    code_characters = sum([len(line.strip()) for line in lines])

    s = 0
    for line in lines:
        line = line.strip()
        quotes = line.count('"')
        escapes = line.count("\\")
        s += (len(line) - quotes - escapes) + 2 + (2 * quotes) + (2 * escapes)
        # print(line, "->", len(line), sum)

    print(s - code_characters)
