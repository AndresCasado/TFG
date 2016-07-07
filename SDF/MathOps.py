import numpy as np

def get2DTransformationMatrix(tx,ty,theta):
    return np.array([[np.cos(theta),-np.sin(theta),tx],[np.sin(theta),np.cos(theta),ty],[0,0,1]])

def get2DRotationMatrix(theta):
    return np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]])

if __name__=="__main__":
    rot = get2DTransformationMatrix(1,1,np.pi/4)
    point = np.array([2,2])
    point = np.append(point,[1])
    invrot = np.linalg.inv(rot)
    print(invrot.dot(point.T))