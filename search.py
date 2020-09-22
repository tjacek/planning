class State(object):
    def __init__(self,state_id):
        self.id=state_id
        self.visited=False
        self.parent=None

class FowardSearch(object):
    def __call__(self,x0):
        Q=[x0]
        x0.visited=True
        while(Q):
            x_i=Q.pop()
            if(self.is_goal(x_i)):
                return True
            for x_j in self.next_state(x_i):
                if(not x_j.visited):
                    x_j.parent=x_i
                    x_j.visited=True
                    Q.append(x_j)
        return False

    def is_goal(self,state_i):
        raise NotImplemented()

    def next_state(self,state_i):
        raise NotImplemented()