import numpy as np
import pygame

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
            pygame.draw.rect(window, color, rect_i)

pygame.init()
window = pygame.display.set_mode((1000, 1000))

def rect_world(n_rect,bounds=(25,75),world=(900,900)):
    rects=[]
    for i in range(n_rect):
        width,height=np.random.uniform(bounds[0],bounds[1],2)
        x=np.random.uniform(0.0,world[0])
        y=np.random.uniform(0.0,world[1])
        rects.append(pygame.Rect(x,y,width,height))
    return Envir(rects)

envir=rect_world(10)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    point = pygame.mouse.get_pos()
    window.fill(0)
    envir.show(window)#,color)
    pygame.draw.circle(window, (0,255,0),point, 5)

    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.MOUSEBUTTONUP:
            pygame.display.flip()

pygame.quit()
exit()
