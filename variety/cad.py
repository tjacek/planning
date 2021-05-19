import sys
sys.path.append("..")
import sympy
import variety,plot

def cad(variety_i):
	f=variety_i.polynomials[0]
	for pol_j in variety_i.polynomials:
		f*=pol_j
	f=f.as_expr().as_poly() 
	roots=sympy.real_roots(f)
	roots=list(set(roots))
	roots.sort()
	print(roots)

var0=variety.make_1D()
for i in range(len(var0.polynomials)):
	var0.polynomials[i]=var0.polynomials[i]+var0.vars[1]
cad(var0)