"""Re-run at CAD mass (6.0 / 6.4 / 6.9 kg), unsprung 0.84 kg/side, hip min height 140 mm.
Run: python3 o14_cad_mass.py > o14_output.txt  (reuses theory_calc, o9_wheel_motor, p3_spring, sim_lqr_2d)
Leg synthesis geometry is the P1 4-bar (B pivot (46,34) vs CAD (46,30): <5 % effect on J, not re-synthesised).
"""
import math
import numpy as np
import theory_calc as tc
import o9_wheel_motor as o9
import p3_spring as sp
import o13_rerun as o
import sim_lqr_2d as cs

MU_SIDE = 0.84
Y_MIN = 0.140
HIP_N = 8
RUNS = (6.0, 6.4, 6.9)


_LEG = []


def legs_cached():
    """Synthesise the P1 leg ONCE with the original 101 mm crouch (synth score depends on Y_CROUCH)."""
    if not _LEG:
        tc.Y_CROUCH = 0.101
        _LEG.append(o.legs_geom())
    return _LEG[0]


def setup(mass):
    p, ph, y, K, C, W, J = legs_cached()
    tc.set_motor(130)
    tc.M_TOT = mass
    tc.Y_CROUCH = Y_MIN
    sp.A = np.array([94.1, 71.2]) * 1e-3          # P3 re-fit anchor (span 111 -> ~150 mm), 2.7 N/mm, 8 N
    return p, ph, y, K, C, W, J


def spring_fn(k, F0, r=0.040):
    return sp.make(k, F0, r)[0]


def run(mass):
    p, ph, y, K, C, W, J = setup(mass)
    legs = (ph, y, J)
    mb = mass - 2 * MU_SIDE
    print(f"\n# M = {mass} kg, unsprung {MU_SIDE}/side, m_b = {mb:.2f} kg")
    v = math.sqrt(2 * 9.81 * tc.JUMP_H)
    vb = v * mass / mb
    E = mb * 9.81 * (tc.Y_EXT - Y_MIN) + 0.5 * mb * vb**2
    print(f"Jump energy: ideal {E:.1f} J (snatch loss {0.5*mb*vb**2-0.5*mass*v**2:.1f} J), /0.85 = {E/0.85:.1f} J; "
          f"stroke {tc.Y_EXT-Y_MIN:.3f} m")
    spr = spring_fn(2700, 8.0)
    print("| case | 19.8 V sim / real cm | 22.2 V sim / real cm | peak hip A / Nm | battery A |")
    print("|---|---|---|---|---|")
    for lab, s in (("springs 2.7 N/mm (5.5 J)", spr), ("no springs", lambda q: 0.0)):
        a = tc.jump(HIP_N, 19.8, mb, 2 * MU_SIDE, s, legs)
        b = tc.jump(HIP_N, 22.2, mb, 2 * MU_SIDE, s, legs)
        print(f"| {lab} | {a['h']*100:.1f} / {a['h']*80:.1f} | {b['h']*100:.1f} / {b['h']*80:.1f} | "
              f"{a['Imax']:.0f} / {tc.KT*a['Imax']*HIP_N*tc.ETA_H:.1f} | {a['Ibat']:.0f} |")
    # fixes
    print("Fixes (19.8 V real cm, from 140):")
    rows = []
    for lab, k, F0, hn, N in (("stiffer 4.1 N/mm", 4100, 8, 8, 8), ("4.1 N/mm, F0 20", 4100, 20, 8, 8),
                              ("5.5 N/mm", 5500, 8, 8, 8), ("hip 6:1 + 2.7 N/mm", 2700, 8, 6, 6),
                              ("hip 6:1 + 4.1 N/mm", 4100, 8, 6, 6)):
        s = spring_fn(k, F0)
        r = tc.jump(N, 19.8, mb, 2 * MU_SIDE, s, legs)
        r2 = tc.jump(N, 22.2, mb, 2 * MU_SIDE, s, legs)
        phi_c = float(np.interp(Y_MIN, y, ph))
        sl = float(sp.spring_len(np.array(phi_c))) - float(sp.spring_len(np.radians(-72.677)))
        print(f"  {lab}: {r['h']*80:.1f} cm @19.8 V, {r2['h']*80:.1f} @22.2 V, F_max {F0+k*sl:.0f} N, E/leg {F0*sl+0.5*k*sl**2:.2f} J")

    # hip torque statics (worst pose within 140..289)
    F = mb * 9.81 / 2
    ok = y >= Y_MIN
    print("Hip torque per leg (worst pose in stroke):")
    for name, f in (("standing", F), ("single-leg climb (x2.25)", 2.25 * F)):
        worst = max(abs(tc.statics(p, K[i], C[i], W[i], f)[0]) for i in range(len(y)) if ok[i])
        print(f"  {name}: leg {f:.1f} N, {worst:.2f} Nm, no-spring motor {worst/(HIP_N*tc.ETA_H)/tc.KT:.1f} A")
    i_n = int(np.argmin(abs(y - tc.Y_NOM)))
    for nm, i in (("nominal", i_n), ("crouch 140", int(np.argmin(abs(y - Y_MIN))))):
        g_t = F * J[i]
        s_t = spr(ph[i])
        print(f"  {nm}: gravity {g_t:.2f} Nm, spring {s_t:.2f} Nm -> motor {abs(g_t-s_t):.2f} Nm = "
              f"{abs(g_t-s_t)/(HIP_N*tc.ETA_H)/tc.KT:.1f} A")
    f = 2.25 * F
    i = i_n
    gt = f * J[i]
    print(f"  climb at nominal with spring: motor {abs(gt-spr(ph[i])):.2f} Nm = {abs(gt-spr(ph[i]))/(HIP_N*tc.ETA_H)/tc.KT:.1f} A "
          f"(cont limit 20 A hip, thermal 5.7 Nm)")

    # landing: soft end stop 10 kN/m engaging 20 mm above min height
    src_ns = vars(tc).copy()
    import inspect
    s2 = inspect.getsource(tc.landing).replace("25000.0 * max(0.0, (Y_CROUCH + 0.005) - L)",
                                               f"10000.0 * max(0.0, {Y_MIN + 0.020} - L)").replace("def landing", "def landing2")
    exec(s2, src_ns)
    print("Landing (10 kN/m TPU stop engaging at 160 mm; one-wheel cases use full m_b):")
    print("| LC | body g | unsprung g | axle N | leg N | hip torque Nm (total/motor) | knee pin N | stroke mm | hip gear spike Nm | wheel gear spin-up Nm |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    frac = 3.5**2 * 4e-5 / (3.5**2 * 4e-5 + 2.0e-3)
    for name, mbody, mode in (("A sym ctrl", mb / 2, "controlled"), ("B sym off", mb / 2, "off"),
                              ("C one ctrl", mb, "controlled"), ("D one off", mb, "off")):
        pk = src_ns["landing2"](mbody, MU_SIDE, legs, spr, HIP_N, mode, y0=0.27)
        i = int(np.argmin(abs(y - pk["y_at"])))
        T, fc, fk = tc.statics(p, K[i], C[i], W[i], pk["Fl"])
        print(f"| {name} | {pk['ab']:.1f} | {pk['au']:.0f} | {pk['Ft']:.0f} | {pk['Fl']:.0f} | {pk['Th']:.1f} / {pk['Tm']:.1f} | "
              f"{fk:.0f} | {pk['s']*1e3:.0f} | {pk['Tgear_es']:.1f} | {0.8*pk['Ft']*0.085*frac:.1f} |")

    # speed / torque (wheel MN5008 KV170 3.5:1)
    saved = tc.CRR
    tc.CRR = saved * mass / 3.3
    out = []
    for R in (0.27, 0.72):
        v0, vl, Tp, Tc, v2 = o9.perf(170, R, 15.0, 3.5)
        out.append(f"R={R}: loaded {vl:.1f} km/h, 2 Nm/wheel to {v2:.1f} km/h")
    tc.CRR = saved
    trac = 0.8 * mass * 9.81 * 0.085 / 2
    lean = mass * 9.81 * 0.011
    print(f"Speed: {'; '.join(out)}; peak/cont per wheel 2.30/0.92 Nm; traction cap/wheel {trac:.2f} Nm; "
          f"CoM +11 mm forward holds {lean:.2f} Nm total continuous ({lean/2:.2f}/wheel, {lean/2/0.92*100:.0f} % of 0.92 cont)")

    # balance LQR sim
    print("Balance LQR (torques TOTAL both wheels; I_wheel 2e-3 per wheel, k_g 0.13):")
    for l in (0.15, 0.23, 0.35):
        pp = dict(cs.PARAMS, m_total=mass, m_wheel=MU_SIDE, l=l, N=3.5, KV=170.0, J_rotor=4e-5, i_max=15.0,
                  I_wheel=2.0e-3, k_g=0.13)
        A_, B_ = cs.linear(pp)
        Kg = cs.lqr(A_, B_, cs.Q, cs.R)
        u_lim, motor, tract = cs.torque_limit(pp)
        mt = cs.max_tilt(pp, Kg, u_lim)
        s = []
        for th0 in (5, 10):
            okl, pkl, dv = cs.sim(pp, Kg, th0, u_lim)
            s.append(f"{th0}deg: floor {cs.hold_torque(pp, th0)[0]:.2f}, min-sat {cs.min_torque(pp, Kg, th0):.2f}, "
                     f"LQR pk {cs.sim(pp, Kg, th0)[1]:.1f}, ok@limit {okl}, dv {dv:.2f}")
        print(f"  l={l}: " + " | ".join(s) + f" | max tilt {mt:.1f} deg | limit {u_lim:.2f} Nm (motor {motor:.2f}, traction {tract:.2f})")


def main():
    # check anchor span at the 140 mm crouch
    setup(6.4)
    p, ph, y, K, C, W, J = legs_cached()
    phi140 = float(np.interp(Y_MIN, y, ph))
    print(f"Spring span ext {float(sp.spring_len(np.radians(-72.677)))*1e3:.1f} mm, at 140 mm crouch "
          f"{float(sp.spring_len(np.array(phi140)))*1e3:.1f} mm; thigh angle at 140: {math.degrees(phi140):.1f} deg")
    for m in RUNS:
        run(m)
    # what mass passes 20 cm at 19.8 V with springs, from 140
    print("\n## Max mass for 20 cm real @19.8 V (springs 2.7 N/mm, 40 A hips)")
    for m in np.arange(4.4, 7.01, 0.2):
        p, ph, y, K, C, W, J = setup(float(m))
        mb = m - 2 * MU_SIDE
        r = tc.jump(HIP_N, 19.8, mb, 2 * MU_SIDE, spring_fn(2700, 8.0), (ph, y, J))
        print(f"  M={m:.1f}: {r['h']*80:.1f} cm")


if __name__ == "__main__":
    main()
