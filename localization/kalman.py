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

class KalmanEnvir(Envir):
    def __init__(self,A,gauss,bounds=(512,512)):
        super(KalmanEnvir, self).__init__(bounds)
        self.A=A
        self.gauss=Gauss()

    def update(self):
        state= np.dot(self.A,self.state)
        state+=self.gauss()
        self.set_state(state)

class Gauss(object):
    def __init__(self,mean,cov):
        self.mean=mean
        self.cov=cov

    def __call__():
        a=np.random.multivariate_normal(self.mean,self.cov)
        return a


class View(object):
    def __init__(self,envir,scale=512):
        self.envir=envir

    def on_click(self,point): 
        self.envir.set_state(point)
        print(self.envir.state)

    def on_key(self,key):
        if(self.envir.has_state()):
            self.envir.update()

    def show(self,window):
        window.fill((0,0,0))
        state=self.envir.state
        if(not (state is None)):
            pg.draw.circle(window,(0,0,128),state,10)

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
    A=np.array(get_rotation(1))#[[0.5,0.9],[1,1]])
    return KalmanEnvir(A)

def get_rotation(theta):
    A=np.array([[np.cos(theta),-np.sin(theta)],
                [np.sin(theta),np.cos(theta)]])
    return A

view=View(get_envir())
loop(view)