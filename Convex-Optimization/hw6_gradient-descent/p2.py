import numpy as np
import utils
import gd

X = [2, 0, 0, 1, 0, 0]
y = [3, 2, 2]
X = np.array(X).reshape(3, 2)
y = np.array(y)


def f(w):
    return w.T@X.T@X@w - 2 * y.T@X@w + y.T@y


def fp(w):
    return 2 * (X.T@X@w - X.T@y)


w0 = np.array([1, 1])
stepsize=0.01
w_traces = gd.gd_const_ss(fp, w0, stepsize=stepsize)
print(f'stepsize={stepsize}, number of iterations={len(w_traces)-1}')
print('optimum variable of running gradient descent: ', w_traces[len(w_traces)-1])
print('optimum variable of running np.linalg: ', np.linalg.solve(X.T@X, X.T@y))
utils.plot_f(f, w_traces, f'../hw6/figures/lso_ss{stepsize}.pdf')
