import numpy as np
from pySophus import *
from Optimization.Solver import *
from Optimization.ThreeDimensionalPointAdjuster import ThreeDimensionalPointsAdjuster as threeDPA

# Random points creation
limit = 50
numberofpoints = 50
Original = np.random.randint(low=-limit, high=limit, size=(numberofpoints, 3))

# Transformation creation
tfAlgebra = se3(vector=np.array([0.3, -0.6, 0.75, -5.0, 1.0, 0.0]))

# Transform points
tfGroup = tfAlgebra.exp()
Changed = tfGroup * Original

# Adding random error
mean = 0.0
error = 0.001
OriginalR = Original + np.random.normal(loc=mean, scale=error, size=Original.shape)
ChangedR = Changed + np.random.normal(loc=mean, scale=error, size=Changed.shape)


startingvalue = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
something = threeDPA(Original, Changed)
resultDos = something.solve()

print(resultDos)
