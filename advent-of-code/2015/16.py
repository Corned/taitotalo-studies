import re

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
            if key in ticker_tape and ticker_tape[key] != datum[key]:
                the_correct_aunt = False

        if the_correct_aunt:
            print(f"The correct aunt is {datum['index']}.")
