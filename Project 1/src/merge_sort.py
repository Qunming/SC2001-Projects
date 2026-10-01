def merge_sort(A):

    if len(A) <= 1:
        return A, 0

    middle = len(A) // 2

    left = A[:middle]
    right = A[middle:]

    left, left_comparisons = merge_sort(left)
    right, right_comparisons = merge_sort(right)

    result, merge_comparisons = merge(left, right)

    total_comparisons = (left_comparisons + right_comparisons + merge_comparisons)

    return result, total_comparisons


def merge(left, right):

    result = []
    i = 0
    j = 0

    comparisons = 0

    while i < len(left) and j < len(right):

        comparisons += 1

        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    while i < len(left):
        result.append(left[i])
        i += 1

    while j < len(right):
        result.append(right[j])
        j += 1

    return result, comparisons


if __name__ == "__main__":
    numbers = [8, 3, 2, 9, 1, 2, 0, 1, 3, 10, -2, 77, 22, 34, 93]

    sorted_numbers, comparisons = merge_sort(numbers)

    print("Sorted:", sorted_numbers)
    print("Number of key comparisons =", comparisons)
