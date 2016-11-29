import numpy as np
from pySophus import *
from Optimization.Solver import GaussNewton


class ProjectedPointsAdjuster:
    def __init__(self, Original, Projected, camera):
        self.Original = Original
        self.Projected = Projected
        self.camera = camera

    def __T(self, P, vector):
        algebra = se3(vector=vector)
        return algebra.exp() * P

    def __JT(self, P, vector):
        Q = self.__T(P, vector)
        j = np.zeros((3, 6))
        m = so3(vector=Q).matrix()
        j[:3, :3] = -m
        j[:3, 3:6] = np.eye(3)
        return j

    def __r(self):
        def function(vector):
            m = len(self.Original)
            rvalue = np.zeros(m)
            for i in range(m):
                P = self.Original[i]
                Q = self.Projected[i]
                rvalue[i] = np.linalg.norm(self.camera.projectPoint(self.__T(P, vector)) - Q) ** 2
            return rvalue

        return function

    def __Jr(self):
        def function(vector):
            m = len(self.Original)
            jvalue = np.zeros((m, 6))
            for i in range(m):
                P = self.Original[i]
                Q = self.Projected[i]
                Tp = self.__T(P, vector)
                diff = self.camera.projectPoint(Tp) - Q
                jt = self.__JT(P, vector)
                jpi = self.camera.Jacobian(Tp)
                j = jpi.dot(jt)
                jvalue[i] = j.T.dot(diff)
            return jvalue

        return function

    def solve(self, maxSteps=20, startingValue=np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]), precision=1e-10, k=1):
        gn = GaussNewton(f=self.__r(), J=self.__Jr(), args=startingValue, precision=precision, maxSteps=maxSteps, k=k)
        result = gn.solve()
        return result


class Camera:
    def __init__(self, fx, fy=None):
        self.fx = fx
        self.fy = fy if fy is not None else fx

    def projectPoint(self, P):
        x, y, z = P
        return np.array([x * self.fx / z, y * self.fy / z])

    def Jacobian(self, P):
        x, y, z = P
        return np.array([[self.fx / z, 0, - x * self.fx / (z ** 2)],
                         [0, self.fy / z, -y * self.fy / (z ** 2)]])
