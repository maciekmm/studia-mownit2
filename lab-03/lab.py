from decimal import *
import math
import numpy as np

funs = [(lambda x: (Decimal(math.cos(x)) * Decimal(math.cosh(x)) - 1),
         lambda x: Decimal(-math.cosh(x) * math.sin(x) + math.cos(x) * math.sinh(x)),
         3 / 2 * math.pi, 2 * math.pi),

        (lambda x: 1 / x + Decimal(math.tan(x)),
         lambda x: -1 / (x * x) + (1 / Decimal(math.cos(x))) ** 2,
         math.pi, math.pi / 2),

        (lambda x: Decimal(2) ** (-x) * Decimal(math.e) ** x * 2 * Decimal(math.cos(x)) - 6,
         lambda x: Decimal(math.e) ** x - Decimal(2) ** (-x) * Decimal(math.log(2, math.e)) - 2 * Decimal(math.sin(x)),
         1.7, 1.9)]

# getcontext().prec = 28
getcontext().Emax = 100000000000000000000


def bisect(f, der, a, b, eps=Decimal(1e-8), max=1e4):
    # assert np.sign(f(a)) * np.sign(f(b)) < 0
    c = a + (b - a) / 2
    res = f(c)
    c = 0
    it = 0
    while abs(res) > eps and it < max:
        c = a + (b - a) / 2
        res = f(c)
        a, b = (a, c) if np.sign(f(a)) * np.sign(res) < 0 else (c, b)
        it += 1
    return (c, it) if it < max else (None, max)


def newton(f, der, x, y=None, eps=Decimal(1e-8), max=1e6):
    res = x
    it = 0
    while abs(f(res)) > eps and it < max:
        res = res - f(res) / der(res)
        it += 1
    return (res, it) if it < max else (None, max)


def secant(f, x, y, eps=Decimal(1e-8), max=1e5):
    xnm1 = x
    xn = y
    it = 0
    while abs(f(xn)) > eps and it < max and xnm1 != xn:
        res = xn - f(xn) / ((f(xn) - f(xnm1)) / (xn - xnm1))
        # print(res)
        xnm1, xn = xn, res
        it += 1
    return (res, it) if it < max and xnm1 != xn else (None, max)


for fun, derivative, a, b in funs:
    print("Bisekcja: ", bisect(fun, derivative, Decimal(a), Decimal(b)))
    print("Newton: ", newton(fun, derivative, Decimal(a), Decimal(b)))
    print("Secant: ", secant(fun, Decimal(a), Decimal(b)))
    print("")
