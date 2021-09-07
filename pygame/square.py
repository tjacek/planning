import numpy as np
import pygame

class Envir(object):
    def __init__(self,obstacles):
        self.obstacles=obstacles

    def show(self,window,color=(255,255,255)):
        for rect_i in envir.obstacles:
            pygame.draw.rect(window, color, rect_i)

pygame.init()
window = pygame.display.set_mode((250, 250))

def rect_world(n_rect,bounds=(5,10),world=(130,150)):
    rects=[]
    for i in range(n_rect):
        width,height=np.random.uniform(bounds[0],bounds[1],2)
        x=np.random.uniform(0.0,world[0])
        y=np.random.uniform(0.0,world[1])
        rects.append(pygame.Rect(x,y,width,height))
    return Envir(rects)


envir=rect_world(5)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

#    color=(255,255,255)
    window.fill(0)
    envir.show(window)
    pygame.display.flip()

pygame.quit()
exit()
