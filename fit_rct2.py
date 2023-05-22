import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from scipy.interpolate import interp1d

def fn_sococv(soc):
    po = np.array([-1.2918e+00, 9.6896e+00, -2.1023e+01, 1.9749e+01, -8.0028e+00, 1.6362e+00, 3.4722e+00])
    ocv = np.polyval(po, soc)
    return ocv

def fn_ccv(fn_r0, fn_r1, fn_c1, fn_r2, fn_c2, soc, for_ocv_soc, t0, t1, current):
    ocv = fn_sococv(for_ocv_soc)
    v0 = fn_r0(soc) * current * t0
    v1 = fn_r1(soc) * current * (1 - np.exp(-t1 / fn_r1(soc) / fn_c1(soc)))
    v2 = fn_r2(soc) * current * (1 - np.exp(-t1 / fn_r2(soc) / fn_c2(soc)))
    ccv = ocv + v0 + v1 + v2
    return ccv

def rc_fitting_all(x, xdata, ydata, current):
    n = len(xdata)
    soc_ary = np.array([0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    r0_ary = x[0:9]
    r1_ary = x[9:18]
    c1_ary = x[18:27]
    r2_ary = x[27:36]
    c2_ary = x[36:]
    fn_r0 = interp1d(soc_ary, r0_ary, kind="linear")
    fn_r1 = interp1d(soc_ary, r1_ary, kind="linear")
    fn_c1 = interp1d(soc_ary, c1_ary, kind="linear")
    fn_r2 = interp1d(soc_ary, r2_ary, kind="linear")
    fn_c2 = interp1d(soc_ary, c2_ary, kind="linear")
    res = np.array([])
    for i in range(n):
        soc = soc_ary[i] + current * xdata[i] / 3600 / 3.0
        for_ocv_soc = soc.copy()
        if any(soc < 0.1):
            soc[soc < 0.1] = 0.1
        t1 = xdata[i]
        t0 = np.ones(len(t1))
        t0[0] = 0.0
        ccv_ary = fn_ccv(fn_r0, fn_r1, fn_c1, fn_r2, fn_c2, soc, for_ocv_soc, t0, t1, current)
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

x0 = np.array([3.726e-03, 7.001e-02, 3.606e-02, 2.820e-21, 9.052e-25, 3.984e-20, 5.693e-20, 1.397e-02, 3.222e-03,
    1.489e-01, 9.591e-02, 9.284e-02, 4.628e-02, 4.424e-02, 4.853e-02, 2.926e-02, 2.943e-02, 1.771e-02,
    2.280e+02, 3.398e+02, 4.798e+02, 5.525e+02, 4.821e+02, 8.973e+02, 7.251e+02, 8.319e+02, 1.331e+03,
    1.828e-01, 5.855e-02, 5.747e-02, 7.315e-02, 4.506e-02, 4.005e-02, 5.219e-02, 1.181e-02, 3.226e-04,
    5.326e-01, 7.040e+00, 6.131e+00, 2.289e+00, 8.575e+00, 1.378e+01, 8.003e+00, 1.149e+02, 1.000e+01])
bnds_min = np.zeros(len(x0))
bnds_max = np.ones(len(x0)) * 10000
res = least_squares(rc_fitting_all, x0, args=(xdata, ydata, current), bounds=(bnds_min, bnds_max), verbose=2)
print("res.x=")
print(res.x)

soc_ary = np.array([0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
r0_ary = res.x[0:9]
r1_ary = res.x[9:18]
c1_ary = res.x[18:27]
r2_ary = res.x[27:36]
c2_ary = res.x[36:]
fn_r0 = interp1d(soc_ary, r0_ary, kind="linear")
fn_r1 = interp1d(soc_ary, r1_ary, kind="linear")
fn_c1 = interp1d(soc_ary, c1_ary, kind="linear")
fn_r2 = interp1d(soc_ary, r2_ary, kind="linear")
fn_c2 = interp1d(soc_ary, c2_ary, kind="linear")
n = len(soc_ary)
for i in range(n):
    t1 = np.arange(0, 30.1, 0.1)
    t0 = np.ones(len(t1))
    t0[0] = 0.0
    soc = soc_ary[i] + current * t1 / 3600 / 3.0
    for_ocv_soc = soc.copy()
    if any(soc < 0.1):
        soc[soc < 0.1] = 0.1
    ccv_ary = fn_ccv(fn_r0, fn_r1, fn_c1, fn_r2, fn_c2, soc, for_ocv_soc, t0, t1, current)
    plt.plot(xdata[i], ydata[i], "o")
    plt.plot(t1, ccv_ary)
    plt.show()
