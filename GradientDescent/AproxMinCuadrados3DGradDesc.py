import numpy as np
from pySophus import *
from Solver import *

Original = np.random.randint(low=-50, high=50, size=(20, 3))

tfAlgebra = se3(vector=np.array([0.3, -0.6, 0.75, -5.0, 1.0, 0.0]))
tfGroup = tfAlgebra.exp()
Changed = tfGroup * Original


def T(P, vector):
    algebra = se3(vector=vector)
    return algebra.exp() * P


def JT(P, vector):
    Q = T(P, vector)
    j = np.zeros((3, 6))
    m = so3(vector=Q).matrix()
    j[:3, :3] = -m
    j[:3, 3:6] = np.eye(3)
    return j


def E():
    def function(algebra):
        j = np.zeros((1, 3))
        for i in range(len(Original)):
            diff = T(Original[i], algebra) - Changed[i]
            j = j + diff
        return j

    return function


def gE():
    def function(vector):
        g = np.zeros(6)
        for i in range(len(Original)):
            P = Original[i]
            diff = T(P, vector) - Changed[i]
            j = JT(P, vector)
            g = g + j.T.dot(diff).T
        return g

    return function


point = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
gn = GradientDescent(dF=gE(), args=point, precision=0.0000001, maxSteps=4000**2, k = 0.00005)
result = gn.solve()
print("result:", result)
matrix=se3(vector=result).exp().matrix()
print("matrix:", matrix)
print("goodMatrix:", tfGroup.matrix())
print("point:", specialDotMatrix(matrix,Original))
print("goodPoint:",Changed)