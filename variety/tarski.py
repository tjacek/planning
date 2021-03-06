from lark import Lark,Transformer,Token,Tree

class Polynomial(dict):
	def __init__(self,variables,values,degree):
		super(Polynomial, self).__init__(values)
		self.variables=variables
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
	def helper(coff_i, prod_i):
		key_i=[0 for i in range(degree)]
		for var_j,degree_j in get_product(prod_i):
			key_i[var_dict[var_j]]=degree_j
		values[tuple(key_i)]=coff_i
	for pol_i in tree.find_pred(lambda x: x.data=='polynomial'):
		if(len(pol_i.children)==3):
			sign_i=get_sign(pol_i.children[1])
			product_i=pol_i.children[2]
			if(type(product_i.children[0])==Token):
				key_i=tuple([0 for i in range(degree)])
				values[key_i]=sign_i*float(product_i.children[0])
			else:
				has_coff=len(product_i.children)>1
				coff_i= float(product_i.children[0]) if(has_coff) else 1.0
				prod_i= product_i.children[1] if(has_coff) else product_i.children[0]
				helper(coff_i,prod_i)
		if(len(pol_i.children)==1):
			prod_i=pol_i.children[0]
			coff_i=float(prod_i.children[0])
			helper(coff_i,prod_i.children[1])
	print(values)
	return Polynomial(variables,values,degree)

def get_product(product):
	result=[]
	if(len(product.children)==1):
		var_i=str(product.children[0].children[0])
		return [(var_i,1)]
	if(type(product.children[1])==Token):
		var_i=str(product.children[0].children[0])
		degree_i=int(product.children[1])
		return [(var_i,degree_i)]
	result=get_product(product.children[0])
	var_i=product.children[1].children[0]
	result.append((var_i,1))
	return result

def get_sign(sign_node):
	if(sign_node.data=='minus'):
		return -1.0
	return 1.0

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