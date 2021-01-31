import sympy
import tarski

def plot2D(pol_i):
	if(pol_i.degree!=2):
		raise Exception("Pol degree %d" % pol_i.degree)
	symbols=[sympy.symbols(var_i) for var_i in pol_i.variables]
	print(len(symbols))
#	x=sympy.symbols('x')
#	y=sympy.symbols('y')
#	pol=sympy.Eq(x**2+y**2-5,0)
#	sympy.plot_implicit(pol,show=True)

def eclipse():
	pol=tarski.parse_polynomial("2x^2*y+y^2-5")
	plot2D(pol)

eclipse()