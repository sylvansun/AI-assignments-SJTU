import numpy as np
import newton
import utils
import math


def f(x):
	return f_2d(x[0], x[1])


def fp(x):
	rst = np.array(x)
	rst[0] = np.exp(x[0] + 3 * x[1] - 0.1) + np.exp(x[0] - 3 * x[1] - 0.1) -np.exp(-x[0]-0.1)
	rst[1] = 3 * np.exp(x[0] + 3 * x[1] - 0.1) - 3 * np.exp(x[0] - 3 * x[1] - 0.1)
	return rst


def fpp(x):
	partial11 = np.exp(x[0] + 3 * x[1]) + np.exp(x[0] - 3 * x[1]) + np.exp(-x[0])
	partial22 = 9 * (np.exp(x[0] + 3 * x[1]) + np.exp(x[0] - 3 * x[1]))
	partial12 = 3 * (np.exp(x[0] + 3 * x[1]) - np.exp(x[0] - 3 * x[1]))
	rst = np.matrix([partial11, partial12, partial12, partial22]).reshape(2,2)
	rst *= np.exp(-0.1)
	return rst


def f_2d(x1, x2):
	return np.exp(x1+3*x2-0.1) + np.exp(x1 - 3*x2 - 0.1) + np.exp(-x1-0.1)


f_opt = 2*math.sqrt(2)/math.exp(0.1)


def gap(x):
	return f(x) - f_opt


x0 = np.array([-1.5, 1.0])
path = '../hw8/figures/'

x_traces = newton.newton(fp, fpp, x0)
f_value = f(x_traces[-1])
print()
print("Newton's method with x0=(-1.5,1)")
print('  number of iterations:', len(x_traces)-1)
print('  solution:', x_traces[-1])
print('  value:', f_value)
utils.plot_traces_2d(f_2d, x_traces, path+'nt_traces_1a.pdf')
utils.plot(gap, x_traces, path+'nt_gap_1a.pdf')

x0 = np.array([1.5, 1.0])
x_traces = newton.newton(fp, fpp, x0)
f_value = f(x_traces[-1])
print()
print("Newton's method with x0=(1.5,1)")
print('  number of iterations:', len(x_traces)-1)
print('  solution:', x_traces[-1])
print('  value:', f_value)
utils.plot_traces_2d(f_2d, x_traces, path+'nt_traces_1b.pdf')
utils.plot(gap, x_traces, path+'nt_gap_1b.pdf')
