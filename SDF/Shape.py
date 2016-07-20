from __future__ import division

import numpy as np


class Shape:
    def distance(self,p):
        return np.power(2,62)

class ViejoSquare(Shape):
    def __init__(self, width=1, height=1, centerX=0, centerY=0, angle=0):
        self.width = width
        self.height = height
        self.centerX = centerX
        self.centerY = centerY
        self.angle = angle

    def distance(self,p):
        x = p[0]
        y = p[1]

        difX = np.abs(self.centerX - x) / (self.width / 2)
        difY = np.abs(self.centerY - y) / (self.height/2)

        return np.maximum(difX*np.cos(self.angle)-difY*np.sin(self.angle), difX*np.sin(self.angle)+difY*np.cos(self.angle)) - 1
        #return np.power(x,30)+np.power(y,30)-1
class Square(Shape):
    def __init__(self,size,r=0):
        self.size=size
        self.r=r

    def distance(self,p):
        d = np.abs(p)-self.size
        v = np.array([])
        for i in range(len(d)):
            v = np.append(v,max(d[i],0))
        return np.linalg.norm(v)-self.r

class Circle(Shape):
    def __init__(self,radius=1):
        self.radius=radius

    def distance(self,p):
        return np.linalg.norm(p) - self.radius

class Transformation(Shape):

    def __init__(self,M,thing):
        self.M = M
        self.Mi = np.linalg.inv(self.M)
        self.thing = thing

    def distance(self,p):
        point = np.append(p,1)
        point = np.dot(self.Mi,point)
        return self.thing.distance(np.delete(point,len(point)-1))

class Join(Shape):
    def __init__(self,thing1,thing2,operation):
        self.thing1 = thing1
        self.thing2 = thing2
        self.operation = operation

    def distance(self,p):
        return self.operation(self.thing1.distance(p),self.thing2.distance(p))