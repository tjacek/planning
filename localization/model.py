import numpy as np

class MotionModel(object):
    def __init__(self,det_t=5):
    	self.F=np.identity(4)
    	self.det_t=det_t

    def __call__(self,x,u):
        theta=x[2]
        B=[[self.det_t*np.cos(theta),0],
           [self.det_t*np.sin(theta),0],
           [0,self.det_t],
           [1,0]]
        B=np.array(B)	
        return np.dot(self.F,x)+np.dot(B,u)

model=MotionModel()
print(model([7,6,5,3],[2,1]))