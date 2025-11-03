import re

with open("./input/09.txt", "r") as file:
    lines = file.readlines()
    city_data = {}

    for line in lines:
        match = re.match(r"(\w+) to (\w+) = (\d+)", line.strip())
        if match:
            city_a, city_b, distance = match.groups()

            if not city_data.get(city_a):
                city_data[city_a] = {}

            if not city_data.get(city_b):
                city_data[city_b] = {}

            city_data[city_a][city_b] = int(distance)
            city_data[city_b][city_a] = int(distance)

    city_count = len(city_data.keys())

    # London -> Dublin -> Belfast = 605

    def traverse(
        visited_cities=[], travelled_distance=0, current_answer=[99999999, ""]
    ):
        current_city = visited_cities[-1]

        if len(visited_cities) == len(city_data):
            # print(
            # f"Currently in city '{' -> '.join(visited_cities)}' ({travelled_distance})"
            # )

            new_answer = (
                current_answer[0]
                if current_answer[0] > travelled_distance
                else travelled_distance
            )

            return (
                visited_cities,
                travelled_distance,
                [new_answer, " -> ".join(visited_cities)],
            )

        for next_city in city_data:
            if next_city not in visited_cities:
                _, __, current_answer = traverse(
                    [*visited_cities, next_city],
                    travelled_distance + city_data[current_city][next_city],
                    current_answer,
                )

        return visited_cities, travelled_distance, current_answer

    best_answer = (-1, "")
    for city in city_data:
        _, __, answer = traverse([city], 0, [-1, ""])
        if answer[0] > best_answer[0]:
            best_answer = answer

    print(best_answer)
