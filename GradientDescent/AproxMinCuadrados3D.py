import numpy as np
from pySophus import *
from Solver import *

Original = np.array([[1, 1, 1],
                     [1, 3, 1],
                     [3, 3, 1],
                     [3, 1, 1],
                     [1, 1, 3],
                     [1, 3, 3],
                     [3, 3, 3],
                     [3, 1, 3],
                     [0, 0, 0],
                     [0.2, 1.5, 3.6],
                     [1.4, 2.67, 1.69],
                     [2.4, 2.35, 3.056]])

tfAlgebra = se3(vector=np.array([0.3, 0.0, 0.0, 0.0, 0.0, 0.0]))
tfGroup = tfAlgebra.exp()
Changed = tfGroup * Original


def T(P, vector):
    algebra = se3(vector=vector)
    return algebra.exp() * P


def JT(P, vector):
    Q = T(P, vector)
    algebra = se3(vector=vector)
    g = algebra.generators()
    j = np.array([[], [], []])
    for a in g:
        p = specialDotMatrix(a, Q)
        p = np.reshape(p, (len(Q), 1))
        j = np.concatenate((j, p), axis=1)
    return j


def E():
    def function(algebra):
        j = np.array([0.0, 0.0, 0.0])
        for i in range(len(Original)):
            diff = T(Original[i], algebra) - Changed[i]
            j = j + diff
        return j

    return function


def JE():
    def function(algebra):
        j = np.zeros((3, 6))
        for i in range(len(Original)):
            j = j + JT(Original[i], algebra)
        return j

    return function


point = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
gn = GaussNewton(f=E(), J=JE(), args=point, precision=0.0000000, maxSteps=4000)
result = gn.solve()
print(result)
print("Let's test")
resultM = se3(vector=result).exp().matrix()
realM = tfAlgebra.exp().matrix()
print(resultM - realM)
print("A ver los puntos")
resultC = se3(vector=result).exp() * Original
print(Changed)
print(resultC)
print(Changed-resultC)