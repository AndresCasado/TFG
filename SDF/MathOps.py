import numpy as np

def exDot(matrix, exPoint):
    exPoint = np.append(exPoint,1)
    point = np.dot(matrix,exPoint)
    return point[:len(point)-1]


def gaussian(mu, sigma, x):
    # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
    return np.exp(- ((mu - x) ** 2) / (2 * sigma ** 2)) / np.sqrt(2.0 * np.pi * (sigma ** 2))

def vectorOfDirection(theta):
    return np.array([np.sin(theta), np.cos(theta)])
