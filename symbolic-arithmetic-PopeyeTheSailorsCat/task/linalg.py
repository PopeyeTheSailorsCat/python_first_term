import copy


def dot(a, x):
    """
    Computer matrix-vector product A @ x.

    Parameters
    ----------
    a : List[List]
        Matrix A.
    x : List[float]
        Vector x.

    Returns
    -------
    Dop product A @ x.

    """
    y = []
    for i in range(len(a)):
        semi_res = 0
        for j in range(len(a[0])):  # Scalar product of a row and a column
            semi_res += a[i][j] * x[j]
        y.append(semi_res)
    return y
    # raise NotImplementedError


def __gauss(b):  # Implementation of the Jordan Gauss method for the inverse matrix
    out = []
    for i in range(len(b)):  # Creating a diagonal unit matrix
        stroka = []
        for j in range(len(b[0])):
            if i != j:
                stroka.append(0)
            else:
                stroka.append(1)
        out.append(stroka)
    # print(out)

    for i in range(len(b)):  # Forward stroke
        deleter = b[i][i]
        for j in range(len(b[0])):
            out[i][j] = out[i][j] / deleter
            b[i][j] = b[i][j] / deleter

        for i_2 in range(i + 1, len(b)):

            mul = b[i_2][i]
            for j_2 in range(len(b[0])):
                out[i_2][j_2] = out[i_2][j_2] - out[i][j_2] * mul
                b[i_2][j_2] = b[i_2][j_2] - b[i][j_2] * mul
    for i in range(len(b) - 1, -1, -1):  # Reverse motion
        for j in range(i):

            for k in range(len(b)):
                out[j][k] = out[j][k] - out[i][k] * b[j][i]
            b[j][i] = b[j][i] - b[j][i] * b[i][i]
    return out
    # raise NotImplementedError


def inv(a):
    """
    Compute inverse of matrix A.

    Parameters
    ----------
    a : List[list]
        Matrix A in the list form.

    Returns
    -------
    ret : List[List]
        Inverse of matrix A A^{-1}.

    """
    b = copy.deepcopy(a)  # So that changes in Gaussian don't affect a

    return __gauss(b)  # out
    # raise NotImplementedError
