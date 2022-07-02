import sys
import pygame as pg
import world,editor
import geometry

class AlgControler(object):
    def __init__(self,problem,alg=None):
        if(alg is None):
        	alg=simple_alg
        self.problem=problem
        self.mode=editor.EditorMode.START
        self.alg=alg
    
    def on_click(self,point):
        if(self.mode==editor.EditorMode.START):
            self.problem.start=point
        if(self.mode==editor.EditorMode.END):
            self.problem.end=point

    def on_key(self,key):
        if(self.mode==editor.EditorMode.START):
            self.mode=editor.EditorMode.END
        else:
            self.mode=editor.EditorMode.START
        print(self.mode==editor.EditorMode.START)
        print(self.mode)

    def show(self,window):
        window.fill((0,0,0))
        self.problem.world.show(window)
        self.problem.show(window)
        if(self.problem.posed()):
            for (x,y) in self.alg(self.problem):
                pg.draw.line(window,(255,255,0),x,y)

class VertexControler(object):
    def __init__(self,problem):
        self.world=problem.world
        self.n_polygon=0
        self.n_vertex=0

    def on_click(self,point):
        pass

    def on_key(self,key):
        print((self.n_polygon,self.n_vertex))
        pol_i=self.world.polygons[self.n_polygon]
        self.n_vertex= (self.n_vertex+1) % len(pol_i)
        if(self.n_vertex==0):
            self.n_polygon= (self.n_polygon+1) % len(self.world)

    def show(self,window):
        window.fill((0,0,0))
        self.world.show(window)
        pol_i=self.world.polygons[self.n_polygon]
        vertex_j=pol_i.vertices[self.n_vertex]
        pg.draw.circle(window,(0,0,128), vertex_j, 5) 
        segments= pol_i.get_segments()
        x,y=segments[self.n_vertex]
        pg.draw.line(window,(255,255,0),x,y)
        x,y=segments[self.n_vertex-1]
        pg.draw.line(window,(255,255,0),x,y)

def simple_alg(problem):
    return [(problem.start,problem.end)]	

def all_collision(problem):
    line=(problem.start,problem.end)
    result=[line]
    polygons=problem.world.collision(line)
    for pol_i in polygons:
        indexes=pol_i.colision_segm(line)
        segm=pol_i.get_segments()
        for i in indexes:
            result.append(segm[i])
    return result

def bug1(problem):
    line=(problem.start,problem.end)
    pol_i=problem.world.nearest_polygon(line)
    if(pol_i is None):
        return [line]
    line_i=(pol_i.vertices[0],line[1])
    inter=pol_i.get_intersections(line_i)
    return [ (inter_i,line_i[1]) for inter_i in inter]

def demo_loop(in_path,alg,bounds=(512,512)):
    controler=AlgControler(world.read_json(in_path),alg)
    editor.loop_template(controler)
    pg.quit()

if __name__ == "__main__":
    demo_loop(sys.argv[1],bug1)
#    controler=VertexControler(world.read_json(sys.argv[1]))
#    editor.loop_template(controler)
#    pg.quit()