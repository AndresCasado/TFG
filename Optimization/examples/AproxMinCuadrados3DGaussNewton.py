import numpy as np
from pySophus import *
from Optimization.Solver import *

# Random points creation
limit = 5000
numberofpoints = 5000
Original = np.random.randint(low=-limit, high=limit, size=(numberofpoints, 3))

# Transformation creation
tfAlgebra = se3(vector=np.array([0.3, -0.6, 0.75, -5.0, 1.0, 0.0]))

# Transform points
tfGroup = tfAlgebra.exp()
Changed = tfGroup * Original

# Adding random error
mean = 0.0
error = 0.1
Original = Original + np.random.normal(loc=mean, scale=error, size=Original.shape)
Changed = Changed + np.random.normal(loc=mean, scale=error, size=Changed.shape)


# Point transformation function
def T(P, vector):
    algebra = se3(vector=vector)
    return algebra.exp() * P


# Jacobian matrix of point transformation function
def JT(P, vector):
    Q = T(P, vector)
    j = np.zeros((3, 6))
    m = so3(vector=Q).matrix()
    j[:3, :3] = -m
    j[:3, 3:6] = np.eye(3)
    return j


# Objective function creation function (calling this function returns the objective function)
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


# Jacobian of objective function creation function (calling this function returns the jacobian of objective function)
def Jr():
    def function(vector):
        m = len(Original)
        jvalue = np.zeros((m, 6))
        for i in range(m):
            P = Original[i]
            Q = Changed[i]
            diff = T(P, vector) - Q
            jt = JT(P, vector)
            jvalue[i] = jt.T.dot(diff)
        return jvalue

    return function


startingvalue = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
gn = GaussNewton(f=r(), J=Jr(), args=startingvalue, precision=1e-10, maxSteps=2000, k=0.7)
result = gn.solve()
print(result)
