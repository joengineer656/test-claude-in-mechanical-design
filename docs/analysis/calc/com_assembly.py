"""CoM of the whole assembly from the real bodies (volume centroids from SolidCraft) x assigned masses.
python3 com_assembly.py bodies.json   (bodies.json = list of {name,bbox,com,vol}, nominal pose)
Mass rule: printed/metal parts = CAD volume x density (solid, conservative); bought envelope blocks = real mass (table).
Lumped items without geometry are added at their layout positions. 'sliced' scales PRINTED parts by SLICE."""
import json, sys, re
SLICE = 0.75            # assumed solid->sliced ratio for printed parts (docs/analysis/mass_actual.md: 6.41/6.86 overall, printed ~0.7-0.8)
AXLE_X = 17.43          # rev 2 leg CAD: axle at nominal = hip x 28 minus 10.57
RHO = dict(paht=1.2, petg=1.27, tpu=1.21, al=2.70, steel=7.85, bronze=8.8)
FIXED = {   # bought envelopes: real mass in g (layout.md / bom)
 "REF_Battery":340, "REF_Pi4":56, "REF_ESP32":25, "REF_IMU":0, "REF_Camera3":7, "REF_XDrive_hip_L":41, "REF_XDrive_hip_R":41, "REF_XDrive_whl_L":41, "REF_XDrive_whl_R":41, "REF_Fan":15, "REF_Res_L":10, "REF_Res_R":10,
 "REF_LD19":47, "REF_LD19_part":0,
 "REF_ResBracket_Al1mm":6.5}
LUMPS = [  # (name, g, x, y, z) layout.md section 2, no geometry in the CAD
 ("PDB", 25, 52, 0, 160), ("Buck5V", 7, 52, -35, 158), ("EStop", 30, -100, 0, 335), ("Switch", 18, -100, 38, 332), ("Fuse50A", 15, -97.5, -40, 328),
 ("Harness", 131, -45, 0, 245), ("BodyFasteners", 160, -20, 0, 245),
 ("LegCable_L", 28.5, 66, 74, 152), ("LegCable_R", 28.5, 66, -74, 152), ("HipEncLeg_L", 8, 28, 85, 280), ("HipEncLeg_R", 8, 28, -85, 280),
 ("HipFasteners_L", 17.5, 28, 40, 280), ("HipFasteners_R", 17.5, 28, -40, 280),
 ("WheelFasteners_L", 19, AXLE_X, 100, 85), ("WheelFasteners_R", 19, AXLE_X, -100, 85)]
def material(n):
    b = re.sub(r"^(HG[LR]_|WH[LR]_|Leg[LR]_)", "", n)
    if b.startswith("REF_Encoder_env") or b.startswith("REF_EncBoard"): return ("fixed", 8 if "Encoder_env" in b else 6)
    if b == "REF_8308_KV130": return ("fixed", 360.5)
    if b == "REF_MN5008": return ("fixed", 128)
    if b.startswith("B_6806"): return ("fixed", 19)
    if b.startswith("B_685ZZ"): return ("fixed", 1.9)
    if b.startswith("B_Pin5x"): return ("steel", 0)
    if b.startswith("B_Magnet"): return ("fixed", 0.3)
    if b == "Spring_env" or b == "Leg_Spring_env" or b == "Spring_env": return ("fixed", 35)
    if b.startswith("Leg_Spring"): return ("fixed", 35)
    if b.startswith("Leg_Pin") or b.startswith("Leg_Spacer") or b.startswith("Leg_HexSleeve") or b.startswith("Leg_ArchPost") or b.startswith("Leg_Brg"): return ("steel", 0) if not b.startswith("Leg_Brg") else ("fixed", 19)
    if b.startswith("Leg_Bush"): return ("bronze", 0)
    if b.startswith("Leg_ShankPlate") or b.startswith("Leg_KneeStrap") or b.startswith("Leg_ArchPlate") or b.startswith("Leg_OutriggerBeam") or b in ("HG_AlPlate", "WH_Axle", "B1S_HipSeat_L", "B1S_HipSeat_R") or b.startswith("REF_DrvPlate"): return ("al", 0)
    if b.startswith("Leg_StopPad") or b.startswith("Leg_Bumper") or b.startswith("Leg_Dot") or b == "WH_Tyre": return ("tpu", 0)
    if b in ("WH_Hub", "WH_Cover") or re.match(r"B[2-7]", b) and not b.startswith("B1"): return ("petg", 0)
    return ("paht", 0)
def run(bodies, sliced=False):
    rows = []
    for b in bodies:
        n = b["name"]
        if n in FIXED: kind, m = "fixed", FIXED[n]
        else:
            kind, m = material(n)
            if kind != "fixed": m = b["vol"] / 1000 * RHO[kind]
        if sliced and kind in ("paht", "petg"): m *= SLICE
        rows.append((n, kind, m, b["com"]))
    rows += [(n, "lump", g, (x, y, z)) for n, g, x, y, z in LUMPS]
    M = sum(r[2] for r in rows)
    c = [sum(r[2] * r[3][i] for r in rows) / M for i in range(3)]
    return M, c, rows
if __name__ == "__main__":
    bodies = json.load(open(sys.argv[1]))
    for lab, sl in (("solid", False), ("sliced", True)):
        M, c, rows = run(bodies, sl)
        print(f"{lab}: mass {M:.0f} g  CoM x {c[0]:.1f} (vs axle {c[0]-AXLE_X:+.1f}), y {c[1]:+.2f}, z {c[2]:.1f} (above axle {c[2]-85:.1f})")
    M, c, rows = run(bodies)
    grp = {}
    for n, k, m, com in rows:
        g = re.match(r"(HG[LR]|WH[LR]|Leg[LR])_", n); g = g.group(1)[:-1] if g else ("Body+electronics" if k != "lump" else "lumps")
        grp[g] = grp.get(g, 0) + m
    print({k: round(v) for k, v in grp.items()})
