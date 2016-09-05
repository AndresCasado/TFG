import numpy as np

maxDist = 10000


class Map:
    def __init__(self):
        self.things = []

    def add(self, thing):
        self.things.append(thing)

    def SDF(self, p):
        dist = maxDist
        for thing in self.things:
            dist = min(dist, thing.distance(p))
        return dist

    def JSDF(self, p, delta=0.0001):
        ex = np.array([delta, 0])
        ey = np.array([0, delta])
        dx = (self.SDF(p) - self.SDF(p - ex)) / delta
        dy = (self.SDF(p) - self.SDF(p - ey)) / delta
        return np.array([dx, dy])

    def rayMarching(self, p, v, minimum=0.0001):
        t = 0
        maxDistance = 1000
        for i in range(1000):
            newP = p + v * t
            d = self.SDF(newP)
            if (d > maxDistance) or (np.absolute(d - minimum) < 0.0001):
                break
            t += d - minimum
        if not (d > maxDistance):
            return t
        else:
            raise ValueError("No point found")

    def drawMap(self, width, height, definition=50):
        from visual import rate, box
        rate(1)
        for i in np.linspace(-width / 2, width / 2, num=definition):
            for j in np.linspace(-height / 2, height / 2, num=definition):
                point = np.array([j, i])
                d = self.SDF(point)
                if d > 0:
                    color = (d / 10, d / 10, d / 10)
                else:
                    color = (1 - d, 1 - d * width, 0)
                theBox = box(pos=point, color=color)
                theBox.size = (0.4, 0.4, 0.4)
                theBox.z -= np.abs(d)