from __future__ import division
import numpy as np


class Solver(object):
    def solve(self):
        pass


class GradientDescent(Solver):
    def __init__(self, dF, args, k=0.001, precision=1 / np.power(10, 10)):
        self.dF = dF
        self.args = args
        self.k = k
        self.precision = precision

    def solve(self):
        result = self.args
        keepGoing = True
        while (keepGoing):
            value = self.dF(result)
            norm = np.linalg.norm(value)
            if norm < self.precision:
                keepGoing = False
            else:
                result = result - self.k * value
        return result


class GaussNewton(Solver):
    def __init__(self, J, args, k=0.001, precision=1 / np.power(10, 10)):
        self.J = J
        self.args = args
        self.k = k
        self.precision = precision

    def solve(self):
        result = self.args
        keepGoing = True
        while (keepGoing):
            matrix = self.J(result)
            value = result - np.dot(np.linalg.inv(np.dot(matrix.T, matrix)), np.dot(matrix.T, matrix))
            norm = np.linalg.norm(value)
            if norm < self.precision:
                keepGoing = False
            else:
                result = value
        return result
