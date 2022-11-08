import numpy as np


def soft_th(w, th):
	for i in range(2):
		if w[i] > th:
			w[i] = w[i] - th
		elif w[i] < -th:
			w[i] = w[i] + th
		else:
			w[i] = 0
	return w


# this function does not work properly...
def soft_th2(w, th):
	rst = np.sign(w) * (np.abs(w) - th)
	np.clip(rst, 0, rst, out=rst)
	return rst


def ista(X, y, lambd, w0, stepsize, tol=1e-9, maxiter=1000):
	w_traces = [np.array(w0)]
	w = np.array(w0)
	for k in range(maxiter):
		w_next = soft_th(w-stepsize*X.T@(X@w-y), lambd*stepsize)
		if np.linalg.norm(w_next - w) < tol:
			break
		w = w_next
		w_traces.append(np.array(w))
	return w_traces
