#from foward import State

class BidirectionalSearch(object):
    def __init__(self,problem,queue_type=None):
        if(queue_type is None):
            queue_type=SetQueue
        self.problem=problem
        self.start_queue=queue_type()
        self.goal_queue=queue_type()

    def __call__(self,x_0,x_g):
        self.start_queue.append(x_0)
        x_0.visited=True
        self.goal_queue.append(x_g) 	
        x_g.visited=True
        while(self.start_queue and self.goal_queue):
            x_i=self.start_queue.pop()
            if(self.problem.is_goal(x_i) 
                or x_i in self.goal_queue):
                return True
            for x_j in self.problem.next_state(x_i):
                if(not x_j.visited):
                    x_j.parent=x_i
                    x_j.visited=True
                    self.start_queue.append(x_j)

            x_i=self.goal_queue.pop()
            if(self.problem.is_goal(x_i) 
                or x_i in self.start_queue):
                return True
            for x_j in self.problem.next_state(x_i):
                if(not x_j.visited):
                    x_i.parent=x_j
                    x_j.visited=True
                    self.goal_queue.append(x_j)           
        return False

class SetQueue(object):
    def __init__(self):
        self.active_states=[]
        self.all_states=set()

    def pop(self):
        return self.active_states.pop()	

    def append(self,state_i):
        self.append(state_i)
        self.active_states.update(state_i)	

    def __contains__(self, state_i):
        return self.all_states in state_i  

    def __bool__(self):
        return bool(self.active_states)	