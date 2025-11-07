from math import floor

# TODO: finish the code


def merge_sort(arr):
    def split(arr):
        return arr[0 : floor(len(arr) / 2)], arr[floor(len(arr) / 2) :]

    def merge(a, b):
        arr = []

        while len(a) != 0 or len(b) != 0:
            if len(a) == 0:
                return arr + b
            elif len(b) == 0:
                return arr + a

            if a[0] <= b[0]:
                arr.append(a.pop(0))
            else:
                arr.append(b.pop(0))

        return arr

    print(merge([1, 2, 5, 7], [5, 6, 7, 11]))
    return arr


def main():
    unsorted_array = [34, 7, 23, 32, 5, 62, 32, 7, 4, 23, 1]
    solution_array = [1, 4, 5, 7, 7, 23, 23, 32, 32, 34, 62]
    sorted_array = merge_sort(unsorted_array)

    print("UNSORTED: ", unsorted_array)
    print("SOLUTION: ", solution_array)
    print("SORTED  : ", sorted_array)


if __name__ == "__main__":
    main()
