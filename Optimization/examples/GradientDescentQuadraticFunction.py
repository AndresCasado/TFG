import numpy

def function(x):
    return 3*x*x-2*x+1

def derivative(x):
    return 6*x-2

def gradientDescent(start,step):
    value = derivative(start)
    while(abs(derivative(value))>0.0000000001):
        value = value - step*derivative(value)
        print(value)
    return value

x = gradientDescent(2,0.1)
print("x es " + str(x))