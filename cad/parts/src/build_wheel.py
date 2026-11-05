"""Wheel module (one side; the other is mirrored). Generates SolidCraft command scripts, one per part + all.
Run:  python3 build_wheel.py OUTDIR      (then see run_wheel.sh: solidcraft-cli run OUTDIR/<part>.json --out ...)
Local frame: Z = axle, u = Z, outboard +. World (left wheel) = (0, 80+u, 85). Spur gears (herringbone not used: reliability, see docs/parts/wheel.md).
Client decision: mass cuts of the spec skipped (stronger version); track not reduced.
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../docs/analysis/calc"))
import hip_gear_geometry as g

M = 1.25
ZS, ZP, ZR = 24, 18, 60
AC = M * (ZS + ZP) / 2          # 26.25
BL = g.BL
PR = {"sun": g.external(ZS, M, -BL, phase_deg=7.5),
      "planet": g.external(ZP, M, -BL, phase_deg=0),
      "ring_space": g.external(ZR, M, +BL, add=1.25, ded=0.9, rf_fac=0.0, phase_deg=0)}
PLAN = [0, 120, 240]
POSTS = [60, 180, 300]
C = []


def cmd(c, **p): C.append({"command": c, "params": p})
def pol(r, deg): return r * math.cos(math.radians(deg)), r * math.sin(math.radians(deg))
def rot(pts, deg, c=(0.0, 0.0)):
    a = math.radians(deg); cs, sn = math.cos(a), math.sin(a)
    return [[round(c[0] + x * cs - y * sn, 4), round(c[1] + x * sn + y * cs, 4)] for x, y in pts]
def shift(pts, dx, dy): return [[round(x + dx, 4), round(y + dy, 4)] for x, y in pts]

def circles_sketch(name, z, circles):
    cmd("sketch.create", plane="XY", offset=str(z), name=name)
    for (x, y, r) in circles: cmd("sketch.circle.center", center=[round(x, 4), round(y, 4)], radius=r)
    cmd("sketch.finish")
def polys_sketch(name, z, polys):
    cmd("sketch.create", plane="XY", offset=str(z), name=name)
    for p in polys: cmd("sketch.line", points=p, closed=True, connect=False)
    cmd("sketch.finish")
def ext(name, sk, dist, op, targets=None, body=None, profiles=None):
    p = dict(sketch=sk, distance=dist, operation=op, name=name)
    if targets: p["targets"] = targets
    if body: p["body_name"] = body
    if profiles is not None: p["profiles"] = profiles
    cmd("solid.extrude", **p)
def cyl(name, d, z0, h, body=None, op="new", targets=None, x=0.0, y=0.0):
    p = dict(diameter=d, height=h, base=[round(x, 4), round(y, 4), z0], operation=op, name=name)
    if body: p["body_name"] = body
    if targets: p["targets"] = targets
    cmd("solid.cylinder", **p)
def tube(name, z0, h, ro, ri, body=None, op="new", targets=None):
    circles_sketch(name + "_sk", z0, [(0, 0, ro), (0, 0, ri)])
    ext(name, name + "_sk", h, op, targets, body, profiles=[{"point": [(ro + ri) / 2, 0]}])
def holes(name, z0, h, pts_r, targets):   # through/blind cut, sketch at z0 extruded +h
    circles_sketch(name + "_sk", z0, pts_r); ext(name, name + "_sk", h, "cut", targets)

def rect_ray(ang, t0, t1, hw):  # rectangle along a ray: radial t0..t1, half width hw
    ux, uy = math.cos(math.radians(ang)), math.sin(math.radians(ang)); vx, vy = -uy, ux
    return [[round(t * ux + s * vx, 4), round(t * uy + s * vy, 4)] for t, s in ((t0, -hw), (t1, -hw), (t1, hw), (t0, hw))]

# ---------------------------------------------------------------- parts
def axle():   # Al 6061, CNC. Mass cuts skipped: 4 mm flange, no windows, fins 8 high
    cyl("Flange", 56, -16, 4, body="WH_Axle")
    cyl("Neck", 38, -12, 12, op="join", targets=["WH_Axle"])
    cyl("Shoulder", 40, 0, 0.5, op="join", targets=["WH_Axle"])
    cyl("Journal", 30, 0.5, 14, op="join", targets=["WH_Axle"])
    polys_sketch("Fin_sk", -24, [rect_ray(30 * k, 16.5, 27.2, 0.6) for k in range(12)])
    ext("Fins", "Fin_sk", 8.01, "join", ["WH_Axle"])
    tube("FinRing", -24, 8.01, 27.7, 26.5, op="join", targets=["WH_Axle"])
    cyl("BoreEnc", 31.2, -24.1, 23.1, op="cut", targets=["WH_Axle"])        # to u -1: board + screw heads (journal is OD 30, so the Ø31.2 seat cannot reach the bearings)
    cyl("Bore14", 14, -24.1, 38.7, op="cut", targets=["WH_Axle"])           # through to u 14.5
    holes("MotHoles", -1.1, 15.7, [(*pol(12.5, 45 + 90 * k), 1.7) for k in range(4)], ["WH_Axle"])
    holes("FlH", -16.1, 4.2, [(*pol(23, 45 + 90 * k), 2.1) for k in range(4)], ["WH_Axle"])  # M4 clearance, flange PCD 46
    circles_sketch("Cable_sk", -16.1, [(0, 0, 0.01)]) if False else None

def ringsleeve():  # PAHT-CF
    # ring teeth by loft of two identical sections (as the hip ring; a plain extrude+join hangs this kernel)
    for i, z in enumerate((49.5, 56.0, 62.5)):
        cmd("sketch.create", plane="XY", offset=str(z), name=f"RsRing{i}_sk")
        cmd("sketch.circle.center", center=[0, 0], radius=42)
        cmd("sketch.line", points=[[round(x, 4), round(y, 4)] for x, y in PR["ring_space"]], closed=True, connect=False)
        cmd("sketch.finish")
    P = [{"point": [40.5, 0]}]
    cmd("solid.loft", sections=[{"sketch": f"RsRing{i}_sk", "profiles": P} for i in (0, 1, 2)], body_name="WH_RingSleeve", name="RsRing")
    cyl("RsFlange", 60, 14.5, 3, op="join", targets=["WH_RingSleeve"])
    tube("RsTube", 17.5, 31, 31.5, 29.5, op="join", targets=["WH_RingSleeve"])
    tube("RsWeb", 48.5, 1, 42, 29.5, op="join", targets=["WH_RingSleeve"])
    cyl("RsCentre", 16, 14.4, 3.2, op="cut", targets=["WH_RingSleeve"])
    tube("RsRecess", 14.4, 1.9, 26.5, 18.5, op="cut", targets=["WH_RingSleeve"])   # clearance for hub boss + circlip
    holes("RsHoles", 14.4, 3.2, [(*pol(12.5, 45 + 90 * k), 1.7) for k in range(4)], ["WH_RingSleeve"])

def sun():
    cyl("SunCollar", 26, 44.5, 5.5, body="WH_Sun")
    polys_sketch("SunT_sk", 50, [[[round(x, 4), round(y, 4)] for x, y in PR["sun"]]])
    ext("SunTeeth", "SunT_sk", 12, "join", ["WH_Sun"])
    cyl("SunRecess", 21, 44.4, 3.0, op="cut", targets=["WH_Sun"])
    cyl("SunBore", 6.2, 44.4, 17.7, op="cut", targets=["WH_Sun"])
    holes("SunScr", 44.4, 17.7, [(*pol(9, 45 + 90 * k), 1.7) for k in range(4)], ["WH_Sun"])
    holes("SunCb", 47, 15.1, [(*pol(9, 45 + 90 * k), 2.9) for k in range(4)], ["WH_Sun"])

def planets():
    for k, a in enumerate(PLAN):
        n = f"WH_Planet_{k+1}"
        polys_sketch(f"Pl{k}_sk", 50, [rot(shift(PR["planet"], AC, 0), a)])
        ext(f"Planet{k}", f"Pl{k}_sk", 12, "new", body=n)
        x, y = pol(AC, a)
        cyl(f"PlPocA{k}", 11.1, 49.9, 5.2, op="cut", targets=[n], x=x, y=y)
        cyl(f"PlPocB{k}", 11.1, 56.9, 5.2, op="cut", targets=[n], x=x, y=y)
        cyl(f"PlPin{k}", 5.05, 49.9, 12.2, op="cut", targets=[n], x=x, y=y)

def carrierA():
    cyl("CaPlate", 58, 45, 4.5, body="WH_CarrierA")
    cyl("CaHole", 28, 44.9, 4.7, op="cut", targets=["WH_CarrierA"])
    circles_sketch("CaPost_sk", 49.5, [(*pol(24, a), 5) for a in POSTS])
    ext("CaPosts", "CaPost_sk", 13, "join", ["WH_CarrierA"])
    holes("CaPin", 46, 3.5, [(*pol(AC, a), 2.525) for a in PLAN], ["WH_CarrierA"])
    holes("CaPilot", 54.5, 8, [(*pol(24, a), 1.25) for a in POSTS], ["WH_CarrierA"])

def carrierB():
    cyl("CbPlate", 58, 62.5, 4.5, body="WH_CarrierB")
    cyl("CbHole", 24, 62.4, 4.7, op="cut", targets=["WH_CarrierB"])
    holes("CbPin", 62.5, 3.5, [(*pol(AC, a), 2.525) for a in PLAN], ["WH_CarrierB"])
    holes("CbIns", 62.5, 4.6, [(*pol(20, 45 + 90 * k), 2.0) for k in range(4)], ["WH_CarrierB"])  # M3 heat-set inserts, cover side
    holes("CbScr", 62.4, 4.7, [(*pol(24, a), 1.7) for a in POSTS], ["WH_CarrierB"])
    holes("CbCb", 65, 2.1, [(*pol(24, a), 3.0) for a in POSTS], ["WH_CarrierB"])

GAPS = [15 + 30 * k for k in range(12)]     # slot centres between hub tabs and tyre ribs
SLOT_HW = 4.3

def tab_poly(g0, r_in, r_out, n=10):
    t_in = math.sqrt(r_in ** 2 - SLOT_HW ** 2); t_out = math.sqrt(r_out ** 2 - SLOT_HW ** 2)
    a0 = g0 + math.degrees(math.atan2(SLOT_HW, t_out)); a1 = g0 + 30 - math.degrees(math.atan2(SLOT_HW, t_out))
    b0 = g0 + math.degrees(math.atan2(SLOT_HW, t_in)); b1 = g0 + 30 - math.degrees(math.atan2(SLOT_HW, t_in))
    outer = [pol(r_out, a0 + (a1 - a0) * i / n) for i in range(n + 1)]
    inner = [pol(r_in, b1 + (b0 - b1) * i / n) for i in range(n + 1)]
    return [[round(x, 4), round(y, 4)] for x, y in outer + inner]

def hub():   # PETG
    tube("HbWeb", 0.5, 3, 37.4, 21.05, body="WH_Hub")
    tube("HbBoss", 3.5, 12.3, 26, 21.05, op="join", targets=["WH_Hub"])
    tube("HbDrum", 3.4, 40.7, 37.4, 35, op="join", targets=["WH_Hub"])
    polys_sketch("HbSpk_sk", 40, [rect_ray(30 * k, 36, 67, 1.2) for k in range(12)])
    ext("HbSpokes", "HbSpk_sk", 8, "join", ["WH_Hub"])
    tube("HbStop", 44, 2.01, 75, 66, op="join", targets=["WH_Hub"])
    tube("HbRim", 46, 22.5, 69, 66, op="join", targets=["WH_Hub"])
    polys_sketch("HbTab_sk", 46, [tab_poly(g0, 68.5, 72.9) for g0 in GAPS])
    ext("HbTabs", "HbTab_sk", 22.5, "join", ["WH_Hub"])
    circles_sketch("HbBoss8_sk", 54, [(*pol(62.5, 22.5 + 45 * k), 4) for k in range(8)])
    ext("HbInsBoss", "HbBoss8_sk", 14.5, "join", ["WH_Hub"])
    holes("HbIns", 62, 6.5, [(*pol(62.5, 22.5 + 45 * k), 2.0) for k in range(8)], ["WH_Hub"])
    tube("HbCirclip", 14.5, 1.2, 21.65, 21.0, op="cut", targets=["WH_Hub"])   # DIN 472 circlip groove (Ø42 ring, 1.2) retains the outboard race

def cover():  # PETG
    cyl("CvDisc", 145, 68.5, 1.3, body="WH_Cover")
    cyl("CvStep", 139, 69.8, 1.2, op="join", targets=["WH_Cover"])
    cyl("CvBoss", 46, 67, 1.5, op="join", targets=["WH_Cover"])
    holes("CvPat", 66.9, 4.2, [(*pol(50, 30 * k + 15), 8) for k in range(12)], ["WH_Cover"])
    holes("CvM3", 66.9, 4.2, [(*pol(20, 45 + 90 * k), 1.7) for k in range(4)], ["WH_Cover"])
    holes("CvM3b", 68.4, 2.7, [(*pol(62.5, 22.5 + 45 * k), 1.7) for k in range(8)], ["WH_Cover"])
    holes("CvCb", 70, 1.1, [(*pol(62.5, 22.5 + 45 * k), 3.0) for k in range(8)] + [(*pol(20, 45 + 90 * k), 3.0) for k in range(4)], ["WH_Cover"])

NCELL = 32
def tyre():   # TPU 95A
    tube("TyBody", 46, 25, 85, 72.7, body="WH_Tyre")
    tube("TyLip", 69.8, 1.2, 73, 69.6, op="join", targets=["WH_Tyre"])
    polys_sketch("TyRib_sk", 46, [rect_ray(a, 69.0, 73.5, 4.0) for a in GAPS])
    ext("TyRibs", "TyRib_sk", 22.5, "join", ["WH_Tyre"])
    polys_sketch("TyCell_sk", 45.9, [rect_ray(360 * k / NCELL + 360 / NCELL / 2, 74.9, 82.8, 6.9) for k in range(NCELL)])
    ext("TyCells", "TyCell_sk", 25.2, "cut", ["WH_Tyre"])
    polys_sketch("TyGroove_sk", 45.9, [rect_ray(15 * k, 84.2, 86.5, 1.0) for k in range(24)])
    ext("TyGrooves", "TyGroove_sk", 25.2, "cut", ["WH_Tyre"])

def bought():
    cyl("MN5008", 55.6, 17.5, 27, body="REF_MN5008")
    cyl("MotCap", 20, 44.5, 2.4, op="join", targets=["REF_MN5008"])
    cyl("MotShaft", 6, 12.5, 5, op="join", targets=["REF_MN5008"])
    tube("B6806_1", 0.5, 7, 21, 15, body="B_6806_1")
    tube("B6806_2", 7.5, 7, 21, 15, body="B_6806_2")
    for k, a in enumerate(PLAN):
        x, y = pol(AC, a)
        for j, z0 in enumerate((50, 57)):
            circles_sketch(f"B685_{k}{j}_sk", z0, [(x, y, 5.5), (x, y, 2.5)])
            ext(f"B685_{k}{j}", f"B685_{k}{j}_sk", 5, "new", body=f"B_685ZZ_{2*k+j+1}", profiles=[{"point": [x + 4, y]}])
        cyl(f"Pin{k}", 5, 46, 20, body=f"B_Pin5x20_{k+1}", x=x, y=y)
    cyl("EncBoard", 30, -11.5, 8, body="REF_EncBoard_D30x8")
    cyl("MagHolder", 12.6, -2, 16.5, body="WH_MagHolder")
    cyl("MagPocket", 6.1, -2.1, 2.6, op="cut", targets=["WH_MagHolder"])
    cyl("MagShaftHole", 5.95, 12.5, 2.1, op="cut", targets=["WH_MagHolder"])
    cyl("Magnet", 6, -2, 2.5, body="B_Magnet_D6x2.5")

PARTS = {"axle": axle, "ringsleeve": ringsleeve, "sun": sun, "planets": planets, "carrierA": carrierA,
         "carrierB": carrierB, "hub": hub, "cover": cover, "tyre": tyre, "bought": bought}

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for n, f in list(PARTS.items()) + [("all", None)]:
        C.clear()
        for fn in ([f] if f else PARTS.values()): fn()
        json.dump({"commands": C}, open(f"{out}/{n}.json", "w"))
        print(n, len(C))
