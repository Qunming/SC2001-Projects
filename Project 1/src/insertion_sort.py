def insertion_sort(A):

    n = len(A)
    comparisons = 0

    for i in range(1, n):

        j = i - 1

        while j >= 0:

            comparisons += 1

            if A[j] > A[j + 1]:
                A[j], A[j + 1] = A[j + 1], A[j]
                j -= 1
            else:
                break

    return A, comparisons


if __name__ == "__main__":
    numbers = [8, 3, 2, 9, 1, 2, 0, 1, 3, 10, -2, 77, 22, 34, 93]

    sorted_numbers, comparisons = insertion_sort(numbers)

    print("Sorted:", sorted_numbers)
    print("Number of key comparisons =", comparisons)
