from lark import Lark,Transformer,Token

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
				 | "+" product
				 | "-" product

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

def get_variable(tree):
	var_names=set()
	for node_i in tree.iter_subtrees():
		if(node_i.data=='variable'):
			var_names.update(node_i.children[0])
	return var_names

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
tree=parser.parse("-x^3*y+z^2")
#print(tree)
print(get_degree(tree))
#print(EvalAtomic().transform(tree))