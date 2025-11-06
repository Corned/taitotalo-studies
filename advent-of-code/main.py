import itertools
import subprocess
from pathlib import Path

current_dir = Path(__file__).parent
current_dir_contents = current_dir.glob("./*")
year_dirs = [path for path in current_dir_contents if (current_dir / path).is_dir()]

select_year_prompt = "Select year:\n"
for index, directory in enumerate(year_dirs, start=1):
    select_year_prompt += f"({index}) {directory.name}\n"
select_year_prompt = select_year_prompt.strip()


def format(strings: list[str], item_length: int = 0) -> str:
    output = ""
    for batch in itertools.batched(strings, 5):
        line = ""
        for item in batch:
            line += item.rjust(item_length, " ") + " "
        output += f"{line.strip()}\n"

    return output.strip()


def main():
    print("Advent of Code 🎅")
    selected_year = input(f"{select_year_prompt}\n> ")
    year_dir = year_dirs[int(selected_year) - 1]
    day_dirs = sorted(list(year_dir.glob("*")))

    day_numbers = [day.name[4:] for day in day_dirs]
    formatted_days = format(day_numbers, item_length=3)
    select_day_prompt = f"Enter day (e.g. 2):\n{formatted_days}\n> "
    selected_day = int(input(select_day_prompt))

    print(day_dirs[selected_day - 1])

    pass


if __name__ == "__main__":
    main()
