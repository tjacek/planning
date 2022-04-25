import numpy as np

class Envir(object):
    def __init__(self,A,B,C,cov_v,cov_w):
        self.A=A 
        self.B=B 
        self.C=C
        self.cov_v=cov_v
        self.cov_w=cov_w 
        self.state=None

    def set_state(self,state):
    	self.state=state

    def next_state(self):
    	self.state=self.A.dot(self.state)

    def observe(self):
        return self.C.dot(self.state)