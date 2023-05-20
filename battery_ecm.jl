using Interpolations
using LinearAlgebra

const SOC_MIN = 0.1
const SOC_MAX = 0.8
const COEFFICIENTS = [-1.2918e+00, 9.6896e+00, -2.1023e+01, 1.9749e+01, -8.0028e+00, 1.6362e+00, 3.4722e+00]

function fn_soc_ocv(soc)
    return sum(coefficient * soc^(power-1) for (power, coefficient) in enumerate(reverse(COEFFICIENTS)))
end

function validate_soc(soc)
    return clamp(soc, SOC_MIN, SOC_MAX)
end

function fn(soc, soc_ary, ary)
    soc = validate_soc(soc)
    knots = (soc_ary,)
    itp = interpolate(knots, ary, Gridded(Linear()))
    return itp(soc)
end

function fn_r0(soc)
    soc_ary = [0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    r0_ary = [0.16200, 0.10775, 0.078078, 0.060736, 0.036552, 0.027808, 0.023195, 0.019685, 0.0035443]
    return fn(soc, soc_ary, r0_ary)
end

function fn_r1(soc)
    soc_ary = [0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    r1_ary = [0.10985, 0.075364, 0.061635, 0.042633, 0.042815, 0.036871, 0.034016, 0.027794, 0.017711]
    return fn(soc, soc_ary, r1_ary)
end

function fn_c1(soc)
    soc_ary = [0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    c1_ary = [92.268, 117.80, 181.77, 195.97, 246.10, 192.03, 157.80, 404.30, 1331.0]
    return fn(soc, soc_ary, c1_ary)
end

function calc_soc(soc, current, dt, ah)
    return soc + current * dt / 3600.0 / ah
end

function runge_kutta(f, x, t, dt)
    k1 = dt * f(x, t)
    k2 = dt * f(x + 0.5 * k1, t + 0.5 * dt)
    k3 = dt * f(x + 0.5 * k2, t + 0.5 * dt)
    k4 = dt * f(x + k3, t + dt)
    x += (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
    return x
end

function calc_v0(soc, current)
    r0 = fn_r0(soc)
    v0 = r0 * current
    return v0
end

function calc_v1(soc, current, dt, v1)
    r1 = fn_r1(soc)
    c1 = fn_c1(soc)
    fv1 = (v, t) -> current / c1 - v / r1 / c1
    v1 = runge_kutta(fv1, v1, 0, dt)
    return v1
end

function equivalent_circuit_model(soc, current, dt, v1, ah)
    soc = calc_soc(soc, current, dt, ah)
    ocv = fn_soc_ocv(soc)
    v0 = calc_v0(soc, current)
    v1 = calc_v1(soc, current, dt, v1)
    dv = v0 + v1
    ccv = ocv + dv
    hgen = abs(dv * current)
    return soc, ccv, hgen, v1
end
