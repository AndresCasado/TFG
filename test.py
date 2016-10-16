from visual import *
import numpy as np
from pySophus import *
import MathOps as mo

x = np.linspace(-10, 10, 20 + 1)

pList = []
for i in x:
    for j in x:
        pList.append([i, j, 0])

points(pos=pList)

testPoint = np.array([0, 6, 0])
x = np.linspace(0, 2 * np.pi, 121)
p = testPoint
for i in x:
    algebra = se3(vector=np.array([0.2, 0, 0, 0, 5, 0]))
    group = algebra.exp()
    gMatrix = group.matrix()
    p = mo.exDot(gMatrix, p)
    sphere(pos=p, radius=0.2, color=color.red)
