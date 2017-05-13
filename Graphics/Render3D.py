from SDF.Shape import *
from SDF.Map import Map
from visual import *
import numpy as np
from pySophus import *

camera = np.array([0, -100, 0])
factor = 16
frameSizeX = 16 * factor
frameSizeY = 9 * factor

s = Sphere(radius=70)
c = RoundBoxUnsigned(size=np.array([1, 1, 1]) * 60)
firstrotation = se3(vector=np.array([0, 0, 1, 0, 0, 0]))
secondrotation = se3(vector=np.array([0, 0, 0, 0, 0, 0]))
sum = firstrotation + secondrotation
tM = firstrotation.exp().matrix()
t = Transformation(tM, c)

m = Map()
# m.add(s)
m.add(t)


def render():
    for i in (np.linspace(0, frameSizeX, frameSizeX + 1) - (frameSizeX / 2)):
        print(i)
        for j in np.linspace(0, frameSizeY, frameSizeY + 1) - (frameSizeY / 2):
            try:
                dist = m.rayMarching(camera, np.array([i, -80, j]) - camera)
                col = color.red
            except ValueError:
                col = color.blue
            box(pos=(i, j, 0), color=col)
    rate(60)


render()
