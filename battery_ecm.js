const math = require('mathjs');

const SOC_MIN = 0.1;
const SOC_MAX = 0.8;
const COEFFICIENTS = [-1.2918e+00, 9.6896e+00, -2.1023e+01, 1.9749e+01, -8.0028e+00, 1.6362e+00, 3.4722e+00];

function fn_soc_ocv(soc) {
    return COEFFICIENTS.slice().reverse().reduce((acc, coefficient, power) => {
        return acc + coefficient * Math.pow(soc, power);
    }, 0);
}

function validate_soc(soc) {
    return math.max(SOC_MIN, math.min(SOC_MAX, soc));
}

function interp1d(soc, soc_ary, ary) {
    // Implement a 1d cubic interpolation function
    // This is non-trivial in JavaScript and will need a third-party library or a manual implementation.
    // This function should return a function that accepts a soc value and returns the interpolated result.
}

function fn(soc, soc_ary, ary) {
    soc = validate_soc(soc);
    let f = interp1d(soc_ary, ary);
    return f(soc);
}

function fn_r0(soc) {
    const soc_ary = [0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8];
    const r0_ary = [0.16200, 0.10775, 0.078078, 0.060736, 0.036552, 0.027808, 0.023195, 0.019685, 0.0035443];
    return fn(soc, soc_ary, r0_ary);
}

// Similar implementations for fn_r1 and fn_c1

function calc_soc(soc, current, dt, ah) {
    return soc + current * dt / 3600.0 / ah;
}

function runge_kutta(f, x, t, dt) {
    let k1 = dt * f(x, t);
    let k2 = dt * f(x + 0.5 * k1, t + 0.5 * dt);
    let k3 = dt * f(x + 0.5 * k2, t + 0.5 * dt);
    let k4 = dt * f(x + k3, t + dt);
    x += (k1 + 2 * k2 + 2 * k3 + k4) / 6;
    return x;
}

function calc_v0(soc, current) {
    let r0 = fn_r0(soc);
    return r0 * current;
}

function calc_v1(soc, current, dt, v1) {
    let r1 = fn_r1(soc);
    let c1 = fn_c1(soc);
    let fv1 = (v, t) => current / c1 - v / r1 / c1;
    return runge_kutta(fv1, v1, 0, dt);
}

function equivalent_circuit_model(soc, current, dt, v1, ah) {
    soc = calc_soc(soc, current, dt, ah);
    let ocv = fn_soc_ocv(soc);
    let v0 = calc_v0(soc, current);
    v1 = calc_v1(soc, current, dt, v1);
    let dv = v0 + v1;
    let ccv = ocv + dv;
    let hgen = Math.abs(dv * current);
    return { soc, ccv, hgen, v1 };
}
