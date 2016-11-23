from __future__ import division, print_function

from Robots.SimulatedRobot import *
from SDF.JoinFunctions import *
from SDF.Map import *
from SDF.Shape import *

m = Map()
c = Circle(3)
s = Square(np.array([3, 3]))

tfMatrix = se2(vector=np.array([np.pi / 4, 10, 0])).exp().matrix()
s = Transformation(tfMatrix, s)

j = Join(c, s, softPolynomialUnion(3.0))
m.add(j)

m.drawMap(20, 20)

steps = 10

import time

startTime = time.time()
robotM = se2(vector=np.array([0, 0, 0])).exp().matrix()
robot = SimulatedRobot(robotM, 0)

from visual import *

for i in range(steps):
    rate(60)
    box(pos=robot.position(), color=(1 - i / steps, 0 + i / steps, 0))
    vx = np.array([1, 0, 0])
    robotV = robot.direction()
    arrow(pos=np.append(robot.position(), 1), axis=np.append(robotV, 0))
    p = robot.scan2D(m, relative=False, cost=0.3, scanPoints=True)
    q = []
    for point in p:
        q.append(np.append(point, 1))
    myPoints = points(pos=q, color=(1 - i / steps, 0 + i / steps, 0))
    robot.forward(2)
    robot.rotate(np.pi / 4)
finishTime = time.time()
print(finishTime - startTime)
