import numpy as np
import pygame as pg

class View(object):
    def __init__(self,envir,alg=None):
        self.envir=envir
        self.obs_state=None
        self.alg=alg

    def on_click(self,point):
        point=[cord_i-256 for cord_i in point]
#        self.envir.set_state(point)
        self.envir.state=point

    def on_key(self,key):
        if(self.envir.has_state()):
            self.envir.update()
            self.obs_state= self.envir.observe()

    def show(self,window):
        window.fill((0,0,0))
        state=self.envir.get_state()
        if(not (state is None)):
            pg.draw.circle(window,(0,0,128),state,10)
        if(not (self.obs_state is None)):
            pg.draw.circle(window,(0,128,0),self.obs_state,7)
        if(not (self.alg is None or self.obs_state is None)):
            estm_state=self.alg(self.envir,self.obs_state)
            estm_state=self.envir.bound_state(estm_state)
#            print(f"estm:{estm_state}")
            pg.draw.circle(window,(128,0,0),estm_state,5)

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