import numpy as np

class Gauss(object):
    def __init__(self,mean=None,cov=None):
        if(mean is None):
            dim=cov.shape[0]
            mean=np.zeros((dim,))
        if(cov is None):
            cov=np.identity(2)
        if(is_number(cov)):
            cov=cov*np.identity(2)
        self.mean=mean
        self.cov=cov

    def __call__(self):
        return np.random.multivariate_normal(self.mean,self.cov)
    
    def likehood(self,x):
        sigma=np.linalg.inv(self.cov) 
        return np.exp(-0.5((x-self.cov).T @ sigma @ (x-self.cov)))

    def __str__(self):
        return f'Gauss{sel.conv.shape[0]}D'
        
def is_number(var):
    return (type(var) == int or type(var) == float)

def rot_matrix(theta):
    mat=[[np.cos(theta), -np.sin(theta)],
         [np.sin(theta),  np.cos(theta)]]
    return np.array(mat)