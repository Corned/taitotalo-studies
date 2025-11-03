import re

pt1 = 2503


def parse(lines):
    reindeer = []

    for line in lines:
        match = re.match(
            r"(\w+) can fly (\d+) km\/s for (\d+) seconds, but then must rest for (\d+) seconds.",
            line.strip(),
        )

        if match:
            name, speed, duration, rest = match.groups()
            reindeer.append(
                {
                    "name": name,
                    "speed": int(speed),
                    "duration": int(duration),
                    "rest": int(rest),
                    "distance_travelled": 0,
                    "is_resting": False,
                    "time_remaining": int(duration),
                    "score": 0,
                }
            )

    return reindeer


with open("./input/14.txt", "r") as file:
    lines = file.readlines()
    reindeer_list = parse(lines)

    time_elapsed = 0
    for time_elapsed in range(pt1):
        for reindeer in reindeer_list:
            if not reindeer["time_remaining"]:
                reindeer["is_resting"] = not reindeer["is_resting"]
                reindeer["time_remaining"] = (
                    reindeer["rest"] if reindeer["is_resting"] else reindeer["duration"]
                )

            reindeer["time_remaining"] -= 1
            if not reindeer["is_resting"]:
                reindeer["distance_travelled"] += reindeer["speed"]

        # After every second, give a point to every leader
        reindeer_list = list(
            reversed(sorted(reindeer_list, key=lambda item: item["distance_travelled"]))
        )

        highest_distance_travelled = reindeer_list[0]["distance_travelled"]
        for reindeer in reindeer_list:
            if reindeer["distance_travelled"] == highest_distance_travelled:
                reindeer["score"] += 1

    reindeer_list = list(
        reversed(sorted(reindeer_list, key=lambda item: item["distance_travelled"]))
    )

    reindeer = reindeer_list[0]
    print("Part 1 (distance):", reindeer["name"], reindeer["distance_travelled"])

    reindeer_list = list(
        reversed(sorted(reindeer_list, key=lambda item: item["score"]))
    )

    reindeer = reindeer_list[0]
    print("Part 2 (score):", reindeer["name"], reindeer["score"])
