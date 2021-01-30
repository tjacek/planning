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
	
	polynomial:  coff_product
			   | polynomial sign coff_product

	coff_product:  product
				 | NUMBER
				 | NUMBER product

	sign: "+" -> plus
		| "-" -> minus

	product:  variable
			| product "*" variable 
			| variable "^" INT

	variable: LETTER+

    %import common.INT
	%import common.LETTER
	%import common.NUMBER
	%import common.WS
	%ignore WS
"""

def build_polynomial(tree):
	variables=get_variable(tree)
	variables.sort()
	var_dict={ var_i:i for i,var_i in enumerate(variables)}
	degree=get_degree(tree)
	values={}
	def helper(raw_result):
		key_i=[0 for i in range(degree)]
		if(raw_result is None):
			return key_i
		for var_j,degree_j in raw_result:
			key_i[var_dict[var_j]]=degree_j
		return key_i
	for pol_i in tree.find_pred(lambda x: x.data=='polynomial'):
		if(len(pol_i.children)==3):
			sign_i=get_sign(pol_i.children[1])
			coff_i,result=get_product(pol_i.children[2])
			key_i=helper(result)
			coff_i*=sign_i
			values[tuple(key_i)]=coff_i
		if(len(pol_i.children)==1):
			coff_i,result=get_product(pol_i.children[0])
			key_i=helper(result)
			values[tuple(key_i)]=coff_i
	return Polynomial(variables,values,degree)

def get_sign(sign_node):
	if(sign_node.data=='minus'):
		return -1.0
	return 1.0

def get_product(node_i):
	print("*****")
	if(len(node_i.children)>1):
		coff=float(node_i.children[0])
		product=node_i.children[1]
	else:
		coff=1.0
		product=node_i.children[0]
	if( type(product)==Token):
		return float(product),None
	result=[]
	for child_i in product.children:
		if(type(child_i)==Tree):
			if( child_i.data=='variable' ):
				result.append((str(child_i.children[0]),1))
			if( child_i.data=='product'):
				var_i=str(child_i.children[0].children[0])
				degree_i=int(child_i.children[1])
				result.append((var_i,degree_i))
	return coff,result

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

def parse_polynomial(text):
	parser=Lark(grammar,start='polynomial')
	tree=parser.parse(text)
	return build_polynomial(tree)

#parse_polynomial("-2x^3*y-z^2")