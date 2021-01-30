import sympy

def plot2D():
	x=sympy.symbols('x')
	y=sympy.symbols('y')
	pol=sympy.Eq(x**2+y**2-5,0)
	sympy.plot_implicit(pol,show=True)

plot2D()