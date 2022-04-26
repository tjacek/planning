import numpy as np

class Envir(object):
    def __init__(self,A,B,C,cov_v,cov_w):
        self.A=A 
        self.B=B 
        self.C=C
        self.cov_v=cov_v
        self.cov_w=cov_w 
        self.state=None

    def get_dim(self):
        return self.A.shape[0]

    def set_state(self,state):
    	self.state=state

    def next_state(self):
    	self.state=self.A.dot(self.state)

    def observe(self):
        return self.C.dot(self.state)

def random_envir(dim=3):
    A=2*np.random.rand(dim,dim)
    B=np.random.rand(dim,dim)
    C=np.random.rand(dim,dim)
    cov_v=np.random.rand(dim,dim)
    cov_w=np.random.rand(dim,dim)
    return Envir(A,B,C,cov_v,cov_w)

envir=random_envir()
print(envir.get_dim())