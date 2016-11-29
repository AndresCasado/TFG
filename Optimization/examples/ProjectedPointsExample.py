from Optimization.ProjectedPointsAdjuster import *
from pySophus import *

c = Camera(1)

points = np.random.random_integers(-100, 100, (20, 3)) + [0, 0, 102]

projectedPoints = np.zeros((20, 2))

for i in range(len(projectedPoints)):
    projectedPoints[i] = c.projectPoint(points[i])

tfAlgebra = se3(vector=np.array([0.3, -0.5, 0.15, 1.2, -0.69, -2.35]))
tfGroup = tfAlgebra.exp()

points = tfGroup * points

ppa = ProjectedPointsAdjuster(points, projectedPoints, c)

result = ppa.solve()

print(result)
