import numpy as np
import matplotlib.pyplot as plt

points = [
    (-5, 2),
    (-4, 7),
    (-3, 9),
    (-2, 12),
    (-1, 13),
    (0, 14),
    (1, 14),
    (2, 13),
    (3, 10),
    (4, 8),
    (5, 4),
]

A = np.array([[1, x, x ** 2] for x, y in points])
b = np.array([y for x, y in points])

r = np.linalg.lstsq(A, b, rcond=None)[0]

def solve(A, b):
    Q, R = np.linalg.qr(A)
    print(Q)
    np.linalg.solve(np.concatenate(R, Q.T @ b))


solve(A, b)
