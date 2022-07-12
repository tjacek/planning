import pygame as pg

class Envir(object):
    def __init__(self,bounds=(512,512)):
        self.state=None
        self.bounds=bounds
    
    def set_state(self,state):
        self.state=[]
        for i in (0,1):
            mult_i=int(state[i]/self.bounds[i])
            value_i=state[i]
            if(mult_i):
                value_i-=(mult_i*self.bounds[i])
            self.state.append(value_i)

#    def get_state(self):
#        return self.current_state


class View(object):
    def __init__(self,envir,scale=512):
        self.envir=envir

    def on_click(self,point):
#        self.envir.state()
        self.envir.set_state(point)
        print(self.envir.state)

    def show(self,window):
        window.fill((0,0,0))
#        state=0.5*self.scale*(self.envir.state+1)
        state=self.envir.state
        if(not (state is None)):
            pg.draw.circle(window,(0,0,128),state,10)
#        state=0.5*self.scale*(self.kalman.x_pred+1)
#        pg.draw.circle(window,(0,128,0),state,10)

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
#        if event.type == pg.KEYDOWN:
#            controler.on_key(event.key)
        view.show(window)
        pg.display.flip()
        clock.tick(3)
    pg.quit()

view=View(Envir())
loop(view)