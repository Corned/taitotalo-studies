import subprocess
from pathlib import Path

current_folder = Path(__file__).parent
relative_paths = current_folder.glob("./*")
absolute_paths = [current_folder / file for file in relative_paths]
directories = [path for path in absolute_paths if path.is_dir()]

select_year_prompt = "Select year:\n"
for index, directory in enumerate(directories, start=1):
    select_year_prompt += f"({index}) {directory.name}\n"
select_year_prompt = select_year_prompt.strip()

print(select_year_prompt)
