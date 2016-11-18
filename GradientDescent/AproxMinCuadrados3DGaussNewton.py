import numpy as np
from pySophus import *
from Solver import *

Original = np.random.randint(low=-5000, high=5000, size=(50000, 3))

tfAlgebra = se3(vector=np.array([1.6, -1.6, 6, -5.0, 1.0, -3.0]))
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


def r():
    def function(vector):
        m = len(Original)
        rvalue = np.zeros(m)
        for i in range(m):
            P = Original[i]
            Q = Changed[i]
            rvalue[i] = np.linalg.norm(T(P, vector) - Q) ** 2
        return rvalue

    return function


def Jr():
    def function(vector):
        m = len(Original)
        jvalue = np.zeros((m,6))
        for i in range(m):
            P = Original[i]
            Q = Changed[i]
            diff = T(P, vector) - Q
            jt = JT(P, vector)
            jvalue[i] = jt.T.dot(diff)
        return jvalue

    return function


point = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
gn = GaussNewton(f=r(), J=Jr(), args=point, precision=1e-32, maxSteps=4000, k=0.001)
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
print(Changed - resultC)
