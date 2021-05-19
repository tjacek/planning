import sympy 
from sympy.abc import x,y,z

class Variety(object):
	def __init__(self,vars,polynomials,conds):
		self.vars=vars
		self.polynomials=polynomials
		self.conds=conds

	def n_vars(self):
		return len(self.vars)

	def __call__(self,point_i):
		point_dir={ var_j:cord_j
			for var_j,cord_j in zip(self.vars,point_i)}
		values=[pol_i.eval(point_dir) for pol_i in self.polynomials]
		return all([ cond_i(value_i) 
				for value_i,cond_i in zip(values,self.conds)])

def less(pol_value):
	return pol_value<0
		
def more(pol_value):
	return pol_value>0

def eq(pol_value):
	return pol_value==0


def make_pol(r1=5,r2=1,r3=1,
			x2=2,y2=2.5,x3=-2,y3=2.5,
			y4=-3,a=2.0,b=1 ):
	f0=sympy.Poly(x**2+y**2-r1**2,x,y)
	f1=sympy.Poly((x-x2)**2+(y-y2)**2-r2**2,x,y)
	f2=sympy.Poly((x-x3)**2+(y-y3)**2-r3**2,x,y)
	a,b=1/a,1/b
	f3=sympy.Poly((a*x)**2+(b*(y-y4))**2-1,x,y)
	pols=[f0,f1,f2,f3]
	conds=[less,less,less,less]
	return Variety([x,y],pols,conds)

def make_1D():
	f0=sympy.Poly(x**2-2*x-y,x,y)
	f1=sympy.Poly(x**2-4*x+3-y,x,y)
	pols=[f0,f1]
	conds=[less,less]
	return Variety([x,y],pols,conds)

if __name__ == "__main__":
	variety=make_pol()
	print(variety([0.5,1]))