import re


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


with open("./13-input.txt", "r") as file:
    lines = file.readlines()

    # person dict[person]'s relationship with dict[person][other_person]'
    happiness = format_data(lines)

    # create a dict of all pairs' values added together
    mutual_relationship = {}
    for person_a in happiness:
        for person_b in happiness[person_a]:
            a_likes_b = happiness[person_a][person_b]
            b_likes_a = happiness[person_b][person_a]

            combined_name = f"{person_a}-{person_b}"
            combined_name2 = f"{person_b}-{person_a}"

            print(f"{person_a.ljust(5)} -> {person_b.ljust(5)} = {a_likes_b}")
            print(f"{person_b.ljust(5)} -> {person_a.ljust(5)} = {b_likes_a}")

            if combined_name2 not in mutual_relationship:
                mutual_relationship[combined_name] = a_likes_b + b_likes_a

    mutual_relationship = reversed(
        sorted(mutual_relationship.items(), key=lambda item: item[1])
    )

    print("")
    sum = 0
    q = []
    for pair, value in mutual_relationship:
        a, b = pair.split("-")

        if q.count(a) < 2 and q.count(b) < 2:
            q += [a, b]
            sum += value

    print(sum)
