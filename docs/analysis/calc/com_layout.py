# NOTE 2026-11-05: the real-body CoM of the full assembly is in cad/assembly/src/com_assembly.py (copy docs/analysis/calc/com_assembly.py): 6.96 kg solid, CoM +22 mm fwd of the axle. This layout script is the old 4.37 kg layout; see docs/assembly.md.
"""P2 master layout: 4-bar pose, clearance checks and centre of mass.

Frame: X forward, Y left, Z up, mm. Origin = ground under the robot centre at nominal stance.
The body is fixed in this frame; in other poses the legs and wheels move and the ground is at
axle_z - wheel_d/2. Masses from bom/bom.md + docs/analysis/mass_budget.md (rev 2) plus the
P2 changes listed in docs/layout.md. Run: python3 com_layout.py  (asserts the targets).
The same numbers drive the SolidCraft parameters (printed at the end per pose).
"""
import math
import numpy as np

# ---------------- parameters (keep equal to the SolidCraft user parameters) ----------------
P = dict(
    wheel_d=170, tyre_w=25, track_w=275, hub_d=86,
    thigh=121, shank=189, coupler=113, knee_pin=42, shank_bend=175,   # theory.md 3.3
    Bx=46, Bz=34,                                                    # coupler body pivot from hip
    hip_h_nom=195, hip_h_crouch=101, hip_h_ext=289,                  # hip above axle (100-290 range)
    crank_r=40,
    body_w=126, body_h=190, body_d=210, body_x0=-125, body_z0=150,    # body box: x from body_x0, z from body_z0
    bat_x=-104.5,                                                    # battery centre x (CoM trim rail)
)
R = P["wheel_d"] / 2
# Y planes (left side, mirrored to the right), [y_min, y_max]
Y = dict(
    hip_enc=(0.5, 8.5), hip_plate=(8.5, 11.5), hip_motor=(11.5, 40.0), hip_gbx=(40.0, 80.0),
    shank=(68.0, 80.0), thigh=(81.0, 91.0), spring=(81.0, 95.0), coupler=(93.0, 101.0),
    wheel_enc=(70.0, 78.0), hub_stack=(80.0, 125.0), wheel=(125.0, 150.0),
    lug=(63.0, 101.0), stop=(81.0, 91.0), stop_brkt=(63.0, 81.0),
)

# ---------------- 4-bar kinematics (theory frame: x fwd, y up, hip at origin) ----------------
B = np.array([P["Bx"], P["Bz"]], float)


def leg(phi):
    K = P["thigh"] * np.array([math.cos(phi), math.sin(phi)])
    d = np.linalg.norm(B - K)
    a = (P["knee_pin"] ** 2 - P["coupler"] ** 2 + d ** 2) / (2 * d)
    h = math.sqrt(max(P["knee_pin"] ** 2 - a ** 2, 0.0))
    u = (B - K) / d
    C = K + a * u - h * np.array([-u[1], u[0]])          # branch that matches theory.md table
    ang = math.atan2(C[1] - K[1], C[0] - K[0]) - math.radians(P["shank_bend"])
    W = K + P["shank"] * np.array([math.cos(ang), math.sin(ang)])
    return K, C, W


def phi_for(h):
    lo, hi = math.radians(-85), math.radians(5)       # hip height rises as phi falls
    for _ in range(60):
        m = (lo + hi) / 2
        lo, hi = (lo, m) if -leg(m)[2][1] < h else (m, hi)
    return (lo + hi) / 2


PHI = {k: phi_for(P[f"hip_h_{k}"]) for k in ("crouch", "nom", "ext")}
PHI["stop"] = phi_for(130)                            # rev 2.1: end stop engages at 130 mm
HIP_X = -leg(PHI["nom"])[2][0]                         # axle under the origin at nominal
HIP_Z = R + P["hip_h_nom"]


def w(p):  # theory point -> world XZ
    return np.array([HIP_X + p[0], HIP_Z + p[1]])


def crank(phi):  # 40 mm crank opposite the thigh
    return P["crank_r"] * np.array([math.cos(phi + math.pi), math.sin(phi + math.pi)])


# spring anchor on the body: along the reverse tangent of the crank pin at full extension
_pe, _t = crank(PHI["ext"]), PHI["ext"] + math.pi
ANCHOR = _pe + 62 * np.array([math.sin(_t), -math.cos(_t)])
# end stop: TPU pad over the thigh top face at r = 70 mm, touching at phi_stop
_r, _ps = 70.0, PHI["stop"]
_n = np.array([-math.sin(_ps), math.cos(_ps)])
STOP_C = _r * np.array([math.cos(_ps), math.sin(_ps)]) + _n * (7 + 15)   # pad 30 thick, centre 15 above face

# ---------------- static components (nominal world) ----------------
bx0, bz0 = P["body_x0"], P["body_z0"]
BODY = (bx0, bx0 + P["body_d"], -P["body_w"] / 2, P["body_w"] / 2, bz0, bz0 + P["body_h"])
ZTOP = BODY[5]


def box(cx, cy, cz, lx, ly, lz):
    return (cx - lx / 2, cx + lx / 2, cy - ly / 2, cy + ly / 2, cz - lz / 2, cz + lz / 2)


def cyl_y(cx, cz, d, y0, y1):
    return (cx - d / 2, cx + d / 2, y0, y1, cz - d / 2, cz + d / 2)


def mir(b):
    return (b[0], b[1], -b[3], -b[2], b[4], b[5])


hx, hz = HIP_X, HIP_Z
# name: (mass g, AABB) ; inside-body items are checked for overlap with each other
STATIC = {
    "battery 6S 2200 + cradle": (365, box(P["bat_x"], 0, 206.5, 35, 45, 107)),   # upright at the rear wall
    "Pi 4 + heatsink": (56, box(-42.5, 0, 214, 85, 56, 28)),
    "ESP32 PCB + IMU": (25, box(25, 0, 190, 70, 50, 10)),
    "PDB": (25, box(52, 0, 160, 34, 40, 14)),
    "5 V buck": (7, box(52, -35, 158, 22, 18, 10)),
    "fan 40 mm + vents": (15, box(77, 0, 185, 10, 40, 40)),
    "driver hip L (on 70x70 Al)": (61, box(-85, 46.75, 275, 70, 26.5, 70)),
    "driver hip R (on 70x70 Al)": (61, box(-85, -46.75, 275, 70, 26.5, 70)),
    "driver wheel L (on 70x70 Al)": (61, box(-85, 46.75, 195, 70, 26.5, 70)),
    "driver wheel R (on 70x70 Al)": (61, box(-85, -46.75, 195, 70, 26.5, 70)),
    "brake resistor L": (10, box(-72.5, 15, 257.5, 15, 28, 51)),
    "brake resistor R": (10, box(-72.5, -15, 257.5, 15, 28, 51)),
    "e-stop (top, rear)": (30, box(-100, 0, ZTOP - 5, 40, 40, 50)),
    "anti-spark switch (top)": (18, box(-100, 38, ZTOP - 7.5, 30, 20, 15)),
    "fuse 50 A + holder (top hatch)": (15, box(-97.5, -40, ZTOP - 12.5, 45, 20, 25)),
    "LD19 lidar + mast": (52, box(-40, 0, ZTOP + 25 + 33.5 / 2, 38.6, 38.6, 33.5)),
    "Pi camera (front)": (7, box(P["body_d"] + bx0 + 5.75, 0, 300, 11.5, 25, 24)),
    "body shell + mast": (282, BODY),
    "harness + PDB wiring + NTC + misc": (131, box(-45, 0, 245, 40, 60, 20)),
    "body fasteners/inserts": (160, BODY),
}
for s, sgn in (("L", 1), ("R", -1)):
    f = (lambda b: b) if sgn > 0 else mir
    STATIC[f"hip encoder {s}"] = (8, f(cyl_y(hx, hz, 30, *Y["hip_enc"])))
    STATIC[f"hip Al plate {s}"] = (32, f(cyl_y(hx, hz, 100, *Y["hip_plate"])))
    STATIC[f"hip motor 8308 {s}"] = (336 + 24.5, f(cyl_y(hx, hz, 92, *Y["hip_motor"])))
    STATIC[f"hip gearbox 8:1 {s}"] = (253, f(cyl_y(hx, hz, 100, *Y["hip_gbx"])))
INSIDE_SKIP = {"body shell + mast", "body fasteners/inserts", "LD19 lidar + mast", "Pi camera (front)",
               "harness + PDB wiring + NTC + misc", "e-stop (top, rear)"}
IMU = np.array([0.0, 0.0, 187.0])                       # on the ESP32 PCB underside, mid-plane


def leg_parts(phi):
    """Moving parts of the left leg: name -> (mass g, centroid XZ world, y centre, capsule/circle)."""
    K, C, W = leg(phi)
    H = np.zeros(2)
    Pc, A = crank(phi), ANCHOR
    yc = lambda k: sum(Y[k]) / 2
    parts = {
        "thigh": (33, (H + K) / 2, yc("thigh"), ("cap", w(H), w(K), 7)),
        "crank": (0, Pc / 2, yc("thigh"), ("cap", w(H), w(Pc), 6)),
        "shank": (63, (C + W) / 2, yc("shank"), ("cap", w(C), w(W), 7)),
        "coupler": (31, (B + C) / 2, yc("coupler"), ("cap", w(B), w(C), 5)),
        "spring": (35, (Pc + A) / 2, yc("spring"), ("cap", w(Pc), w(A), 7)),
        "knee joint hw": (40, K, yc("thigh"), ("cap", w(K), w(K), 12)),
        "C joint hw": (25, C, yc("coupler"), ("cap", w(C), w(C), 9)),
        "B joint hw": (16, B, yc("coupler"), ("cap", w(B), w(B), 8)),
        "hip joint hw": (16, H, yc("thigh"), ("cap", w(H), w(H), 8)),
        "leg cable": (28.5, (K + W) / 2, yc("shank"), None),
        "wheel module": (497, W, 125.0, ("cap", w(W), w(W), R)),
        "hub stack": (0, W, yc("hub_stack"), ("cap", w(W), w(W), P["hub_d"] / 2)),
        "wheel encoder": (0, W, yc("wheel_enc"), ("cap", w(W), w(W), 15)),
        "end stop (TPU+brkt)": (10 + 3, STOP_C, yc("stop"), ("cap", w(STOP_C), w(STOP_C), 15)),
        "leg-side hip encoder": (8, H, 85.0, None),
    }
    return parts, (K, C, W)


def seg_dist(p, q, a, b):
    """Min distance between 2D segments pq and ab."""
    def pt_seg(x, s0, s1):
        d = s1 - s0
        t = 0.0 if not d.any() else np.clip(np.dot(x - s0, d) / np.dot(d, d), 0, 1)
        return np.linalg.norm(x - (s0 + t * d))
    def cross(o, u, v):
        return (u[0] - o[0]) * (v[1] - o[1]) - (u[1] - o[1]) * (v[0] - o[0])
    if (p != q).any() and (a != b).any():
        d1, d2, d3, d4 = cross(a, b, p), cross(a, b, q), cross(p, q, a), cross(p, q, b)
        if d1 * d2 < 0 and d3 * d4 < 0:
            return 0.0
    return min(pt_seg(p, a, b), pt_seg(q, a, b), pt_seg(a, p, q), pt_seg(b, p, q))


def cap_rect(cap, r):
    _, p, q, rad = cap
    x0, x1, z0, z1 = r
    corners = [np.array(c, float) for c in ((x0, z0), (x1, z0), (x1, z1), (x0, z1))]
    inside = lambda v: x0 <= v[0] <= x1 and z0 <= v[1] <= z1
    if inside(p) or inside(q):
        return -rad
    return min(seg_dist(p, q, corners[i], corners[(i + 1) % 4]) for i in range(4)) - rad


def overlap(a, b):
    return a[0] < b[1] and b[0] < a[1]


# pairs that are joined on purpose (no clearance check)
JOINED = {frozenset(p) for p in [("thigh", "shank"), ("thigh", "crank"), ("thigh", "knee joint hw"),
          ("shank", "knee joint hw"), ("shank", "C joint hw"), ("coupler", "C joint hw"),
          ("coupler", "B joint hw"), ("shank", "hub stack"), ("shank", "wheel encoder"),
          ("spring", "crank"), ("thigh", "hip joint hw"), ("crank", "hip joint hw"), ("spring", "thigh"),
          ("hub stack", "wheel encoder"), ("hub stack", "wheel module"), ("knee joint hw", "C joint hw"),
          ("coupler", "knee joint hw"), ("spring", "hip joint hw"), ("thigh", "C joint hw")]}
YR = {"thigh": Y["thigh"], "crank": Y["thigh"], "shank": Y["shank"], "coupler": Y["coupler"],
      "spring": Y["spring"], "knee joint hw": (Y["shank"][0], Y["thigh"][1]),
      "C joint hw": (Y["shank"][0], Y["coupler"][1]), "B joint hw": Y["lug"],
      "hip joint hw": Y["thigh"], "wheel module": Y["wheel"], "hub stack": Y["hub_stack"],
      "wheel encoder": Y["wheel_enc"], "end stop (TPU+brkt)": (Y["stop_brkt"][0], Y["stop"][1])}
# fixed obstacles for the leg: hip gearbox / motor / plate (circles) and body box (rect)
FIXED = {"hip gearbox": (Y["hip_gbx"], ("cap", w((0, 0)), w((0, 0)), 50)),
         "hip motor": (Y["hip_motor"], ("cap", w((0, 0)), w((0, 0)), 46)),
         "body": ((-1, P["body_w"] / 2), ("rect", (BODY[0], BODY[1], BODY[4], BODY[5])))}


def clearances(pose):
    parts, _ = leg_parts(PHI[pose])
    out = []
    names = [n for n in parts if parts[n][3] is not None]
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if frozenset((a, b)) in JOINED or not overlap(YR[a], YR[b]):
                continue
            if pose == "crouch" and {a, b} == {"thigh", "end stop (TPU+brkt)"}:
                continue   # compressed on purpose below 130 mm
            ca, cb = parts[a][3], parts[b][3]
            out.append((a, b, seg_dist(ca[1], ca[2], cb[1], cb[2]) - ca[3] - cb[3]))
        for f, (yr, shp) in FIXED.items():
            if not overlap(YR[a], yr) or (a == "end stop (TPU+brkt)"):
                continue
            if a == "B joint hw" and f == "hip gearbox":
                continue   # B pivot lug is part of the stationary hip housing
            ca = parts[a][3]
            d = cap_rect(ca, shp[1]) if shp[0] == "rect" else seg_dist(ca[1], ca[2], shp[1], shp[2]) - ca[3] - shp[3]
            out.append((a, f, d))
    return out


def com(pose):
    parts, (K, C, W) = leg_parts(PHI[pose])
    m_tot, mom = 0.0, np.zeros(3)
    rows = []
    for n, (m, b) in STATIC.items():
        c = np.array([(b[0] + b[1]) / 2, (b[2] + b[3]) / 2, (b[4] + b[5]) / 2])
        rows.append((n, m, c))
    for n, (m, c2, yc, _) in parts.items():
        cw = w(c2)
        for s in (1, -1):
            rows.append((f"{n} {'L' if s > 0 else 'R'}", m, np.array([cw[0], s * yc, cw[1]])))
    for n, m, c in rows:
        m_tot += m
        mom += m * c
    cg = mom / m_tot
    axle = w(W)
    return m_tot, cg, axle, rows


def static_overlaps():
    names = [n for n in STATIC if n not in INSIDE_SKIP]
    bad = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            A, Bb = STATIC[a][1], STATIC[b][1]
            if all(overlap((A[2 * k], A[2 * k + 1]), (Bb[2 * k], Bb[2 * k + 1])) for k in range(3)):
                if {a.split()[1] if a.startswith("hip") else a, b.split()[1] if b.startswith("hip") else b} <= {"encoder", "Al", "motor", "gearbox"}:
                    continue  # coaxial hip stack parts touch by design
                bad.append((a, b))
    return bad


def dist_box(p, b):
    q = np.array([np.clip(p[0], b[0], b[1]), np.clip(p[1], b[2], b[3]), np.clip(p[2], b[4], b[5])])
    return np.linalg.norm(p - q)


def dist_cyl_y(p, cx, cz, r, y0, y1):
    radial = max(math.hypot(p[0] - cx, p[2] - cz) - r, 0)
    axial = max(y0 - abs(p[1]), abs(p[1]) - y1, 0)
    return math.hypot(radial, axial)


if __name__ == "__main__":
    print(f"hip x = {HIP_X:.1f} mm, hip z = {HIP_Z:.1f} mm (nominal), axle z = {R:.1f}")
    print("pose     phi_deg  hip_h   K(x,z)world      C(x,z)world      W(x,z)world")
    for p in ("crouch", "stop", "nom", "ext"):
        K, C, W = leg(PHI[p])
        print(f"{p:7s} {math.degrees(PHI[p]):7.1f} {-W[1]:6.1f}  {np.round(w(K),1)}  {np.round(w(C),1)}  {np.round(w(W),1)}")
    sl = {p: np.linalg.norm(crank(PHI[p]) - ANCHOR) for p in ("crouch", "nom", "ext")}
    print(f"spring anchor (hip rel) {np.round(ANCHOR,1)} world {np.round(w(ANCHOR),1)}; length crouch/nom/ext "
          f"{sl['crouch']:.1f}/{sl['nom']:.1f}/{sl['ext']:.1f} -> stroke {sl['crouch']-sl['ext']:.1f} mm (target 52)")
    stop_travel = 70 * (math.sin(PHI['crouch']) - math.sin(PHI['stop']))
    print(f"end stop pad centre world {np.round(w(STOP_C),1)}; engages at hip 130, pad compression at full crouch "
          f"{stop_travel:.1f} mm (hip travel {130 - P['hip_h_crouch']} mm)")

    bad = static_overlaps()
    print("static overlaps:", bad or "none")
    assert not bad

    worst = {}
    for p in ("crouch", "nom", "ext"):
        for a, b, d in clearances(p):
            k = (a, b)
            worst[k] = min(worst.get(k, 1e9), d)
            if d < 3:
                print(f"  CLASH/TIGHT {p}: {a} vs {b}: {d:.1f} mm")
    print("min leg clearances over crouch/nom/ext (mm):")
    for (a, b), d in sorted(worst.items(), key=lambda kv: kv[1])[:12]:
        print(f"  {a:22s} vs {b:16s} {d:6.1f}")
    assert min(worst.values()) >= 3, "leg clearance < 3 mm"

    res = {}
    for p in ("crouch", "nom", "ext"):
        m, cg, axle, rows = com(p)
        ground = axle[1] - R
        dx = cg[0] - axle[0]
        res[p] = (m, cg, axle, dx, cg[2] - ground, cg[2] - axle[1])
        print(f"{p:7s} mass {m/1000:.3f} kg  CoM world ({cg[0]:.1f},{cg[1]:.2f},{cg[2]:.1f})  axle x {axle[0]:.1f}  "
              f"fore-aft vs axle {dx:+.1f}  lateral {cg[1]:+.2f}  height above ground {cg[2]-ground:.1f}  above axle {cg[2]-axle[1]:.1f}")
    # targets: nominal fore-aft +-5, lateral <=5 everywhere; other poses within the +-20 mm battery-rail trim
    assert abs(res["nom"][3]) <= 5, "nominal fore-aft CoM outside +-5 mm"
    assert all(abs(r[1][1]) <= 5 for r in res.values()), "lateral CoM > 5 mm"
    assert all(abs(r[3]) <= 20 for r in res.values()), "crouch/extended offset beyond trim range"
    assert abs(sum(STATIC[n][0] for n in STATIC) + 2 * sum(v[0] for v in leg_parts(0)[0].values()) - 4370) < 1  # 4312 BOM + 42 (2 extra driver Al plates) + 16 (2 hip motor-side encoder kits)

    # IMU rules
    m, cg, *_ = res["nom"]
    print(f"IMU {IMU} vs CoM: d = {np.round(IMU - cg,1)}")
    assert np.all(np.abs(IMU - cg) <= 30), "IMU not within +-30 mm of the CoM"
    dmin = min([dist_box(IMU, STATIC[n][1]) for n in STATIC if n.startswith(("driver", "brake", "fan"))] +
               [dist_cyl_y(IMU, HIP_X, HIP_Z, 50, Y["hip_plate"][0], Y["hip_gbx"][1])])
    print(f"IMU distance to nearest motor/driver/resistor/fan: {dmin:.1f} mm")
    assert dmin >= 40

    # envelope
    for p in ("crouch", "nom", "ext"):
        parts, (K, C, W) = leg_parts(PHI[p])
        ground = w(W)[1] - R
        top = STATIC["LD19 lidar + mast"][1][5]
        xs = [BODY[0], BODY[1] + 11.5] + [w(v)[0] + 10 for v in (K, C)] + [w(W)[0] - R, w(W)[0] + R]
        print(f"{p:7s} height {top-ground:.1f}  depth {max(xs)-min(xs):.1f}  width {2*Y['wheel'][1]:.0f}  "
              f"body bottom above ground {BODY[4]-ground:.1f}")
    print("SolidCraft pose parameters (deg):")
    for p in ("crouch", "nom", "ext"):
        K, C, W = leg(PHI[p])
        sh = math.degrees(math.atan2(W[1] - C[1], W[0] - C[0]))
        cp = math.degrees(math.atan2(C[1] - B[1], C[0] - B[0]))
        cr = crank(PHI[p]); sp = math.degrees(math.atan2(ANCHOR[1] - cr[1], ANCHOR[0] - cr[0]))
        print(f"  {p}: thigh_ang={math.degrees(PHI[p]):.3f} shank_ang={sh:.3f} coupler_ang={cp:.3f} spring_ang={sp:.3f} "
              f"spring_len={np.linalg.norm(ANCHOR-cr):.2f} shank_full={np.linalg.norm(W-C):.2f}")
