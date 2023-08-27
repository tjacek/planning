import numpy as np
import show,utils

class Experiment(object):
    def __init__(self,envir,alg):
        self.envir=envir
        self.alg=alg

    def __call__(self,u):
        true_state=self.envir.get_state()
        obs_state=self.envir.observe()
        pred_state=self.alg(self.envir,obs_state,u)
        self.envir.act(u)
        return true_state,obs_state,pred_state

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

    def jacobian_f(self):
        theta,v=self.state[2:]
        det_t=self.det_t
        J_f=[[1,0,-v*np.sin(theta)*det_t,np.cos(theta)*det_t],
             [0,1, v*np.cos(theta)*det_t,np.sin(theta)*det_t],
             [0,0,1,0],
             [0,0,0,1]]
        return np.array(J_f)

    def get_H(self):
        H=[[1,0,0,0],
           [0,1,0,0]]
        return np.array(H)

    def jacobian_g(self):
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
    def __init__(self,n=4):
        self.estm_state=np.random.rand(n)
        self.estm_cov=np.random.rand(n,n)
        self.I=np.identity(n)

    def __call__(self,envir,z,u):
        x_pred=envir.F @ self.estm_state + envir.get_B() @ u
        J_f= envir.jacobian_f()
        P_pred= J_f @ self.estm_cov @ J_f.T
       
        z_pred= envir.get_H() @ x_pred
        y = z - z_pred
        
        J_g= envir.jacobian_g()
        S =J_g @ P_pred @ J_g.T  +envir.obs_noise.cov

        K = P_pred @ J_g.T @ np.linalg.inv(S)

        self.estm_state= x_pred + K @ y
        self.estm_cov = (self.I - K @ J_g) @ P_pred
        return  self.estm_state