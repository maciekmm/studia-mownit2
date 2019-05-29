import numpy as np
import matplotlib.pyplot as plt


def factor_qr(A):
    n = A.shape[1]
    Q = np.zeros((n, n))

    for k in range(0, n):
        Q[:, k] = A[:, k]
        if k != 0:
            sum = 0
            for i in range(k):
                sum += np.dot(Q[:, i], A[:, k]) * Q[:, i]
            Q[:, k] -= sum
        Q[:, k] = Q[:, k] / np.linalg.norm(Q[:, k])

    R = np.zeros((n, n))

    for x in range(0, n):
        for y in range(x, n):
            R[x, y] = np.dot(Q[:, x], A[:, y])
    return Q, R


n = 5
A = np.random.rand(8, 8)
q, r = np.linalg.qr(A)

x = []
y = []


for mtx in range(50):
    A = np.random.rand(n, n)
    u, s, t = np.linalg.svd(A)
    s[0] *= 10**mtx
    A = (u @ (s[..., None] * t))
    q, r = factor_qr(A)
    x.append(np.linalg.cond(A))
    y.append(np.linalg.norm(np.identity(n) - q.T @ q))

plt.scatter(x, y)
plt.show()
