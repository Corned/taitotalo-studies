from glob import glob
from pathlib import Path

current_folder = Path(__file__).parent
relative_files = glob("./2015/*")
absolute_files = [current_folder / file for file in relative_files]
file_sizes_in_bytes = [file.stat().st_size for file in absolute_files]

in_bytes = sum(file_sizes_in_bytes)
in_kilo_bytes = in_bytes / 1024
in_mega_bytes = in_bytes / 1024**2

print(f"{in_bytes:.2f} B")
print(f"{in_kilo_bytes:.2f} KiB")
print(f"{in_mega_bytes:.2f} MiB")
