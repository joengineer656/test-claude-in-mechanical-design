"""Wheel planetary 24/18/60, m1.25, spur. Kinematic mesh check by raster overlap (no shapely): sweeps the carrier angle and
reports the maximum overlap area of planet/sun and planet/ring material. Run: python3 wheel_gear_geometry.py"""
import math, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../cad/parts/src"))
import build_wheel as w
ZS, ZP, ZR, AC = w.ZS, w.ZP, w.ZR, w.AC
print("ratio", 1 + ZR / ZS, "centre dist", AC, "assembly (zs+zr)/3", (ZS + ZR) / 3, "zs/3", ZS / 3, "zr/3", ZR / 3)
rotp = lambda P, a, c=(0, 0): np.array(w.rot([list(p) for p in P], a, c))
res = 0.15; xs = np.arange(-45, 45, res); X, Y = np.meshgrid(xs, xs); pts = np.c_[X.ravel(), Y.ravel()]
def inside(poly):   # even-odd ray casting
    poly = np.asarray(poly); x, y = pts[:, 0], pts[:, 1]; c = np.zeros(len(pts), bool)
    for (x1, y1), (x2, y2) in zip(poly, np.roll(poly, -1, axis=0)):
        m = (y1 > y) != (y2 > y)
        with np.errstate(divide="ignore", invalid="ignore"):
            c ^= m & (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1)
    return c
ring_void = inside(np.array(w.PR["ring_space"]))               # ring spaces = void bounded by the polyline
worst_s = worst_r = 0
for phi in np.linspace(0, 360 / ZP, 13):                    # carrier angle sweep (deg)
    th_p = phi * (1 - ZR / ZP)                                    # planet spin (ring fixed)
    th_s = phi * (1 + ZR / ZS)                                    # sun rotation
    sun = inside(rotp(w.PR["sun"], th_s))
    pl = np.zeros(len(pts), bool)
    for a in w.PLAN:
        P = rotp(w.PR["planet"], th_p - phi); P = P + np.array([AC, 0]); P = rotp(P, a + phi)
        m = inside(P); worst_s = max(worst_s, (m & sun).sum() * res * res)
        r_mat = ~ring_void & (np.hypot(pts[:, 0], pts[:, 1]) < 42)
        worst_r = max(worst_r, (m & r_mat).sum() * res * res)
print("max overlap planet-sun mm2", round(worst_s, 3), " planet-ring mm2", round(worst_r, 3), "(raster noise ~0.05)")
