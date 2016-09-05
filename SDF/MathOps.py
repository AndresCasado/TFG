import numpy as np

def get2DTransformationMatrix(tx,ty,theta):
    return np.array([[np.cos(theta), -np.sin(theta), tx],
                     [np.sin(theta), np.cos(theta), ty],
                     [0, 0, 1]])

def get2DRotationMatrix(theta):
    return np.array([[np.cos(theta), -np.sin(theta)],
                     [np.sin(theta), np.cos(theta)]])

def gaussian(mu, sigma, x):
    # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
    return np.exp(- ((mu - x) ** 2) / (2 * sigma ** 2)) / np.sqrt(2.0 * np.pi * (sigma ** 2))

def vectorOfDirection(theta):
    return np.array([np.sin(theta), np.cos(theta)])