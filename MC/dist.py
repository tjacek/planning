import numpy as np


class Gauss1D(object):
    def __init__(self,mean=0.0,std=1.0):
        self.mean=mean
        self.std=std

    def __call__(self):
        return np.random.normal(loc=self.mean, 
                                scale=self.std, 
                                size=None)
    
    def dim(self):
        return 1

    def likehood(self,x):
        Z= 1/(self.std *np.sqrt(2*np.pi))
        return np.exp(-0.5*((x-self.mean)/self.std)**2)

    def __str__(self):
        return f'Gauss:mean{self.mean},std:{self.std}'