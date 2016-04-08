import numpy

A = numpy.array((2,2))
B = numpy.array((5,2))
C = numpy.array((5,5))
D = numpy.array((2,5))
AA = numpy.array((7.77,4.45))
BB = numpy.array((9.44,1.95))
CC = numpy.array((11.94,3.62))
DD = numpy.array((10.27,6.11))

Original=[A,B,C,D]
Changed=[AA,BB,CC,DD]

def T(P,theta,tx,ty):
    rotMat = numpy.array([[numpy.cos(theta), -numpy.sin(theta)],
                         [numpy.sin(theta),  numpy.cos(theta)]])
    return numpy.dot(rotMat,P)+numpy.array((tx,ty))

def dT(P,Q,theta,tx,ty):
    return numpy.array((1,1))

def E(P,Q,theta,tx,ty):
    return numpy.square(numpy.linalg.norm(T(P,theta,tx,ty) - Q))

def dE(P,Q,theta,tx,ty):
    dif = T(P,theta,tx,ty) - Q
    #norm = numpy.linalg.norm(dif)
    dRotMat = numpy.array([[-numpy.sin(theta), -numpy.cos(theta)],
                         [numpy.cos(theta),  -numpy.sin(theta)]])
    dAlpha = 2*numpy.dot(numpy.dot(dRotMat,P),dif)
    dTx = 2*dif[0]
    dTy = 2*dif[1]
    return numpy.array((dAlpha,dTx,dTy))

def minimumByGradientDescent(start, step, precission):
    keepDoing = True
    params = start
    try:
        while(keepDoing):
            dETotal = numpy.array((0,0,0))
            for i in range(len(Original)):
                dETotal = dETotal + dE(Original[i],Changed[i],params[0],params[1],params[2])
            params = params - step*dETotal
            print(params)
            keepDoing = numpy.linalg.norm(dETotal)>precission
    except ValueError:
        print("error "+str(keepDoing))
    return numpy.array(params)




result = minimumByGradientDescent(numpy.array((0,0,0)), 0.001, 0.0000001)
print(result)