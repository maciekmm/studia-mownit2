import numpy as np
import time
from benchmarking import timing

@timing
def gauss_jordan(matrix):
    columns, ci = matrix.shape[1], 0
    rows, ri = matrix.shape[0], 0

    # scaling
    while ri < rows and ci < columns-1:
        pivot = np.argmax(matrix[ri:, ci:], axis=0)
        matrix[ri], matrix[ri+pivot[0]] = matrix[ri+pivot[0]].copy(), matrix[ri].copy()
        row = matrix[ri]
        # Lower diagonal
        for adv_row in range(ri+1, rows):
            frac = matrix[adv_row][ci] / row[ci]
            matrix[adv_row] = matrix[adv_row] - row*frac
            matrix[adv_row][ci] = 0
        # print(matrix)

        # Upper diagonal
        for adv_row in range(ri):
            frac = matrix[adv_row][ci] / row[ci]
            matrix[adv_row] = matrix[adv_row] - row*frac
            matrix[adv_row][ci] = 0

        ri += 1
        ci += 1

    # Scaling
    for i in range(rows):
        matrix[i][columns-1] /= matrix[i][i]
        matrix[i][i] /= matrix[i][i]

    return matrix


if __name__ == "__main__":
    size=300
    arr = np.random.rand(size, size+1)
    gauss_jordan(arr.copy())
    timing(np.linalg.solve)(arr[:,:size], arr[:,size])
