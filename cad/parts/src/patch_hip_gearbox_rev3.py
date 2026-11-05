"""Rev 3 patch (assembly review A1-A7) on the saved hip_gearbox.solidcraft - small run, no rebuild.
python3 patch_hip_gearbox_rev3.py OUT.json [thigh_deg]   (thigh_deg = final thigh angle, default -33.19; re-run on the .bak to re-set the tab)
then: solidcraft-cli run OUT.json --in hip_gearbox.solidcraft --save hip_gearbox.solidcraft
Local frame as build_hip_gearbox.py (NOM_THIGH = -thigh_ang)."""
import json, math, sys
thigh = float(sys.argv[2]) if len(sys.argv) > 2 else -33.19
OLD, NEW = 29.99 + 180, -thigh + 180          # tab centre angle, old and new
C = []
def cmd(c, **p): C.append({"command": c, "params": p})
def quad(a, r0, r1, w): 
    u = (math.cos(math.radians(a)), math.sin(math.radians(a))); v = (-u[1], u[0])
    return [[round(r*u[0]+s*v[0], 4), round(r*u[1]+s*v[1], 4)] for r, s in ((r0, -w), (r1, -w), (r1, w), (r0, w))]
def sk_ext(name, z, pts, dist, op, tgt):
    cmd("sketch.create", plane="XY", offset=str(z), name=name)
    cmd("sketch.line", points=pts, closed=True); cmd("sketch.finish")
    cmd("solid.extrude", sketch=name, distance=dist, operation=op, targets=[tgt], name=name + "_f")
# M1: delete bearing 2, arch, journal extension (hex stays; clamp insert hole moved into the hex z55..65)
cmd("solid.remove", bodies=["B_6806_2", "HG_Arch"])
cmd("solid.cylinder", diameter=31, height=9, base=[0, 0, 65], operation="cut", targets=["HG_CarrierOut"], name="JournalCut")
cmd("solid.cylinder", diameter=5.6, height=10, base=[0, 0, 55], operation="cut", targets=["HG_CarrierOut"], name="OutEndIns2")
# M4: cover boss/lip trimmed to z 52 (world y 92)
cmd("solid.cylinder", diameter=140, height=3, base=[0, 0, 52], operation="cut", targets=["HG_Cover"], name="CoverTrim")
# M3: homing tab to the new thigh angle (old tab outside the plate r 40.75 cut away, new tab joined)
sk_ext("TabOld_sk", 40, quad(OLD, 40.8, 48, 4.2), 8.6, "cut", "HG_CarrierOut")
sk_ext("TabNew_sk", 40, quad(NEW, 39.5, 47.5, 4.0), 8.5, "join", "HG_CarrierOut")
json.dump({"commands": C}, open(sys.argv[1], "w"))
