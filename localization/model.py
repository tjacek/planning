import numpy as np
import show,utils

class MotionEnvir(object):
    def __init__(self,det_t=1,noise=None,obs_noise=None):
        if(noise is None):
            noise=utils.Gauss()
        if(obs_noise is None):
            obs_noise=utils.Gauss()          
        self.state=None
        self.F=np.identity(4)
        self.F[3][3]=0
        self.det_t=det_t
        self.noise=noise
        self.obs_noise=obs_noise

    def empty_state(self):
        return (self.state is None)
    
    def get_state(self):
        if(self.empty_state()):
            self.state=np.ones((4,))
        return self.state

    def act(self,u):
        B=self.get_B()
        self.state= (self.F @ self.state)+ (B @ u)

    def observe(self):
        obs_state= np.dot(self.get_H(),self.get_state())
        obs_state[:2]+= self.obs_noise()
        return obs_state

    def get_B(self):
        theta=self.state[2]
        B=[[self.det_t*np.cos(theta),0],
           [self.det_t*np.sin(theta),0],
           [0,self.det_t],
           [1,0]]
        B=np.array(B) 
        return B

    def jacobian_f(self,state):
        theta,v=self.state[2:]
        j=np.identity(4)
        j[0][3]= -v*np.sin(theta)*self.det_t
        j[0][4]=  np.cos(theta)*self.det_t
        j[1][3]= v*np.cos(theta)*self.det_t
        j[1][4]= np.sin(theta)*self.det_t
        return j

    def get_H(self):
        H=np.zeros((2,4))
        H[0][0]=1
        H[1][1]=1
        return 0

    def jacobian_h(self,state):
        return self.get_H()

    def __str__(self):
        s=f'x:{self.state[0]:4f}'
        s+=f'y:{self.state[1]:4f}'
        s+=f'theta:{self.state[2]:4f}'
        s+=f'v:{self.state[3]:4f}'
        return s

class ExtendedKalman(object):
    def __init__(self,envir):
        self.estm_state=np.random.rand(n)
        self.estm_cov=np.random.rand(n,n)

    def __call__(self,envir,x,u):
        x_pred= np.dot(envir.F,x)
        x_pred+= np.dot(envir.get_B(),u)

        J_f= envir.jacobian_f(x)
        P_pred= np.dot(J_f,self.estm_cov)
        P_pred= np.dot(P_pred,J_f.T)+envir.noise()

        z_pred= np.dot(self.get_H(),x_pred)
        z=envir.observe()

        y= z - z_pred