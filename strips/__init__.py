class STRIPS(object):
    def __init__(self,instances,predicates,operators,
    	            init,goal):
        self.instances=instances
        self.predicates=predicates
        self.operators=operators
        self.init=init
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
	def __init__(self,valid_args,fun,arity=2):
		self.valid_args=valid_args
		self.arity=arity
		self.fun=fun

	def get_args(self,instances):
		return self.valid_args(instances,self.arity)

    def __call__(self,args,instances):
		arg_values=[instances[arg_i]  
					for arg_i in self.args]
		return self.fun(*arg_values)

class ValidArgs(object):
	def __init__(self,types):
		self.types=[set(type_i) for type_i in types]

	def __call__(self,instances,arity):
		pairs=[[name_j
				for name_j,inst_j in instances.items()
		           if( type(inst_j) in type_i)]
					for i in range(arity)]

def get_predictate(fun,arg_types):
	arity=len(arg_types)
	return Predictate(ValidArgs(arg_types),fun,arity)