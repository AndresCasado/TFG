from __future__ import division
import numpy as np

EPSILON = 1e-16


def union():
    def calc(x, y):
        return np.minimum(x, y)

    return calc


def softExponentialUnion(r=5):
    assert not r == 0

    def calc(x, y):
        res = np.exp(-r * x) + np.exp(-r * y)
        return -np.log(res) / r

    return calc


def softPolynomialUnion(r):
    def calc(x, y):
        a = np.clip(0.5 + 0.5 * (y - x) / r, 0, 1)
        return a * x + (1 - a) * y - r * a * (1 - a)

    return calc


def intersection():
    def calc(x, y):
        return np.maximum(x, y)

    return calc


def difference():
    def calc(x, y):
        return np.maximum(x, -y)

    return calc


def softExponentialDifference(r=5):
    assert not r < EPSILON

    def calc(x, y):
        res = np.exp(r * x) + np.exp(-r * y)
        return np.log(res) / r

    return calc
