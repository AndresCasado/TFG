import numpy
from Solver import *

P = numpy.array((1, 2))
Q = numpy.array((150563.456, -9950.5))


def F(P):
    def function(args):
        return P + args

    return function


def E(P, Q):
    def function(args):
        return F(P)(args) - Q

    return function


def dE(P, Q):
    def function(args):
        dif = F(P)(args) - Q
        return dif

    return function


def JE(P, Q):
    def function(args):
        return np.eye(2)

    return function


point = np.array([0, 0])

gradientDescent = GradientDescent(args=point, dF=dE(P, Q), k=0.1)
result = gradientDescent.solve()
print("Gradient: " + str(result))

gaussNewton = GaussNewton(f=E(P, Q), J=JE(P, Q), args=point)
result = gaussNewton.solve()
print("Gauss-Newton: " + str(result))
