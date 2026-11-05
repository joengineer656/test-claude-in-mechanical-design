"""Lewis bending + Hertz contact check for 3D-printed planetary stages (P1, Materials Eng.).

Run: python3 gear_lewis.py   (prints markdown tables used in ../materials_gears.md)

Key relation (simple planetary, carrier output, Np planets, ring pitch dia D_r):
    tangential force per mesh  Ft = 2*T_out / (Np * D_r) * K
It does NOT depend on the ratio -> the ring pitch diameter is the main strength lever.
The same expression holds for the output mesh of a compound (stepped-planet) stage
with D_r = pitch dia of the output ring.
"""
import math

# ---- printed material allowables, 100 % infill, gear axis = print Z (tooth bending in XY plane) ----
# UTS_xy from Bambu TDS (dry). k_static = 0.7 (perimeter/root defects, notch at layer seams, scatter);
# fatigue allowable for ~1e7 cycles, ONE-WAY bending = 0.30*UTS, fully REVERSED (planets, balance) = 0.22*UTS.
# Temperature factor applied separately (see TEMP).
MAT = {  # name: (UTS_xy MPa, density g/cm3, HDT@0.45MPa C)
    "PLA":      (39, 1.24, 57),
    "PETG":     (34, 1.27, 69),
    "PAHT-CF":  (65, 1.06, 194),   # 92 MPa dry TDS; 65 = conditioned (moisture-saturated) estimate
}
K_STATIC, K_FAT_1WAY, K_FAT_REV = 0.70, 0.30, 0.22
# strength retention vs temperature (rough, from generic polymer DMA trends); PLA collapses near Tg~57-60 C
TEMP = {"PLA": {25: 1.0, 40: 0.80, 50: 0.45}, "PETG": {25: 1.0, 40: 0.88, 50: 0.75},
        "PAHT-CF": {25: 1.0, 40: 0.95, 50: 0.90}}

K_SHARE = 1.30  # load sharing, 3 printed planets (tolerance ~0.1 mm) -> worst planet carries 1.3/3
K_V = 1.10      # dynamic factor, low pitch-line speed (<3 m/s), printed profile errors

# Lewis form factor Y (module based, 20 deg full depth); interpolated
_Y = [(12, .245), (13, .261), (14, .277), (15, .290), (16, .296), (17, .303), (18, .309), (19, .314),
      (20, .322), (22, .331), (24, .337), (26, .346), (28, .353), (30, .359), (34, .371), (38, .384),
      (43, .397), (50, .409), (60, .422), (75, .435), (100, .447)]


def lewis_Y(z):
    if z <= _Y[0][0]:
        return _Y[0][1]
    for (z0, y0), (z1, y1) in zip(_Y, _Y[1:]):
        if z <= z1:
            return y0 + (y1 - y0) * (z - z0) / (z1 - z0)
    return _Y[-1][1]


def mesh_force(T_out, D_r_mm, Np=3):
    return 2 * T_out * 1000 / (Np * D_r_mm) * K_SHARE * K_V  # N


def bending(T_out, D_r, m, b, z_min, Np=3):
    return mesh_force(T_out, D_r, Np) / (b * m * lewis_Y(z_min))  # MPa


def allow(mat, kind="static", T=25):
    uts = MAT[mat][0] * TEMP[mat][T]
    return uts * {"static": K_STATIC, "1way": K_FAT_1WAY, "rev": K_FAT_REV}[kind]


def hertz(T_out, D_r, m, b, zs, zp, Np=3, E=3000.0, nu=0.38):
    """Sun-planet contact stress, plastic/plastic, Z_H=2.49 (20 deg spur)."""
    ZE = math.sqrt(E / (2 * math.pi * (1 - nu ** 2)))
    u = zp / zs
    Ft = mesh_force(T_out, D_r, Np)
    return 2.49 * ZE * math.sqrt(Ft / (b * m * zs) * (u + 1) / u)


def find_stage(m, ratio, D_r_max, Np=3, zmin=12):
    """Biggest-ring integer simple planetary within +-3 % of ratio and ring pitch <= D_r_max."""
    best = None
    for zs in range(zmin, 60):
        for zr in range(round(zs * (ratio - 1)) - 3, round(zs * (ratio - 1)) + 4):
            zp = (zr - zs) // 2
            if (zr - zs) % 2 or (zs + zr) % Np or zp < zmin or m * zr > D_r_max:
                continue
            if abs(1 + zr / zs - ratio) > 0.03 * ratio:
                continue
            key = (-zr, abs(1 + zr / zs - ratio))
            if best is None or key < best[0]:
                best = (key, zs, zp, zr)
    return None if best is None else best[1:]


def pin_check(T_out, D_r, d_pin=4.0, span=None, b=12, Np=3):
    """Steel planet pin, simply supported in two carrier cheeks, central load 2*Ft."""
    F = 2 * mesh_force(T_out, D_r, Np)
    L = span or b + 4
    sig = 32 * (F * L / 4) / (math.pi * d_pin ** 3)
    p_cheek = F / 2 / (d_pin * 5.0)  # bearing pressure on 5 mm thick printed cheek, MPa
    return F, sig, p_cheek


def main():
    print("## Wheel stage (simple planetary, Np=3, ring pitch <= 84 mm)\n")
    print("| m | ratio | Zs/Zp/Zr | i actual | D_r | b | sigma@6Nm | SF PLA | SF PETG | SF PAHT-CF | "
          "sigma@1.5Nm cont. | SFfat(rev) PAHT-CF 40C | Hertz@6Nm |")
    print("|" + "---|" * 13)
    for m in (1.0, 1.25, 1.5):
        for ratio in (4, 5, 6):
            st = find_stage(m, ratio, 84)
            if not st:
                print(f"| {m} | {ratio} | no fit | | | | | | | | | | |")
                continue
            zs, zp, zr = st
            D = m * zr
            for b in (10, 15):
                s = bending(6, D, m, b, min(zs, zp))
                sc = bending(1.5, D, m, b, min(zs, zp))
                h = hertz(6, D, m, b, zs, zp)
                print(f"| {m} | {ratio} | {zs}/{zp}/{zr} | {1 + zr / zs:.2f} | {D:.0f} | {b} | {s:.1f} | "
                      f"{allow('PLA') / s:.1f} | {allow('PETG') / s:.1f} | {allow('PAHT-CF') / s:.1f} | {sc:.1f} | "
                      f"{allow('PAHT-CF', 'rev', 40) / sc:.1f} | {h:.0f} |")

    print("\n## Hip output mesh (2-stage or compound), weakest gear z_min=14, Np=3\n")
    print("| D_r | m | b | sigma@8Nm | sigma@15Nm | SF@15 PLA 25C | SF@15 PETG 40C | SF@15 PAHT-CF 50C | "
          "T_max PAHT-CF 50C (SF=1.5) | sigma@4Nm cont. | SFfat(rev) PAHT-CF 50C |")
    print("|" + "---|" * 11)
    for D in (84, 96):
        for m in (1.0, 1.25, 1.5):
            for b in (12, 16, 20):
                s8, s15, s4 = (bending(T, D, m, b, 14) for T in (8, 15, 4))
                tmax = allow('PAHT-CF', 'static', 50) / 1.5 / s15 * 15
                print(f"| {D} | {m} | {b} | {s8:.1f} | {s15:.1f} | {allow('PLA') / s15:.2f} | "
                      f"{allow('PETG', 'static', 40) / s15:.2f} | {allow('PAHT-CF', 'static', 50) / s15:.2f} | "
                      f"{tmax:.1f} | {s4:.1f} | {allow('PAHT-CF', 'rev', 50) / s4:.2f} |")

    print("\n## Steel planet pin (2*Ft on pin, d=4/5 mm, span b+4) and printed cheek bearing pressure\n")
    print("| case | T_out | D_r | b | F_pin N | d=4: sigma MPa | d=5: sigma MPa | cheek p (d=4, t=5) MPa |")
    print("|" + "---|" * 8)
    for name, T, D, b in (("wheel peak", 6, 84, 15), ("hip peak", 15, 96, 16), ("hip peak", 15, 84, 20)):
        F, s4, p = pin_check(T, D, 4.0, b=b)
        _, s5, _ = pin_check(T, D, 5.0, b=b)
        print(f"| {name} | {T} | {D} | {b} | {F:.0f} | {s4:.0f} | {s5:.0f} | {p:.0f} |")

    # motor torque capability vs gear limit: KV90 -> Kt ~ 9.55/KV
    kt = 9.55 / 90
    print(f"\nKV90 -> Kt ~ {kt:.3f} Nm/A. Output torque at motor current I (eta 0.9):")
    for i_ratio, label in ((5, "wheel 5:1"), (9, "hip 9:1")):
        print(f"  {label}: " + ", ".join(f"{I} A -> {I * kt * i_ratio * 0.9:.1f} Nm" for I in (10, 20, 30, 40)))

    # self-check
    assert abs(lewis_Y(17) - 0.303) < 1e-9 and find_stage(1.0, 5, 84) is not None
    assert abs(mesh_force(3, 100, 3) - 20 * K_SHARE * K_V) < 1e-6


def b_required(T_out, D_r, m, z_min, mat="PAHT-CF", T=50, sf=1.5, Np=3):
    """Face width (mm) for Lewis SF = sf at temperature T."""
    return mesh_force(T_out, D_r, Np) * sf / (m * lewis_Y(z_min) * allow(mat, "static", T))


def followup():
    """P1 follow-up O3: theory design torques (hip 20 Nm at 8:1, wheel 10 Nm at 3.91:1), 50 C."""
    print("\n## O3 wheel 3.91:1 (23/22/67), 10 Nm, 50 C\n")
    print("| m | D_r | b | sigma | SF PAHT-CF | SF PETG | b for SF1.5 PAHT-CF |")
    print("|" + "---|" * 7)
    for b in (15, 18, 20):
        s = bending(10, 1.25 * 67, 1.25, b, 22)
        print(f"| 1.25 | 83.75 | {b} | {s:.1f} | {allow('PAHT-CF', 'static', 50) / s:.2f} | "
              f"{allow('PETG', 'static', 50) / s:.2f} | {b_required(10, 83.75, 1.25, 22):.1f} |")

    print("\n## O3 hip 8:1 at 20 Nm, 50 C, PAHT-CF (stage tooth counts Zs/Zp/Zr)\n")
    print("| layout | stage | Zs/Zp/Zr | i | stage T_out Nm | m | D_r | b | sigma | SF | b for SF1.5 |")
    print("|" + "---|" * 11)
    rows = [  # (layout, stage, zs, zp, zr, T_out, m, b)
        ("1-stage", "only", 12, 36, 84, 20, 1.0, 20), ("1-stage", "only", 12, 36, 84, 20, 1.25, 20),
        ("2-stage 3.0x2.667", "1 (input)", 24, 12, 48, 20 / (60 / 36 + 1), 1.0, 12),
        ("2-stage 3.0x2.667", "1 (input)", 24, 12, 48, 20 / (60 / 36 + 1), 1.25, 12),
        ("2-stage 3.0x2.667", "2 (output)", 36, 12, 60, 20, 1.5, 20),
        ("2-stage 3.0x2.667", "2 (output)", 36, 12, 60, 20, 1.5, 24),
        ("2-stage 3.0x2.667", "2 (output)", 36, 12, 60, 20, 1.25, 24),
    ]
    for lay, st, zs, zp, zr, T, m, b in rows:
        assert (zs + zr) % 3 == 0 and zr - zs == 2 * zp
        D = m * zr
        s = bending(T, D, m, b, min(zs, zp))
        print(f"| {lay} | {st} | {zs}/{zp}/{zr} | {1 + zr / zs:.3f} | {T:.1f} | {m} | {D:.0f} | {b} | {s:.1f} | "
              f"{allow('PAHT-CF', 'static', 50) / s:.2f} | {b_required(T, D, m, min(zs, zp)):.1f} |")


def compound_search(T_out=20.0, i_lo=7.8, i_hi=8.2, D_max=96, m2=1.5, b1=14, b2=20, Np=3):
    """Stepped-planet compound, ring fixed, carrier output: i = 1 + Zr*Zp1/(Zs*Zp2).
    Sun(m1)-big planet step Zp1, small step Zp2(m2)-ring Zr. Same centre distance within 0.3*m2
    (taken up by profile shift). Assembly: (Zs*Zp2 + Zr*Zp1)/(Np*gcd(Zp1,Zp2)) integer (verify in CAD)."""
    out = []
    for m1 in (1.0, 1.25):
        for zs in range(13, 30):
            for zp1 in range(zs, 60):
                a = m1 * (zs + zp1) / 2
                if (zp1 + 2) * m1 >= a * math.sqrt(3) - 1.0:  # big planets must clear each other
                    continue
                for zp2 in range(14, zp1):
                    zr = round(2 * a / m2 + zp2)
                    if abs(m2 * (zr - zp2) / 2 - a) > 0.3 * m2 or m2 * zr > D_max:
                        continue
                    i = 1 + zr * zp1 / (zs * zp2)
                    if not i_lo <= i <= i_hi or (zs * zp2 + zr * zp1) % (Np * math.gcd(zp1, zp2)):
                        continue
                    s1 = mesh_force(T_out / i, m1 * zs, Np) / (b1 * m1 * lewis_Y(zs))  # sun mesh
                    s2 = mesh_force(T_out * (1 - 1 / i), m2 * zr, Np) / (b2 * m2 * lewis_Y(zp2))  # ring mesh
                    sa = allow("PAHT-CF", "static", 50)
                    out.append((min(sa / s1, sa / s2), m1, zs, zp1, zp2, zr, i, sa / s1, sa / s2))
    out.sort(reverse=True)
    print(f"\n## O3 hip compound stepped-planet 8:1 at {T_out} Nm, 50 C, PAHT-CF, b1={b1} b2={b2}, m2={m2}\n")
    print("| m1 | Zs | Zp1 | Zp2 | Zr | i | D_r | SF sun mesh | SF ring mesh |")
    print("|" + "---|" * 9)
    for r in out[:6]:
        _, m1, zs, zp1, zp2, zr, i, f1, f2 = r
        print(f"| {m1} | {zs} | {zp1} | {zp2} | {zr} | {i:.3f} | {m2 * zr:.0f} | {f1:.2f} | {f2:.2f} |")
    return out


def o9_wheel():
    """O9: MN5008 KV170 hub, single stage ~3.5:1, 3 planets. Design torques 2.3 fatigue / 4.5 max op / 8.5 ult.
    Criteria at 50 C: SF>=1.5 static on 4.5 Nm, SF>=1.2 static on 8.5 Nm, reversed-fatigue SF>=1.5 on 2.3 Nm."""
    print("\n## O9 wheel 3.5:1 candidates (valid 3-planet assembly)\n")
    sets = []
    for zs in range(12, 40):
        for zr in range(30, 120):
            zp, ok = (zr - zs) // 2, (zr - zs) % 2 == 0 and (zs + zr) % 3 == 0
            i = 1 + zr / zs
            if ok and zp >= 12 and abs(i - 3.5) <= 0.06 and (zp + 2) < (zs + zp) * math.sqrt(3) / 2 * 2 - 1:
                sets.append((zs, zp, zr, i))
    print("valid sets (Zs/Zp/Zr i):", ", ".join(f"{a}/{b}/{c} {i:.3f}" for a, b, c, i in sets[:8]))
    print("theory 20/15/50: (20+50)%3 =", (20 + 50) % 3, "-> fails equal spacing")
    print("\n| Zs/Zp/Zr | m | D_r | b | SF 4.5Nm PAHT-CF | SF 8.5Nm PAHT-CF | SFfat 2.3Nm PAHT-CF | "
          "SF 4.5 PETG | SF 8.5 PETG | SFfat PETG | SF 4.5 PLA | pass PETG? |")
    print("|" + "---|" * 12)
    for zs, zp, zr in ((24, 18, 60), (20, 16, 52)):
        for m in (1.0, 1.25):
            for b in (8, 10, 12):
                D, z = m * zr, min(zs, zp)
                s45, s85, s23 = (bending(T, D, m, b, z) for T in (4.5, 8.5, 2.3))
                r = lambda mat: (allow(mat, "static", 50) / s45, allow(mat, "static", 50) / s85, allow(mat, "rev", 50) / s23)
                a, c, p_ = r("PAHT-CF"), r("PETG"), r("PLA")
                ok = c[0] >= 1.5 and c[1] >= 1.2 and c[2] >= 1.5
                print(f"| {zs}/{zp}/{zr} | {m} | {D:.0f} | {b} | {a[0]:.2f} | {a[1]:.2f} | {a[2]:.2f} | "
                      f"{c[0]:.2f} | {c[1]:.2f} | {c[2]:.2f} | {p_[0]:.2f} | {'yes' if ok else 'no'} |")
    # pin load at ultimate, planet bearing check, m1.0 24/18/60 b10
    F = 2 * mesh_force(8.5, 60, 3)
    print(f"\nPlanet pin load at 8.5 Nm (D_r 60): {F:.0f} N; d4 pin sigma (span 14) = "
          f"{32 * F * 14 / 4 / (math.pi * 4 ** 3):.0f} MPa")
    return sets


if __name__ == "__main__":
    main()
    followup()
    assert compound_search(), 'no compound 8:1 layout found'
    assert any(x[:3] == (24, 18, 60) for x in o9_wheel())
