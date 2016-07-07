import Map, SimulatedRobot.SimulatedRobot, numpy as np

class ParticleFilter:
    def __init__(self, sdfmap, realRobot, minX=-50, maxX=50, minY=-50, maxY=50):
        self.sdfmap = sdfmap
        self.realRobot = realRobot
        self.simulatedRobots = []
        for x in np.linspace(start=minX,stop=maxX,num=20):
            for y in np.linspace(start=minY, stop=maxY, num=20):
                robot = SimulatedRobot(np.array([x, y]), 0)
                self.simulatedRobots.append(robot)