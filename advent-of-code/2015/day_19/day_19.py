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


with open("input/19.txt", "r") as file:
    lines = file.readlines()
    pairs, molecule = parse(lines)

    # format pairs into a better format
    replacement_data = {}
    for mol_a, mol_b in pairs:
        if not replacement_data.get(mol_a):
            replacement_data[mol_a] = []

        replacement_data[mol_a].append(mol_b)

    molecule_data = re.findall("([A-Z]{1}[a-z]?)", molecule)

    pprint(replacement_data)
    pprint(molecule_data)
