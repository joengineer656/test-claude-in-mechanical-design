"""Generates the SolidCraft command script for the P3a hip gearbox (left side).
Run:  python3 build_hip_gearbox.py OUT.json [--explode]
      solidcraft-cli run OUT.json --save hip_gearbox.solidcraft
Local frame: Z = gearbox axis (outboard +), z = 0 = 8308 rotor face, X = world X (forward), Y = -world Z.
Left side world = (28 + x, 40 + z, 280 - y). Right side = mirror about world XZ (see docs/parts/hip_gearbox.md).
Gear polylines: docs/analysis/calc/hip_gear_geometry.py (phasing documented there).
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../docs/analysis/calc"))
import hip_gear_geometry as g

PR = g.profiles()
A = 33.75                      # centre distance (both stages)
TANPSI = math.tan(math.radians(20))   # herringbone helix on the ring stage
TW_P = TANPSI * 10 / 13.5      # small-step twist over half face (b/2 = 10)
TW_R = TANPSI * 10 / 47.25     # ring twist, same hand (internal mesh)
NOM_THIGH = 29.99              # local output angle of the thigh at nominal pose (= -thigh_ang)
C = []                          # commands


def cmd(c, **p):
    C.append({"command": c, "params": p})


def rot(pts, a, c=(0.0, 0.0)):
    cs, sn = math.cos(a), math.sin(a)
    return [[round(c[0] + x * cs - y * sn, 4), round(c[1] + x * sn + y * cs, 4)] for x, y in pts]


def poly_sketch(name, z, pts):
    cmd("sketch.create", plane="XY", offset=str(z), name=name)
    cmd("sketch.line", points=pts, closed=True, connect=False)
    cmd("sketch.finish")


def circles_sketch(name, z, circles):
    cmd("sketch.create", plane="XY", offset=str(z), name=name)
    for (x, y, r) in circles:
        cmd("sketch.circle.center", center=[round(x, 4), round(y, 4)], radius=r)
    cmd("sketch.finish")


def cyl(name, d, z0, h, body=None, op="new", targets=None, x=0.0, y=0.0):
    p = dict(diameter=d, height=h, base=[round(x, 4), round(y, 4), z0], operation=op, name=name)
    if body: p["body_name"] = body
    if targets: p["targets"] = targets
    cmd("solid.cylinder", **p)


def ext(name, sketch, dist, op, targets=None, body=None, profiles=None):
    p = dict(sketch=sketch, distance=dist, operation=op, name=name)
    if targets: p["targets"] = targets
    if body: p["body_name"] = body
    if profiles is not None: p["profiles"] = profiles
    cmd("solid.extrude", **p)


def pol(r, deg):
    return r * math.cos(math.radians(deg)), r * math.sin(math.radians(deg))


def ring_tube(name, z0, h, ro, ri, body=None, op="new", targets=None):
    """annulus by sketch (two circles, pick the ring region)"""
    sk = name + "_sk"
    circles_sketch(sk, z0, [(0, 0, ro), (0, 0, ri)])
    ext(name, sk, h, op, targets, body, profiles=[{"point": [(ro + ri) / 2, 0]}])


PLANETS = [0, 120, 240]
POSTS = [60, 180, 300]
EARS = [345, 285, 255, 195, 165]      # local deg; world angle = -local (left side) = 15,75,105,165,195: clear of the body hip posts (world 45/135/225/315, +-15) and of the shank sector local 20..110
ARCH_EAR = 255
R_EAR = 64.0

# ---------------- parameters (documentation + key values) ----------------
for n, e, u in [("m_in", "1.25 mm", "mm"), ("m_out", "1.5 mm", "mm"), ("a_c", "33.75 mm", "mm"),
                ("b_big", "14 mm", "mm"), ("b_ring", "20 mm", "mm"), ("helix", "20 deg", "deg"),
                ("ring_root_r", "49.125 mm", "mm"), ("big_sweep_r", "57.5 mm", "mm")]:
    cmd("parameters.add", name=n, expression=e, unit=u)

# ---------------- SUN (PAHT-CF) ----------------
cyl("SunFlange", 50, 0, 5, body="HG_Sun")
poly_sketch("SunTeeth_sk", 5, PR["sun"])
ext("SunTeeth", "SunTeeth_sk", 15.5, "join", ["HG_Sun"])
cyl("SunRelief", 14, -0.01, 2.01, op="cut", targets=["HG_Sun"])
circles_sketch("SunBolt_sk", 5, [(*pol(20, 45 + 90 * k), 3.25) for k in range(4)])
ext("SunCbore", "SunBolt_sk", -3.2, "cut", ["HG_Sun"])
circles_sketch("SunHole_sk", 0, [(*pol(20, 45 + 90 * k), 1.7) for k in range(4)])
ext("SunHole", "SunHole_sk", 5, "cut", ["HG_Sun"])

# ---------------- PLANET 1 (PAHT-CF, 100 %) at (33.75, 0) ----------------
poly_sketch("PBig_sk", 5.5, rot(PR["planet_big"], 0, (A, 0)))
ext("PlanetBig", "PBig_sk", 14, "new", body="HG_Planet_1")
for i, (z, a) in enumerate([(19.5, 0), (29.5, TW_P), (39.5, 0)]):
    poly_sketch(f"PSm{i}_sk", z, rot(PR["planet_small"], a, (A, 0)))
cmd("solid.loft", sections=[{"sketch": "PSm0_sk"}, {"sketch": "PSm1_sk"}], operation="join", targets=["HG_Planet_1"], name="PlanetSmallA")
cmd("solid.loft", sections=[{"sketch": "PSm1_sk"}, {"sketch": "PSm2_sk"}], operation="join", targets=["HG_Planet_1"], name="PlanetSmallB")
cyl("PlanetBore", 6.0, 5, 35, op="cut", targets=["HG_Planet_1"], x=A)
cyl("PlanetBrgA", 11.0, 5, 5.5, op="cut", targets=["HG_Planet_1"], x=A)
cyl("PlanetBrgB", 11.0, 34.5, 5.5, op="cut", targets=["HG_Planet_1"], x=A)
circles_sketch("PLight_sk", 5.5, [(A + 13.5 * math.cos(math.radians(30 + 60 * k)), 13.5 * math.sin(math.radians(30 + 60 * k)), 3.5) for k in range(6)])
ext("PlanetLight", "PLight_sk", 14, "cut", ["HG_Planet_1"])   # 6 x D7 lightening holes on r 13.5 (6:1 rev: inside the big-step root D37.3)
for k, ang in enumerate(PLANETS[1:], start=2):
    # 6:1: planet k = copy spun on its own pin by 20*j deg (Zs/3 not an integer), then rotated 120(k-1) deg about the main axis
    nm = f"HG_Planet_1 ({k})"
    cmd("solid.move", bodies=["HG_Planet_1"], translate=[-A, 0, 0], copy=True)
    cmd("solid.move", bodies=[nm], axis=[0, 0, 1], angle=f"{20 * g.PLANET_SPIN_J[k - 1]} deg")
    cmd("solid.move", bodies=[nm], translate=[A, 0, 0])
    cmd("solid.move", bodies=[nm], axis=[0, 0, 1], angle=f"{ang} deg")
# copies get default names -> renamed after the run (see below)

# ---------------- CARRIER IN (inboard ring) ----------------
ring_tube("CarrierIn", 1, 4, 40.75, 26, body="HG_CarrierIn")
circles_sketch("CinPin_sk", 1, [(*pol(A, a), 2.475) for a in PLANETS])
ext("CinPin", "CinPin_sk", 4, "cut", ["HG_CarrierIn"])
circles_sketch("Posts_sk", 5, [(*pol(A, a), 7) for a in POSTS])
ext("Posts", "Posts_sk", 35, "join", ["HG_CarrierIn"])          # posts printed with the inboard ring (ring face on the bed)
circles_sketch("PostIns_sk", 40, [(*pol(A, a), 2.0) for a in POSTS])
ext("PostIns", "PostIns_sk", -7, "cut", ["HG_CarrierIn"])      # M3 heat-set inserts in the post tops

# ---------------- CARRIER OUT (plate + posts + stub + hex, PAHT-CF) ----------------
cyl("CoutPlate", 81.5, 40, 9, body="HG_CarrierOut")
ring_tube("BrgGroove", 43, 6.5, 25, 17, op="cut", targets=["HG_CarrierOut"])     # floor z 43 (3 mm)
ring_tube("BrgSeat", 44, 5.5, 17.3, 14.98, op="cut", targets=["HG_CarrierOut"])  # inner-race shoulder r 15..17 at z 43..44
cyl("CoutStub", 30, 43.5, 9.5, op="join", targets=["HG_CarrierOut"])
cmd("sketch.create", plane="XY", offset="53", name="Hex_sk")
cmd("sketch.polygon.inscribed" if False else "sketch.line", points=[[round(26 / math.sqrt(3) * math.cos(math.radians(30 + 60 * k)), 4), round(26 / math.sqrt(3) * math.sin(math.radians(30 + 60 * k)), 4)] for k in range(6)], closed=True)
cmd("sketch.finish")
ext("OutHex", "Hex_sk", 12, "join", ["HG_CarrierOut"])      # hex z 53..65, thigh plane z 54..63
cyl("OutJournal", 30, 65, 8, op="join", targets=["HG_CarrierOut"])   # journal for the 2nd 6806 (z 65..73)
cyl("OutEndIns", 5.6, 63, 10, op="cut", targets=["HG_CarrierOut"])   # M4 steel insert in the journal end (bearing clamp washer)
circles_sketch("CoutBolt_sk", 40, [(*pol(A, a), 1.7) for a in POSTS])
ext("CoutBolt", "CoutBolt_sk", 9, "cut", ["HG_CarrierOut"])    # M3 x 12 low-head from the outboard face
circles_sketch("CoutCb_sk", 49, [(*pol(A, a), 3.0) for a in POSTS])
ext("CoutCb", "CoutCb_sk", -2.2, "cut", ["HG_CarrierOut"])
circles_sketch("CoutPin_sk", 40, [(*pol(A, a), 2.475) for a in PLANETS])
ext("CoutPin", "CoutPin_sk", 6, "cut", ["HG_CarrierOut"])
# thigh clamp: no radial/axial inserts on the hex face (the journal closes them). Thigh sits between the z53 shoulder and a 2 mm spacer (z63..65) pushed by bearing-2 inner race; one M4 + washer in the OutEndIns steel insert clamps the stack
# homing tab (thigh at nominal -> tab opposite the thigh)
tab_c = NOM_THIGH + 180
cmd("sketch.create", plane="XY", offset="40", name="Tab_sk")
w = 4.0
ux, uy = math.cos(math.radians(tab_c)), math.sin(math.radians(tab_c))
vx, vy = -uy, ux
cmd("sketch.line", points=[[round(r * ux + s * vx, 4), round(r * uy + s * vy, 4)] for r, s in ((39.5, -w), (47.5, -w), (47.5, w), (39.5, w))], closed=True)
cmd("sketch.finish")
ext("HomeTab", "Tab_sk", 8.5, "join", ["HG_CarrierOut"])

# ---------------- RING (fixed, PAHT-CF 100 %, herringbone) ----------------
# ring = loft of sections (lobed outline with 5 bolt holes, minus the tooth-space polyline): booleans on the
# lofted teeth hang this kernel, so ears and bolt holes are part of every loft section
def lobed(ro, r_ear, w_ear, ears, n=1440):
    def ext_r(t):
        r = ro
        for a in ears:
            d = math.radians(a) - t
            d = math.atan2(math.sin(d), math.cos(d))
            perp = r_ear * math.sin(abs(d))
            if perp < w_ear / 2 and abs(d) < math.pi / 2:
                r = max(r, r_ear * math.cos(d) + math.sqrt((w_ear / 2) ** 2 - perp ** 2))
        return r
    return [[round(ext_r(2 * math.pi * k / n) * math.cos(2 * math.pi * k / n), 4),
             round(ext_r(2 * math.pi * k / n) * math.sin(2 * math.pi * k / n), 4)] for k in range(n)]
RING_OUT = lobed(52.1, R_EAR, 10, EARS)
for i, (z, a) in enumerate([(19.5, 0), (29.5, TW_R), (39.5, 0)]):
    cmd("sketch.create", plane="XY", offset=str(z), name=f"RSp{i}_sk")
    cmd("sketch.line", points=RING_OUT, closed=True, connect=False)
    cmd("sketch.line", points=rot(PR["ring_space"], a), closed=True, connect=False)
    for e in EARS:
        cmd("sketch.circle.center", center=[round(pol(R_EAR, e)[0], 4), round(pol(R_EAR, e)[1], 4)], radius=1.7)
    cmd("sketch.finish")
RPR = [{"point": [50.6, 0]}]
cmd("solid.loft", sections=[{"sketch": "RSp0_sk", "profiles": RPR}, {"sketch": "RSp1_sk", "profiles": RPR}], body_name="HG_Ring", name="RingA")
cmd("solid.loft", sections=[{"sketch": "RSp1_sk", "profiles": RPR}, {"sketch": "RSp2_sk", "profiles": RPR}], operation="join", targets=["HG_Ring"], name="RingB")

# ---------------- COVER (bearing boss + stop blocks) ----------------
ring_tube("CoverFlange", 39.5, 3, 52.1, 49, body="HG_Cover")
cmd("sketch.create", plane="XY", offset="39.5", name="CovEar_sk")
for a in EARS:
    p0, p1 = pol(51, a), pol(R_EAR, a)
    cmd("sketch.slot.center_to_center", p0=[round(p0[0], 4), round(p0[1], 4)], p1=[round(p1[0], 4), round(p1[1], 4)], width=10)
cmd("sketch.finish")
ext("CoverEars", "CovEar_sk", 3, "join", ["HG_Cover"])
circles_sketch("CovBolt_sk", 39.5, [(*pol(R_EAR, a), 1.7) for a in EARS])
ext("CovBolt", "CovBolt_sk", 3, "cut", ["HG_Cover"])
ring_tube("CoverWall", 42.5, 9.5, 52.1, 49, op="join", targets=["HG_Cover"])
ring_tube("CoverTop", 49.5, 2.5, 52.1, 21, op="join", targets=["HG_Cover"])
ring_tube("CoverLip", 51, 2, 23.5, 19, op="join", targets=["HG_Cover"])   # axial lip: 2 mm x 2.2 mm bite (was 1 x 1.5)
ring_tube("CoverBoss", 44.5, 5.5, 24.5, 21, op="join", targets=["HG_Cover"])
# stop blocks: tab half width at r 44 ~ 5.2 deg; crouch stop at thigh local -1.5 deg, extension stop at +74.7 deg
half = math.degrees(w / 44)
for nm, a0, a1 in (("StopCrouch", 180 - 1.5 - half - 14, 180 - 1.5 - half), ("StopExt", 180 + 74.7 + half, 180 + 74.7 + half + 14)):
    pts = [pol(42.25, a0), pol(49.5, a0), pol(49.5, (a0 + a1) / 2), pol(49.5, a1), pol(42.25, a1), pol(42.25, (a0 + a1) / 2)]
    cmd("sketch.create", plane="XY", offset="41", name=nm + "_sk")
    cmd("sketch.line", points=[[round(x, 4), round(y, 4)] for x, y in pts], closed=True)
    cmd("sketch.finish")
    ext(nm, nm + "_sk", 8.5, "join", ["HG_Cover"])

# ---------------- SKIRT / HOUSING (revolved, PAHT-CF) ----------------
# skirt tube wall 3.4 mm (was 2.4: SF 1.41 -> about 2.4 by section modulus x1.65 and fewer stress concentrations)
# built from annuli + one lofted 45 deg cone (a revolved polyline made later booleans hang in this kernel)
ring_tube("SkFlange", -28.5, 4, 58, 48, body="HG_Skirt")
ring_tube("SkTube", -24.5, 19, 51.4, 48, op="join", targets=["HG_Skirt"])
for i, (z, ro, ri) in enumerate([(-5.5, 51.4, 48), (5, 60.9, 58.5)]):
    circles_sketch(f"SkCone{i}_sk", z, [(0, 0, ro), (0, 0, ri)])
CPR = lambda r: [{"point": [r, 0]}]
cmd("solid.loft", sections=[{"sketch": "SkCone0_sk", "profiles": CPR(49.7)}, {"sketch": "SkCone1_sk", "profiles": CPR(59.7)}],
    operation="join", targets=["HG_Skirt"], name="SkCone")
ring_tube("SkBig", 5, 14.5, 60.9, 58.5, op="join", targets=["HG_Skirt"])
circles_sketch("SkEar_sk", 13.5, [(*pol(R_EAR, a), 5) for a in EARS])
ext("SkEars", "SkEar_sk", 6, "join", ["HG_Skirt"])
circles_sketch("SkEarH_sk", 13.4, [(*pol(R_EAR, a), 1.7) for a in EARS])
ext("SkEarH", "SkEarH_sk", 6.2, "cut", ["HG_Skirt"])
# lip closing the gap over the big planets (r 52.1..57.5), notched around the ring ears (regions between the ears)
cmd("sketch.create", plane="XY", offset="19.0", name="SkLip_sk")   # 0.5 overlap into SkBig so the lip joins (face contact left loose bodies)
cmd("sketch.circle.center", center=[0, 0], radius=60.0)
cmd("sketch.circle.center", center=[0, 0], radius=52.6)
for a in EARS:
    p0, p1 = pol(50, a), pol(R_EAR, a)
    cmd("sketch.slot.center_to_center", p0=[round(p0[0], 4), round(p0[1], 4)], p1=[round(p1[0], 4), round(p1[1], 4)], width=10.6)
cmd("sketch.finish")
_e = sorted(EARS)
_mids = [(_e[i] + _e[(i + 1) % len(_e)] + (360 if i == len(_e) - 1 else 0)) / 2 for i in range(len(_e))]
ext("SkLip", "SkLip_sk", 2.5, "join", ["HG_Skirt"], profiles=[{"point": [round(pol(56.75, m)[0], 3), round(pol(56.75, m)[1], 3)]} for m in _mids])
circles_sketch("SkFlH_sk", -28.5, [(*pol(54, 45 + 90 * k), 1.7) for k in range(4)])
ext("SkFlH", "SkFlH_sk", 4, "cut", ["HG_Skirt"])
for k in range(3):   # 6 vent / wire windows 10 x 10 mm through the motor skirt, between the flange bolts
    t = math.radians(30 + 60 * k)
    cmd("sketch.create", plane={"origin": [0, 0, 0], "x_dir": [-math.sin(t), math.cos(t), 0], "y_dir": [0, 0, 1]}, name=f"SkWin{k}_sk")
    cmd("sketch.rectangle.two_point", p0=[-5, -22], p1=[5, -12])
    cmd("sketch.finish")
    cmd("solid.extrude", sketch=f"SkWin{k}_sk", distance=140, direction="symmetric", operation="cut", targets=["HG_Skirt"], name=f"SkWin{k}")

# shortcut: 45 deg gussets under the 5 skirt ears hang this kernel (boolean never returns); print with 5 small tree supports instead (docs/parts/hip_gearbox.md)

# ---------------- AL MOTOR PLATE (6061, 3 mm) ----------------
cmd("sketch.create", plane="XY", offset="-31.5", name="Plate_sk")
cmd("sketch.rectangle.center", center=[0, 0], corner=[52, 52])
cmd("sketch.finish")
ext("AlPlate", "Plate_sk", 3, "new", body="HG_AlPlate")
cmd("solid.fillet", edges=[[52, 52, -30], [-52, 52, -30], [52, -52, -30], [-52, -52, -30]], radius=8, name="PlateCorners")
holes = [(0, 0, 6)] + [(*pol(20, 90 * k), 2.25) for k in range(4)] + [(*pol(54, 45 + 90 * k), 1.25) for k in range(4)] \
    + [(sx * 45, sy * 45, 2.25) for sx in (1, -1) for sy in (1, -1)] + [(*pol(33, 45 + 90 * k), 11) for k in range(4)] \
    + [(10.5, 0, 0.8), (-10.5, 0, 0.8)]
circles_sketch("PlateH_sk", -31.5, holes)
ext("PlateHoles", "PlateH_sk", 3, "cut", ["HG_AlPlate"])

# ---------------- bought parts and references ----------------
for k, a in enumerate(PLANETS):
    x, y = pol(A, a)
    for j, z0 in enumerate((5.5, 34.5)):
        ring_tube(f"B685_{k}{j}", z0, 5, 5.5, 2.5, body=f"B_685ZZ_{2 * k + j + 1}")
    cyl(f"BPin{k}", 5, 1, 45, body=f"B_Pin5x45_{k + 1}", x=x, y=y)
cmd("solid.move", bodies=["B_685ZZ_3", "B_685ZZ_4"], axis=[0, 0, 1], angle="0 deg")  # placeholder no-op removed below
ring_tube("B6806", 44, 7, 21, 15, body="B_6806")
ring_tube("B6806_2", 65, 7, 21, 15, body="B_6806_2")
# ---------------- ARCH (2nd output bearing, body-fixed, bolted on the 6th stack ear at local 270 = world +90) ----------------
_ux, _uy = math.cos(math.radians(ARCH_EAR)), math.sin(math.radians(ARCH_EAR)); _vx, _vy = -_uy, _ux
def _quad(u0, u1, v0, v1): return [[round(u * _ux + v * _vx, 4), round(u * _uy + v * _vy, 4)] for u, v in ((u0, v0), (u1, v0), (u1, v1), (u0, v1))]
cmd("sketch.create", plane="XY", offset="64", name="ArchBar_sk"); cmd("sketch.line", points=_quad(10, 72, -8, 8), closed=True, connect=False); cmd("sketch.finish")
ext("ArchBar", "ArchBar_sk", 12, "new", body="HG_Arch")
cmd("sketch.create", plane="XY", offset="42.5", name="ArchPost_sk"); cmd("sketch.line", points=_quad(56, 72, -8, 8), closed=True, connect=False); cmd("sketch.finish")
ext("ArchPost", "ArchPost_sk", 21.5, "join", ["HG_Arch"])
cyl("ArchRing", 47, 64, 12, op="join", targets=["HG_Arch"])
cyl("ArchBore", 42, 63.9, 8.1, op="cut", targets=["HG_Arch"])        # 6806 seat z 65..72, open towards the thigh
cyl("ArchLip", 38, 71.9, 4.3, op="cut", targets=["HG_Arch"])         # top lip r 19..23.5, z 72..76
cyl("ArchBolt", 3.4, 42, 36, op="cut", targets=["HG_Arch"], x=pol(64, ARCH_EAR)[0], y=pol(64, ARCH_EAR)[1])   # M3 x 60 stack bolt through post + cover/ring/skirt ears
cyl("Ref8308", 92, -28.5, 28.5, body="REF_8308_KV130")
cyl("RefEnc", 30, -39.5, 8, body="REF_Encoder_env_D30x8")
cyl("RefMag", 6, -31.0, 2.5, body="REF_Magnet_D6x2.5")

if __name__ == "__main__":
    # bearings were built around the origin: move each to its planet centre
    out = []
    for c in C:
        if c["command"] == "solid.move" and c["params"].get("angle") == "0 deg":
            continue
        out.append(c)
        if c["command"] == "solid.extrude" and c["params"]["name"].startswith("B685_"):
            k = int(c["params"]["name"][5]); x, y = pol(A, PLANETS[k])
            out.append({"command": "solid.move", "params": {"bodies": [c["params"]["body_name"]], "translate": [round(x, 4), round(y, 4), 0]}})
    out += [{"command": "body.rename", "params": {"body": f"HG_Planet_1 ({k})", "name": f"HG_Planet_{k}"}} for k in (2, 3)]
    if "--explode" in sys.argv:
        dz = {"REF_Encoder_env_D30x8": -60, "REF_Magnet_D6x2.5": -45, "HG_AlPlate": -40, "REF_8308_KV130": -20, "HG_Skirt": 0,
              "HG_Sun": 15, "HG_CarrierIn": 30, "HG_Ring": 95, "HG_CarrierOut": 125, "B_6806": 145, "HG_Cover": 165, "B_6806_2": 200, "HG_Arch": 225}
        for b, d in dz.items():
            out.append({"command": "solid.move", "params": {"bodies": [b], "translate": [0, 0, d]}})
    json.dump({"commands": out}, open(sys.argv[1], "w"))
    print(len(out), "commands")
