const SOC_MIN = 0.1;
const SOC_MAX = 0.8;
const COEFFICIENTS = [-1.2918e+00, 9.6896e+00, -2.1023e+01, 1.9749e+01, -8.0028e+00, 1.6362e+00, 3.4722e+00];

class Interp1d {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }

    interpolate(soc) {
        let idx = 0;
        for (let i = 0; i < this.x.length - 1; i++) {
            if (this.x[i] <= soc && soc <= this.x[i+1]) {
                idx = i;
                break;
            }
        }
        const a = (this.y[idx + 1] - this.y[idx]) / (this.x[idx + 1] - this.x[idx]);
        const y = a * (soc - this.x[idx]) + this.y[idx];
        return y;
    }
}

function fn_soc_ocv(soc) {
    return COEFFICIENTS.slice().reverse().reduce((acc, coefficient, power) => {
        return acc + coefficient * Math.pow(soc, power);
    }, 0);
}

function validate_soc(soc) {
    return Math.max(SOC_MIN, Math.min(SOC_MAX, soc));
}

function interp1d(soc_ary, ary) {
    const interpolator = new Interp1d(soc_ary, ary);
    return interpolator.interpolate.bind(interpolator);
}

function fn(soc, soc_ary, ary) {
    soc = validate_soc(soc);
    const f = interp1d(soc_ary, ary);
    return f(soc);
}

function fn_r0(soc) {
    const soc_ary = [0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8];
    const r0_ary = [1.62322321e-01, 1.03056232e-01, 7.78689760e-02, 6.02799637e-02,
        3.65430740e-02, 2.30869539e-02, 3.58919538e-02, 1.95094583e-02,
        3.51122775e-03];
    return fn(soc, soc_ary, r0_ary);
}

function fn_r1(soc) {
    const soc_ary = [0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8];
    const r1_ary = [1.11216274e-01, 5.80927037e-02, 5.45906505e-02, 3.98037914e-02, 
        4.04388408e-02, 3.68435947e-02, 3.53608238e-02,2.49264780e-02, 
        1.33529555e-02];
    return fn(soc, soc_ary, r1_ary);
}

function fn_c1(soc) {
    const soc_ary = [0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8];
    const c1_ary = [9.51582328e+01, 7.29282262e+01, 1.80562595e+02, 1.80725822e+02, 
        2.48823073e+02, 1.65873625e+02,1.26423340e+02, 3.93429988e+02, 
        1.37549871e+03];
    return fn(soc, soc_ary, c1_ary);
}

function calc_soc(soc, current, dt, ah) {
    return soc + current * dt / 3600.0 / ah;
}

function runge_kutta(f, x, t, dt) {
    const k1 = dt * f(x, t);
    const k2 = dt * f(x + 0.5 * k1, t + 0.5 * dt);
    const k3 = dt * f(x + 0.5 * k2, t + 0.5 * dt);
    const k4 = dt * f(x + k3, t + dt);
    x += (k1 + 2 * k2 + 2 * k3 + k4) / 6;
    return x;
}

function calc_v0(soc, current) {
    const r0 = fn_r0(soc);
    return r0 * current;
}

function calc_v1(soc, current, dt, v1) {
    const r1 = fn_r1(soc);
    const c1 = fn_c1(soc);
    const fv1 = (v, t) => current / c1 - v / r1 / c1;
    return runge_kutta(fv1, v1, 0, dt);
}

function equivalent_circuit_model(soc, current, dt, v1, ah) {
    soc = calc_soc(soc, current, dt, ah);
    const ocv = fn_soc_ocv(soc);
    const v0 = calc_v0(soc, current);
    v1 = calc_v1(soc, current, dt, v1);
    const dv = v0 + v1;
    const ccv = ocv + dv;
    const hgen = Math.abs(dv * current);
    return { soc, ccv, hgen, v1 };
}

module.exports = {
    equivalent_circuit_model,
    fn_soc_ocv
};
