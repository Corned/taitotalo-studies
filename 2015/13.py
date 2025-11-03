import re
import itertools


def format_data(lines):
    happiness = {}

    for line in lines:
        line = line.strip()
        match = re.match(
            r"(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+).",
            line,
        )

        if match:
            person_a, sign, points, person_b = match.groups()
            points = int(points) if sign == "gain" else -int(points)

            if not happiness.get(person_a):
                happiness[person_a] = {}

            happiness[person_a][person_b] = points
            # print(f"{person_a} gets {points} points with {person_b}")

    return happiness


with open("./input/13.txt", "r") as file:
    lines = file.readlines()

    # person dict[person]'s relationship with dict[person][other_person]'
    happiness = format_data(lines)
    people = happiness.keys()

    max_happiness = 0
    for arrangement in itertools.permutations(people):
        pair_happiness_sum = 0
        for index_a, person_a in enumerate(arrangement):
            index_b = (index_a + 1) % len(arrangement)
            person_b = arrangement[index_b]

            pair_happiness = (
                happiness[person_a][person_b] + happiness[person_b][person_a]
            )

            pair_happiness_sum += pair_happiness

        max_happiness = max(max_happiness, pair_happiness_sum)

    print(max_happiness)
