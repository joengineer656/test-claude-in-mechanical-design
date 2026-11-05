"""P3a hip gearbox envelope vs the P2 layout (com_layout.py). Left side, world frame (X fwd, Y left, Z up).
Gearbox local frame: z_local = world Y - 40, local angle = -(world XZ angle about the hip axis).
Run: python3 hip_gearbox_envelope.py (asserts the leg clearances that must hold)."""
import io, contextlib, math
import numpy as np
with contextlib.redirect_stdout(io.StringIO()):
    import com_layout as L

H = L.w((0, 0))
EARS_LOCAL = [315, 230, 185, 145, 120]
R_EAR_OUT = 69.0                  # ear centre r 64 + 5
# (y_min, y_max, plain radius, has ears) of the stationary housing sections
SECTIONS = {
    "Al plate 104x104 (axis-aligned square: max x/z = half width 52)": (8.5, 11.5, 52.0, False),
    "skirt flange": (11.5, 15.5, 58.0, False),
    "skirt tube": (15.5, 34.5, 50.4, False),
    "skirt cone + big-planet section": (34.5, 59.5, 60.9, True),
    "skirt lip": (59.5, 61.5, 60.9, True),
    "ring": (59.5, 79.5, 52.1, True),
    "cover": (79.5, 92.0, 52.1, True),
    "output hex (rotating)": (92.0, 99.0, 15.0, False),
}


def housing_r(world_ang_deg, sec):
    y0, y1, r, ears = SECTIONS[sec]
    if ears:
        loc = (-world_ang_deg) % 360
        for e in EARS_LOCAL:
            if abs((loc - e + 180) % 360 - 180) < math.degrees(5 / 64) + 1e-9:
                r = max(r, R_EAR_OUT)
    return r


def leg_clearance(part, yr, rad):
    worst = (1e9, None, None)
    for phi in np.linspace(L.PHI["ext"], L.PHI["crouch"], 240):
        c = L.leg_parts(phi)[0][part][3]
        a, b = c[1], c[2]
        for t in np.linspace(0, 1, 300 if (a != b).any() else 1):
            q = a + t * (b - a); v = q - H
            ang = math.degrees(math.atan2(v[1], v[0]))
            for sec, (y0, y1, _, _) in SECTIONS.items():
                if y0 < yr[1] and yr[0] < y1:
                    d = np.linalg.norm(v) - c[3] - housing_r(ang, sec)
                    if d < worst[0]:
                        worst = (d, sec, round(math.degrees(phi), 1))
    return worst


if __name__ == "__main__":
    print("leg part (Y range) -> min clearance to the stationary hip housing over crouch..extended")
    res = {}
    for part, yr in (("shank", L.Y["shank"]), ("knee joint hw", (L.Y["shank"][0], L.Y["thigh"][1])),
                     ("C joint hw", (L.Y["shank"][0], L.Y["coupler"][1]))):
        d, sec, phi = leg_clearance(part, yr, None)
        res[part] = d
        print(f"  {part:14s} y{yr}: {d:6.1f} mm vs {sec} (thigh {phi} deg)")
    assert res["shank"] > 5.0
    # body box (layout): front x = body_x0 + body_d, top z = body_z0 + body_h
    front, top = L.P["body_x0"] + L.P["body_d"], L.P["body_z0"] + L.P["body_h"]
    for sec, (y0, y1, r, ears) in SECTIONS.items():
        if y1 <= L.P["body_w"] / 2 + 0.01 or y0 < L.P["body_w"] / 2:
            xm = max(H[0] + housing_r(a, sec) * math.cos(math.radians(a)) for a in range(0, 360))
            zm = max(H[1] + housing_r(a, sec) * math.sin(math.radians(a)) for a in range(0, 360))
            print(f"  body box: {sec:34s} y {y0}-{y1}: max x {xm:6.1f} (front {front}), max z {zm:6.1f} (top {top})"
                  + ("  ** EXCEEDS body box" if xm > front or zm > top else ""))
    print(f"  output face (thigh inboard face) at world y = 93.0 (layout thigh starts at {L.Y['thigh'][0]})")
