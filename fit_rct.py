import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from scipy.interpolate import interp1d
import sys

def fn_sococv(soc):
    po = np.array([-1.2918e+00, 9.6896e+00, -2.1023e+01, 1.9749e+01, -8.0028e+00, 1.6362e+00, 3.4722e+00])
    ocv = np.polyval(po, soc)
    return ocv

def fn_ccv(fn_r0, fn_r1, fn_c1, soc, for_ocv_soc, t0, t1, current):
    ocv = fn_sococv(for_ocv_soc)
    v0 = fn_r0(soc) * current * t0
    v1 = fn_r1(soc) * current * (1 - np.exp(-t1 / fn_r1(soc) / fn_c1(soc)))
    ccv = ocv + v0 + v1
    return ccv

def rc_fitting_all(x, xdata, ydata, current):
    n = len(xdata)
    soc_ary = np.array([0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    r0_ary = x[0:9]
    r1_ary = x[9:18]
    c1_ary = x[18:]
    fn_r0 = interp1d(soc_ary, r0_ary, kind="cubic")
    fn_r1 = interp1d(soc_ary, r1_ary, kind="cubic")
    fn_c1 = interp1d(soc_ary, c1_ary, kind="cubic")
    res = np.array([])
    for i in range(n):
        soc = soc_ary[i] + current * xdata[i] / 3600 / 3.0
        for_ocv_soc = soc.copy()
        if any(soc < 0.1):
            soc[soc < 0.1] = 0.1
        t1 = xdata[i]
        t0 = np.ones(len(t1))
        t0[0] = 0.0
        ccv_ary = fn_ccv(fn_r0, fn_r1, fn_c1, soc, for_ocv_soc, t0, t1, current)
        tmp = ydata[i] - ccv_ary
        res = np.hstack([res, tmp])
    return res

finname_list = ["soc01.csv", "soc015.csv", "soc02.csv", "soc03.csv", 
                "soc04.csv", "soc05.csv", "soc06.csv", "soc07.csv", "soc08.csv"]
xdata = []
ydata = []
for finname in finname_list:
    df = pd.read_csv(finname)
    xdata.append(df.iloc[:, 0].values)
    ydata.append(df.iloc[:, 1].values)

current = -3.0
soc_ini = 0.1

# r0 = [0.16, 0.11, 0.078, 0.061, 0.037, 0.028, 0.023, 0.02, 0.004]
# r1 = [0.11, 0.075, 0.062, 0.043, 0.043, 0.037, 0.034, 0.028, 0.018]
# c1 = [92, 118, 182, 196, 246, 192, 158, 404, 1331]
# because ValueError: `x0` must have at most 1 dimension.
x0 = np.array([0.16, 0.11, 0.078, 0.061, 0.037, 0.028, 0.023, 0.02, 0.004,
               0.11, 0.075, 0.062, 0.043, 0.043, 0.037, 0.034, 0.028, 0.018,
               92, 118, 182, 196, 246, 192, 158, 404, 1331])
res = least_squares(rc_fitting_all, x0, args=(xdata, ydata, current))
print("res.x=")
print(res.x)

soc_ary = np.array([0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
r0_ary = res.x[0:9]
r1_ary = res.x[9:18]
c1_ary = res.x[18:]
fn_r0 = interp1d(soc_ary, r0_ary, kind="cubic")
fn_r1 = interp1d(soc_ary, r1_ary, kind="cubic")
fn_c1 = interp1d(soc_ary, c1_ary, kind="cubic")
n = len(soc_ary)
for i in range(n):
    t1 = np.arange(0, 30.1, 0.1)
    t0 = np.ones(len(t1))
    t0[0] = 0.0
    soc = soc_ary[i] + current * t1 / 3600 / 3.0
    for_ocv_soc = soc.copy()
    if any(soc < 0.1):
        soc[soc < 0.1] = 0.1
    print(soc, for_ocv_soc)
    ccv_ary = fn_ccv(fn_r0, fn_r1, fn_c1, soc, for_ocv_soc, t0, t1, current)
    plt.plot(xdata[i], ydata[i], "o")
    plt.plot(t1, ccv_ary)
    plt.show()
