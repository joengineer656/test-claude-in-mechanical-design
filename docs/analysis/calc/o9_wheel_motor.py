"""O9 follow-up: light wheel hub motor selection + jump re-run with new unsprung mass.
Run: python3 o9_wheel_motor.py  (reuses theory_calc.py; output -> o9_output.txt)
Speed limit: ODrive v3.6 max rpm = 0.7*KV*Vbus. Requirements (control.md R-W1/R-W2):
peak >= 2.0 Nm, cont >= 0.6 Nm per wheel; 12 km/h at 19.8 V; R-W2: v_top + 1.0 m/s with load.
"""
import math
import theory_calc as tc

V_LOW = 19.8
R_W = 0.085
ETA = 0.90
I_DRIVER = 40.0
# name: KV, R_ll ohm, I_peak (A, 180 s mfr rating), mass kg, dims, rotor inertia est kg m2, source key
MOTORS = {
    "T-Motor MN5008 KV170": (170, 0.270, 15.0, 0.128, "D55.6 x 32, 24N28P, 6 mm shaft", 4e-5),
    "T-Motor MN5008 KV340": (340, 0.055, 35.0, 0.135, "D55.6 x 32, 24N28P, 6 mm shaft", 4e-5),
    "T-Motor MN6007II KV160": (160, 0.227, 18.0, 0.159, "D67.2 x 26.1, 12N22P, 6 mm shaft", 7e-5),
    "iPower GM5208-12 (gimbal)": (25, 15.2, 1.5, 0.200, "D63 x 23, 12N14P, 12 mm hollow", 8e-5),
}
I_CONT_FRAC = 0.4          # continuous = 40 % of 180 s rating (enclosed in wheel, no prop air) - ASSUMPTION
GEARBOX_MASS = {1: 0.0, 3: 0.060, 3.5: 0.062, 4: 0.065, 5: 0.070, 6: 0.075, 8: 0.110, 10: 0.120}  # printed + steel pins


def perf(kv, R, Ipk, N):
    kt, ke = 8.27 / kv, 1.0 / (kv * 2 * math.pi / 60)
    I = min(Ipk, I_DRIVER)
    veff = 0.7 * V_LOW
    v0 = veff / ke / N * R_W * 3.6
    Tpk = kt * min(I, veff / R) * N * (ETA if N > 1 else 1.0)   # stall current also limited by V/R
    Tc = kt * I_CONT_FRAC * Ipk * N * (ETA if N > 1 else 1.0)
    vl = 0.0                                   # loaded: resistive + 30 % of peak kept for balance
    for i in range(1, 3000):
        vv = i * 0.005
        wm = vv / R_W * N
        Ia = min(I, max(0.0, (veff - ke * wm) / R))
        Tres = (tc.CRR * 3.3 * 9.81 + 0.5 * 1.2 * tc.CDA * vv**2) * R_W / 2
        if kt * Ia * N * ETA < Tres + 0.3 * Tpk:
            break
        vl = vv
    # speed at which 2.0 Nm (R-W1 peak) is still available
    v2 = 0.0
    for i in range(1, 3000):
        vv = i * 0.005
        Ia = min(I, max(0.0, (veff - ke * vv / R_W * N) / R))
        if kt * Ia * N * ETA < 2.0:
            break
        v2 = vv
    return v0, vl * 3.6, Tpk, Tc, v2 * 3.6


def main():
    print("## Candidate wheel motors x ratio (Vbus 19.8 V, 0.7*KV*Vbus, D170 wheel)")
    print("| motor | N | no-load km/h | loaded km/h (30 % headroom) | v with 2.0 Nm still available km/h | T peak Nm | T cont Nm | R-W1 | 12 km/h loaded | control rule N<=Nmax | unsprung/side kg |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for name, (kv, R, Ipk, m, dims, Jr) in MOTORS.items():
        nmax = 0.85 * 0.7 * kv * V_LOW * 2 * math.pi / 60 * R_W / (3.333 + 1.0)   # control.md rule
        for N in ((1,) if kv < 60 else (1, 3, 3.5, 4, 5, 6, 8, 10)):
            v0, vl, Tp, Tc, v2 = perf(kv, R, Ipk, N)
            unspr = m + GEARBOX_MASS[N] + 0.210 + 0.040 + 0.025
            ok1 = Tp >= 2.0 and Tc >= 0.6
            print(f"| {name} | {N:g}:1 | {v0:.1f} | {vl:.1f} | {v2:.1f} | {Tp:.2f} | {Tc:.2f} | {'ok' if ok1 else 'FAIL'} | "
                  f"{'ok' if vl >= 12 else 'FAIL'} | {'ok' if N <= nmax else 'FAIL'} ({nmax:.2f}) | {unspr:.3f} |")

    # jump re-run with chosen motor (MN5008 KV170, 4:1)
    m_side = 0.128 + GEARBOX_MASS[4] + 0.210 + 0.040 + 0.025
    print(f"\n## Jump re-run, hub unsprung {m_side:.3f} kg/side (was 0.721), hip 8308 KV130 8:1, spring 8 J")
    (p, res), phi = tc.synth_leg()
    _, idx, _, _, _ = res
    ph, y, x, K, C, W, mus = tc.leg_tables(p, phi, idx)
    import numpy as np
    J = np.abs(np.gradient(-W[:, 1], ph))
    legs = (ph, y, J)
    tc.set_motor(130)
    for M in (3.6, 3.2):
        mb = M - 2 * m_side
        spr = tc.make_spring(ph, y, J, mb * 9.81 / 2, E_leg=4.0)[0]
        v = math.sqrt(2 * 9.81 * tc.JUMP_H)
        vb = v * M / mb
        E = mb * 9.81 * (tc.Y_EXT - tc.Y_CROUCH) + 0.5 * mb * vb**2
        lost = 0.5 * mb * vb**2 - 0.5 * M * v**2
        print(f"M={M} kg, m_b={mb:.2f}: E_ideal={E:.1f} J (snatch loss {lost:.1f} J), /0.85 = {E/0.85:.1f} J")
        for V in (22.2, 19.8):
            for lab, s in (("spring", spr), ("none", lambda q: 0.0)):
                r = tc.jump(8, V, mb, 2 * m_side, s, legs)
                print(f"   {V} V {lab}: jump {r['h']*100:.1f} cm, push {r['t']*1e3:.0f} ms, snatch loss {r['lost']:.1f} J")
        tc.M_TOT = M
        for name, mode, mbody, mu in (("A symmetric controlled", "controlled", mb / 2, m_side),
                                      ("C one wheel first controlled", "controlled", mb, m_side),
                                      ("D one wheel first motors off", "off", mb, m_side)):
            pk = tc.landing(mbody, mu, legs, spr, 8, mode)
            Ft = pk["Ft"]
            Jr, N = 4e-5, 4
            frac = N**2 * Jr / (N**2 * Jr + tc.I_WHEEL)
            print(f"   landing {name}: axle {Ft:.0f} N, unsprung {pk['au']:.0f} g, body {pk['ab']:.1f} g, "
                  f"spin-up mu*F*r={0.8*Ft*R_W:.1f} Nm, through gear {0.8*Ft*R_W*frac:.2f} Nm (inertia share {frac:.2f})")


if __name__ == "__main__":
    main()
