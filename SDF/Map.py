import numpy as np
import MathOps as mo


class Map:
    def __init__(self, maxDist=100, maxIterations=1000, epsilon=1e-10):
        self.things = []
        self.maxDist = maxDist
        self.maxIterations = maxIterations
        self.epsilon = epsilon

    def add(self, thing):
        self.things.append(thing)

    def SDF(self, p):
        dist = self.maxDist
        for thing in self.things:
            dist = min(dist, thing.distance(p))
        return dist

    def JSDF(self, p):
        delta = 1e-5
        result = np.zeros_like(p, dtype=float)
        for i in range(len(result)):
            pointRight = np.array(p)
            pointRight[i] += delta
            pointLeft = np.array(p)
            pointLeft[i] -= delta
            result[i] = (self.SDF(pointRight) - self.SDF(pointLeft)) / delta
        return result

    def rayMarching(self, p, v, border=0.0001):
        t = 0
        v = mo.normalize(v)
        d = self.SDF(p)
        for i in range(self.maxIterations):
            newP = p + v * t
            d = self.SDF(newP)
            if (d > self.maxDist) or (np.absolute(d - border) < self.epsilon):
                break
            t += d - border
        if not (d > self.maxDist):
            return t
        else:
            raise ValueError("No point found")

    def drawMap(self, width, height, definition=50):
        from visual import rate, box
        for i in np.linspace(-width / 2, width / 2, num=definition):
            rate(60)
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

if __name__=='__main__':
    m = Map()
    import Shape
    s = Shape.Box(np.array([20., 10.]))
    d = s.distance(np.array([2,3]))
    print(d)
    m.add(s)
    jsdf = m.JSDF(np.array([2,3.]))
    print(jsdf)