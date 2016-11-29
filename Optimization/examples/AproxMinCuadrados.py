import numpy as np
import SDF.MathOps as mo
from Optimization.Solver import *

Original = np.array([[1, 1],
                     [1, 2],
                     [2, 3],
                     [3, 3],
                     [3, 1]])

transform = mo.get2DTransformationMatrix(0.2, -0.2, 0.1)

Changed = np.dot(transform, np.append(Original.T, np.ones((1, len(Original))), axis=0))
Changed = Changed[0:len(Changed) - 1, ...]
Changed = Changed.__T


def T(P, args):
    result = np.dot(mo.get2DRotationMatrix(args[0]), P) + args[1:2]
    return result


def E(P, Q):
    def function(args):
        return np.linalg.norm(T(P, args) - Q)

    return function


def acumulador(f):
    def function(args):
        e = 0
        for i in range(len(Original)):
            e += f(Original[i], Changed[i])(args)
        return e

    return function


def dE(P, Q):
    def function(args):
        dif = T(P, args) - Q
        theta = args[0]
        derivadaTheta = np.array([[-np.sin(theta), np.cos(theta)],
                                  [-np.cos(theta), -np.sin(theta)]])
        dAlpha = -np.dot(dif, np.dot(derivadaTheta, P))
        dTx = dif[0]
        dTy = dif[1]
        return np.array([dAlpha, dTx, dTy])

    return function


# '''
def minimumByGradientDescent(start, step, precision):
    global norm
    keepDoing = True
    params = start
    from visual import *
    points(pos=Original, color=color.green)
    points(pos=Changed, color=color.blue)

    try:
        while (keepDoing):
            rate(60)
            dETotal = acumulador(dE)(params)
            params = params - step * dETotal

            test = []
            for a in Original:
                test.append(T(a, params))
            points(pos=test, color=color.yellow)
            z = acumulador(dE)(params)
            sphere(pos=(params[1], params[0], 0), radius=0.1, color=color.red)

            print("params" + str(params))
            print(np.linalg.norm(dETotal))
            if np.linalg.norm(dETotal) < .01:
                print("mn")
            keepDoing = np.linalg.norm(dE(Original[i], Changed[i])(params)) > precision
    except ValueError:
        print("error " + str(keepDoing))
    return np.array(params)


list = []
for xxx in np.linspace(-4, 4, num=100):
    for theta in np.linspace(-4, 2, num=100):
        e = 0
        for i in range(len(Original)):
            e += E(Original[i], Changed[i])(np.array([theta, xxx, 0]))
            print(e)
        list.append((xxx, theta, e))
list = np.array(list)
norm = np.max(list, axis=0)
norm = norm[2]
list[:, 2] = list[:, 2] / norm
from visual import rate, points, color

rate(60)
colores = np.ones(list.shape)
colores[:, 0] = 1 - list[:, 2]
colores[:, 1] = 1 - list[:, 2]
colores[:, 2] = 1 - list[:, 2]
points(pos=list, color=colores)
# '''

args = np.array([0, 0, 0])
gradientDescent = GradientDescent(acumulador(E), args, acumulador(dE), k=0.001, precision=0.5)
# result = gradientDescent.calculate()
result = minimumByGradientDescent(args, .03, 0.1)
print(result)

print("lets see if everything is ok")
for p in Original:
    test = np.dot(mo.get2DTransformationMatrix(result[1], result[2], result[0]), np.array([p[0], p[1], 1]))
    print(test)
print(Changed)
