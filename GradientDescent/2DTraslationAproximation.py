import numpy


P = numpy.array((1,2))
Q = numpy.array((150,-540))

def T(traslation):
    return P+traslation

def dT(traslation):
    return numpy.array((1,1))

def E(traslation):
    return numpy.linalg.norm(T(traslation) - Q)

def dE(traslation):
    dif = T(traslation) - Q
    norm = E(traslation)
    return numpy.array([dif[0], dif[1]])

def minimumByGradientDescent(start, step, precission):
    traslation = dE(start)
    while(E(traslation)>precission):
        traslation = traslation - step*dE(traslation)
        print("traslation es" + str(traslation) + " y la derivada es " + str(dE(traslation)))
    return traslation


result = minimumByGradientDescent(numpy.array((0,0)), 0.1, 0.0000000001)
print(result)