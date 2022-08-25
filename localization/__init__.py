
class View(object):
    def __init__(self,envir,alg=None):
        self.envir=envir
        self.obs_state=None
        self.alg=alg

    def on_click(self,point): 
        self.envir.set_state(point)
        print(self.envir.state)

    def on_key(self,key):
        if(self.envir.has_state()):
            self.envir.update()
            self.obs_state= self.envir.observe()

    def show(self,window):
        window.fill((0,0,0))
        state=self.envir.state
        if(not (state is None)):
            pg.draw.circle(window,(0,0,128),state,10)
        if(not (self.obs_state is None)):
            pg.draw.circle(window,(0,128,0),self.obs_state,7)
        if(not (self.alg is None or self.obs_state is None)):
            estm_state=self.alg(self.envir,self.obs_state)
            estm_state=self.envir.bound_state(estm_state)
            print(f"estm:{estm_state}")
            pg.draw.circle(window,(128,0,0),estm_state,5)

class Envir(object):
    def __init__(self,bounds=(512,512)):
        self.state=None
        self.bounds=bounds
    
    def has_state(self):
        return not (self.state is None)
    
    def set_state(self,state):
        self.state=self.bound_state(state)

    def bound_state(self,state):
        new_state=[]
        for i in (0,1):
            mult_i=int(state[i]/self.bounds[i])
            value_i=state[i]
            if(mult_i):
                value_i-=(mult_i*self.bounds[i])
            if(value_i<0):
                value_i=self.bounds[i]+value_i
            new_state.append(value_i)
        return new_state

    def update(self):
        print(self.state)

    def observe(self):
        return self.state

class Gauss(object):
    def __init__(self,mean=None,cov=None):
        if(mean is None):
            mean=np.zeros((2,))
        if(cov is None):
            cov=np.identity(2)
        self.mean=mean
        self.cov=cov

    def __call__(self):
        return np.random.multivariate_normal(self.mean,self.cov)

class AffineTransform(object):
    def __init__(self,A=None,b=None):
        if(A is None):
            A=np.identity(2)
        if(b is None):
            b=np.zeros((2,))
        self.A=A 
        self.b=b

    def __call__(self,x):
        return np.dot(self.A,x)+self.b

    def op(self,P):
        return np.dot(np.dot(self.A,P),self.A.T)

def loop(view):
    bounds=view.envir.bounds
    window = pg.display.set_mode(bounds)
    clock = pg.time.Clock()
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONUP:
                point = pg.mouse.get_pos()
                view.on_click(point)
            if event.type == pg.KEYDOWN:
                view.on_key(event.key)
        view.show(window)
        pg.display.flip()
        clock.tick(3)
    pg.quit()

def get_rotation(theta):
    A=np.array([[np.cos(theta),-np.sin(theta)],
                [np.sin(theta),np.cos(theta)]])
    return A