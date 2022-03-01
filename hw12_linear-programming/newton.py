import numpy as np


def newton_eq(f, fp, fpp, x0, A, b, initial_stepsize=1, alpha=0.5, beta=0.5, tol=1e-8, maxiter=100000):
	x_traces = [np.array(x0)]
	m = len(b)
	xlen = len(x0)
	x = np.array(x0)
	for it in range(maxiter):
		K = np.block([[fpp(x), A.T], [A, np.zeros([m, m])]])
		c = np.block([-fp(x), np.zeros(m)])
		dlambd = np.linalg.solve(K, c)
		d = dlambd[:xlen]
		alpha_grad_d = alpha*fp(x)@d
		t = initial_stepsize
		while f(x+t*d) > f(x)+t*alpha_grad_d:
			t = t* beta
		x = x + t*d
		x_traces.append(x)
		if np.linalg.norm(d.T@fpp(x)@d) <= tol:
			break
	return x_traces
