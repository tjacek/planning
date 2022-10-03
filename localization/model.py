import numpy as np
import pygame as pg
import show

class MotionEnvir(object):
    def __init__(self,det_t=5):
        self.state=None
        self.F=np.identity(4)
        self.det_t=det_t

    def empty_state(self):
        return (self.state is None)
    
    def get_state(self):
        if(self.empty_state()):
            self.state=np.ones((4,))
        return self.state

    def __call__(self,u):
        theta=self.state[2]
        B=[[self.det_t*np.cos(theta),0],
           [self.det_t*np.sin(theta),0],
           [0,0.2*self.det_t],
           [1,0]]
        B=np.array(B)   
        self.state=np.dot(self.F,self.state)+np.dot(B,u)

class MotionControler(object):
    def __init__(self,envir,bounds=(256,256)):
        self.envir=envir
        self.bounds=np.array(bounds)
        self.scale=[1.0,1.0]

    def get_bounds(self):
        return 2*self.bounds

    def on_click(self,point):
        print(point)
        self.envir([1,0])

    def on_key(self,key):
        if(not self.envir.empty_state()):
            print(self.envir.get_state())

            self.envir([0,np.pi/4])

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
#            if(state_i)
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