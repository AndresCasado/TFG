import random

import numpy as np

import SDF.MathOps as mo

from pySophus import *


class SimulatedRobot:
    def __init__(self, matrix, error=0.0):
        self.matrix = np.array(matrix)
        self.dimensions = np.shape(self.matrix)[0] - 1
        self.error = error

    def direction(self):
        pointInFront = np.zeros(self.dimensions)
        pointInFront[0] = 1
        return specialDotMatrix(self.matrix, pointInFront) - self.position()

    def position(self):
        return self.matrix[:self.dimensions, self.dimensions]

    def copy(self):
        return SimulatedRobot(self.matrix, self.error)

    def drawRobot(self):
        from visual import box, arrow
        self.box = box(pos=self.position(), color=(0, 1, 0))
        self.arrow = arrow(pos=np.append(self.position(), [1]), axis=np.append(self.direction(), [0]))

    def undrawRobot(self):
        self.box.visible = False
        self.arrow.visible = False

    def forward(self, distance):
        a = se2(vector=np.array([0, distance, 0])) if self.dimensions == 2 else se3(
            vector=np.array([0, 0, 0, distance, 0, 0]))
        self.__transform(a)

    def __transform(self, algebra):
        self.matrix = np.dot(self.matrix, algebra.exp().matrix())

    def rotate(self, alpha, axis=None):
        if self.dimensions == 2:
            a = se2(vector=np.array([alpha, 0, 0]))
        else:
            if axis == None:
                raise ValueError("A 3D rotation needs an axis (3D vector)")
            v = mo.normalize(axis)
            a = se3(vector=np.append(v * alpha, [0, 0, 0]))
        self.__transform(a)

    def scan2D(self, sdfmap, steps=180, relative=True, cost=0.0001, scanPoints=False):
        result = []
        theta = SE2(self.matrix).log().vector()[0]
        for i in range(steps):
            angle = theta + 2 * i * np.pi / steps
            v = mo.vectorOfDirection(angle)
            try:
                distance = sdfmap.rayMarching(self.position(), v, border=cost) + random.gauss(0, self.error)
                point = self.position() + distance * v
                if relative:
                    point = specialDotMatrix(np.linalg.inv(self.M), point)
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
        return "SimulatedRobot at " + str(self.position()) + " with direction " + str(self.direction()) + "<<"

    def __repr__(self):
        return self.__str__()
