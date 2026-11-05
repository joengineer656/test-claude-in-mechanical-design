"""2D mesh check of the hip gear polylines (hip_gear_geometry.py): rotates each pair through one tooth
pitch in the carrier frame with the 6:1 kinematics (sun 28T / big step 40T m1.0 shifted, 3 planets with pin spin 20*j) and reports interference and the minimum flank gap.
Run: python3 hip_gear_mesh_check.py (asserts no interference and 0.03 < gap < 0.2 mm)."""
import math, sys, numpy as np
import hip_gear_geometry as g

P = {k: np.array(v) for k, v in g.profiles().items()}
A_C = g.A_C


def rot(A, t, c=(0, 0)):
    cs, sn = math.cos(t), math.sin(t)
    return A @ np.array([[cs, -sn], [sn, cs]]).T + np.array(c)


def inside(poly, pts):  # even-odd ray casting, vectorised over pts
    x, y = pts[:, 0][:, None], pts[:, 1][:, None]
    a, b = poly, np.roll(poly, -1, 0)
    cond = (a[:, 1] > y) != (b[:, 1] > y)
    xi = a[:, 0] + (y - a[:, 1]) * (b[:, 0] - a[:, 0]) / (b[:, 1] - a[:, 1] + 1e-15)
    return (np.sum(cond & (x < xi), axis=1) % 2) == 1


def dens(A, n=4):
    B = np.roll(A, -1, 0)
    return np.concatenate([A + (B - A) * f for f in np.linspace(0, 1, n, endpoint=False)])


def near(A, c, r):
    return A[np.hypot(A[:, 0] - c[0], A[:, 1] - c[1]) < r]


def stage1(ts, js, k_list=(0, 1, 2)):
    """interference points / min gap sun vs planets k, planet k = rotated copy by 120k + pin spin 20*j_k deg."""
    tp = -ts * g.Zs / g.Zp1
    S = rot(P["sun"], ts)
    hit, gap = 0, 9.0
    for k in k_list:
        Q = rot(rot(P["planet_big"], tp + math.radians(20 * js[k])), 2 * math.pi * k / 3, (0, 0)) if False else None
        Q0 = rot(P["planet_big"], tp + math.radians(20 * js[k]), (A_C, 0))
        Q = rot(Q0, 2 * math.pi * k / 3)
        c = (A_C * math.cos(2 * math.pi * k / 3), A_C * math.sin(2 * math.pi * k / 3))
        s_, q1 = near(dens(S), c, 25), near(dens(Q), (0, 0), 16)
        hit += inside(Q, s_).sum() + inside(S, q1).sum()
        gap = min(gap, np.min(np.hypot(*(s_[:, None, :] - q1[None, :, :]).transpose(2, 0, 1))))
    return hit, gap


def main():
    res = {}
    steps = np.linspace(0, math.radians(20) * g.Zp1 / g.Zs, 60)   # planet turns one small-step pitch (20 deg)
    js = g.PLANET_SPIN_J
    for ts in steps:
        tp = -ts * g.Zs / g.Zp1
        hit1, gap1 = stage1(ts, js)
        Q2 = rot(P["planet_small"], tp, (A_C, 0)); R = rot(P["ring_space"], tp * g.Zp2 / g.Zr)
        q2, r = near(dens(Q2), (0, 0), 60), near(dens(R), (A_C, 0), 17)
        q2 = q2[np.hypot(q2[:, 0], q2[:, 1]) > 44]
        hit2 = (~inside(R, q2)).sum()
        gap2 = np.min(np.hypot(*(q2[:, None, :] - r[None, :, :]).transpose(2, 0, 1)))
        for k, h, gp in (("sun-big (3 planets)", hit1, gap1), ("small-ring", hit2, gap2)):
            o = res.setdefault(k, [0, 9.0, 0.0]); o[0] += h; o[1] = min(o[1], gp); o[2] = max(o[2], gp)
    for k, (h, lo, hi) in res.items():
        print(f"{k}: interference points {h}, min flank gap over one pitch {lo:.3f} mm (max of per-step min {hi:.3f})")
        assert h == 0 and 0.03 < lo < 0.25


if __name__ == "__main__":
    if "--search" in sys.argv:
        best = []
        ts0 = 0.0
        for j1 in range(18):
            for j2 in range(18):
                hs = sum(stage1(ts, (0, j1, j2))[0] for ts in np.linspace(0, 0.4, 6))
                g_ = min(stage1(ts, (0, j1, j2))[1] for ts in np.linspace(0, 0.4, 6))
                if hs == 0: best.append((j1, j2, round(float(g_), 3)))
        print(best)
    else:
        main()
