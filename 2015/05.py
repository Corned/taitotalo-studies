with open("./input/05.txt", "r") as file:
    lines = file.readlines()

    nice_words = 0
    for line in lines:
        # aeiou
        vowel_count = sum(
            [
                line.count("a"),
                line.count("e"),
                line.count("i"),
                line.count("o"),
                line.count("u"),
            ]
        )

        # Check for two of the same characters in a row
        two_letters_in_a_row = False
        for index in range(0, len(line) - 1):
            if line[index] == line[index + 1]:
                two_letters_in_a_row = True
                break

        contains_illegal_substring = False
        # Check for illegal substrings
        for illegal in ["ab", "cd", "pq", "xy"]:
            if illegal in line:
                contains_illegal_substring = True
                break

        if contains_illegal_substring:
            continue

        if vowel_count < 3:
            continue

        if not two_letters_in_a_row:
            continue

        nice_words += 1

    print(nice_words)
