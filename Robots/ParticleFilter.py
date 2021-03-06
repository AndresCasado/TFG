from Util import MathOps as mo

from Robots.SimulatedRobot import *
from SDF.Map import Map
from SDF.Shape import *


class Particle(SimulatedRobot):
    def __init__(self, p, theta, error=0, weight=1):
        SimulatedRobot.__init__(self, p, theta, error)
        self.weight = weight

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return SimulatedRobot.__str__(self) + " with w: " + str(self.weight)

    def undrawParticle(self):
        self.myBox.visible = False

class ParticleFilter:
    def __init__(self, sdfmap, realRobot, minX=-20, maxX=20, minY=-20, maxY=20, numOfBots=100):
        self.sdfmap = sdfmap
        self.realRobot = realRobot
        self.simulatedRobots = []
        self.error = realRobot.error
        self.N = numOfBots
        valuesX = np.linspace(start=minX, stop=maxX, num=np.sqrt(numOfBots))
        valuesY = np.linspace(start=minY, stop=maxY, num=np.sqrt(numOfBots))
        for x in valuesX:
            for y in valuesY:
                self.simulatedRobots.append(Particle(np.array([x, y]), 0, self.error))

    def updateWeights(self):
        realScan = self.realRobot.scan2D(self.sdfmap)

        correction = mo.gaussian(0, self.error, 0)
        for particle in self.simulatedRobots:
            simulatedScan = particle.scan(self.sdfmap)
            probM = 1
            probD = 1
            for i in range(len(realScan)):
                real = realScan[i]
                simulated = simulatedScan[i]
                a = mo.gaussian(real, self.error, simulated) / correction
                a = np.exp(-np.abs(real-simulated))
                probM *= a
                probD /= a
            particle.weight = np.log(probM)
        self.simulatedRobots.sort(key=lambda b: b.weight, reverse=True)

    def resample(self):
        weights = map(lambda a: a.weight, self.simulatedRobots)
        totalSum = sum(weights)
        newRobots = list(self.simulatedRobots)

        for particle in newRobots:
            particle.weight *= (self.N / totalSum)

        self.simulatedRobots = []
        for particle in newRobots:
            for i in range(int(round(particle.weight))):
                new = Particle(particle.p, particle.theta, particle.error, particle.weight)
                self.simulatedRobots.append(new)

    def move(self, distance):
        self.realRobot.forward(distance)
        for p in self.simulatedRobots:
            p.forward(distance + random.gauss(0, self.error))

    def getCalculatedPosition(self):
        weights = map(lambda a: a.weight, self.simulatedRobots)
        totalSum = sum(weights)
        newRobots = list(self.simulatedRobots)

        result = np.array([0.0, 0.0])

        for particle in newRobots:
            particle.weight *= 1 / totalSum
            result += particle.p * particle.weight

        return result

    def oneIteration(self, distance=5):
        self.move(distance)
        self.updateWeights()
        self.resample()


if __name__ == "__main__":
    c = Sphere(radius=3)
    s = Box(size=[5,5])
    t = Transformation(M=mo.get2DTransformationMatrix(30, -4, np.pi / 3), thing=s)
    m = Map()
    m.add(c)
    m.add(s)

    robot = SimulatedRobot(np.array([6, 6]), 0, error=2)

    pf = ParticleFilter(m, robot, minX=4, maxX=8, minY=4, maxY=8, numOfBots=5 ** 2)
    for i in range(40):
        print "Iteracion " + str(i)
        pf.oneIteration(distance=2)
        print "Robot en " + str(pf.realRobot)
        print "Calculado " + str(pf.getCalculatedPosition())
        print ""
        print ""
