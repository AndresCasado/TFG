from visual import *
import numpy as np
from pySophus import *
import SDF.MathOps as mo


def dibujo():
    x = np.linspace(-10, 10, 20 + 1)

    pList = []
    for i in x:
        for j in x:
            pList.append([i, j, 0])

    points(pos=pList)

    testPoint = np.array([0, 0, 0])
    x = np.linspace(0, 2 * np.pi, 51)
    p = testPoint
    algebra = se3(vector=np.array([0, 0, 0.2, 0.1, 0.2, 0]))
    group = algebra.exp()
    gMatrix = group.matrix()
    print(gMatrix)
    for i in x:
        sphere(pos=p, radius=0.2, color=color.red)
        print(p)
        p = mo.exDot(gMatrix, p)
        print("")


def optimizacion():
    import Optimization.Solver as solver
    originalPoints = np.array([[0, 0], [0, 2], [2, 2], [2, 0]])
    algebra = se2(vector=np.array([np.pi/6,1,0.3]))
    group = algebra.exp()
    mat = group.matrix()
    changedPoints = mo.exDot(mat,originalPoints)
    def gradE(algebra):
        pass
    #gradientDescent = solver.Optimization(Df,args)

def test():
    x = np.linspace(-10,10,6)/3.0
    for i in x:
        for j in x:
            for k in x:
                for a in x:
                    for b in x:
                        for c in x:
                            v = np.array([i,j,k,a,b,c])
                            aa = se3(vector = v)
                            v2 = np.array([2*i,2*j,2*k,2*a,2*b,2*c])
                            bb = se3(vector = v2)
                            cc = aa + aa
                            if np.linalg.norm((cc-bb).vector())>0.000001:
                                print("ta mal")
                                print(v)
                                print("")
                            else:
                                print("ta bien")
test()