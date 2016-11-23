from Optimization.Solver import GaussNewton
import numpy as np


def Jfacil(args):
    return np.array([[1, 1], [-1, 2]])


def ffacil(args):
    point = np.array(args)
    return np.array([point[0] + point[1] - 3, -point[0] + 2 * point[1] - 4])


point = np.array([3009.5, 52360.4])
gn = GaussNewton(f=ffacil, J=Jfacil, args=point)

print(gn.solve())


def Jdificil(args):
    x, y = args
    return np.array([[2 * x + y - 2, x - 6 * y + 5], [-4 * x - y * y + 3, -2 * x * y]])


def fdificil(args):
    x, y = args
    return np.array([x * x + x * y - 3 * y * y - 2 * x + 5 * y - 30, -2 * x * x - x * y * y + 3 * x + 15])


gn = GaussNewton(f=fdificil, J=Jdificil, args=point)

result = gn.solve()
print(result)
print(fdificil(result).dot(fdificil(result)))
