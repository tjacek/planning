import numpy as np
import pygame as pg
import show

class MotionEnvir(object):
    def __init__(self,det_t=5,noise=None,
        obs_noise=None):
        if(noise is None):
            noise=envir.Gauss()
        if(obs_noise is None):
            obs_noise=envir.Gauss()          
        self.state=None
        self.F=np.identity(4)
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
        B=self.get_B(self,u)
        self.state=np.dot(self.F,self.state)+np.dot(B,u)
    
    def observe(self):
        obs_state= np.dot(self.H,self.get_state())
        obs_noise+=self.obs_noise()
        return obs_noise

    def get_B(self,u):
        theta=self.state[2]
        B=[[self.det_t*np.cos(theta),0],
           [self.det_t*np.sin(theta),0],
           [0,0.2*self.det_t],
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

class MotionControler(object):
    def __init__(self,envir,bounds=(256,256)):
        self.envir=envir
        self.bounds=np.array(bounds)
        self.scale=[1.0,1.0]

    def get_bounds(self):
        return 2*self.bounds

    def on_click(self,point):
        print(point)
        self.envir.act([1,0])

    def on_key(self,key):
        if(not self.envir.empty_state()):
            print(self.envir.get_state())

            self.envir.act([0,np.pi/4])

    def show(self,window):
        window.fill((0,0,0))
        x,y=self.envir.get_state()[:2]
        state=[self.rescale(x,0)*x,self.rescale(y,1)*y]
        state= self.translate(state)
        state=np.array(state)
        pg.draw.circle(window,(0,0,128),state,10)
        self.draw_lines(window,step=self.scale[0]*64,horiz=True)
        self.draw_lines(window,step=self.scale[1]*64,horiz=False)

    def translate(self,state):
        state=[state_i+bound_i 
            for state_i,bound_i in zip(state,self.bounds)]
        return np.array(state)

    def rescale(self,cord,i):
        if( cord<-self.bounds[i] or 
          self.bounds[i]<cord):
            self.scale[i]=0.9*(self.bounds[i]/np.abs(cord))
        else:
            self.scale[i]=1
        return self.scale[i]

    def draw_lines(self,window,step=64,horiz=True,color=(0,128,0)):
        bounds=self.get_bounds()
        n_lines= int(bounds[0]/step)    
        for i in range(n_lines):
            x_i= i*step
            if(horiz):
                start,end=(0,x_i),(bounds[0],x_i)
            else:
                start,end=(x_i,0),(x_i,bounds[1])
            pg.draw.line(window,color,start,end)

model=MotionEnvir()
show.loop(MotionControler(model))