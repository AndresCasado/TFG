import numpy


def function(P):
    x = P[0]
    y = P[1]
    return x * x + 2 * y * y - + 3 * x - 5 * y + 5


def derivative(P):
    x = P[0]
    y = P[1]
    return numpy.array((2 * x + 3, 4 * y - 5))


def minimumByGradientDescent(start, step, precission):
    point = derivative(start)
    while (numpy.linalg.norm(derivative(point)) > precission):
        point = point - step * derivative(point)
        print(point)
    return point


P = numpy.array([0, 0])
x = minimumByGradientDescent(P, 0.1, 0.000000001)
print("x es " + str(x))
