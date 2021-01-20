from src import NV_alignment as align


def hamming(seq_1, seq_2):  # This function calculates the Hamming distance
    """
       >>> hamming("aa","ab")
       1
    """
    count = 0
    for i in range(len(seq_1)):  # Consider all of the different characters in a string
        if seq_1[i] != seq_2[i]:  # It is guaranteed that the rows are the same size
            count += 1

    return count


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Enter your sequences")
    seq_1 = input()
    seq_2 = input()
    print("gap_penalty:")
    penalty = float(input())
    print("match reward, mismatch reward:")
    match, mismatch = map(float, input().split())
    coef, result_line = align.align(seq_1, seq_2, penalty, match, mismatch)
    print("maximum score among all possible alignments:", coef)
    print(result_line[0])
    print(result_line[1])
    print("hamming distance:", hamming(result_line[0], result_line[1]))
    print("finish")
