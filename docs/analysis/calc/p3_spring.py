"""P3 spring re-fit on the P2 layout geometry (layout.md / com_layout.py).
Spring = straight extension spring from body anchor A (hip-relative x,z = 47.3, 56.6 mm) to crank pin P on
the thigh, r = 40 mm, opposite the thigh: P = -r (cos phi, sin phi). Checked against layout lengths
62.0 (ext) / 89.7 (nom) / 104.2 (crouch) mm. Spring torque on hip by virtual work: T = F(L) * dL/dphi.
Run: python3 p3_spring.py > p3_output.txt
"""
import math
import numpy as np
import theory_calc as tc
import o13_rerun as o

M, MU_SIDE = 4.37, 0.536
MB = M - 2 * MU_SIDE
A = np.array([47.3, 56.6]) * 1e-3


def spring_len(phi, r=0.040):
    P = -r * np.stack([np.cos(phi), np.sin(phi)], -1)
    return np.linalg.norm(A - P, axis=-1)


def make(k, F0, r=0.040, ph=None):
    """F0 = force at the extended pose (L_ext). Returns hip torque function per leg and table data."""
    L_ext = float(spring_len(np.radians(-72.677), r))
    def T(phi):
        L = spring_len(np.array(phi), r)
        dL = (spring_len(np.array(phi) + 1e-5, r) - spring_len(np.array(phi) - 1e-5, r)) / 2e-5
        return float(max(0.0, F0 + k * (L - L_ext)) * abs(dL))
    return T, L_ext


def wire(Fmax, d, D, k, G=81.5e9, Rm=None):
    """Music wire extension spring check (EN 10270-1 DH)."""
    Rm = Rm or (2230e6 - 230e6 * (d * 1e3 - 1.0))     # rough DH tensile strength vs d (1 mm 2230, 2 mm ~2000 MPa)
    C = D / d
    Kw = (4 * C - 1) / (4 * C - 4) + 0.615 / C
    tau = 8 * Fmax * D * Kw / (math.pi * d**3)
    n = G * d**4 / (8 * D**3 * k)
    body = (n + 1) * d                             # close-wound body length
    return C, tau / 1e6, 0.45 * Rm / 1e6, n, body


def main():
    p, ph, y, K, C, W, J = o.legs_geom()
    legs = (ph, y, J)
    tc.set_motor(130)
    print("check layout lengths ext/nom/crouch mm:",
          [round(float(spring_len(np.radians(a))) * 1e3, 1) for a in (-72.677, -29.987, 0.482)])
    print(f"M={M} kg, m_b={MB:.3f} kg, unsprung {MU_SIDE} kg/side\n")
    opts = [("O0 current spring 2.7 N/mm, F0 8 N (r 40)", 2700, 8.0, 0.040),
            ("O1 stiffer 4.1 N/mm, F0 8 N (r 40)", 4100, 8.0, 0.040),
            ("O2 3.5 N/mm, F0 20 N (r 40)", 3500, 20.0, 0.040),
            ("O3 50 mm crank, 2.7 N/mm, F0 8 N (same anchor, NOT checked for clearance)", 2700, 8.0, 0.050)]
    print("| option | stroke mm | F crouch N | E/leg J | crouch | jump 19.8 V sim cm | real x0.8 cm | jump 22.2 V real cm | hold @nominal A | hold @crouch A |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    F = MB * 9.81 / 2
    for name, k, F0, r in opts:
        T, L_ext = make(k, F0, r)
        for yc in (0.101, 0.130):
            tc.Y_CROUCH = yc
            phi_c = float(np.interp(yc, y, ph))
            L_c = float(spring_len(np.array(phi_c), r))
            s = L_c - L_ext
            E = F0 * s + 0.5 * k * s**2
            r19 = tc.jump(8, 19.8, MB, 2 * MU_SIDE, T, legs)
            r22 = tc.jump(8, 22.2, MB, 2 * MU_SIDE, T, legs)
            i_n = int(np.argmin(abs(y - tc.Y_NOM)))
            hn = abs(T(ph[i_n]) - F * J[i_n]) / (8 * tc.ETA_H) / tc.KT
            hc = abs(T(phi_c) - F * float(np.interp(yc, y, J))) / (8 * tc.ETA_H) / tc.KT
            print(f"| {name} | {s*1e3:.1f} | {F0 + k*s:.0f} | {E:.2f} | {yc*1e3:.0f} | {r19['h']*100:.1f} | {r19['h']*80:.1f} | "
                  f"{r22['h']*80:.1f} | {hn:.1f} | {hc:.1f} |")
    tc.Y_CROUCH = 0.101
    tc.Y_CROUCH = 0.130
    r = tc.jump(8, 19.8, MB, 2 * MU_SIDE, lambda q: 0.0, legs)
    print(f"| no spring | - | - | 0 | 130 | {r['h']*100:.1f} | {r['h']*80:.1f} | | | |")
    tc.Y_CROUCH = 0.101
    r = tc.jump(8, 19.8, MB, 2 * MU_SIDE, lambda q: 0.0, legs)
    print(f"| no spring | - | - | 0 | 101 | {r['h']*100:.1f} | {r['h']*80:.1f} | | | |")

    print("\n## Wire check, music wire DH, G 81.5 GPa (tau allowable = 0.45 Rm body; hooks ~0.75 of that)")
    print("| k N/mm | Fmax N | d mm | D mean mm | OD mm | C | tau MPa | allow MPa | active coils | body length mm |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for k, Fm in ((2700, 125), (4100, 180)):
        for d, D in ((1.8, 11.0), (2.0, 11.0), (2.0, 12.0), (2.2, 11.5)):
            Cc, tau, al, n, body = wire(Fm * 1.0, d * 1e-3, D * 1e-3, k)
            print(f"| {k/1000:.1f} | {Fm} | {d} | {D} | {D+d:.1f} | {Cc:.1f} | {tau:.0f} | {al:.0f} | {n:.1f} | {body*1e3:.0f} |")


if __name__ == "__main__":
    main()


def moved_anchor(extra=0.049):
    """Anchor moved outward along the extended-pose spring line so a longer catalogue spring fits."""
    global A
    P_ext = -0.040 * np.array([math.cos(math.radians(-72.677)), math.sin(math.radians(-72.677))])
    u = (A - P_ext) / np.linalg.norm(A - P_ext)
    A0 = A.copy()
    A = A + extra * u
    p, ph, y, K, C, W, J = o.legs_geom()
    legs = (ph, y, J)
    tc.set_motor(130)
    T, L_ext = make(2700, 8.0)
    tc.Y_CROUCH = 0.101
    Lc = float(spring_len(np.array(float(np.interp(0.101, y, ph)))))
    r19 = tc.jump(8, 19.8, MB, 2 * MU_SIDE, T, legs)
    r22 = tc.jump(8, 22.2, MB, 2 * MU_SIDE, T, legs)
    tc.Y_CROUCH = 0.130
    r13 = tc.jump(8, 19.8, MB, 2 * MU_SIDE, T, legs)
    print(f"\n## Anchor moved {extra*1e3:.0f} mm outward along the spring line: A = {np.round(A*1e3,1)} mm (hip-rel x,z), "
          f"was {np.round(A0*1e3,1)}")
    print(f"span ext/crouch {L_ext*1e3:.1f}/{Lc*1e3:.1f} mm, stroke {(Lc-L_ext)*1e3:.1f} mm, F crouch {8+2700*(Lc-L_ext):.0f} N")
    print(f"jump real (x0.8): 19.8 V from 101: {r19['h']*80:.1f} cm; 22.2 V: {r22['h']*80:.1f} cm; 19.8 V from 130: {r13['h']*80:.1f} cm")
    A = A0


if __name__ == "__main__":
    moved_anchor()
