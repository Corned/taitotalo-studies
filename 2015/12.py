import json


def flatten(l):
    new_l = []
    for index, element in enumerate(l):
        if type(element) is list:
            new_l = new_l + flatten(element)
        elif type(element) is dict:
            new_l = new_l + flatten(element.values())
        else:
            new_l = new_l + [element]

    return new_l


with open("./12-input.json", "r") as file:
    d = json.load(file)
    a = flatten(d)

    numbers = [item for item in a if type(item) is int]
    answer = sum(numbers)

    print(answer)
