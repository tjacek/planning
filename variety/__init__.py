import sympy 
from sympy.abc import x,y,z

class TarskiSentence(object):
	def __init__(self,polynomials,conds):
		self.polynomials=polynomials
		self.conds=conds

def simple_cond(pol_value):
	return pol_value <0
		
def make_pol():
	p0=sympy.Poly(x**2+y**2-1)
	print(dir(p0))
	p1=sympy.Poly(x**2)
	conds=[simple_cond,simple_cond]
	return TarskiSentence([p0,p1],conds)

tarski=make_pol()