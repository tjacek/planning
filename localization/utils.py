import numpy as np

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