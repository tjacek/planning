from lark import Lark,Transformer

class EvalAtomic(Transformer):
	def atomic(self, items):
		value=float(items[0])
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

grammar="""
	atomic: SIGNED_NUMBER relation "0"

	relation:   "<"   -> higer
	           | "<=" -> higer_eq
	           | ">"  -> lover
	           | ">=" -> lower_eq
	           | "="  -> eq
	           | "!=" -> ineq
	
	%import common.ESCAPED_STRING
	%import common.SIGNED_NUMBER
	%import common.WS
	%ignore WS
"""

parser=Lark(grammar,start='atomic')
tree=parser.parse("0=0")
print(EvalAtomic().transform(tree))