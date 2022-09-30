import numpy as np
import pygame as pg
import show

class MotionEnvir(object):
    def __init__(self,det_t=5):
        self.state=None
        self.F=np.identity(4)
        self.det_t=det_t

    def no_state(self):
        return (self.state is None)
    
    def get_state(self):
        if(self.no_state()):
            self.state=np.ones((4,))
        return self.state

    def __call__(self,u):
        theta=self.state[2]
        B=[[self.det_t*np.cos(theta),0],
           [self.det_t*np.sin(theta),0],
           [0,self.det_t],
           [1,0]]
        B=np.array(B)   
        self.state=np.dot(self.F,self.state)+np.dot(B,u)

class MotionControler(object):
    def __init__(self,envir):
        self.envir=envir

    def on_click(self,point):
        print(point)
        self.envir([1,0])

    def on_key(self,key):
        print(key)
        self.envir([0,1])

    def show(self,window):
        window.fill((0,0,0))
        state=self.envir.get_state()[:2]
        if(not (state is None)):
            pg.draw.circle(window,(0,0,128),state,10)

model=MotionEnvir()
show.loop(MotionControler(model))