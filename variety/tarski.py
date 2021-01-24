from lark import Lark,Transformer,Token,Tree

class Polynomial(object):
	def __init__(self,variables,values,degree):
		self.variables=variables
		self.values=values
		self.degree=degree

class EvalAtomic(Transformer):
	def atomic(self, items):
		value=float(items[0])
		print(value)
		relation=items[1].data
		if(relation=='higher'):
			return value<0
		if(relation=='higher_eq'):
			return value<=0
		if(relation=='lower'):
			return value>0
		if(relation=='lower_eq'):
			return value>=0
		if(relation=='eq'):
			return value==0
		if(relation=='ineq'):
			return value!=0
		return items

	def relation(self, items):
		print("relation")
		print(items)
		return items

	def polynomial(self,items):
		if(type(items[0])==float):
			return items[0]+float(items[1])
		if( items[0].type=='SIGNED_NUMBER'):
			return float(items[0])
		raise Exception(items)

grammar="""
	atomic: polynomial relation "0"

	relation:   "<"   -> higher
			   | "<=" -> higher_eq
	           | ">"  -> lover
	           | ">=" -> lower_eq
	           | "="  -> eq
	           | "!=" -> ineq
	
	polynomial:  SIGNED_NUMBER
			   | coff_product
			   | polynomial coff_product

	coff_product:  product
				 | SIGNED_NUMBER product
				 | sign product
				 | sign product 

	sign: "+" -> plus
		| "-" -> minus

	product:  variable
			| product "*" variable 
			| variable "^" INT

	variable: LETTER+

    %import common.INT
	%import common.LETTER
	%import common.SIGNED_NUMBER
	%import common.WS
	%ignore WS
"""

def build_polynomial(tree):
	variables=get_variable(tree)
	variables.sort()
	var_dict={ var_i:i for i,var_i in enumerate(variables)}
	degree=get_degree(tree)
	result=tree.find_pred(lambda x: x.data=='coff_product')
	values={}
	for node_i in result:
		coff_i=get_coff(node_i)
		key_i=[0 for i in range(degree)]
		for var_j,degree_j in get_product(node_i):
			key_i[var_dict[var_j]]=degree_j
		print(key_i)
		values[tuple(key_i)]=coff_i
	return Polynomial(variables,values,degree)

def get_product(node_i):
	product=node_i.children[1]
	result=[]
	for child_i in product.children:
		if(type(child_i)==Tree):
			if( child_i.data=='variable' ):
				result.append((str(child_i.children[0]),1))
			if( child_i.data=='product'):
				var_i=str(child_i.children[0].children[0])
				degree_i=int(child_i.children[1])
				result.append((var_i,degree_i))
	return result

def get_coff(node_i):
	coff=node_i.children[0]
	if(type(coff)==Token):
		return float(coff.value)
	if(coff.data=='minus'):
		return -1.0
	if(coff.data=='plus'):
		return 1.0
	return 0.0

def get_variable(tree):
	var_names=set()
	for node_i in tree.iter_subtrees():
		if(node_i.data=='variable'):
			var_names.update(node_i.children[0])
	return list(var_names)

def get_degree(tree):
	degree=[]
	result=tree.find_pred(lambda x: x.data=='product')
	for node_i in result:
		for child_i in node_i.children:
			if(type(child_i)== Token):
				if(child_i.isdigit()):
					degree.append(int(child_i))
	if(not degree):
		return 0
	return max(degree)

parser=Lark(grammar,start='polynomial')
tree=parser.parse("-2x^3*y-z^2")
print(build_polynomial(tree))