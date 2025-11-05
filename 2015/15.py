import re
import itertools


def parse_ingredient_data(lines):
    ingredient_data = []
    for line in lines:
        # Sugar: capacity 0, durability 0, flavor -2, texture 2, calories 1
        match = re.match(
            r"(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)",
            line.strip(),
        )

        if match:
            name, capacity, durability, flavor, texture, calories = match.groups()
            ingredient_data.append(
                {
                    "name": name,
                    "capacity": int(capacity),
                    "durability": int(durability),
                    "flavor": int(flavor),
                    "texture": int(texture),
                    "calories": int(calories),
                }
            )

    return ingredient_data


with open("./input/15.txt", "r") as file:
    lines = file.readlines()
    ingredient_data = parse_ingredient_data(lines)

    print(list(map(lambda item: item["name"], ingredient_data)))

    # hardcoding
    best_answer = 0
    for a in range(0, 101):
        for b in range(0, 101):
            for c in range(0, 101):
                for d in range(0, 101):
                    if a + b + c + d != 100:
                        continue

                    amounts = [a, b, c, d]
                    capacity = 0
                    durability = 0
                    flavor = 0
                    texture = 0

                    for i, _ in enumerate(ingredient_data):
                        capacity += amounts[i] * ingredient_data[i]["capacity"]
                        durability += amounts[i] * ingredient_data[i]["durability"]
                        flavor += amounts[i] * ingredient_data[i]["flavor"]
                        texture += amounts[i] * ingredient_data[i]["texture"]

                    answer = (
                        max(0, capacity)
                        * max(0, durability)
                        * max(0, flavor)
                        * max(0, texture)
                    )
                    if answer >= best_answer:
                        best_answer = answer

    print(best_answer)
