import re


def parse(lines: list[str]):
    data: list[tuple] = []
    starting_mol = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = re.match(r"(\w+) => (\w+)", line)

        if match:
            data.append(match.groups())
        else:
            starting_mol = line

    return data, starting_mol


def iterate(
    replacement_data: list[tuple[str, str]],
    current_mol: str,
    iteration: int = 0,
):
    # print("depth", iteration, current_mol)

    for from_mol, to_mol in replacement_data:
        if from_mol not in current_mol:
            continue

        new_mol: str = current_mol.replace(from_mol, to_mol, 1)
        # print(current_mol, f"-> replacing {from_mol} with {to_mol} -> {new_mol}")

        if new_mol == "e":
            print(f"Found '{new_mol}' after {iteration} iterations.")
            exit(1)

        iterate(replacement_data, new_mol, iteration + 1)


with open("input.txt", "r") as file:
    lines: list[str] = file.readlines()
    (pairs, start_mol) = parse(lines)

    # Reversed mapping compared to part-1
    replacement_data: list[tuple[str, str]] = []
    for mol_a, mol_b in pairs:
        replacement_data.append((mol_b, mol_a))

    replacement_data = sorted(
        replacement_data, key=lambda item: len(item[0]), reverse=True
    )

    iterate(replacement_data, start_mol, 1)
