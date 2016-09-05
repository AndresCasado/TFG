import numpy as np
import Util.MathOps as mo

A = np.array((2, 2))
B = np.array((5, 2))
C = np.array((5, 5))
D = np.array((2, 5))
AA = np.array((7.77, 4.45))
BB = np.array((9.44, 1.95))
CC = np.array((11.94, 3.62))
DD = np.array((10.27, 6.11))

Original = [A, B, C, D]
Changed = [AA, BB, CC, DD]


def T(P, theta, tx, ty):
    result = np.dot(mo.get2DTransformationMatrix(tx, ty, theta), np.array([P[0], P[1], 1]))
    return np.array([result[0], result[1]])


def dT(P, Q, theta, tx, ty):
    return np.array([1, 1])


def E(P, Q, theta, tx, ty):
    return np.linalg.norm(T(P, theta, tx, ty) - Q)


def dE(P, Q, theta, tx, ty):
    dif = T(P, theta, tx, ty) - Q
    # norm = np.linalg.norm(dif)
    dRotMat = mo.get2DRotationMatrix(theta)
    dAlpha = 2 * np.dot(np.dot(dRotMat, P), dif)
    dTx = 2 * dif[0]
    dTy = 2 * dif[1]
    return np.array((dAlpha, dTx, dTy))


def minimumByGradientDescent(start, step, precission):
    keepDoing = True
    params = start
    try:
        while (keepDoing):
            dETotal = np.array((0, 0, 0))
            for i in range(len(Original)):
                dETotal = dETotal + dE(Original[i], Changed[i], params[0], params[1], params[2])
            params = params - step * dETotal
            print(params)
            keepDoing = np.linalg.norm(dETotal) > precission
    except ValueError:
        print("error " + str(keepDoing))
    return np.array(params)


result = minimumByGradientDescent(np.array((0, 0, 0)), .01, 0.001)
print(result)
