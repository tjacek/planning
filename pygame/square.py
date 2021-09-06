import pygame

class Envir(object):
    def __init__(self,obstacles):
        self.obstacles=obstacles

pygame.init()
window = pygame.display.set_mode((250, 250))

obstacles=[(50,100,10,10),(10,10,10,10),(40,40,10,10),(60,30,10,10)]
rects=[]

for x,y,width,height in obstacles:
    rects.append(pygame.Rect(x,y,width,height))  #pygame.Rect(*window.get_rect().center, x, y).inflate(width, height))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

#    point = pygame.mouse.get_pos()
#    collide = rect.collidepoint(point)
#    color = (255, 0, 0) if collide else (255, 255, 255)
    color=(255,255,255)
    window.fill(0)
    for rect_i in rects:
        pygame.draw.rect(window, color, rect_i)
    pygame.display.flip()

pygame.quit()
exit()
