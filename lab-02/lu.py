from benchmarking import timing
import numpy as np
import scipy.linalg
import scipy
import sys


@timing
def lu(matrix):
    up = matrix.copy()
    lo = np.identity(up.shape[0])
    columns, ci = up.shape[1], 0
    rows, ri = up.shape[0], 0

    while ri < rows and ci < columns:
        row = up[ri]
        # Lower diagonal
        for adv_row in range(ri + 1, rows):
            frac = up[adv_row][ci] / row[ci]
            up[adv_row] = up[adv_row] - row * frac
            up[adv_row][ci] = 0
            lo[adv_row][ci] = frac

        ri += 1
        ci += 1

    return (lo, up)


if __name__ == "__main__":
    size = int(sys.argv[1])
    arr = np.random.rand(size, size)
    L, U = lu(arr.copy())
    P, SL, SU = timing(scipy.linalg.lu)(arr)
