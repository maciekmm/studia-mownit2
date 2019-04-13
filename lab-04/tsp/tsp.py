import math
from copy import copy, deepcopy
from time import sleep
import matplotlib.pyplot as plt

import numpy as np
import random

REPORT_EVERY = 5000


def generate_points(n, minp, maxp):
    return np.array([(random.randint(minp, maxp), random.randint(minp, maxp)) for _ in range(n)])


def generate_points_normal(n, minp, maxp):
    return np.array(list(zip(np.random.normal(size=n) * maxp, np.random.normal(size=n))))


def draw(title, original: np.ndarray, points: np.ndarray, costs=None):
    plt.clf()
    plt.subplot(2, 1, 1)
    # plt.yscale('log')
    x = [i * REPORT_EVERY for i in range(len(costs))]
    plt.plot(x, costs)
    plt.subplot(2, 2, 3)
    # plt.yscale('linear')
    plt.scatter(*zip(*original))
    plt.subplot(2, 2, 4)
    plt.plot(*zip(*points))
    plt.savefig('./output/result-{}-{}-{}-{}.png'.format(title, len(points), cost(points), len(costs)))


def distance_squared(p1, p2):
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


def cost(perm):
    return sum(map(lambda x: distance_squared(*x), zip(perm, perm[1:])))


def consecutive_swap(perm):
    a = random.randrange(0, len(perm) - 1),
    return a[0], (a[0] + 1)


def arbitrary_swap(perm):
    a, b = random.randrange(0, len(perm)), random.randrange(0, len(perm))
    return tuple(sorted([a, b]))


def next_permutation_cost(perm, cost):
    # a, b = random.randrange(0, len(perm)), random.randrange(0, len(perm))
    # a, b = tuple(sorted([a, b]))
    a, b = consecutive_swap(perm)
    if a == b:
        return a, b, cost

    new_cost = cost
    if a != 0:
        new_cost -= distance_squared(perm[a - 1], perm[a])
        new_cost += distance_squared(perm[a - 1], perm[b])

    if b != len(perm) - 1:
        new_cost -= distance_squared(perm[b], perm[b + 1])
        new_cost += distance_squared(perm[a], perm[b + 1])

    if abs(a - b) != 1:
        new_cost -= distance_squared(perm[a], perm[a + 1])
        new_cost += distance_squared(perm[b], perm[a + 1])
        new_cost -= distance_squared(perm[b - 1], perm[b])
        new_cost += distance_squared(perm[b - 1], perm[a])

    return a, b, new_cost


def acceptance_probability(cp, cn, temp):
    if cn < cp:
        return 1.0

    return math.exp((cp - cn) / temp)


def anneal(temp, perm, max_it):
    costs = []
    # best, best_cost = perm, cost(perm)
    cp = cost(perm)
    for i in range(max_it):
        a, b, cn = next_permutation_cost(perm, cp)

        ap = acceptance_probability(cp, cn, temp)

        if temp < 20:
            return perm, costs

        if ap > random.random():
            perm[[a, b]] = perm[[b, a]]
            cp = cn
            # if cn < best_cost:
            #     best = copy(perm)
            #     best_cost = cn

        if i % REPORT_EVERY == 0:
            costs.append(cp)
            print(cp, ap, temp, i)

        temp = temp / 1.00001
    return perm, costs


if __name__ == "__main__":
    for n in [10, 30, 100]:
        pre = generate_points(n, 0, 100)
        perm, costs = anneal(cost(pre) / math.log10(n), pre, int(1000000))
        draw("uniform", pre, perm, costs)


    for n in [10, 30, 100]:
        pre = generate_points_normal(n, 0, 100)
        perm, costs = anneal(cost(pre) / math.log10(n), pre, int(1000000))
        draw("normal", pre, perm, costs)

    seg_size = 150
    for n in [10, 25]:
        points = []
        for i in range(3):
            for j in range(3):
                for point in [[point[0] + 2 * i * seg_size, point[1] + j * (seg_size + 5 * seg_size)] for
                              point in
                              generate_points(n, 0, seg_size)]:
                    points.append(point)
        random.shuffle(points)
        points = np.array(points)
        perm, costs = anneal(cost(points) * n, points, int(100000000))
        draw("islands", points, perm, costs)
        exit()
