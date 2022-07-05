import sys
import pygame as pg
import world,editor

class VertexControler(object):
    def __init__(self,problem):
        self.problem=problem
        self.mode=editor.EditorMode.START
        self.n_polygon=0
        self.n_vertex=0

    def on_click(self,point):
        if(self.mode==editor.EditorMode.START):
            self.problem.start=point
        if(self.mode==editor.EditorMode.END):
            self.problem.end=point

    def on_key(self,key):
        print((self.n_polygon,self.n_vertex))
        print(key)
        if(key==115):
            self.mode=editor.EditorMode.END
        elif(key==101):
            self.mode=editor.EditorMode.START
        else:
            pol_i=self.problem.world.polygons[self.n_polygon]
            self.n_vertex= (self.n_vertex+1) % len(pol_i)
            if(self.n_vertex==0):
                self.n_polygon= (self.n_polygon+1) % len(self.problem.world)
        print(self.mode)

    def show(self,window):
        window.fill((0,0,0))
        self.problem.world.show(window)
        self.problem.show(window)
        pol_i=self.problem.world.polygons[self.n_polygon]
        vertex_j=pol_i.vertices[self.n_vertex]
        pg.draw.circle(window,(0,0,128), vertex_j, 5) 
#        segments= pol_i.get_segments()
#        x,y=segments[self.n_vertex]
#        pg.draw.line(window,(255,255,0),x,y)
#        x,y=segments[self.n_vertex-1]
#        pg.draw.line(window,(255,255,0),x,y)

if __name__ == "__main__":
    controler=VertexControler(world.read_json(sys.argv[1]))
    editor.loop_template(controler)
    pg.quit()