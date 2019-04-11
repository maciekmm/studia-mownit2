import numpy as np
from mpl_toolkits.mplot3d import axes3d, Axes3D  # <-- Note the capitalization!
import matplotlib.pyplot as plt

fig = plt.figure()


def sphere():
    s = np.linspace(0, 2 * np.pi, 50)
    t = np.linspace(0, np.pi, 50)

    x = np.outer(np.cos(s), np.sin(t))
    y = np.outer(np.sin(s), np.sin(t))
    z = np.outer(np.ones(s.shape), np.cos(t))
    return x, y, z


def create_axis(a, n, title):
    ax = fig.add_subplot(a, a, n, projection='3d')
    ax.axis('equal')
    ax.set_zlim(-1, 1)
    ax.set_xlim(-1, 1)
    ax.set_title(title)
    ax.set_ylim(-1, 1)
    return ax


def draw_sphere_with_transformation(
        ax, transformation, draw_axis
):
    x, y, z = sphere()
    if ax is not None:
        apply_linear_transformation(x, y, z, transformation)
    ax.plot_surface(x, y, z, linewidth=0.0, cstride=stride, rstride=stride, alpha=0.5)
    if draw_axis:
        # axis
        u, s, v = np.linalg.svd(A)
        U, V, W = zip(*v)
        C = np.zeros(3)
        ax.quiver(C, C, C, U, V, W)
    return x, y, z


def apply_linear_transformation(x, y, z, A):
    for s in range(x.shape[0]):
        for t in range(x.shape[1]):
            v = np.array([x[s, t], y[s, t], z[s, t]])
            x[s, t], y[s, t], z[s, t] = tuple(np.dot(A, v))


if __name__ == "__main__":
    grid = 3
    stride = 2
    draw_sphere_with_transformation(create_axis(grid, 1, "Sphere"), np.identity(3), False)

    # A, B, C = np.random.rand(3, 3), np.random.rand(3, 3), np.random.rand(3, 3)
    A = [[1, 0.25, 1],
         [0, 1, 0],
         [0.1, 1, 1]]
    draw_sphere_with_transformation(create_axis(grid, 2, "Ellipsoid"), A, True)

    # find matrix with eigenvalues ratio > 100
    while True:
        B = np.random.rand(3, 3)
        _, s, _ = np.linalg.svd(B)
        if s[0] / s[2] < 100:
            continue
        draw_sphere_with_transformation(create_axis(grid, 3, "Eigenratio: {:.2f}".format(s[0] / s[2])), B, True)
        break

    u, s, v = np.linalg.svd(A)
    for i, transformation in enumerate([v, s[..., None] * v, u @ (s[..., None] * v)]):
        draw_sphere_with_transformation(create_axis(grid, 4 + i, ""), transformation, True)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
