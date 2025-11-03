with open("./input/05.txt", "r") as file:
    lines = file.readlines()

    nice_words = 0
    for line in lines:
        line = line.strip()
        has_two_two_letter_nonoverlapping_substring = False
        for index in range(0, len(line) - 2):
            substr = line[index : index + 2]

            if substr in line[index + 2 :]:
                has_two_two_letter_nonoverlapping_substring = True
                break

        gap_between_two_characters = False
        for index in range(0, len(line) - 2):
            if line[index] == line[index + 2]:
                gap_between_two_characters = True
                break

        if not gap_between_two_characters:
            continue

        if not has_two_two_letter_nonoverlapping_substring:
            continue

        nice_words += 1

    print(nice_words)
