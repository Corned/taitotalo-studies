input_string = "hxbxxyzz"

char_count = 26


def increment_string(string):
    reversed_string = string[::-1]
    incremented_string = ""

    increment_next_one = True

    for char in reversed_string:
        if increment_next_one:
            char_num = ord(char) - ord("a")
            next_char_num = (char_num + 1) % char_count
            incremented_string += chr(next_char_num + ord("a"))

            if char_num < next_char_num:
                # No need to increment the next character
                # a -> b happened, not z -> a
                increment_next_one = False
        else:
            incremented_string += char

    return incremented_string[::-1]


def is_valid_password(string):
    """
    1. Passwords must include one increasing straight of at least three letters,
    like abc, bcd, cde, and so on, up to xyz. They cannot skip letters; abd doesn't count.

    2. Passwords may not contain the letters i, o, or l, as these letters can be
    mistaken for other characters and are therefore confusing.

    3. Passwords must contain at least two different, non-overlapping pairs of
    letters, like aa, bb, or zz.
    """

    first_requirement = False
    second_requirement = False
    third_requirement = False

    # Increasing straight check
    # I can just check for three repeating values
    # if I subtract the index of the value from the value
    ords = [ord(char) - index for index, char in enumerate(string)]
    repetition = 0
    current_value = None

    for value in ords:
        if not current_value or value != current_value:
            current_value = value
            repetition = 1
        elif value == current_value:
            repetition += 1

        if repetition == 3:
            first_requirement = True
            break

    if string.count("i") + string.count("l") + string.count("o") == 0:
        second_requirement = True

    third_requirement = False
    count = 0
    other = ""
    for index in range(0, len(string) - 1):
        a = string[index]
        b = string[index + 1]

        if a == b and a + b != other:
            count += 1
            other = a + b

    if count >= 2:
        third_requirement = True

    return first_requirement, second_requirement, third_requirement


while True:
    input_string = increment_string(input_string)
    (
        has_three_increasing_repeats,
        no_illegal_characters,
        two_nonoverlapping_substrings,
    ) = is_valid_password(input_string)

    a = int(not not has_three_increasing_repeats)
    b = int(not not no_illegal_characters)
    c = int(not not two_nonoverlapping_substrings)

    print(input_string, a, b, c)

    if a and b and c:
        print(input_string)
        break
