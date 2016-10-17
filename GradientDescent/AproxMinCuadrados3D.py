import numpy as np
import SDF.MathOps as mo

np.array([[1,1,1],
          [1,3,1],
          [3,3,1],
          [3,1,1],
          [1,1,3],
          [1,3,3],
          [3,3,3],
          [3,1,3]])


Original = [A, B, C, D]
Changed = [AA, BB, CC, DD]


def T(P, theta, tx, ty):
    result = np.dot(mo.get2DTransformationMatrix(tx, ty, theta), np.array([P[0], P[1], 1]))
    return np.array([result[0], result[1]])


def dT(P, theta, tx, ty):
    return np.array([[-P[0] * np.sin(theta) - P[1] * np.cos(theta), 1, 0],
                     [P[0] * np.cos(theta) + P[0] * np.sin(theta), 0, 1]])


def E(P, Q, theta, tx, ty):
    return np.linalg.norm(T(P, theta, tx, ty) - Q)


def dE(P, Q, theta, tx, ty):
    dif = T(P, theta, tx, ty) - Q
    norm = E(P, Q, theta, tx, ty)
    derivadaTheta = np.array([[-np.sin(theta), np.cos(theta)],
                              [np.cos(theta), -np.sin(theta)]])
    dAlpha = np.dot(dif, np.dot(derivadaTheta, P))
    dTx = dif[0] / norm
    dTy = dif[1] / norm
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


result = minimumByGradientDescent(np.array((0, 0, 0)), .001, 0.0000001)
print(result)


print("lets see if everything is ok")
for p in Original:
    test = np.dot(mo.get2DTransformationMatrix(result[1],result[2],result[0]),np.array([p[0],p[1],1]))
    print(test)