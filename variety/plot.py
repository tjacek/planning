import sympy
import tarski

def plot2D(pol_i):
	if(pol_i.degree!=2):
		raise Exception("Pol degree %d" % pol_i.degree)
	symbols=[sympy.symbols(var_i) for var_i in pol_i.variables]
	products=[]
	for key_i,coff_i in pol_i.items():
		if(sum(key_i)!=0):
			prod_i=sympy.poly(symbols[0]**key_i[0] * symbols[1]**key_i[1])
			products.append(coff_i*prod_i)
	eq=sum(products)+pol_i[(0,0)]
	print(eq)
#	x=sympy.symbols('x')
#	y=sympy.symbols('y')
#	eq=sympy.poly(x**2+y**2-5)
#	print(eq +7)
	sympy.plot_implicit(eq.as_expr(),show=True)

def eclipse():
	pol=tarski.parse_polynomial("8x^2+y^2-5")
	plot2D(pol)

eclipse()