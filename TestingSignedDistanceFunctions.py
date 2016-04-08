import numpy as np

def circulo(x,y,r):
    return np.square(x)+np.square(y)-np.square(r)

rango = np.arange(-5, 5, 1/2)
matriz = np.eye(len(rango))
for i in rango:
    for j in rango:
        matriz[i,j]=circulo(i,j,1)

print(matriz)