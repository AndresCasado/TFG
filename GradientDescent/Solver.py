from __future__ import division
import numpy as np


class Solver(object):
    def solve(self):
        pass


class GradientDescent(Solver):
    def __init__(self, dF, args, k=0.001, precision=1 / np.power(10, 10), maxSteps=500):
        self.dF = dF
        self.args = args
        self.k = k
        self.precision = precision
        self.maxSteps = maxSteps

    def solve(self):
        result = self.args
        for i in range(self.maxSteps):
            value = self.dF(result)
            norm = np.linalg.norm(value)
            if norm < self.precision:
                break
            else:
                result = result - self.k * value
        return result


class GaussNewton(Solver):
    def __init__(self, f, J, args, k=0.001, precision=1 / np.power(10, 10), maxSteps=500):
        self.f = f
        self.J = J
        self.args = args
        self.k = k
        self.precision = precision
        self.maxSteps = maxSteps

    def solve(self):
        result = self.args
        for i in range(self.maxSteps):
            matrix = self.J(result)
            fvalue = self.f(result)
            value = result - np.dot(np.linalg.pinv(np.dot(matrix.T, matrix)), np.dot(matrix.T, fvalue))
            norm = np.linalg.norm(fvalue.dot(fvalue))
            if norm < self.precision:
                break
            else:
                result = value
        return result
