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
        if(self.envir.empty_state()):
            return None#self.envir.act(self.action.u)
        if(self.action.update(key)):
            self.envir.act(self.action.u)
        print(str(self.action))
        print(str(self.envir))

    def show(self,window):
        window.fill((0,0,0))
        self.draw_lines(window,step=self.scale[0]*64,horiz=True)
        self.draw_lines(window,step=self.scale[1]*64,horiz=False)
        
        obs_state=self.envir.observe()
        obs_state=self.transform_point(obs_state)
        pg.draw.circle(window,(128,0,0),obs_state,10)

        x,y,theta,v=self.envir.get_state()        
        true_state=self.transform_point([x,y])
        pg.draw.circle(window,(0,0,128),true_state,10)
        x,y=true_state
        pg.draw.line(window,
                     color=(128,128,0),
                     start_pos=(x,y),
                     end_pos=(int(x+25*np.cos(theta)),
                              int(y+25*np.sin(theta))))
    
    def transform_point(self,point):
        point=[self.rescale(p_i,i)*p_i 
                for i,p_i in enumerate(point)]
        point=np.array(point)
        point+=self.bounds
        return point

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
            return False 
        elif(key==115):
            self.u[0]-=1
            return False
        elif(key==101):
            self.u[1]+=(np.pi/12)
            return False
        elif(key==100):
            self.u[1]-=(np.pi/12)
            return False        
        return True

    def __str__(self):
        return f'v:{self.u[0]:4f},omega:{self.u[1]:4f}'

if __name__ == '__main__':
    motion_model=model.simple_motion_model()
#    model=model.MotionEnvir()
    show.loop(MotionControler(motion_model))