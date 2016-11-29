import numpy as np
from pySophus import *
from Optimization.Solver import *


class ThreeDimensionalPointsAdjuster:
    def __init__(self, unchangedPoints, changedPoints):
        self.Original = unchangedPoints
        self.Changed = changedPoints

    # Point transformation function
    def __T(self, P, vector):
        algebra = se3(vector=vector)
        return algebra.exp() * P

    # Jacobian matrix of point transformation function
    def __JT(self, P, vector):
        Q = self.__T(P, vector)
        j = np.zeros((3, 6))
        m = so3(vector=Q).matrix()
        j[:3, :3] = -m
        j[:3, 3:6] = np.eye(3)
        return j

    # Objective function creation function (calling this function returns the objective function)
    def __r(self):
        def function(vector):
            m = len(self.Original)
            rvalue = np.zeros(m)
            for i in range(m):
                P = self.Original[i]
                Q = self.Changed[i]
                rvalue[i] = np.linalg.norm(self.__T(P, vector) - Q) ** 2
            return rvalue

        return function

    # Jacobian of objective function creation function (calling this function returns the jacobian of objective function)
    def __Jr(self):
        def function(vector):
            m = len(self.Original)
            jvalue = np.zeros((m, 6))
            for i in range(m):
                P = self.Original[i]
                Q = self.Changed[i]
                diff = self.__T(P, vector) - Q
                jt = self.__JT(P, vector)
                jvalue[i] = jt.T.dot(diff)
            return jvalue

        return function

    def solve(self, maxSteps=20, startingValue=np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]), precision=1e-10, k=1):
        gn = GaussNewton(f=self.__r(), J=self.__Jr(), args=startingValue, precision=precision,
                         maxSteps=maxSteps, k=k)
        result = gn.solve()
        return result
