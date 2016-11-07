import random

import numpy as np

import MathOps as mo

from pySophus import *


class SimulatedRobot:
    def __init__(self, matrix, error=0):
        self.matrix = matrix
        self.error = error

    def __exDot(self, point):
        return mo.exDot(self.matrix, point)

    def direction(self):
        return self.__exDot(np.array([1, 0]))-self.position()

    def position(self):
        return self.__exDot(np.array([0, 0]))

    def copy(self):
        return SimulatedRobot(self.matrix, self.error)

    def drawRobot(self):
        from visual import box, arrow
        self.box = box(pos=self.position(), color=(0, 1, 0))
        self.arrow = arrow(pos=np.append(self.position, 1), axis=np.append(self.direction(), 0))

    def undrawRobot(self):
        self.box.visible = False
        self.arrow.visible = False

    def forward(self, distance):
        a = se2(vector=np.array([0, distance, 0]))
        self.__transform(a)

    def __transform(self, algebra):
        self.matrix = np.dot(self.matrix, algebra.exp().matrix())

    def rotate(self, alpha):
        a = se2(vector=np.array([alpha, 0, 0]))
        self.__transform(a)

    def scan(self, sdfmap, steps=180, relative=True, cost=0.0001, scanPoints=False):
        result = []
        theta = SE2(self.matrix).log().vector()[0]
        for i in range(steps):
            angle = theta + 2 * i * np.pi / steps
            v = mo.vectorOfDirection(angle)
            try:
                distance = sdfmap.rayMarching(self.position(), v, minimum=cost) + random.gauss(0, self.error)
                point = self.position() + distance * v
                if relative:
                    point = mo.exDot(np.linalg.inv(self.M), point)
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
