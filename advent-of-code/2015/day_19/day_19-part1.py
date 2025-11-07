import re
from pprint import pprint


def parse(lines: list[str]):
    data = []
    molecule = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = re.match(r"(\w+) => (\w+)", line)

        if match:
            data.append(match.groups())
        else:
            molecule = line

    return data, molecule


with open("input.txt", "r") as file:
    lines = file.readlines()
    pairs, molecule = parse(lines)

    # format pairs into a better format
    replacement_data = {}
    for mol_a, mol_b in pairs:
        if not replacement_data.get(mol_a):
            replacement_data[mol_a] = []

        replacement_data[mol_a].append(mol_b)

    molecule_data = re.findall("([A-Z]{1}[a-z]?)", molecule)
    unique_strings = set()

    for pointer in range(len(molecule_data)):
        left_half = molecule_data[:pointer]
        right_half = molecule_data[pointer + 1 :]
        to_replace = molecule_data[pointer]

        if not replacement_data.get(to_replace):
            continue

        for replace_with in replacement_data[to_replace]:
            string = "".join([*left_half, replace_with, *right_half])
            unique_strings.add(string)

    print(f"Answer: {len(unique_strings)}")
