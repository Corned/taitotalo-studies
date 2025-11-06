"""
This is both the 10 part 1 and 10 part 2 solution.
"""

input_string = "1321131112"


def look_and_say(a):
    current_value = a[0]
    length = 0
    answer = ""

    for index, char in enumerate(a):
        if char == current_value:
            length += 1
        else:
            answer += str(length) + current_value
            current_value = char
            length = 1

    return answer + str(length) + current_value


for _ in range(50):
    input_string = look_and_say(input_string).strip()
    print(len(input_string))


# print(input_string)
