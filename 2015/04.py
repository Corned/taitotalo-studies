import hashlib

with open("./04-input.txt", "r") as file:
    secret_key = file.read().strip()

    i = 0
    while True:
        str = f"{secret_key}{i}"
        res = hashlib.md5(str.encode())
        hex = res.hexdigest()

        if hex.startswith("00000"):
            print(i)
            break

        i += 1
