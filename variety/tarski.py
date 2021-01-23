from lark import Lark

grammar="""
	atomic: SIGNED_NUMBER relation "0"

	relation: "<"|"<="|">"|">="|"="|"!="
	
	%import common.ESCAPED_STRING
	%import common.SIGNED_NUMBER
	%import common.WS
	%ignore WS
"""

parser=Lark(grammar,start='atomic')
tree=parser.parse("-5=0")
print(dir(tree))