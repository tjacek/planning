import sys
import pygame as pg
import world,editor

class VertexIterator(object):
    def __init__(self,world):
        self.world=world
        self.n_polygon=0
        self.n_vertex=0

    def next(self):
        pol_i=self.world.polygons[self.n_polygon]
        self.n_vertex= (self.n_vertex+1) % len(pol_i)
        if(self.n_vertex==0):
            self.n_polygon= (self.n_polygon+1) % len(self.world)

    def current(self):
        pol_i=self.world.polygons[self.n_polygon]
        vertex_j=pol_i.vertices[self.n_vertex]
        return pol_i,vertex_j

    def __str__(self):
        return f"{self.n_polygon},{self.n_vertex}"

class VertexControler(object):
    def __init__(self,problem,alg):
        self.problem=problem
        self.alg=alg
        self.mode=editor.EditorMode.START
        self.vertices=VertexIterator(problem.world)

    def on_click(self,point):
        if(self.mode==editor.EditorMode.START):
            self.problem.start=point
        if(self.mode==editor.EditorMode.END):
            self.problem.end=point

    def on_key(self,key):
        print(self.vertices)
        print(key)
        if(key==115):
            self.mode=editor.EditorMode.END
        elif(key==101):
            self.mode=editor.EditorMode.START
        else:
            self.vertices.next()
        print(self.mode)

    def show(self,window):
        window.fill((0,0,0))
        self.problem.world.show(window)
        self.problem.show(window)
        pol_i,vertex_j=self.vertices.current()
        pg.draw.circle(window,(0,0,128), vertex_j, 5) 
        if(self.problem.posed()):
            for (x,y) in self.alg(pol_i,vertex_j,self.problem):
                pg.draw.line(window,(255,255,0),x,y)

def simple_alg(pol_i,vertex_j,problem):
    return [(vertex_j,problem.end)]

def colision_alg(pol_i,vertex_j,problem):
    result=[(vertex_j,problem.end)]
    inter_points,segm=pol_i.get_intersections(result[0])
    result+=segm
    return result

if __name__ == "__main__":
    problem=world.read_json(sys.argv[1])
    controler=VertexControler(problem,colision_alg)
    editor.loop_template(controler)
    pg.quit()