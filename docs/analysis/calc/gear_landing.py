"""O4: back-driven torque reaching the hip gear teeth at landing (P1 follow-up, Materials Eng.).

Spring acts body->thigh in PARALLEL with the gearbox (theory.md 3.4), so spring force never
passes the teeth. What does reach the teeth:
  1. motor electromagnetic torque x N (current-limited by the driver), and
  2. the inertial torque needed to stop/accelerate the motor rotor through the gear: N^2*J_r*alpha.
Case 2 peaks when the leg hits the end stop with the motor unpowered (theory LC-B/LC-D).
Rigid-gear 1-DOF model: everything moves at the hip angular rate w = v/J; the end stop is a linear
spring of angular stiffness k_th = k_axle*J^2. Peak stop torque T_b = w*sqrt(k_th*I_tot) and the
gear carries the rotor share T_gear = T_b * N^2*J_r / I_tot.
shortcut: ignores gear/carrier torsional compliance (dynamic overshoot up to ~2x if comparable to the
stop stiffness) and spring/gravity work during the stop; upgrade with the P5 multibody sim.
Run: python3 gear_landing.py
"""
import math

N = 8
J_R = 2.0e-4            # rotor inertia kg m2 (theory A4, +-40 %)
I_LEG = 0.029           # leg about hip, kg m2 (theory 3.7)
M_BODY_LEG = 2.16 / 2   # body mass per leg, kg (theory 3.3)
J_STOP = 0.201          # leg ratio dy/dphi at the 120 mm end stop, m/rad (interp. theory 3.3 table)
KT = 0.0636             # Nm/A, KV130
R_LL = 0.186 * (90 / 130) ** 2  # ohm, scaled from KV90 (theory)
T_ALLOW = 20 * 2.09     # Nm: compound hip layout reaches SF 2.09 at 20 Nm -> T at SF=1 (static allowable, 50 C)


def stop_spike(v, k_axle, m_body=M_BODY_LEG, J=J_STOP, jr=J_R):
    i_rot = N * N * jr
    i_tot = I_LEG + i_rot + m_body * J * J
    w = v / J
    t_b = w * math.sqrt(k_axle * J * J * i_tot)
    travel = t_b / (k_axle * J * J) * J * 1000  # axle-referred bumper travel, mm
    return t_b, t_b * i_rot / i_tot, travel


def main():
    print(f"Gear static allowable at 50 C (compound 8:1, PAHT-CF): {T_ALLOW:.0f} Nm  (UTS-level ~{T_ALLOW / 0.7:.0f} Nm)\n")
    print("| case | v at stop m/s | stop k (axle) kN/m | body on leg kg | J_r | stop torque Nm | gear torque Nm | SF vs allowable | bumper travel mm |")
    print("|" + "---|" * 9)
    cases = [("LC-B-like, TPU bumper", 2.0, 25e3, M_BODY_LEG, J_R),
             ("LC-B-like, J_r +40 %", 2.0, 25e3, M_BODY_LEG, 1.4 * J_R),
             ("LC-B-like, fast (2.6 m/s)", 2.6, 25e3, M_BODY_LEG, J_R),
             ("LC-D-like, full body on 1 leg", 2.0, 25e3, 2 * M_BODY_LEG, J_R),
             ("soft bumper 10 kN/m", 2.0, 10e3, M_BODY_LEG, J_R),
             ("stiff printed stop 250 kN/m", 2.0, 250e3, M_BODY_LEG, J_R),
             ("stiff printed stop, fast, J_r+40 %", 2.6, 250e3, M_BODY_LEG, 1.4 * J_R)]
    for name, v, k, mb, jr in cases:
        tb, tg, x = stop_spike(v, k, mb, jr=jr)
        print(f"| {name} | {v} | {k / 1e3:.0f} | {mb:.2f} | {jr:.1e} | {tb:.0f} | {tg:.1f} | {T_ALLOW / tg:.2f} | {x:.0f} |")

    print("\nOther gear-torque sources (output side):")
    for amps in (20, 40):
        print(f"  motor at {amps} A: {amps * KT * N:.1f} Nm")
    w_m = N * 2.0 / J_STOP
    i_sc = KT * w_m / R_LL
    print(f"  phases SHORTED (fault brake) at leg 2 m/s: w_m={w_m:.0f} rad/s, I~{i_sc:.0f} A (R-limited, L ignored)"
          f" -> {min(i_sc, 200) * KT * N:.0f} Nm at the output")
    print(f"  end stop acting THROUGH the gearbox (theory LC-D hip torque): 50.8 Nm -> SF {T_ALLOW / 50.8:.2f}")

    assert abs(stop_spike(1.0, 1e3)[0] - (1 / J_STOP) * math.sqrt(1e3 * J_STOP ** 2 * (I_LEG + 64 * J_R + M_BODY_LEG * J_STOP ** 2))) < 1e-9


if __name__ == "__main__":
    main()
