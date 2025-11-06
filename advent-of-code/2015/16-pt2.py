import re

"""
In particular, the cats and trees readings indicates that there are greater than
that many (due to the unpredictable nuclear decay of cat dander and tree pollen),
while the pomeranians and goldfish readings indicate that there are fewer than
that many (due to the modial interaction of magnetoreluctance).

aunt has more cats, trees than ticker_tape
aunt has less pomeranians and goldfish
"""

ticker_tape = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}

# {'index': 40, 'vizslas': 0, 'cats': 7, 'akitas': 0}
exception_greater = ["cats", "trees"]
exception_lesser = ["pomeranians", "goldfish"]


def parse(lines):
    data = []
    for line in lines:
        # Sugar: capacity 0, durability 0, flavor -2, texture 2, calories 1
        match = re.match(
            r"Sue (\d+): (\w+): (\d+), (\w+): (\d+), (\w+): (\d+)",
            line.strip(),
        )

        if match:
            index = int(match.groups()[0])
            name_a = match.groups()[1]
            value_a = int(match.groups()[2])
            name_b = match.groups()[3]
            value_b = int(match.groups()[4])
            name_c = match.groups()[5]
            value_c = int(match.groups()[6])

            data.append(
                {
                    "index": index,
                    name_a: value_a,
                    name_b: value_b,
                    name_c: value_c,
                }
            )
    return data


with open("input/16.txt", "r") as file:
    lines = file.readlines()
    data = parse(lines)

    for datum in data:
        the_correct_aunt = True

        for key in datum:
            if key == "index":
                continue

            value = datum[key]
            if key in ticker_tape:
                if key in exception_greater:
                    if datum[key] <= ticker_tape[key]:
                        the_correct_aunt = False
                        break
                elif key in exception_lesser:
                    if datum[key] >= ticker_tape[key]:
                        the_correct_aunt = False
                        break
                else:
                    if ticker_tape[key] != datum[key]:
                        the_correct_aunt = False
                        break

        if the_correct_aunt:
            print(f"The correct aunt is {datum['index']}.", datum)
            break
