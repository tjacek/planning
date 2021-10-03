import numpy as np
import pygame as pg

class InputBox(object):
    def __init__(self,x,y,w,h):
        self.rect = pg.Rect(x, y, w, h)
        self.text="100.0"
        self.active=False
        self.FONT = pg.font.Font(None, 32)
        self.ACTIVE_COLOR=(128,0,0)
        self.INACTIVE_COLOR=(0,128,0)
        self.txt_surface = self.update_txt()

    def get_color(self):
        return self.ACTIVE_COLOR if self.active else self.INACTIVE_COLOR

    def update_txt(self):
        return self.FONT.render(self.text, True,self.get_color())

    def handle_event(self,event):
        print(event.type)
#        if event.type == pg.MOUSEBUTTONDOWN:
        point=pg.mouse.get_point()
        if self.rect.collidepoint(point):
            self.active = not self.active
        else:
            self.active = False        
        if event.type == pg.KEYDOWN:
            if self.active or True:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface =self.update_txt()
        print("OK")
#        pg.display.flip()

    def draw(self, window):
        window.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pg.draw.rect(window, self.get_color(), self.rect, 2)


class Envir(object):
    def __init__(self,obstacles):
        self.obstacles=obstacles

    def __call__(self,point):
        for rect_i in self.obstacles: 
            if(rect_i.collidepoint(point)):
                return True
        return False

    def show(self,window,color=(255,255,255)):
        for rect_i in envir.obstacles:
            pg.draw.rect(window, color, rect_i)

pg.init()
window = pg.display.set_mode((1000, 1000))

def rect_world(n_rect,bounds=(25,75),world=(900,900)):
    rects=[]
    for i in range(n_rect):
        width,height=np.random.uniform(bounds[0],bounds[1],2)
        x=np.random.uniform(0.0,world[0])
        y=np.random.uniform(0.0,world[1])
        rects.append(pg.Rect(x,y,width,height))
    return Envir(rects)

envir=rect_world(10)

clock = pg.time.Clock()
input_box = InputBox(100, 100, 200, 40)

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    
    point = pg.mouse.get_pos()
    window.fill(0)
    envir.show(window)#,color)
#    pg.draw.circle(window, (0,255,0),point, 5)
    ev = pg.event.get()
#    for event in ev:
#        if event.type == pg.MOUSEBUTTONUP:
#            pg.display.flip()
    input_box.draw(window)
    for event_i in ev:
        input_box.handle_event(event_i)
    pg.display.flip()
    clock.tick(3)

pg.quit()
exit()
