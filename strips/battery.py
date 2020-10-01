import re
#import strips

def make_world():
	S=["On(Cap,Flashlight)"]
	G=[ "On(Cap,Flashlight)",
		"In(Battery1,Flashlight)",
		"In(Battery2,Flashlight)"]
	PlaceCap=[["~On(Cap,Flashlight)"],
				["On(Cap,Flashlight)"]]
	RemoveCap=[["On(Cap,Flashlight)"],
				["~On(Cap,Flashlight)"]]
	Insert1=[["~On(Cap,Flashlight)",
	         "~In(Battery1,Flashlight)" ],
	         ["In(Battery1,Flashlight)"]]
	Insert2=[["~On(Cap,Flashlight)",
	         "~In(Battery2,Flashlight)" ],
	         ["In(Battery2,Flashlight)"]]
	operators=[PlaceCap,Insert1,Insert2,RemoveCap]
	parse_word(S,G,operators)

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
	print(literals.keys())

def parse_operator(raw_operator,literals):
	condition,effects=[],[]
	operator_helper(raw_operator[0],condition,literals)
	operator_helper(raw_operator[1],effects,literals)
	return Operator(condition,effects)

def operator_helper(in_i,out_i,literals):
	for raw_j in in_i:
		name_j,value_j=get_name(raw_j)
		if(not name_j in literals):
			literals[name_j]=Literal(name_j,False)
		out_i.append((name_j,value_j))

def parse_literal(raw_i):
	name_i,value_i=get_name(raw_i)
	return Literal(name_i,value_i)

def get_name(raw_i):
	name_i=re.sub(r'\s+','',raw_i.strip())
	if(re.search("~\S+",name_i)):
		name_i=name_i.replace("~","")
		return name_i,False
	return name_i,True