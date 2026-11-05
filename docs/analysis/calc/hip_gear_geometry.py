"""P3a hip gearbox (rev 3: 6:1 option, sun 28T / planet big step 40T m1.0 with profile shifts; was 8:1, 18T/36T m1.25): compound stepped-planet geometry, checks and tooth polylines.

Run: python3 hip_gear_geometry.py          -> prints checks (asserts them)
     python3 hip_gear_geometry.py --json F  -> writes tooth polylines (mm, gear centre at 0,0) for CAD
Frame of the polylines: gear axis = Z, angle 0 = +X. Phasing (see docs/parts/hip_gearbox.md):
  sun     : gap centred on 0 deg  -> teeth at 6.43 + 12.857k deg
  planets : big and small step share a tooth on the same radial line (offset 0)
            small-step gap at 0 deg (faces the ring), big-step tooth at 180 deg (faces the sun gap)
  ring    : tooth centred on 0 deg -> teeth at k*360/63 deg
"""
import json, math, sys
from math import gcd

PA = math.radians(20)
Zs, Zp1, Zp2, Zr, N = 28, 40, 18, 63, 3
m1, m2 = 1.0, 1.5
XS, XP = -0.146, -0.097     # profile shifts (gear_hip6.py): centre distance 33.75 exactly
A_C = 33.75
BL = 0.06          # circular tooth-thickness reduction per gear at the pitch circle (mm) -> ~0.12 mm per mesh
NPF = 10           # points per involute flank (>= 8)


def inv(a):
    return math.tan(a) - a


def external(z, m, thin, add=1.0, ded=1.25, rf_fac=0.38, phase_deg=0.0, x=0.0):
    """Closed polyline of an external spur gear. Tooth centred at phase_deg. thin: circular thickness change (+ thicker)."""
    r = z * m / 2; rb = r * math.cos(PA); ra = r + (add + x) * m; rr = r - (ded - x) * m
    s = math.pi * m / 2 + 2 * x * m * math.tan(PA) + thin                       # circular thickness at pitch r
    half_t = s / (2 * r) + inv(PA)                   # half angle of tooth at base circle (involute origin)
    r_start = max(rb, rr)
    pitch = 2 * math.pi / z
    pts = []
    for k in range(z):
        c = math.radians(phase_deg) + k * pitch
        flank = []
        for i in range(NPF):
            rad = r_start + (ra - r_start) * i / (NPF - 1)
            a = math.acos(min(1.0, rb / rad))
            flank.append((rad, half_t - inv(a)))       # angle from tooth centre line
        # root: radial drop from involute start to root with fillet approximation (2 extra points)
        rf = rf_fac * m
        root_l = [(rr, half_t + 0.5 * (pitch / 2 - half_t)), (rr + rf * 0.6, half_t + 0.15 * (pitch / 2 - half_t))] if rb > rr else []
        left = root_l + flank                                       # from root (gap side) to tip, at +angles
        tooth = [(rad, c - th) for rad, th in left] + [(ra, c)] + [(rad, c + th) for rad, th in reversed(left)]
        pts += tooth
    # orientation: ascending angle
    xy = [(rad * math.cos(t), rad * math.sin(t)) for rad, t in pts]
    return xy


def checks():
    out = {}
    a2 = m2 * (Zr - Zp2) / 2
    out["centre distance small-ring (mm)"] = a2
    assert abs(A_C - a2) < 1e-9
    # zero-backlash shift sum for the sun-big pair at A_C
    a0 = m1 * (Zs + Zp1) / 2
    ac = math.acos(a0 * math.cos(PA) / A_C)
    sx = (Zs + Zp1) * (inv(ac) - inv(PA)) / (2 * math.tan(PA))
    out["shift sum needed / used"] = (sx, XS + XP)
    assert abs(sx - (XS + XP)) < 0.002
    i = 1 + Zr * Zp1 / (Zs * Zp2)
    out["ratio"] = i; assert abs(i - 6) < 1e-12
    out["assembly (Zs*Zp2+Zr*Zp1)/(N*gcd(Zp1,Zp2))"] = (Zs * Zp2 + Zr * Zp1) / (N * gcd(Zp1, Zp2))
    assert out["assembly (Zs*Zp2+Zr*Zp1)/(N*gcd(Zp1,Zp2))"] % 1 == 0
    out["Zs/N (not an integer: planets 2,3 are spun on their pins, see PLANET_SPIN_J), Zr/N"] = (Zs / N, Zr / N)
    ra_big = m1 * (Zp1 / 2 + 1 + XP)
    spacing = 2 * A_C * math.sin(math.pi / N)
    out["big-step tip clearance between planets (mm)"] = spacing - 2 * ra_big
    assert spacing - 2 * ra_big > 2
    out["big-step swept radius (mm)"] = A_C + ra_big
    assert A_C + ra_big < 57.5
    def cr_ext(z1, z2, m, x1, x2):
        r1, r2 = z1 * m / 2, z2 * m / 2; rb1, rb2 = r1 * math.cos(PA), r2 * math.cos(PA)
        ra1, ra2 = r1 + (1 + x1) * m, r2 + (1 + x2) * m
        L = math.sqrt(ra1 ** 2 - rb1 ** 2) + math.sqrt(ra2 ** 2 - rb2 ** 2) - A_C * math.sin(math.acos((rb1 + rb2) / A_C))
        return L / (math.pi * m * math.cos(PA))
    def cr_int(zp, zr, m):
        rp, rr = zp * m / 2, zr * m / 2; rbp, rbr = rp * math.cos(PA), rr * math.cos(PA)
        L = math.sqrt((rp + m) ** 2 - rbp ** 2) - math.sqrt((rr - 0.9 * m) ** 2 - rbr ** 2) + (rr - rp) * math.sin(PA)
        return L / (math.pi * m * math.cos(PA))
    out["contact ratio sun-big"] = cr_ext(Zs, Zp1, m1, XS, XP)
    out["contact ratio small-ring"] = cr_int(Zp2, Zr, m2)
    assert out["contact ratio sun-big"] > 1.4 and out["contact ratio small-ring"] > 1.4
    # output lost motion from 2*BL per mesh (planet kinematics, sun held; pitch radii)
    r1, r2 = m1 * Zp1 / 2, m2 * Zp2 / 2
    j = 2 * BL
    dth = (j + (r2 / r1) * j) / (A_C * (1 + r2 / r1))
    out["output backlash (deg, approx.)"] = math.degrees(dth); assert out["output backlash (deg)" if False else "output backlash (deg, approx.)"] < 0.5
    out["small step root dia (mm)"] = m2 * Zp2 - 2.5 * m2
    out["wall 685 bore (D11) to small root (mm)"] = (m2 * Zp2 - 2.5 * m2 - 11) / 2
    out["big-step root dia (mm) (lightening holes must stay inside)"] = 2 * (m1 * Zp1 / 2 - (1.25 - XP) * m1)
    return out


# Planet k = planet 0 rotated 120k deg about the main axis, then spun on its own pin by 20*j deg (a multiple of the
# 18T small-step pitch, so the ring mesh is unchanged).  Zs/3 is not an integer, so j is needed for the sun mesh:
# 3k = +-2j (mod 9) -> (j1,j2) in {(6,3),(6,12),(15,3),(15,12)} by the raster search; j found by the raster check (hip_gear_mesh_check.py): see PLANET_SPIN_J there.
PLANET_SPIN_J = (0, 6, 3)


def profiles():
    return {
        # sun: gap at 0 deg -> tooth centred at 10 deg
        "sun": external(Zs, m1, -BL, phase_deg=180 / Zs, x=XS),
        # planet big step: tooth at 0 (and 180) deg
        "planet_big": external(Zp1, m1, -BL, phase_deg=0, x=XP),
        # planet small step: gap at 0 deg -> tooth at 10 deg (a big tooth at 10 deg too -> offset 0)
        "planet_small": external(Zp2, m2, -BL, phase_deg=10),
        # ring: internal = complement of an external 63T 'space gear' with add 1.25m / ded 1.0m,
        # ring addendum shortened to 0.9m (tip-to-root clearance, see mesh check); its teeth are the ring spaces: ring tooth at 0 deg -> space gear tooth at 180/63 deg
        "ring_space": external(Zr, m2, +BL, add=1.25, ded=0.9, rf_fac=0.0, phase_deg=180 / Zr),
    }


if __name__ == "__main__":
    for k, v in checks().items():
        print(f"{k}: {v if not isinstance(v, float) else round(v, 4)}")
    if "--json" in sys.argv:
        p = profiles()
        json.dump({k: [[round(x, 4), round(y, 4)] for x, y in v] for k, v in p.items()}, open(sys.argv[sys.argv.index("--json") + 1], "w"))
        print({k: len(v) for k, v in p.items()})
