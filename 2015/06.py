def toggle(grid, x, y):
    if not grid.get(x):
        grid[x] = {}

    if not grid.get(x).get(y):
        grid[x][y] = 0

    grid[x][y] = 1 if not grid[x][y] else 0


with open("./06-input.txt", "r") as file:
    directions = file.read().strip()

    grid = {}
