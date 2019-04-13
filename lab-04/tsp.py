import math
from time import sleep

import numpy as np
import random


def generate_points(n, minp, maxp):
    return np.array([(random.randint(minp, maxp), random.randint(minp, maxp)) for _ in range(n)])


def distance_squared(p1, p2):
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


def cost(perm):
    return sum(map(lambda x: distance_squared(*x), zip(perm, perm[1:])))

def next_permutation(perm):
    a = random.randint(0, len(perm)-1)
    b = random.randint(0, len(perm)-1)
    perm[a], perm[b] = perm[b], perm[a]
    return perm

def acceptance_probability(permutation, new_permutation, temp):
    cn = cost(new_permutation)
    cp = cost(permutation)
    if cn < cp:
        return 1.0

    return math.exp((cp - cn) / temp)

def anneal(temp, perm, max_it):
    for i in range(max_it):
        new = next_permutation(np.copy(perm))
        ap = acceptance_probability(perm, new, temp)
        if ap == 0:
            return
        if ap > random.random():
            perm = new
        print(cost(perm))
        temp = temp / 1.02


if __name__ == "__main__":
    anneal(100000000.0, generate_points(100, 0, 100), int(1000000))

