import random

import numpy as np

import MathOps as mo

from pySophus import *


class SimulatedRobot:
    def __init__(self, algebra, error=0):
        self.algebra = algebra
        self.error = error

    def copy(self):
        return SimulatedRobot(self.algebra, self.error)

    def drawRobot(self):
        from visual import box, arrow
        self.box = box(pos=self.p, color=(0, 1, 0))
        self.arrow = arrow(pos=np.array([self.p[0], self.p[1], 1]), axis=(np.cos(self.theta), np.sin(self.theta), 0))

    def undrawRobot(self):
        self.box.visible = False
        self.arrow.visible = False

    def forward(self, distance):
        v = mo.vectorOfDirection(self.theta)
        self.p = self.p + distance * v

    def rotate(self, alpha):
        self.theta += alpha



    def scan(self, sdfmap, steps=180, relative=True, cost=0.0001, scanPoints=False):
        result = []
        for i in range(steps):
            angle = self.theta + 2 * i * np.pi / steps
            v = mo.vectorOfDirection(angle)
            try:
                distance = sdfmap.rayMarching(self.p, v, minimum=cost) + random.gauss(0, self.error)
                point = self.p + distance * np.array([np.sin(angle), np.cos(angle)])
                if relative:
                    point = np.dot(np.linalg.inv(self.M), np.array([[point[0]], [point[1]], [1]]))
                if scanPoints:
                    result.append(point)
                else:
                    result.append(distance)
            except ValueError:
                if not scanPoints:
                    result = np.append(result, -1)
                pass
        return np.array(result)

    def __str__(self):
        return ">>Robot at " + str(self.p) + " looking at " + str(self.theta) + "<<"

    def __repr__(self):
        return self.__str__()
