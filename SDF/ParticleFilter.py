import numpy as np
from SimulatedRobot import *
from Map import Map
from Shape import *
import MathOps as mo


class ParticleFilter:
    def __init__(self, sdfmap, realRobot, minX=-20, maxX=20, minY=-20, maxY=20, numOfBots=100):
        self.sdfmap = sdfmap
        self.realRobot = realRobot
        self.simulatedPositions = np.array([])
        self.error = realRobot.error
        valuesX = np.linspace(start=minX, stop=maxX, num=np.sqrt(numOfBots))
        valuesY = np.linspace(start=minY, stop=maxY, num=np.sqrt(numOfBots))
        for x in valuesX:
            for y in valuesY:
                self.simulatedPositions = np.append(self.simulatedPositions, np.array([x, y]))
        self.simulatedPositions = self.simulatedPositions.reshape((-1, 2))

    def test(self):

        realScan = self.realRobot.scan(self.sdfmap)

        result = np.array([[]])
        correction = mo.gaussian(0, self.error, 0)
        for p in self.simulatedPositions:
            r = SimulatedRobot(p, 0, error=self.error)
            simulatedScan = r.scan(self.sdfmap)
            prob = 1
            for i in range(len(realScan)):
                real = realScan[i]
                simulated = simulatedScan[i]
                a = mo.gaussian(real, self.error, simulated) / correction
                prob *= a
            #if prob > 0.001:
            result = np.append(result, [p, prob])
        result = result.reshape((-1,2))
        return result


if __name__ == "__main__":
    c = Circle(radius=3)
    m = Map()
    m.add(c)

    robot = SimulatedRobot(np.array([6, 6]), 0, error=0.5)

    badScan = robot.scan(m)
    goodScan = robot.scan(m)
    prob = 1
    c = mo.gaussian(0, robot.error, 0)
    for i in range(len(badScan)):
        a = badScan[i]
        b = goodScan[i]
        errorprob = mo.gaussian(b, robot.error, a) / c
        prob *= errorprob

    print "end"


    """pf = ParticleFilter(m, robot, minX=5, maxX=7, minY=5,maxY=7, numOfBots=100)
    resultado = pf.test()
    print resultado[:,1]"""
