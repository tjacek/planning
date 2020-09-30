class STRIPS(object):
    def __init__(self,instances,init,
    	         operators,goal):
        self.instances=instances
        self.init=init
        self.operators=operators
        self.goal=goal

class Operator(object):
    def __init__(self,precondition,effects):
        self.precondition=precondition
        self.effects=effects

    def applicable(self,instances):
        literals=[ pred_i(instances)==cond_i 
                    for pred_i,cond_i self.precondition.items()]
        return all(literals)

    def apply(self,instances):
        [ effect_i(instances) 
    	    for effect_i in self.effects]

class Predictate(object):
    def __init__(self,args,fun):
        self.args=args
        self.fun=fun

    def __call__(self,instances):
    	arg_values=[instances[arg_i]  
    	                for arg_i in self.args]
        return self.fun(*arg_values)	