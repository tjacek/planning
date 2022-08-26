import numpy as np
import pygame as pg
import show,envir

class KalmanEnvir(envir.Envir):
    def __init__(self,A=None,H=None,
            noise=None,obs_noise=None,
            bounds=(512,512)):
        if(A is None):
            A=envir.AffineTransform()
        if(H is None):
            H=envir.AffineTransform()
        if(noise is None):
            noise=envir.Gauss()
        if(obs_noise is None):
            obs_noise=envir.Gauss()            
        super(KalmanEnvir, self).__init__(bounds)
        self.A=A
        self.H=H 
        self.noise=noise
        self.obs_noise=obs_noise

    def update(self):
        state= self.A(self.state)
        print(state)
        state+=self.noise()
        self.set_state(state)

    def observe(self):
        obs_state= self.H(self.state)
        obs_noise=self.obs_noise()
        print(f"obs_noise:{obs_noise}")
        obs_state+=obs_noise
        return obs_state

class KalmanFilter(object):
    def __init__(self,n=2):
        self.estm_state=np.random.rand(n)
        self.estm_cov=np.random.rand(n,n)

    def __len__(self):
        return self.estm_state.shape[0]

    def __call__(self,envir,obs_state):
        x= envir.A(obs_state) 
        F,Q=envir.A,envir.obs_noise.cov
        P=envir.A.op(self.estm_cov)+Q 
        y=obs_state - envir.H(x)
        S= envir.H.op(P)+envir.obs_noise.cov
        K=np.dot(np.dot(P,envir.H.A.T),np.linalg.inv(S))
        x=x + np.dot(K,y)
        det_P=(np.identity(len(self)) - np.dot(K,envir.H.A))
        self.estm_cov=np.dot(det_P,P)
        y= obs_state - np.dot(envir.H(x),x)
        self.estm_state=x
        return y

def get_envir(delta_t=4,sigma=4):
    A=envir.AffineTransform(np.array([[1,delta_t],[0,1]]) )
    Q=np.array([[0.25*delta_t**4,0.5*delta_t**3],
         [0.5*delta_t**3,delta_t**2]])
    noise=envir.Gauss(cov=Q)
    return KalmanEnvir(A=A,noise=noise)

view=show.View(get_envir(),alg=KalmanFilter())
show.loop(view)