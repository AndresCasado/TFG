from __future__ import division, print_function

from JoinFunctions import *
from Shape import *
from SimulatedRobot import *
from visual import *

from Map import *

m = Map()
c = Circle(3)
s = Square(np.array([2, 2]))
s = Transformation(mo.get2DTransformationMatrix(3,0,np.pi/3),s)
j = Join(c, s, softExponentialUnion(10))
m.add(j)

m.drawMap(40, 40)

steps = 10

import time

startTime = time.time()
robot = SimulatedRobot(np.array([np.random.randint(-20, 20), np.random.randint(-20, 20)]), 0)

for i in range(steps):
    box(pos=robot.p, color=(1 - i / steps, 0 + i / steps, 0))
    arrow(pos=(robot.p[0], robot.p[1], 1), axis=(np.cos(robot.theta), np.sin(robot.theta), 0))
    p = robot.scan(m, relative=False, cost=0.3, scanPoints=True)
    q = []
    for point in p:
        q.append(np.append(point, 1))
    myPoints = points(pos=q, color=(1 - i / steps, 0 + i / steps, 0))
    rate(1)
    robot.forward(2)
    robot.rotate(np.pi / 4)
finishTime = time.time()
print(finishTime - startTime)
