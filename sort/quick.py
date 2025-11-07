import random


def quick_sort(arr: list[int]) -> list[int]:
    def iterate(arr: list[int]) -> list[int]:
        if len(arr) <= 1:
            return arr

        # select random pivot
        pivot = random.randrange(0, len(arr))
        pivot_value = arr[pivot]

        values = [*arr[0:pivot], *arr[pivot + 1 :]]
        left_partition: list[int] = []
        right_partition: list[int] = []

        for value in values:
            if value <= pivot_value:
                left_partition.append(value)
            else:
                right_partition.append(value)

        return iterate(left_partition) + [pivot_value] + iterate(right_partition)

    return iterate(arr)


def main():
    unsorted_array = [34, 7, 23, 32, 5, 62, 32, 7, 4, 23]
    solution_array = [4, 5, 7, 7, 23, 23, 32, 32, 34, 62]
    sorted_array = quick_sort(unsorted_array)

    print("UNSORTED: ", unsorted_array)
    print("SOLUTION: ", solution_array)
    print("SORTED  : ", sorted_array)


if __name__ == "__main__":
    main()
