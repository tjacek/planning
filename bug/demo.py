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

    indexes=pol_i.colision_segm(line)
    segm_i=pol_i.get_segments()[indexes[0]]
    inter=geometry.intersection(segm_i,line)    
    result=[(inter,segm_i[0])]#(line[0],inter)]
    for i,segm_i in enumerate( pol_i.get_segments()):
        line_i=(segm_i[1], problem.end)
        tabu=set([i])#pol_i.near(i)[1]
#        raise Exception(len(tabu))
        if(not pol_i.detect_collision(line_i,tabu)):
            result.append(line_i)
    return result

def demo_loop(in_path,alg,bounds=(512,512)):
    controler=AlgControler(world.read_json(in_path),alg)
    editor.loop_template(controler)
    pg.quit()

if __name__ == "__main__":
    demo_loop(sys.argv[1],all_collision)