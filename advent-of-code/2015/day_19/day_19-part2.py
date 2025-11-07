import re
import time


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


with open("input_19.txt", "r") as file:
    lines = file.readlines()
    pairs, target_molecule = parse(lines)

    # format pairs into a better format
    replacement_data = {}
    for mol_a, mol_b in pairs:
        if not replacement_data.get(mol_a):
            replacement_data[mol_a] = []

        replacement_data[mol_a].append(mol_b)

    unique_strings = set()
    molecules = [["e"]]
    iteration = 0

    while True:
        time.sleep(1)
        iteration += 1
        new_molecules = []

        print(
            f"iter. {str(iteration).rjust(2, '0')} -- Processing {len(molecules)} molecules..."
        )

        print(f"\tExample molecule: {''.join(molecules[0])}")

        for molecule in molecules:
            for pointer in range(len(molecule)):
                left_half = molecule[:pointer]
                right_half = molecule[pointer + 1 :]
                to_replace = molecule[pointer]

                if not replacement_data.get(to_replace):
                    continue

                for replace_with in replacement_data[to_replace]:
                    replacement = re.findall("([A-Z]{1}[a-z]?)", replace_with)
                    new_molecule = [*left_half, *replacement, *right_half]
                    new_molecule_string = "".join(new_molecule)

                    if new_molecule_string == target_molecule:
                        print(f"Answer: {iteration}")
                        exit(1)

                    if new_molecule_string in unique_strings:
                        continue

                    if len(new_molecule_string) > len(target_molecule):
                        continue

                    unique_strings.add(new_molecule_string)
                    new_molecules = [new_molecule, *new_molecules]

        molecules = new_molecules
