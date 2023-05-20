import numpy as np
from scipy.interpolate import interp1d

def fn_soc_ocv(soc):
    c = np.array([-1.2918e+00, 9.6896e+00, -2.1023e+01, 1.9749e+01, -8.0028e+00, 1.6362e+00, 3.4722e+00])
    return sum(coefficient * soc ** power for power, coefficient in enumerate(c[::-1]))

def fn_r0(soc):
    if soc < 0.1:
        soc = 0.1
    elif soc > 0.8:
        soc = 0.8
    soc_ary = np.array([0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    r0_ary = np.array([0.16200, 0.10775, 0.078078, 0.060736, 0.036552, 0.027808, 0.023195, 0.019685, 0.0035443])
    f = interp1d(soc_ary, r0_ary, kind="cubic")
    r0 = f(soc)
    return r0

def fn_r1(soc):
    if soc < 0.1:
        soc = 0.1
    elif soc > 0.8:
        soc = 0.8
    soc_ary = np.array([0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    r1_ary = np.array([0.10985, 0.075364, 0.061635, 0.042633, 0.042815, 0.036871, 0.034016, 0.027794, 0.017711])
    f = interp1d(soc_ary, r1_ary, kind="cubic")
    r1 = f(soc)
    return r1

def fn_c1(soc):
    if soc < 0.1:
        soc = 0.1
    elif soc > 0.8:
        soc = 0.8
    soc_ary = np.array([0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    c1_ary = np.array([92.268, 117.80, 181.77, 195.97, 246.10, 192.03, 157.80, 404.30, 1331.0])
    f = interp1d(soc_ary, c1_ary, kind="cubic")
    c1 = f(soc)
    return c1

def calc_soc(soc, current, dt, ah):
    return soc + current * dt / 3600.0 / ah

def runge_kutta(f, x, dt):
    k1 = dt * f(x)
    k2 = dt * f(x + 0.5 * k1)
    k3 = dt * f(x + 0.5 * k2)
    k4 = dt * f(x + k3)
    x += (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return x

def calc_v0(soc, current):
    r0 = fn_r0(soc)
    v0 = r0 * current
    return v0

def calc_v1(soc, current, dt, v1):
    r1 = fn_r1(soc)
    c1 = fn_c1(soc)
    fv1 = lambda v: current / c1 - v / r1 / c1
    v1 = runge_kutta(fv1, v1, dt)
    return v1

def equivalent_circuit_model(soc, current, dt, v1, ah):
    soc = calc_soc(soc, current, dt, ah)
    ocv = fn_soc_ocv(soc)
    v0 = calc_v0(soc, current)
    v1 = calc_v1(soc, current, dt, v1)
    dv = v0 + v1
    ccv = ocv + dv
    hgen = abs(dv * current)
    return soc, ccv, hgen, v1
