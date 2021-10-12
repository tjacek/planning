import pygame as pg
import gen,polygons

class DrawControler(object):
    def __init__(self,world):
        self.world=world
        self.points=[]

    def on_click(self,point):
        self.points.append(point)
        print(len(self.points))

    def on_key(self,key):
        if(len(self.points)>2):
            pol=polygons.Polygon(self.points)
            self.world.polygons.append(pol)
            self.points.clear()

    def show(self,window):
        window.fill((0,0,0))
        for point_i in self.points:
            pg.draw.circle(window,(0,0,128), point_i, 5)
        self.world.show(window)

class SimpleControler(object):
    def __init__(self,world):
        self.world=world

    def on_click(self,point):
        print(point)

    def on_key(self,key):
        print(key)

    def show(self,window):
        self.world.show(window)

def polygon_loop(world):
    pg.init()
    a_max=world.get_box()[1]
    bounds=(int(a_max[0]), int(a_max[1]))
    print(bounds)
    window = pg.display.set_mode(bounds)
    clock = pg.time.Clock()
    run = True
    controler=DrawControler(world)
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONUP:
                point = pg.mouse.get_pos()
                controler.on_click(point)
            if event.type == pg.KEYDOWN:
                controler.on_key(event.key)
        controler.show(window)
        pg.display.flip()
        clock.tick(3)
    pg.quit()
#    exit()

if __name__ == "__main__":
    world=polygons.read_world("test.txt")#gen.cell_world(5)
    polygon_loop(world)
    world.save("test.txt")