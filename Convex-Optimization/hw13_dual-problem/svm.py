import numpy as np
import matplotlib.pyplot as plt
import proj_gd as gd

def svm(X,y):
	"""
	X: n x m matrix, X[i,:] is the m-D feature vector of the i-th sample
	y: n-D vector, y[i] is the label of the i-th sample, with values +1 or -1

	This function returns the primal and dual optimal solutions w^*, b^*, mu^*
	"""
	Xy = X * y
	Q = Xy @ Xy.T

	def fp(mu):
		# f(mu) = 0.5 * mu.T@Q@mu - np.sum(mu) note that we want to minimize it
		return Q@mu - np.ones_like(mu)

	def proj(mu):
		zp = [-100000]
		zn = [-100000]
		for i in range(len(y)):
			if (y[i] == 1):
				zp.append(mu[i])
			else:
				zn.append(-mu[i])
		zp.sort()
		zn.sort()
		p = len(zp)
		m = len(zn)
		zp.append(100000)
		zn.append(100000)
		lambd = 0
		found = False
		for k in range(p - 1):
			for l in range(m):
				lambd = 0.0
				for i in range(p - k - 1):
					lambd += zp[i + k + 1]
				for j in range(l):
					lambd += zn[j + 1]
				lambd /= (p - k + l - 1)
				if lambd <= zp[k + 1] and lambd >= zp[k] and lambd <= zn[l + 1] and lambd >= zn[l]:
					found = True
					break
			if found:
				break
		x = np.array(np.array(mu) - lambd * np.array(y))
		for i in range(len(x)):
			if x[i] < 0 :
				x[i] = 0
		return x

	mu0 = np.zeros_like(y)
	mu_traces, _ = gd.proj_gd(fp, proj, mu0, stepsize=0.1, tol=1e-8)
	mu = mu_traces[-1]

	# recover the primal optimal solution from dual optimal solution
	muXy = Xy * mu
	w = np.sum(muXy, axis = 0)
	b=0
	for i in range(len(mu)):
		if mu[i] > 0:
			b = y[i] - X[i]@w
			break;
	return w, b, mu
