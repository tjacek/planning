import numpy as np
import pygame as pg

class Envir(object):
    def __init__(self,bounds=(512,512)):
        self.state=None
        self.bounds=bounds
    
    def has_state(self):
        return not (self.state is None)
    
    def set_state(self,state):
        self.state=[]
        for i in (0,1):
            mult_i=int(state[i]/self.bounds[i])
            value_i=state[i]
            if(mult_i):
                value_i-=(mult_i*self.bounds[i])
            self.state.append(value_i)

    def update(self):
        print(self.state)

    def observe(self):
        return self.state

class KalmanEnvir(Envir):
    def __init__(self,A=None,b=None,
            H=None,c=None,
            noise=None,obs_noise=None,
            bounds=(512,512)):
        if(A is None):
            A=np.identity(2)
        if(b is None):
            b=np.ones((2,))
        if(H is None):
            H=np.identity(2)
        if(c is None):
            c=np.zeros((2,))
        if(noise is None):
            noise=Gauss()
        if(obs_noise is None):
            obs_noise=Gauss()            
        super(KalmanEnvir, self).__init__(bounds)
        self.A=A
        self.b=b
        self.H=H 
        self.c=c
        self.noise=noise
        self.obs_noise=obs_noise

    def update(self):
        state= np.dot(self.A,self.state)
        print(state)
        state+=self.b
        state+=self.noise()
        self.set_state(state)

    def observe(self):
        obs_state=np.dot(self.H,self.state)
        obs_state+=self.c
        obs_noise=self.obs_noise()
        print(f"obs_noise:{obs_noise}")
        obs_state+=obs_noise
        return obs_state

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

class View(object):
    def __init__(self,envir,alg=None):
        self.envir=envir
        self.obs_state=None
        self.alg=alg

    def on_click(self,point): 
        self.envir.set_state(point)
        print(self.envir.state)

    def on_key(self,key):
        if(self.envir.has_state()):
            self.envir.update()
            self.obs_state= self.envir.observe()

    def show(self,window):
        window.fill((0,0,0))
        state=self.envir.state
        if(not (state is None)):
            pg.draw.circle(window,(0,0,128),state,10)
        if(not (self.obs_state is None)):   
            pg.draw.circle(window,(0,128,0),self.obs_state,5)
        if(not (self.alg is None)):
            estm_state=self.alg(self.envir,self.obs_state)
            pg.draw.circle(window,(128,0,0),estm_state,5)

class KalmanFilter(object):
    def __init__(self,n=2):
        self.estm_state=np.random.rand(n)

    def __call__(self,envir,obs_state):
        self.estm_state= np.dot(envir.A,self.estm_state) + envir.b
        return self.estm_state

def loop(view):
    bounds=view.envir.bounds
    window = pg.display.set_mode(bounds)
    clock = pg.time.Clock()
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONUP:
                point = pg.mouse.get_pos()
                view.on_click(point)
            if event.type == pg.KEYDOWN:
                view.on_key(event.key)
        view.show(window)
        pg.display.flip()
        clock.tick(3)
    pg.quit()

def get_envir():
    b=np.array([10,6])
    mean=np.array([2,2])
    cov=np.array([[10,0.3],[0.4,10]])
    noise=Gauss(mean=mean,cov=cov)
    obs_noise=Gauss(cov=cov)
    return KalmanEnvir(b=b,noise=noise,obs_noise=obs_noise)

def get_rotation(theta):
    A=np.array([[np.cos(theta),-np.sin(theta)],
                [np.sin(theta),np.cos(theta)]])
    return A

view=View(get_envir(),alg=KalmanFilter())
loop(view)