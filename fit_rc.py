import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
import sys

def fn_sococv(soc):
    po = np.array([-1.2918e+00, 9.6896e+00, -2.1023e+01, 1.9749e+01, -8.0028e+00, 1.6362e+00, 3.4722e+00])
    ocv = np.polyval(po, soc)
    return ocv

def fn_ccv(r0, r1, c1, soc_ary, t0_ary, t1_ary, current):
    ocv = fn_sococv(soc_ary)
    v0 = r0 * current * t0_ary
    v1 = r1 * current * (1 - np.exp(-t1_ary / r1 / c1))
    ccv = ocv + v0 + v1
    return ccv

def rc_fitting(x, xdata, ydata, current, soc_ini):
    r0 = x[0]
    r1 = x[1]
    c1 = x[2]
    soc_ary = soc_ini + current * xdata / 3600 / 3.0
    t1_ary = xdata
    t0_ary = np.ones(len(xdata))
    t0_ary[0] = 0.0
    ccv_ary = fn_ccv(r0, r1, c1, soc_ary, t0_ary, t1_ary, current)
    res = ydata - ccv_ary
    return res

df = pd.read_csv("data.csv")
xdata = df.iloc[:, 0].values
ydata = df.iloc[:, 1].values

current = -3.0
soc_ini = 0.7

x0 = np.array([0.05, 0.1, 100])
res = least_squares(rc_fitting, x0, args=(xdata, ydata, current, soc_ini))
r0 = res.x[0]
r1 = res.x[1]
c1 = res.x[2]
t1_ary = np.arange(0, 30.1, 0.1)
t0_ary = np.ones(len(t1_ary))
t0_ary[0] = 0.0
soc_ary = soc_ini + current * t1_ary / 3600 / 3.0
ccv = fn_ccv(r0, r1, c1, soc_ary, t0_ary, t1_ary, current)
plt.plot(xdata, ydata, "o")
plt.plot(t1_ary, ccv)
plt.show()
print(r0, r1, c1)
