import numpy as np
import pygame as pg

class Envir(object):
    def __init__(self,bounds=(512,512)):
        self.state=None
        self.bounds=bounds
        self.half_bounds=[int(dim_i/2) 
                for dim_i in self.bounds]

    def has_state(self):
        return not (self.state is None)
    
    def get_state(self):
        if(self.has_state()):
            return [ cord_i+self.half_bounds[i] 
               for i,cord_i in enumerate(self.state)] 
        return None

    def set_state(self,state):
        self.state=self.bound_state(state)

    def state_norm(self):
        return np.linalg.norm(self.state)
    
    def update(self):
        print(self.state)

    def observe(self):
        return self.state

    def bound_state(self,state):
        new_state=[]
        for i in (0,1):
            cord_i=state[i]
            if(cord_i > self.half_bounds[i]):
                cord_i=  (int(cord_i) % self.half_bounds[i])
                cord_i=  -(self.half_bounds[i]-cord_i)
            if(cord_i <  -self.half_bounds[i]):
                cord_i=  (int(-cord_i) % self.half_bounds[i])
#            if(state[i]<0):
#               cord_i*=(-1)
            new_state.append(cord_i)
        return new_state

class Gauss(object):
    def __init__(self,mean=None,cov=None):
        if(mean is None):
            mean=np.zeros((2,))
        if(cov is None):
            cov=np.identity(2)
        self.mean=mean
        self.cov=cov

    def __call__(self):
        return np.random.multivariate_normal(self.mean,self.cov)

class AffineTransform(object):
    def __init__(self,A=None,b=None):
        if(A is None):
            A=np.identity(2)
        if(b is None):
            b=np.zeros((2,))
        self.A=A 
        self.b=b

    def __call__(self,x):
        return np.dot(self.A,x)+self.b

    def op(self,P):
        return np.dot(np.dot(self.A,P),self.A.T)

def get_rotation(theta):
    A=np.array([[np.cos(theta),-np.sin(theta)],
                [np.sin(theta),np.cos(theta)]])
    return A