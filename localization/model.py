import numpy as np
import show,utils

class MotionEnvir(object):
    def __init__(self,F,noise=0.1,obs_noise=0.1,det_t=1):        
        self.state=None
        self.F=F
        self.noise=noise
        self.obs_noise=obs_noise
        self.det_t=det_t

    def empty_state(self):
        return (self.state is None)
    
    def get_state(self):
        if(self.empty_state()):
            self.state=np.ones((4,))
        return self.state

    def act(self,u):
        B=self.get_B()
        self.state= (self.F @ self.state)+ (B @ u)
        return self.state

    def observe(self):
        obs_state= self.get_H() @ self.get_state()
        obs_state+= self.obs_noise()
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
        return H

    def jacobian_g(self,state):
        J_g=np.array([[1,0,0,0],
                      [0,1,0,0]])
        return J_g

    def __str__(self):
        s=f'x:{self.state[0]:4f}'
        s+=f'y:{self.state[1]:4f}'
        s+=f'theta:{self.state[2]:4f}'
        s+=f'v:{self.state[3]:4f}'
        return s

def simple_motion_model():
    Q = np.diag([0.1,0.1,np.deg2rad(1.0),1.0]) ** 2 
    R = np.diag([1.0, 1.0]) ** 2
    F=np.diag([1.0,1.0,1.0,0.0])
    return MotionEnvir(F=F,
                       noise=utils.Gauss(cov=Q),
                       obs_noise=utils.Gauss(cov=R))

class ExtendedKalman(object):
    def __init__(self,envir):
        self.estm_state=np.random.rand(n)
        self.estm_cov=np.random.rand(n,n)

    def __call__(self,envir,x,u):
        x_pred= np.dot(envir.F,x)
        x_pred+= np.dot(envir.get_B(),u)

        J_f= envir.jacobian_f(x)
        P_pred= np.dot(J_f,self.estm_cov)
        P_pred= np.dot(P_pred,J_f.T)+envir.noise.cov

        z_pred= np.dot(self.get_H(),x_pred)
        z=envir.observe()

        y= z - z_pred
        J_g= envir.jacobian_g(x)
        S= J_g @ P_pred @ J_g
