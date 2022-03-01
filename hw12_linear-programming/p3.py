import numpy as np
import LP

## parameters of the standard form dual LP 
c =  np.array([-6,-8,0,0],dtype=float)
A =  np.array([[-1,1,1,0],[-1,-2,0,1]],dtype=float).reshape(2,4)
b =  np.array([-1,-3],dtype=float)

mu0 = np.array([4,1,2,3], dtype=float)

mu_traces = LP.barrier(-c, A, b, mu0)

print('')
for k,mu in enumerate(mu_traces):
	print('iteration %d: %s' % (k, mu))
print('dual optimal value:', c@mu_traces[-1])
