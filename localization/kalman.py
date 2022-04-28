import pygame as pg
import numpy as np
from scipy.stats import special_ortho_group

class View(object):
    def __init__(self,envir,scale=512):
        self.envir=envir
        self.scale=scale

    def on_click(self,key):
        self.envir.next_state()
        print(self.envir.state)

    def show(self,window):
        window.fill((0,0,0))
        state=0.5*self.scale*(self.envir.state+1)
        pg.draw.circle(window,(0,0,128),state,10)

class Envir(object):
    def __init__(self,A,B,C,cov_v,cov_w):
        self.A=A 
        self.B=B 
        self.C=C
        self.cov_v=cov_v
        self.cov_w=cov_w 
        self.state=None
#        self.bounds=bounds

    def get_dim(self):
        return self.A.shape[0]

    def set_state(self,state=None):
        if(state is None):
            state=np.ones((self.get_dim(),))
        self.state=state

    def next_state(self,eps=0.001):
        self.state=self.A.dot(self.state)
        mean=np.ones((self.get_dim(),))
        self.state+=np.random.multivariate_normal(mean,self.cov_v)
        for i in range(self.get_dim()):
            if(self.state[i]>1):
                self.state[i]-=2
            if(self.state[i]<-1):
                self.state[i]+=2 #1+eps#

    def observe(self):
        return self.C.dot(self.state)

def random_envir(dim=2):
    A=special_ortho_group.rvs(dim)  #2*np.random.rand(dim,dim)
    B=np.random.rand(dim,dim)
    C=np.random.rand(dim,dim)
    cov_v=np.random.rand(dim,dim)
    cov_w=np.random.rand(dim,dim)
    envir= Envir(A,B,C,cov_v,cov_w)
    envir.set_state()
    envir.state*= 0.5
    return envir

envir=random_envir()
envir.set_state()
view=View(envir)

window = pg.display.set_mode((view.scale,view.scale))
clock = pg.time.Clock()
run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
                run = False
        if event.type == pg.MOUSEBUTTONUP:
                point = pg.mouse.get_pos()
                view.on_click(point)
#        if event.type == pg.KEYDOWN:
#            controler.on_key(event.key)
    view.show(window)
    pg.display.flip()
    clock.tick(3)
pg.quit()