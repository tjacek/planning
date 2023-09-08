import numpy as np
import pygame as pg
import model,show

class MotionControler(object):
    def __init__(self,exp,bounds=(256,256)):
        self.exp=exp
        self.bounds=BasicBounds()
        self.action=MotionAction()
        self.current=None

    def on_click(self,point):
        new_state=self.bounds.get_state(point)
        new_state=np.array(new_state+[0,0],dtype=float)
        self.exp.envir.state=new_state
        print(str(self.exp.envir))

    def on_key(self,key):
        print(key)

        if(self.exp.envir.empty_state()):
            return None
        if(self.action.update(key)):
            self.current=self.exp(self.action.u)
        print(str(self.action))
        print(str(self.exp.envir))

    def show(self,window):
        window.fill((0,0,0))
        step=64*self.bounds.scale
        self.draw_lines(window,step=step[0],
                        horiz=True)
        self.draw_lines(window,step=step[1],
                        horiz=False)
        

        if(self.current is None):
            return

        true_state,obs_state,pred_state=self.current   
        obs_state=self.bounds.transform_point(obs_state)
        pg.draw.circle(window,(128,0,0),obs_state,10)

        x,y,theta,v= true_state        
        true_state=self.bounds.transform_point([x,y])
        pg.draw.circle(window,(0,0,128),true_state,10)
        x,y=true_state
        pg.draw.line(window,
                     color=(128,128,0),
                     start_pos=(x,y),
                     end_pos=(int(x+25*np.cos(theta)),
                              int(y+25*np.sin(theta))))
        
        pred_state=self.bounds.transform_point(pred_state[:2])
        pg.draw.circle(window,(0,128,0),pred_state,10)
        draw_ellipse(window)

    def draw_lines(self,window,step=64,horiz=True,color=(0,128,0)):
        bounds=self.bounds.get_bounds()
        n_lines= int(bounds[0]/step)    
        for i in range(n_lines):
            x_i= i*step
            if(horiz):
                start,end=(0,x_i),(bounds[0],x_i)
            else:
                start,end=(x_i,0),(x_i,bounds[1])
            pg.draw.line(window,color,start,end)

def draw_ellipse(window):
    surface = pg.Surface((100, 100))
    ellipse = pg.draw.ellipse(surface, (0,128,0), 50)
    surface2 = pg.transform.rotate(surface, 45)
    window.blit() 

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
        elif(key==120):
            self.u[0]=0
            return False
        elif(key==101):
            self.u[1]+=(np.pi/12)
            return False
        elif(key==100):
            self.u[1]-=(np.pi/12)
            return False
        elif(key==99):
            self.u[1]=0
            return False        
        return True

    def __str__(self):
        return f'v:{self.u[0]:4f},omega:{self.u[1]:4f}'

class BasicBounds(object):
    def __init__(self,bounds=(256,256)):
        self.bounds=np.array(bounds)
        self.scale=np.array([1.0,1.0])

    def get_bounds(self):
        return 2*self.bounds

    def get_state(self,point):
        return[ (point_i-bound_i) 
                for point_i,bound_i in zip(point,self.bounds)]

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

class TorusBounds(object):
    def __init__(self,bounds=(256,256)):
        self.bounds=np.array(bounds)
        self.scale=np.array([1.0,1.0])

    def get_bounds(self):
        return 2*self.bounds
    
    def transform_point(self,point):
        state=[]
        for i,point_i in enumerat(point):
            if(point_i>self.bounds[i]):
                state_i= point_i + self.bounds[i]
            elif(point_i<-self.bounds[i]):
                state_i= point_i + self.bounds[i]
            else:
                state_i=point_i
            state.append(state_i)
        return np.array(state)
        
    def rescale(self,cord,i):
        return 1.0

if __name__ == '__main__':
    exp=model.Experiment(envir=model.simple_motion_model(),
                         alg=model.ExtendedKalman())
    show.loop(MotionControler(exp))