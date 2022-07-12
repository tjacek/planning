import pygame as pg

class Envir(object):
    def __init__(self):
        self.state=None
    
    def set_state(self,state):
        self.state=state

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
    window = pg.display.set_mode((512,512))
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