"""O13: re-run jump, speed/torque, landing and control LQR sim at M = 4.31 kg, unsprung 0.536 kg/side.
Run: python3 o13_rerun.py > o13_output.txt   (reuses theory_calc.py, o9_wheel_motor.py, sim_lqr_2d.py unchanged)
"""
import math
import numpy as np
import theory_calc as tc
import o9_wheel_motor as o9
import sim_lqr_2d as cs

M, MU_SIDE = 4.31, 0.536
MB = M - 2 * MU_SIDE
HIP_N = 8


def wheel_check():
    print("## Wheel MN5008 KV170, 3.5:1, 19.8 V (0.7*KV*Vbus), M = 4.31 kg")
    print("| R_ll ohm | loaded km/h (30 % headroom) | v with 2.0 Nm available km/h | T peak / cont Nm per wheel | control N_max |")
    print("|---|---|---|---|---|")
    for R in (0.270, 0.720):
        tc_crr_mass = 3.3
        # perf() uses 3.3 kg for rolling resistance; scale CRR so the force matches 4.31 kg
        saved = tc.CRR
        tc.CRR = saved * M / tc_crr_mass
        v0, vl, Tp, Tc, v2 = o9.perf(170, R, 15.0, 3.5)
        tc.CRR = saved
        nmax = 0.85 * 0.7 * 170 * 19.8 * 2 * math.pi / 60 * 0.085 / (3.333 + 1.0)
        print(f"| {R} | {vl:.1f} | {v2:.1f} | {Tp:.2f} / {Tc:.2f} | {nmax:.2f} (N=3.5) |")
    print(f"Traction cap per wheel mu*M*g*r/2 = {0.8*M*9.81*0.085/2:.2f} Nm")


def legs_geom():
    (p, res), phi = tc.synth_leg()
    _, idx, _, _, _ = res
    ph, y, x, K, C, W, mus = tc.leg_tables(p, phi, idx)
    J = np.abs(np.gradient(-W[:, 1], ph))
    return p, ph, y, K, C, W, J


def main():
    wheel_check()
    p, ph, y, K, C, W, J = legs_geom()
    legs = (ph, y, J)
    tc.set_motor(130)
    tc.M_TOT = M
    spr = tc.make_spring(ph, y, J, MB * 9.81 / 2, E_leg=4.0)[0]   # 8 J total, unchanged hardware

    print(f"\n## Hip torque, m_b = {MB:.2f} kg (statics, per leg)")
    F = MB * 9.81 / 2
    for name, f in (("standing", F), ("height change +0.5 g", 1.5 * F), ("single-leg climb", 2.25 * F)):
        worst = max(abs(tc.statics(p, K[i], C[i], W[i], f)[0]) for i in range(len(y)))
        print(f"{name}: leg {f:.1f} N -> worst hip torque {worst:.2f} Nm "
              f"({worst/(HIP_N*tc.ETA_H)/tc.KT:.1f} A motor)")
    i_nom = int(np.argmin(abs(y - tc.Y_NOM)))
    hold = spr(ph[i_nom]) - F * J[i_nom]
    print(f"nominal stance: spring {spr(ph[i_nom]):.2f} Nm vs gravity {F*J[i_nom]:.2f} Nm -> motor holds {hold:+.2f} Nm "
          f"({abs(hold)/(HIP_N*tc.ETA_H)/tc.KT:.1f} A)")

    v = math.sqrt(2 * 9.81 * tc.JUMP_H)
    vb = v * M / MB
    E = MB * 9.81 * (tc.Y_EXT - tc.Y_CROUCH) + 0.5 * MB * vb**2
    print(f"\n## Jump, M={M}, m_b={MB:.2f}: E_ideal {E:.1f} J (snatch loss {0.5*MB*vb**2-0.5*M*v**2:.1f} J), /0.85 = {E/0.85:.1f} J")
    print("| V | springs | sim jump cm | real est. (x0.80) cm | push ms | spring J | motor J | peak I A | peak hip torque Nm | battery A |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for V in (22.2, 19.8):
        for lab, s in (("8 J", spr), ("none", lambda q: 0.0)):
            r = tc.jump(HIP_N, V, MB, 2 * MU_SIDE, s, legs)
            Tpk = tc.KT * r["Imax"] * HIP_N * tc.ETA_H
            print(f"| {V} | {lab} | {r['h']*100:.1f} | {r['h']*80:.1f} | {r['t']*1e3:.0f} | {r['Es']:.1f} | {r['Em']:.1f} | "
                  f"{r['Imax']:.0f} | {Tpk:.1f} | {r['Ibat']:.0f} |")
    # with hip current capped at 20 A (normal limit) for reference
    tc.I_PEAK = 20.0
    r = tc.jump(HIP_N, 19.8, MB, 2 * MU_SIDE, spr, legs)
    print(f"(hip limit 20 A instead of 40 A, 19.8 V, springs: {r['h']*100:.1f} cm sim)")
    tc.I_PEAK = 40.0

    print("\n## Landing load cases, M = 4.31 kg, unsprung 0.536 kg/side, hip 8:1 KV130")
    print("| LC | body g | unsprung g | axle N | leg N | hip torque total / motor Nm | knee pin N | coupler N | hip bearing N | stroke mm | wheel gear spin-up Nm |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    frac = 3.5**2 * 4e-5 / (3.5**2 * 4e-5 + tc.I_WHEEL)
    for name, mbody, mu, mode in (("A symmetric, controlled", MB / 2, MU_SIDE, "controlled"),
                                  ("B symmetric, motors off", MB / 2, MU_SIDE, "off"),
                                  ("C one wheel first, controlled", MB, MU_SIDE, "controlled"),
                                  ("D one wheel first, motors off", MB, MU_SIDE, "off")):
        pk = tc.landing(mbody, mu, legs, spr, HIP_N, mode)
        i = int(np.argmin(abs(y - pk["y_at"])))
        T, fc, fk = tc.statics(p, K[i], C[i], W[i], pk["Fl"])
        print(f"| {name} | {pk['ab']:.1f} | {pk['au']:.0f} | {pk['Ft']:.0f} | {pk['Fl']:.0f} | {pk['Th']:.1f} / {pk['Tm']:.1f} | "
              f"{fk:.0f} | {fc:.0f} | {fk:.0f} | {pk['s']*1e3:.0f} | {0.8*pk['Ft']*0.085*frac:.1f} |")
    print(f"(wheel gear inertia share at 3.5:1 = {frac:.2f})")

    print("\n## Control LQR sim (sim_lqr_2d.py, unchanged code) at 4.31 kg")
    print("| l m | tilt | hold floor Nm | LQR peak Nm | peak @limit Nm | min saturation Nm | dv peak m/s | max recoverable tilt |")
    print("|---|---|---|---|---|---|---|---|")
    for l in (0.15, 0.23, 0.35):
        pp = dict(cs.PARAMS, m_total=M, m_wheel=MU_SIDE, l=l, N=3.5, KV=170.0, J_rotor=4e-5, i_max=15.0)
        A, B = cs.linear(pp)
        Kg = cs.lqr(A, B, cs.Q, cs.R)
        u_lim, motor, traction = cs.torque_limit(pp)
        mt = cs.max_tilt(pp, Kg, u_lim)
        for th0 in (5, 10):
            ok, pk, _ = cs.sim(pp, Kg, th0)
            okl, pkl, dv = cs.sim(pp, Kg, th0, u_lim)
            print(f"| {l} | {th0}° | {cs.hold_torque(pp, th0)[0]:.2f} | {pk:.2f} | {pkl:.2f}{'' if okl else ' FAIL'} | "
                  f"{cs.min_torque(pp, Kg, th0):.2f} | {dv:.2f} | {mt:.1f}° |")
    print(f"limit total {u_lim:.2f} Nm = min(motor 15 A {motor:.2f}, traction {traction:.2f}); torques are totals for both wheels")


if __name__ == "__main__":
    main()
