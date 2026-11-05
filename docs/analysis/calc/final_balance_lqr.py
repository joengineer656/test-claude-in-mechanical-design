"""Final robot (CAD rev 2) 2D balance check: disturbance rejection, 12 km/h, hill/tilt recovery, 6.4 / 6.9 kg.
Run: python3 final_balance_lqr.py > final_balance_lqr_output.txt   (needs leg_measure_rev2.json = solidcraft-cli eval cad/parts/leg.solidcraft)
Inertia/CoM: point masses from the CAD body centroids (com_assembly rules) + bbox-box own inertia (upper bound).
Wheel: MN5008 KV170 3.5:1, R_ll 0.27, 15 A, eta 0.9, 0.7*Vbus modulation limit (same convention as o9_wheel_motor.py).
Model: sim_lqr_2d.py physics + speed-dependent torque limit + push / slope / drag. Real hardware ~ sim; torques total for both wheels."""
import json, copy, math, sys
import numpy as np
import com_assembly as c
import sim_lqr_2d as cs

BOD = '../../../cad/assembly/src/bodies_nominal.json'
KV, RLL, IMAX, ETA, N = 170.0, 0.270, 15.0, 0.90, 3.5
KT, KE = 8.27 / KV, 1 / (KV * 2 * math.pi / 60)
R, G, MU, CRR, CDA = 0.085, 9.81, 0.8, 0.03, 0.9 * 0.30 * 0.45
I_WHEEL = 2.0e-3      # kg m2 per wheel (CAD estimate 1.4e-3 from hub/tyre/cover/ring; 2.0e-3 kept, conservative)

def cad_inertia():
    """Return {label: dict(M, mw, l, xc, mb, kg)} for sliced (6.35 kg) and solid (6.98 kg) rev 2 CAD."""
    bodies = json.load(open(BOD)); leg = json.load(open('leg_measure_rev2.json'))['bodies']
    DX = (28 - 10.57) - c.AXLE_X
    new = []
    for b in bodies:
        n = b['name']
        if n.startswith('Leg') and n[3] in 'LR' and n[4] == '_': continue
        b = copy.deepcopy(b)
        if n.startswith('WH') and n[2] in 'LR': b['com'][0] += DX
        new.append(b)
    for side, sg in (('L', 1), ('R', -1)):
        for b in leg:
            if b['name'].startswith('REF_'): continue
            com = list(b['center_of_mass']); com[1] *= sg
            bb = b['bbox']
            new.append(dict(name=f"Leg{side}_{b['name']}", com=com, vol=b['volume_mm3'], bbox=[bb['min'], bb['max']]))
    c.AXLE_X += DX
    c.LUMPS = [(n, g, (x + DX if n.startswith('WheelFasteners') else x), y, z) for n, g, x, y, z in c.LUMPS]
    out = {}
    for lab, sl in (('sliced', True), ('solid', False)):
        Mt, com, rows = c.run(new, sl)
        bb = {b['name']: b.get('bbox') for b in new}
        wheel = [r for r in rows if r[0][:2] == 'WH' and r[0][2] in 'LR' or r[0].startswith('WheelFasteners')]
        body = [r for r in rows if r not in wheel]
        mb = sum(r[2] for r in body); mw = sum(r[2] for r in wheel) / 2
        xc = sum(r[2] * r[3][0] for r in body) / mb; zc = sum(r[2] * r[3][2] for r in body) / mb
        Ip = sum(r[2] * ((r[3][0] - xc) ** 2 + (r[3][2] - zc) ** 2) for r in body)          # g mm2
        Ib = 0.0
        for r in body:
            b = bb.get(r[0])
            if b: Ib += r[2] / 12 * ((b[1][0] - b[0][0]) ** 2 + (b[1][2] - b[0][2]) ** 2)
        out[lab] = dict(M=Mt / 1e3, mw=mw / 1e3, mb=mb / 1e3, l=(zc - 85) / 1e3, dx=(xc - c.AXLE_X) / 1e3,
                        kg_pt=math.sqrt(Ip / mb) / 1e3, kg_box=math.sqrt((Ip + Ib) / mb) / 1e3)
    return out

def mk(M, l, kg, mw, Iw=I_WHEEL):
    return dict(cs.PARAMS, m_total=M, m_wheel=mw, l=l, k_g=kg, I_wheel=Iw, J_rotor=4e-5, N=N, KV=KV, i_max=IMAX, eta=ETA, r=R)

def u_lim(p, s, V):
    """Total wheel torque available: min(motor with voltage limit, traction). Same sign convention as u."""
    wr = N * (s[1] / R - s[3])                       # rotor speed rel. stator
    Ia = min(IMAX, max(0.0, (0.7 * V - KE * abs(wr)) / RLL))
    return min(2 * KT * Ia * N * ETA, MU * p['m_total'] * G * R), min(2 * KT * IMAX * N * ETA, MU * p['m_total'] * G * R), wr

def f(s, u, p, F=0.0, al=0.0):
    x, v, th, w = s
    M, mb = cs.matrices(p, th)
    Mtot = p['m_total']
    res = (CRR * Mtot * G * math.cos(al) + 0.5 * 1.2 * CDA * v * v) * math.tanh(v / 0.05)
    rhs = np.array([u / R + mb * p['l'] * math.sin(th) * w * w - Mtot * G * math.sin(al) - res + F,
                    -u + mb * G * p['l'] * math.sin(th - al) + F * p['l'] * math.cos(th)])
    a = np.linalg.solve(M, rhs)
    return np.array([v, a[0], w, a[1]])

def run(p, K, V, T, s0=(0, 0, 0, 0), vref=None, push=None, alpha=None, bias=0.0, dt=1e-3, hz=500, stop_deg=60):
    """Nonlinear sim. vref(t)->m/s, push(t)->N at CoM height, alpha(t)->slope rad, bias = IMU pitch offset (rad).
    Returns dict(ok, th_pk, u_pk, util_pk, v_pk, x_end, th_end, settle, u_end, speed_margin_min)."""
    s = np.array(s0, float); every = int(round(1 / (hz * dt))); u = u_n = 0.0
    xr = 0.0; o = dict(th_pk=0, u_pk=0, util=0, v_pk=0, margin=9, sat=0, settle=None)
    last_bad = 0.0; n = int(T / dt)
    for k in range(n):
        t = k * dt
        vr = vref(t) if vref else 0.0
        al = alpha(t) if alpha else 0.0
        if k % every == 0:
            xr += vr / hz
            e = s - np.array([xr, vr, 0, 0]); e[2] += bias - al   # IMU pitch = angle from true vertical
            lim, lim0, wr = u_lim(p, s, V)
            u, u_n = u_n, float(np.clip(-(K @ e)[0], -lim, lim))
            o['util'] = max(o['util'], abs(u) / lim0)
            o['margin'] = min(o['margin'], 1 - KE * abs(wr) / (0.7 * V))
            o['sat'] += abs(u_n) >= lim - 1e-9
        F = push(t) if push else 0.0
        k1 = f(s, u, p, F, al); k2 = f(s + dt / 2 * k1, u, p, F, al); k3 = f(s + dt / 2 * k2, u, p, F, al); k4 = f(s + dt * k3, u, p, F, al)
        s = s + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        o['th_pk'] = max(o['th_pk'], abs(s[2] - (al if alpha else 0))); o['u_pk'] = max(o['u_pk'], abs(u)); o['v_pk'] = max(o['v_pk'], abs(s[1]))
        if abs(s[2] - al) > math.radians(stop_deg): o['ok'] = False; return o
        if abs(s[2] - al) > math.radians(1.0) or abs(s[3]) > 0.05: last_bad = t
    o.update(ok=True, x_end=s[0], th_end=s[2] - (al if alpha else 0), u_end=u, last_bad=last_bad, s=s)
    return o

def bis(fn, lo, hi, it=12):
    """largest x in [lo,hi] with fn(x) True (fn monotone)."""
    if fn(hi): return hi
    for _ in range(it):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if fn(m) else (lo, m)
    return lo

def main():
    cad = cad_inertia()
    print("CAD inertia (rev 2, bodies_nominal + leg.solidcraft): non-wheel mass, CoM above axle, offset ahead of axle, k_g (point / +box)")
    for lab, d in cad.items():
        print(f"  {lab}: M {d['M']:.3f} kg, wheel module {d['mw']*1e3:.0f} g each, body {d['mb']:.3f} kg, l {d['l']*1e3:.1f} mm, CoM +{d['dx']*1e3:.1f} mm, "
              f"k_g {d['kg_pt']*1e3:.0f} / {d['kg_box']*1e3:.0f} mm  (I_b = {d['mb']*d['kg_box']**2:.4f} kg m2)")
    cases = (("6.4 kg (sliced CAD)", 6.4, cad['sliced']), ("6.9 kg (solid CAD)", 6.9, cad['solid']))
    for name, M, d in cases:
        p = mk(M, d['l'], d['kg_box'], d['mw'])
        A, B = cs.linear(p); K = cs.lqr(A, B, cs.Q, cs.R)
        pole = max(np.linalg.eigvals(A).real)
        print(f"\n## {name}: l {p['l']*1e3:.0f} mm, k_g {p['k_g']*1e3:.0f} mm, wheel {d['mw']:.3f} kg, I_wheel {I_WHEEL:.1e}; open-loop pole {pole:.1f} rad/s; K = {np.round(K,2)}")
        for V in (19.8, 22.2, 25.2):
            lim, lim0, _ = u_lim(p, np.zeros(4), V)
            print(f"  Vbus {V}: standstill torque limit {lim:.2f} N m total (motor 15 A {2*KT*IMAX*N*ETA:.2f}, traction {MU*M*G*R:.2f}); cont. 0.4*15 A = {2*KT*0.4*IMAX*N*ETA:.2f}")
        # --- tilt recovery
        rows = []
        for V in (19.8, 25.2):
            mt = bis(lambda a: run(p, K, V, 5.0, (0, 0, math.radians(a), 0))['ok'], 0, 45, 12)
            rows.append(f"{V} V: max recoverable tilt {mt:.1f} deg")
        print("  Tilt recovery (from rest, 5 s):", "; ".join(rows))
        for th in (5, 10, 20):
            r = run(p, K, 19.8, 4.0, (0, 0, math.radians(th), 0))
            print(f"    start {th:2d} deg @19.8 V: ok {r['ok']}, peak torque {r['u_pk']:.2f} N m ({r['util']*100:.0f} % of limit), peak speed {r['v_pk']:.2f} m/s, settled (<1 deg) at {r['last_bad']:.2f} s")
        # --- push
        print("  Push at CoM height, 0.1 s, standing, 19.8 V:")
        for Fp in (20, 40):
            r = run(p, K, 19.8, 4.0, push=lambda t, F=Fp: F if 0.2 <= t < 0.3 else 0.0)
            print(f"    {Fp} N x 0.1 s: ok {r['ok']}, peak tilt {math.degrees(r['th_pk']):.1f} deg, peak torque {r['u_pk']:.2f} N m, peak speed {r['v_pk']:.2f} m/s, settle (<1 deg, <0.05 rad/s) {r['last_bad']-0.3:.2f} s after push, x drift {r['x_end']*100:+.0f} cm")
        for V in (19.8, 25.2):
            Fm = bis(lambda F: run(p, K, V, 4.0, push=lambda t: F if 0.2 <= t < 0.3 else 0.0)['ok'], 0, 400, 12)
            print(f"    max recoverable 0.1 s push @ {V} V: {Fm:.0f} N (impulse {Fm*0.1:.1f} N s)")
        # --- 12 km/h
        v12 = 12 / 3.6
        prof = lambda t: float(np.clip(1.5 * (t - 0.5), 0, v12)) if t < 6 else float(np.clip(v12 - 1.5 * (t - 6), 0, v12))
        print("  12 km/h run (accel 1.5 m/s2 to 3.33 m/s, cruise, brake 1.5 m/s2), drag+rolling included:")
        for V in (19.8, 22.2, 25.2):
            r = run(p, K, V, 10.0, vref=prof)
            print(f"    {V} V: ok {r['ok']}, peak tilt {math.degrees(r['th_pk']):.1f} deg, peak torque {r['u_pk']:.2f} N m ({r['util']*100:.0f} % of 15 A/traction limit), min speed margin 1-Ke*w/(0.7V) {r['margin']*100:.0f} %, saturated samples {r['sat']}, end speed {r['s'][1]:.2f} m/s")
        vt = lambda V, vm: run(p, K, V, 12.0, vref=lambda t: min(vm, 1.5 * max(0, t - 0.5)))['ok']
        for V in (19.8, 25.2):
            vm = bis(lambda v: vt(V, v), 3.0, 8.0, 10)
            print(f"    top speed that still balances (sim, no push margin) @ {V} V: {vm*3.6:.1f} km/h")
        for V in (19.8, 22.2):
            Fm = bis(lambda F: run(p, K, V, 9.0, vref=lambda t: min(v12, 1.5*max(0, t-0.5)), push=lambda t: F if 5 <= t < 5.1 else 0.0)['ok'], 0, 200, 11)
            print(f"    max forward 0.1 s push while cruising at 12 km/h @ {V} V: {Fm:.0f} N")
        # --- hills
        print("  Slope (wheel contact stays, IMU = true pitch, slope ramped in 0.5 s at t=0.5; no integrator):")
        for a in (10, 15, 20, 25):
            ar = math.radians(a)
            al = lambda t, ar=ar: ar * float(np.clip((t - 0.5) / 0.5, 0, 1))
            r = run(p, K, 19.8, 8.0, alpha=al)
            need = M * G * R * math.sin(ar)
            print(f"    {a} deg: ok {r['ok']}, hold torque {need:.2f} N m total ({need/(2*KT*0.4*IMAX*N*ETA)*100:.0f} % of continuous), peak {r['u_pk']:.2f}, end offset {r['x_end']*100:+.0f} cm, end pitch {math.degrees(r['th_end']):+.1f} deg")
        for V in (19.8,):
            am = bis(lambda a: run(p, K, V, 8.0, alpha=lambda t: math.radians(a) * float(np.clip((t - 0.5) / 0.5, 0, 1)))['ok'], 0, 40, 10)
            print(f"    max slope that holds (sim, 15 A peak / traction) @ {V} V: {am:.1f} deg; continuous-torque slope limit {math.degrees(math.asin(min(1, 2*KT*0.4*IMAX*N*ETA/(M*G*R)))):.1f} deg")
        r = run(p, K, 19.8, 12.0, vref=lambda t: min(1.0, max(0, t - 3.0)), alpha=lambda t: math.radians(10) * float(np.clip((t - 0.5) / 0.5, 0, 1)))
        print(f"    drive up 10 deg at 1 m/s: ok {r['ok']}, peak torque {r['u_pk']:.2f} N m, tilt peak {math.degrees(r['th_pk']):.1f} deg")
        # --- CoM +2 mm / IMU zero error
        dth = d['dx'] / p['l']
        r = run(p, K, 19.8, 12.0, bias=-dth)
        print(f"  CoM +{d['dx']*1e3:.1f} mm ahead of axle = {math.degrees(dth):.2f} deg: hold torque m_b g dx = {p['m_total']*0+ (M-2*d['mw'])*G*d['dx']:.2f} N m total; "
              f"IMU zeroed to the frame (not to the CoM line) -> robot parks {abs(r['x_end'])*100:.0f} cm from its start, steady torque ~0 (trim the pitch zero in 6b)")
    # sensitivity: I_wheel and inertia
    d = cad['solid']; p = mk(6.9, d['l'], d['kg_box'], d['mw'], 1.4e-3); K = cs.lqr(*cs.linear(p), cs.Q, cs.R)
    print("\nSensitivity 6.9 kg, I_wheel 1.4e-3:", "tilt 10 deg ok", run(p, K, 19.8, 4.0, (0, 0, math.radians(10), 0))['ok'])
    p = mk(6.9, d['l'] + 0.05, d['kg_box'], d['mw']); K = cs.lqr(*cs.linear(p), cs.Q, cs.R)
    print("Sensitivity 6.9 kg, CoM 50 mm higher (l+0.05; leg 289):", "tilt 10 deg ok", run(p, K, 19.8, 4.0, (0, 0, math.radians(10), 0))['ok'],
          "max tilt", round(bis(lambda a: run(p, K, 19.8, 5.0, (0, 0, math.radians(a), 0))['ok'], 0, 45, 10), 1))

if __name__ == '__main__':
    main()
