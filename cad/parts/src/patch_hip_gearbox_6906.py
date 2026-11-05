"""A13/C7: bearing 1 6806 -> 6906 (30x47x9), outboard face stays at z 51 (cover lip), bearing now z 42-51.
python3 patch_hip_gearbox_6906.py OUT.json ; solidcraft-cli run OUT.json --in hip_gearbox.solidcraft --save hip_gearbox.solidcraft"""
import json, sys
C = []
def cmd(c, **p): C.append({"command": c, "params": p})
def ring(name, z0, h, ro, ri, op, tgt, body=None):
    cmd("sketch.create", plane="XY", offset=str(z0), name=name + "_sk")
    cmd("sketch.circle.center", center=[0, 0], radius=ro); cmd("sketch.circle.center", center=[0, 0], radius=ri); cmd("sketch.finish")
    p = dict(sketch=name + "_sk", distance=h, operation=op, name=name, profiles=[{"point": [(ro + ri) / 2, 0]}])
    if tgt: p["targets"] = [tgt]
    if body: p["body_name"] = body
    cmd("solid.extrude", **p)
cmd("solid.remove", bodies=["B_6806"])
ring("B6906", 42, 9, 23.5, 15, "new", None, "B_6906")
# carrier: groove floor z 43 -> 41.5 out to r 27.5 (cover boss wall r 23.5-26.5), inner-race shoulder top z 44 -> 42
ring("BrgGroove2", 41.5, 8, 27.5, 17.3, "cut", "HG_CarrierOut")
ring("BrgSeat2", 42, 7.5, 17.3, 14.98, "cut", "HG_CarrierOut")
# cover: thicker boss going down to z 42.5, then bore the seat to D47 (z 42-51, lip z 51-53 stays)
ring("CoverBoss2", 42.5, 8, 26.5, 22, "join", "HG_Cover")
cmd("solid.cylinder", diameter=47, height=9, base=[0, 0, 42], operation="cut", targets=["HG_Cover"], name="CoverSeat47")
json.dump({"commands": C}, open(sys.argv[1], "w"))
