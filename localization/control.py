import numpy as np
import pygame as pg
import model,show

class MotionControler(object):
    def __init__(self,envir,bounds=(256,256)):
        self.envir=envir
        self.bounds=np.array(bounds)
        self.scale=[1.0,1.0]
        self.action=MotionAction()

    def get_bounds(self):
        return 2*self.bounds

    def on_click(self,point):
        new_state=[ (point_i-bound_i) 
            for point_i,bound_i in zip(point,self.bounds)]
        new_state=np.array(new_state+[0,0])
        self.envir.state=new_state
        print(str(self.envir))

    def on_key(self,key):
        if(not self.envir.empty_state()):
            self.envir.act(self.action.u)
        self.action.update(key)
        print(str(self.action))
        print(str(self.envir))

    def show(self,window):
        window.fill((0,0,0))
        x,y=self.envir.get_state()[:2]
        state=[self.rescale(x,0)*x,self.rescale(y,1)*y]
        state= self.translate(state)
        state=np.array(state)
        pg.draw.circle(window,(0,0,128),state,10)
        self.draw_lines(window,step=self.scale[0]*64,horiz=True)
        self.draw_lines(window,step=self.scale[1]*64,horiz=False)

    def translate(self,state):
        state=[state_i+bound_i 
            for state_i,bound_i in zip(state,self.bounds)]
        return np.array(state)

    def rescale(self,cord,i):
        if( cord<-self.bounds[i] or 
          self.bounds[i]<cord):
            self.scale[i]=0.9*(self.bounds[i]/np.abs(cord))
        else:
            self.scale[i]=1
        return self.scale[i]

    def draw_lines(self,window,step=64,horiz=True,color=(0,128,0)):
        bounds=self.get_bounds()
        n_lines= int(bounds[0]/step)    
        for i in range(n_lines):
            x_i= i*step
            if(horiz):
                start,end=(0,x_i),(bounds[0],x_i)
            else:
                start,end=(x_i,0),(x_i,bounds[1])
            pg.draw.line(window,color,start,end)

class MotionAction(object):
    def __init__(self,v=5,omega=(np.pi/12)):
        self.u=np.array([v,omega])
    
    def update(self,key):
        if(key==119):
            self.u[0]+=1 
        elif(key==115):
            self.u[0]-=1
        elif(key==101):
            self.u[1]+=(np.pi/12)
        elif(key==100):
            self.u[1]-=(np.pi/12)        
        print(key)

    def __str__(self):
        return f'v:{self.u[0]:4f},omega:{self.u[1]:4f}'

if __name__ == '__main__':
    model=model.MotionEnvir()
    show.loop(MotionControler(model))