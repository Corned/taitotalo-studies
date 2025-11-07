def bubble_sort(list):
    while True:
        sorted = True

        for i in range(0, len(list) - 1):
            if list[i] > list[i + 1]:
                list[i], list[i + 1] = list[i + 1], list[i]
                sorted = False

        if sorted:
            break

    return list


def main():
    unsorted_list = []
    count = int(input("Anna lajiteltavien numeroiden lukumäärä : "))
    for i in range(count):
        number = int(input(f"Anna taulukon {i} numero : "))
        unsorted_list.append(number)

    sorted_list = bubble_sort(unsorted_list)
    print("Lajiteltu lista nousevassa järjestyksessä ", sorted_list)


if __name__ == "__main__":
    main()
