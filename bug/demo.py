import sys
import pygame as pg
import world,editor

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
            for segm_i in self.alg(self.problem):
                pg.draw.line(window,(255,255,0),segm_i[0],segm_i[1])

def simple_alg(problem):
    return [(problem.start,problem.end)]	

def demo_loop(in_path,bounds=(512,512)):
    controler=AlgControler(world.read_json(in_path))
    editor.loop_template(controler)
    pg.quit()

if __name__ == "__main__":
    demo_loop(sys.argv[1])