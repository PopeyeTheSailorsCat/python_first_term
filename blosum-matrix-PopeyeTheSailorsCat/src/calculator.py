import math
import logging as lg


def create_matrix(elements_of_table, seq_col): # All in one function so as not to spoil the understanding by throwing
    # everything into different functions
    # print(seq_col[0])
    size = len(elements_of_table)  # The dimension of the table will be equal to the size of the resulting dictionary
    # of elements
    working_matrix = [[0] * size for i in range(size)]  # Creating a working matrix
    # print(working_matrix)

    for col in seq_col:  # Performing a calculation for all columns
        for i in range(size):  # It will pass all possible values from dictionaries
            for j in range(i, size):  # Let's go through all the values from the current one to the end, so we get
                # the combinations
                if i == j:  # If we have a diagonal element in the matrix
                    working_matrix[i][j] += col.counter.value_of(elements_of_table.get(i)) * (
                            col.counter.value_of(elements_of_table.get(i)) - 1) / 2
                else:  # Fill in Cij and Cji since the matrix is mirrored
                    working_matrix[j][i] += col.counter.value_of(elements_of_table.get(i)) * col.counter.value_of(
                        elements_of_table.get(j))
                    working_matrix[i][j] += col.counter.value_of(elements_of_table.get(i)) * col.counter.value_of(
                        elements_of_table.get(j))

    # print(working_matrix)
    matrix_sum = 0
    for i in range(size):  # We calculate the total number of transitions(we don't count the entire matrix as otherwise
        # some values will be counted twice)
        for j in range(0, i + 1):
            matrix_sum += working_matrix[i][j]
    # print(matrix_sum)

    for i in range(size):  # Normalizing values
        for j in range(size):
            working_matrix[i][j] = working_matrix[i][j] / matrix_sum
    # print(working_matrix)

    probability_list = [0] * size
    for i in range(size):  # Calculating the probability of an element appearing
        count_sum = 0
        for j in range(size):
            if i != j:
                count_sum += working_matrix[i][j]
        probability_list[i] = working_matrix[i][i] + count_sum / 2  # The amount is halved, since the transition with
        # another an element either on our element or on another with the same probability
    # print(probability_list)
    prob = 0
    for i in range(size):  # For the prob check, the total should be almost 1
        prob += probability_list[i]
    # print(prob)
    result_matrix = [[0] * size for i in range(size)]  # Creating the resulting matrix
    for i in range(size):
        for j in range(size):
            if abs(working_matrix[i][j]) < 1e-5 or abs(probability_list[i]) < 1e-5 or abs(probability_list[
                                                                                              j]) < 1e-5:
                # Trying to catch if the probability of some element SUDDENLY zero
                # or some pair did not occur, but in General this can be considered an extreme case and
                # we recommend checking the source data
                result_matrix[i][j] = 0
                lg.info("bad data may happen")
            # The logarithm does not turn to zero, which means that this result will signal
            # that this data is not present
            else:
                if j != i:
                    result_matrix[i][j] = 2 * math.log2(
                        working_matrix[i][j] / (2 * probability_list[i] * probability_list[j]))
                else:
                    result_matrix[i][j] = 2 * math.log2(
                        working_matrix[i][j] / (probability_list[i] * probability_list[i]))
    return result_matrix
