import numpy as np
import time
import sys
from benchmarking import timing


@timing
def gauss_jordan(matrix):
    columns, ci = matrix.shape[1], 0
    rows, ri = matrix.shape[0], 0
    permutation = np.array([i for i in range(rows)])

    # scaling
    while ri < rows and ci < columns - 1:
        pivot = np.argmax(abs(matrix[ri:, ci:columns - 1].copy()))
        row, col = np.unravel_index(pivot, matrix[ri:, ci:columns - 1].shape) + np.array([ri, ci])
        permutation[[col, ci]] = permutation[[ci, col]]
        matrix[:, [col, ci]] = matrix[:, [ci, col]]
        matrix[[ri, row]] = matrix[[row, ri]]
        row = matrix[ri]
        # Lower diagonal
        for adv_row in range(ri + 1, rows):
            frac = matrix[adv_row][ci] / row[ci]
            matrix[adv_row] = matrix[adv_row] - row * frac
            matrix[adv_row][ci] = 0
        # print(matrix)

        # Upper diagonal
        for adv_row in range(ri):
            frac = matrix[adv_row][ci] / row[ci]
            matrix[adv_row] = matrix[adv_row] - row * frac
            matrix[adv_row][ci] = 0
        ri += 1
        ci += 1

    # Scaling
    for i in range(rows):
        matrix[i][columns - 1] /= matrix[i][i]
        matrix[i][i] /= matrix[i][i]

    # Swap variables from full pivoting
    for i, val in enumerate(permutation):
        while i != val:
            matrix[[i, val], :] = matrix[[val, i], :]
            permutation[[i, val]] = permutation[[val, i]]
            val = permutation[i]
    return matrix[:, columns - 1]


if __name__ == "__main__":
    size = 10  # int(sys.argv[1])
    arr = np.random.rand(size, size + 1)
    gauss_jordan(arr.copy())
    timing(np.linalg.solve)(arr[:,:size], arr[:,size])
