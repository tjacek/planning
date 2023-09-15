import numpy as np

class Gauss1D(object):
    def __init__(self,mean=0.0,std=1.0):
        self.mean=mean
        self.std=std

    def sample(self):
        return np.random.normal(loc=self.mean, 
                                scale=self.std, 
                                size=None)
    
    def dim(self):
        return 1

    def __call__(self,x):
        Z= 1/(self.std *np.sqrt(2*np.pi))
        return np.exp(-0.5*((x-self.mean)/self.std)**2)

    def __str__(self):
        return f'Gauss:mean{self.mean},std:{self.std}'

class GaussMulti(object):
    def __init__(self,mean=5,cov=None):
        if(type(mean)==int):
            mean=np.zeros((mean,))
        if(type(cov)==int):
            cov=np.identity(cov)
        if(cov is None):
            cov=np.identity(len(mean))
        self.mean=mean
        self.cov=cov

    def dim(self):
        return len(self.mean)

    def sample(self):
        return np.random.multivariate_normal(self.mean,self.cov)
    
    def __call__(self,x):
        sigma=np.linalg.inv(self.cov)
        e= (x-self.mean) @ sigma @ (x-self.mean)
        Z= np.sqrt(((2*np.pi)**self.dim())*np.linalg.det(self.cov))
        return np.exp(-0.5*e)/Z 