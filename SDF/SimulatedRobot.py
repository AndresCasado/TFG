import numpy as np

from SDF import MathOps as mo


class SimulatedRobot:

    def __init__(self,p,theta):
        self.p = p
        self.theta=theta
        self.__updateMatrix()

    def drawRobot(self):
        from visual import box,arrow
        box(pos=self.p,color=(0,1,0))
        arrow(pos=np.array([self.p[0],self.p[1],1]),axis=(np.cos(self.theta),np.sin(self.theta),0))

    def __updateMatrix(self):
        self.M = mo.get2DTransformationMatrix(self.p[0],self.p[1],self.theta)

    def move(self,distance):
        v = np.array([np.cos(self.theta),np.sin(self.theta)])
        self.p = self.p + distance*v
        self.__updateMatrix()

    def rotate(self,alpha):
        self.theta+=alpha
        self.__updateMatrix()

    def scan(self, map, steps=360, relative=True,cost=0.0001):
        result = []
        for i in range(steps):
            angle = self.theta + 2 * i * np.pi / steps
            v = np.array([np.sin(angle), np.cos(angle)])
            try:
                point = map.rayMarching(self.p, v,minimum=cost)
                if relative:
                    point = np.dot(np.linalg.inv(self.M),np.array([[point[0]],[point[1]],[1]]))
                result.append(np.array([point[0],point[1]]))
            except ValueError:
                pass
        return result