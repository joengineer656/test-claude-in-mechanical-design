"""A13 body patch (C8/C9/C10/C11) on the saved body.solidcraft: python3 patch_body_a13.py OUT.json ; solidcraft-cli run OUT.json --in ../body.solidcraft --save ../body.solidcraft
Reuses the generator helpers (build_body.py is imported with a dummy stage so nothing runs)."""
import sys, json, math
_o = sys.argv[:]; sys.argv = ["x", "0", "/dev/null"]
import build_body as B
sys.argv = _o
from build_body import cmd, box, cyl, cut, poly, beam, Y, POSTA, POSTS, HX, HZ
(x1, z1), (x2, z2) = POSTA
hp = (HX - 44, HZ + 44)                                   # hip post at world 135 deg, joins the seat
for s, SUF in ((1, "_L"), (-1, "_R")):
    B.SUF = SUF; n = "B1_Side" + SUF; T = "B1T_Tie" + SUF
    # ---- C8/C10: collars on both arch posts, bore D18.4 (guide), 10 mm long y 55-65; post1 D29 (hook slot at x -22 must stay free), post2 D32
    a, b = Y(s, 55, 65); cyl("colA", 29, (x1, a, z1), b-a, "Y", t=n)
    cut("colAtop", n, x1-16, x1+16, a, b, 339.9, 348)   # shortcut: 0.1 mm nick of the plate top, a coplanar cut returns no result
    cyl("colB", 32, (x2, a, z2), b-a, "Y", t=n)
    a, b = Y(s, 54, 66)
    cyl("boreA", 18.4, (x1, a, z1), b-a, "Y", op="cut", t=n); cut("slotA", n, x1-9.2, x1+9.2, a, b, z1, 341)
    cyl("boreB", 18.4, (x2, a, z2), b-a, "Y", op="cut", t=n)
    # ---- C10: post base seat, 4 mm PAHT-CF at y 36-40 (post end face bears on y 40), fused to the 135 deg hip post; 2 x O4.5 per arch post (M4)
    yf = 40 if s > 0 else -36
    for nm, p0, p1, w in (("seatA", (x1, z1), hp, 16), ("seatB", (x2, z2), hp, 16)):
        poly(nm, yf, 4, beam(p0, p1, w), n)
    a, b = Y(s, 36, 40)
    cyl("seatDA", 30, (x1, a, z1), b-a, "Y", t=n); cyl("seatDB", 22, (x2, a, z2), b-a, "Y", t=n); cyl("seatDH", 17, (hp[0], a, hp[1]), b-a, "Y", t=n)
    a, b = Y(s, 35, 41)
    ux, uz = hp[0]-x1, hp[1]-z1; L = math.hypot(ux, uz); ux, uz = ux/L, uz/L           # post1: holes +-11 perpendicular to the strip
    for k in (1, -1): cyl(f"seatHA{k}", 4.5, (x1 - uz*11*k, a, z1 + ux*11*k), b-a, "Y", op="cut", t=n)
    ux, uz = hp[0]-x2, hp[1]-z2; L = math.hypot(ux, uz); ux, uz = ux/L, uz/L           # post2: holes 13 and 22 mm along the strip (plate edge is at x -50)
    for k, d in enumerate((13, 22)): cyl(f"seatHB{k}", 4.5, (x2 + ux*d, a, z2 + uz*d), b-a, "Y", op="cut", t=n)
    cyl("seatBoreA", 18, (x1, a, z1), 0.0001, "Y", op="cut", t=n) if False else None
    # driver plate / XDrive corner relief grows for the R11 seat disc at post2
    a, b = Y(s, 31, 53)
    cut("dpn2", "REF_DrvPlate_hip" + SUF, -62, -49, a, b, 294, 317); cut("xdn2", "REF_XDrive_hip" + SUF, -62, -52, a, b, 294, 317)
    # ---- C11: washer step under the hip-plate nuts (nut pocket stays), M4 x 55 through-bolt + washer both ends
    for i, (px, pz) in enumerate(POSTS):
        a, b = Y(s, 61.6, 62.7); cyl(f"wash{i}", 9.6, (px, a, pz), b-a, "Y", op="cut", t=n)
    # ---- C9: tie rebuilt
    cmd("solid.remove", bodies=[T])
    B.SUF = SUF
    box(T, 66, 85, *Y(s, 63, 66), 340, 359)
    a, b = Y(s, 38, 69.6); box("shelf", 66, 132, a, b, 353, 359, op="join", t=T)
    for i, (hx, hy) in enumerate([(94.5, 42), (94.5, 66), (122.5, 42), (122.5, 66)]):
        cyl(f"th{i}", 5.5, (hx, s*hy, 352), 8, "Z", op="cut", t=T)
    for i, (hx, hz) in enumerate([(71, 346), (80, 346)]):
        a, b = Y(s, 62, 67); cyl(f"tw{i}", 4.5, (hx, a, hz), b-a, "Y", op="cut", t=T)
# lid notch D19 -> D21 for the O18 posts
for s in (1, -1):
    B.SUF = "_%d" % s
    a, b = Y(s, 36, 62); cyl("pn21", 21, (x1, a, z1), b-a, "Y", op="cut", t="B3_Lid")
for nm in ("B1_Side_L", "B1_Side_R", "B1T_Tie_L", "B1T_Tie_R", "B3_Lid"):
    cmd("file.export", path=f"exports/stl/body/{nm}.stl", bodies=[nm])
cmd("inspect.measure", bodies=["B1_Side_L", "B1_Side_R", "B1T_Tie_L", "B1T_Tie_R", "B3_Lid"])
cmd("file.export", path="exports/step/body.step", format="step")
json.dump({"commands": B.C}, open(sys.argv[1], "w")); print(len(B.C), "commands")
