"""Hip 6:1 compound stepped-planet option that re-uses the existing 8:1 hip housing (P1 'Hip 6:1 option').
Constraints: ring 63T m1.5 b20 (pitch D94.5) and planet small step 18T m1.5 KEPT (centre distance 33.75 exactly,
no shift), so only the SUN and the planet BIG STEP change.  i = 1 + (Zp1/Zs)*(Zr/Zp2) = 6  ->  Zp1/Zs = 10/7.
Run: python3 gear_hip6.py
"""
import math
from gear_lewis import allow, bending, lewis_Y, mesh_force

A = 33.75                                   # planet pin radius (fixed by housing)
ZR, ZP2, M2, B2 = 63, 18, 1.5, 20           # unchanged ring stage
INV = lambda a: math.tan(a) - a
AL = math.radians(20)


def shift_sum(z1, z2, m):
    """Sum of profile shifts (x1+x2) that gives zero backlash at centre distance A."""
    a0 = m * (z1 + z2) / 2
    ac = math.acos(a0 * math.cos(AL) / A)
    return (z1 + z2) * (INV(ac) - INV(AL)) / (2 * math.tan(AL)), math.degrees(ac)


def contact_ratio(z1, z2, m, x1, x2):
    """External spur pair, tip circles = standard addendum (1+x)m, tip relief ignored."""
    ra1, ra2 = m * (z1 / 2 + 1 + x1), m * (z2 / 2 + 1 + x2)
    rb1, rb2 = m * z1 / 2 * math.cos(AL), m * z2 / 2 * math.cos(AL)
    ac = math.acos((rb1 + rb2) / A)
    return (math.sqrt(ra1 ** 2 - rb1 ** 2) + math.sqrt(ra2 ** 2 - rb2 ** 2) - A * math.sin(ac)) / (math.pi * m * math.cos(AL))


def main():
    print("## Candidate stage-1 pairs (Zp1/Zs = 10/7, Zp2=18, Zr=63 fixed)\n")
    print("| Zs/Zp1 | m1 | nominal a0 | needed shift (x1+x2) | eps | planet tip R (limit 57.5) | verdict |")
    print("|" + "---|" * 7)
    for k in (3, 4, 5):
        zs, zp = 7 * k, 10 * k
        for m in (0.8, 1.0, 1.25, 1.5):
            a0 = m * (zs + zp) / 2
            if abs(a0 - A) > 0.15 * A:
                continue
            if a0 * math.cos(AL) / A >= 1:
                continue
            sx, _ = shift_sum(zs, zp, m)
            xs, xp = sx * 0.6, sx * 0.4          # larger share to the sun (weaker, undercut-prone)
            eps = contact_ratio(zs, zp, m, xs, xp)
            rt = A + m * (zp / 2 + 1 + xp)
            print(f"| {zs}/{zp} | {m} | {a0:.2f} | {sx:+.3f} | {eps:.2f} | {rt:.1f} | "
                  f"{'USE' if abs(sx) < 0.4 and eps > 1.3 and rt < 57.5 else 'reject'} |")

    zs, zp1, m1 = 28, 40, 1.0
    sx, ac = shift_sum(zs, zp1, m1)
    xs, xp = sx * 0.6, sx * 0.4
    print(f"\nChosen: Zs={zs}, Zp1={zp1}, m1={m1}: sum x = {sx:+.3f} (x_sun {xs:+.3f}, x_planet {xp:+.3f}), "
          f"working PA {ac:.2f} deg, eps {contact_ratio(zs, zp1, m1, xs, xp):.2f}")
    print(f"ratio = 1 + ({zp1}*{ZR})/({zs}*{ZP2}) = {1 + zp1 * ZR / (zs * ZP2):.6f}")
    print(f"assembly: (Zs*Zp2 + Zr*Zp1)/(3*gcd) = {(zs * ZP2 + ZR * zp1) / (3 * math.gcd(zp1, ZP2)):.1f} (integer needed); "
          f"Zs/3={zs / 3:.2f}, Zr/3={ZR / 3:.0f}")
    # planet-phase offset between steps for planet k (mod gcd lattice of the two tooth pitches, 1 deg)
    d = [(-120 * k * (zs / zp1 + ZR / ZP2)) % 1.0 for k in range(3)]
    print("step-offset term for planets 0,1,2 (deg, mod 1): " + ", ".join(f"{x:.3f}" for x in d) + "  -> identical planets")
    print(f"big-step tip gap between planets: {2 * A * math.sin(math.pi / 3) - 2 * m1 * (zp1 / 2 + 1 + xp):.1f} mm; "
          f"sun tip R {m1 * (zs / 2 + 1 + xs):.2f}, sun root R {m1 * (zs / 2 - 1.25 + xs):.2f} (flange R25 below the teeth)")

    print("\n## Strength at 20 Nm output, 50 C, PAHT-CF (static allowable 0.7 UTS, reversed fatigue 0.22 UTS)\n")
    sa, fa = allow("PAHT-CF", "static", 50), allow("PAHT-CF", "rev", 50)
    print("| layout | mesh | Z (weak gear) | m | b | sigma MPa | SF static 20 Nm | SF fatigue @ 8 Nm (rev) | b for SF1.5 |")
    print("|" + "---|" * 9)
    rows = []
    for name, i, zs_, zp_, m_, b_ in (("8:1 frozen", 8.0, 18, 36, 1.25, 14), ("6:1 m1.0 b14", 6.0, 28, 40, 1.0, 14),
                                      ("6:1 m1.0 b16", 6.0, 28, 40, 1.0, 16)):
        T1 = 20 / i
        s = mesh_force(T1, m_ * zs_) / (b_ * m_ * lewis_Y(min(zs_, zp_)))
        sf8 = mesh_force(T1 * 8 / 20, m_ * zs_) / (b_ * m_ * lewis_Y(min(zs_, zp_)))
        print(f"| {name} | sun-planet | {min(zs_, zp_)} | {m_} | {b_} | {s:.1f} | {sa / s:.2f} | {fa / sf8:.2f} | "
              f"{s * b_ / (sa / 1.5):.1f} |")
        rows.append(s)
    for name, i in (("8:1 frozen", 8.0), ("6:1 option", 6.0)):
        T2 = 20 * (1 - 1 / i)
        s = mesh_force(T2, M2 * ZR) / (B2 * M2 * lewis_Y(ZP2))
        print(f"| {name} | planet-ring | {ZP2} | {M2} | {B2} | {s:.1f} | {sa / s:.2f} | "
              f"{fa / (mesh_force(T2 * 8 / 20, M2 * ZR) / (B2 * M2 * lewis_Y(ZP2))):.2f} | {s * B2 / (sa / 1.5):.1f} |")

    print("\n## Loads at the same 20 Nm output (per planet, before K factors)\n")
    print("| i | T_sun Nm | Ft sun mesh N | Ft ring mesh N | pin load N | motor torque for 20 Nm out (eta .85) | motor current A (Kt .0636) | max forward output at 40 A |")
    print("|" + "---|" * 8)
    for i, d_s in ((8, 22.5), (6, 28.0)):
        ts = 20 / i
        f1, f2 = 2 * ts * 1000 / d_s / 3, 2 * 20 * (1 - 1 / i) * 1000 / 94.5 / 3
        tm = 20 / (i * 0.85)
        print(f"| {i}:1 | {ts:.2f} | {f1:.0f} | {f2:.0f} | {(f1 + f2) * 1.43:.0f} (with K) | {tm:.2f} | {tm / 0.0636:.0f} | "
              f"{40 * 0.0636 * i * 0.85:.1f} Nm |")
    print("\nReflected rotor inertia at the output side: N^2 * J_r (J_r 2.0e-4 kg m2 estimate):")
    for i in (8, 6):
        print(f"  {i}:1 -> {i * i * 2e-4:.4f} kg m2  ({(i * i) / 64:.2f} x the 8:1 value)")
    assert abs(1 + zp1 * ZR / (zs * ZP2) - 6) < 1e-12 and (zs * ZP2 + ZR * zp1) % (3 * math.gcd(zp1, ZP2)) == 0


if __name__ == "__main__":
    main()
