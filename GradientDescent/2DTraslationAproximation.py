import numpy
from Solver import *

P = numpy.array((1, 2))
Q = numpy.array((150, -900))


def T(P, args):
    return P + args


def E(P, Q):
    def function(args):
        return numpy.linalg.norm(T(P, args) - Q)

    return function


def dE(P, Q):
    def function(args):
        dif = T(P, args) - Q
        return dif

    return function


args = np.array([0, 0])
gradientDescent = GradientDescent(args=args, dF=dE(P, Q), k=0.1)
gaussNewton = GaussNewton(J=dE(P, Q), args=args)
result = gradientDescent.solve()
print("Gradient:" + str(result))
result = gaussNewton.solve()
print("GaussNewton:" + str(result))
