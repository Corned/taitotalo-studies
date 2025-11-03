import hashlib

with open("./input/04.txt", "r") as file:
    secret_key = file.read().strip()

    i = 0
    while True:
        str = f"{secret_key}{i}"
        res = hashlib.md5(str.encode())
        hex = res.hexdigest()

        if hex.startswith("000000"):
            print(i)
            break

        i += 1
