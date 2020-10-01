import re

class World(object):
	def __init__(self,literals,S,G,operators):
		self.literals=literals
		self.init=S
		self.goal=G
		self.operators=operators
		self.ordering=get_ordering(literals)

	def get_state(self):
		values=[None 
				for i in range(len(self.ordering))]
		for name_i in self.literals.keys():
			k=self.ordering[name_i]
			values[k]=self.literals[name_i].value
		values=[ str(int(value_i)) 
				for value_i in values]
		return "".join(values)

	def is_goal(self,state_i):
		values=[]
		for name_i,cond_i in self.goal:
			k=self.ordering[name_i]
			value_i=bool(int(state_i[k]))==cond_i
			values.append(value_i)
		return all(values)

class Literal(object):
	def __init__(self,name,value=False):
		self.name=name
		self.value=value

class Operator(object):
	def __init__(self,precondition,effects):
		self.precondition=precondition
		self.effects=effects
		
def parse_word(S,G,raw_operators):
	literals=[parse_literal(s_i) for s_i in S]
	literals={ literal_i.name:literal_i 
	                for literal_i in literals}
	operators=[parse_operator(operator_i,literals) 
				for operator_i in raw_operators]
	S,G=parse_goal(S),parse_goal(G)
	return World(literals,S,G,operators)

def parse_operator(raw_operator,literals):
	condition,effects=[],[]
	literal_helper(raw_operator[0],condition,literals)
	literal_helper(raw_operator[1],effects,literals)
	return Operator(condition,effects)

def literal_helper(in_i,out_i,literals):
	for raw_j in in_i:
		name_j,value_j=get_name(raw_j)
		if(not name_j in literals):
			literals[name_j]=Literal(name_j,False)
		out_i.append((name_j,value_j))

def parse_literal(raw_i):
	name_i,value_i=get_name(raw_i)
	return Literal(name_i,value_i)

def parse_goal(raw):
	return [get_name(raw_i)  for raw_i in raw]

def get_name(raw_i):
	name_i=re.sub(r'\s+','',raw_i.strip())
	if(re.search("~\S+",name_i)):
		name_i=name_i.replace("~","")
		return name_i,False
	return name_i,True

def get_ordering(literals):
	names=list(literals.keys())
	names.sort()
	values={literals[name_i].name:i  
				for i,name_i in enumerate(names)}
	return values