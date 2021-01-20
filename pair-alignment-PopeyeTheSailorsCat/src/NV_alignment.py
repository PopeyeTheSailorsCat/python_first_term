def init(line, col,
         err):  # The function implements the initialization of the matrix for the algorithm of Mildmay-Woncha
    """
        >>> init(1,1,2)
        [[0, -2], [-2, 0]]
    """
    matrix = [[0] * (col + 1) for i in range(line + 1)]  # Dimension of the matrix n+1, m+1
    for i in range(col + 1):  # Fill in the first line
        matrix[0][i] = -i * err
    for i in range(line + 1):  # Fill in the first column
        matrix[i][0] = -i * err
    return matrix  # Returning the initialized matrix


def calc_score(up, left, middle, matched, gap_penalty, match,
               mismatch):  # This function calculates the matrix element while the algorithm is running
    """

    :float up: Element values above the current one
    :float left:  Value of the element to the left of the current one
    :float middle:Value of the element at the top left of the current one
    :1 or 0  matched: Did the row values match at this location
    :float gap_penalty: The penalty for skipping
    :float match: The reward for the match
    :float mismatch: The reward for the mismatch
    :return float: maximum match, insert, delete
    """
    if matched:  # Selecting the value of s depending on whether the row elements match
        s = match
    else:
        s = mismatch
    Match = middle + s  # The implementation of the principle of optimality Bella
    Insertion = left - gap_penalty
    Deletion = up - gap_penalty
    return max([Match, Insertion, Deletion])  # Returning the maximum possible value


def get_alignment(seq_1, seq_2, aligned_matrix, gap_penalty, match_reward, mismatch_punishment):  # The function
    # implements finding the return path in the calculated matrix

    res_seq_1 = ""  # Initializing the final sequences
    res_seq_2 = ""
    i = len(seq_1)
    j = len(seq_2)
    while i > 0 and j > 0:  # Remember that in seq, the element is shifted by one until no line ends
        current = aligned_matrix[i][j]  # Trying to figure out how we came here(see calc_score)
        # middle = aligned_matrix[i - 1][j - 1]
        left = aligned_matrix[i][j - 1]
        up = aligned_matrix[i - 1][j]
        if current == left - gap_penalty:
            res_seq_1 = "-" + res_seq_1
            res_seq_2 = seq_2[j - 1] + res_seq_2
            j -= 1
        elif current == up - gap_penalty:
            res_seq_1 = seq_1[i - 1] + res_seq_1
            res_seq_2 = "-" + res_seq_2
            i -= 1
        else:  # For good here you need to check the full match and if it is not, give an error that everything went
            # wrong
            res_seq_1 = seq_1[i - 1] + res_seq_1
            res_seq_2 = seq_2[j - 1] + res_seq_2
            j -= 1
            i -= 1
    # If there are elements left in one sequence, we add it by adding a second one -
    while i > 0:
        res_seq_1 = seq_1[i - 1] + res_seq_1
        res_seq_2 = "-" + res_seq_2
        i -= 1
    while j > 0:
        res_seq_1 = "-" + res_seq_1
        res_seq_2 = seq_2[j - 1] + res_seq_2
        j -= 1

    return [res_seq_1, res_seq_2]


def align(seq_1, seq_2, gap_penalty, match_reward, mismatch_punishment):  # The function implements the alignment of two
    # sequences'
    """

    :str seq_1: The first sequence
    :str seq_2: The second sequence
    :float gap_penalty: The penalty for a gap
    :float match_reward: The reward for the match
    :float mismatch_punishment:
    :return: max_coef, [result line_1, result line_2] Returning the maximum score among all possible values
alignments and two resulting aligned rows
    """
    matrix = init(len(seq_1), len(seq_2), gap_penalty)  # Initializing our matrix
    for i in range(0, len(seq_1)):  # There is an interesting thing going on with indexes, since
        for j in range(0, len(seq_2)):  # in the matrix, we need to work with 1 offset to the right and down
            if seq_1[i] == seq_2[j]:  # If the characters match
                match = 1
            else:
                match = 0
            matrix[i + 1][j + 1] = calc_score(matrix[i][j + 1], matrix[i + 1][j], matrix[i][j], match, gap_penalty,
                                              match_reward, mismatch_punishment)  # Calculating the value of the element

    # Getting the aligned rows
    res = get_alignment(seq_1, seq_2, matrix, gap_penalty, match_reward, mismatch_punishment)
    return matrix[len(seq_1)][len(seq_2)], res


if __name__ == "__main__":
    import doctest

    doctest.testmod()
