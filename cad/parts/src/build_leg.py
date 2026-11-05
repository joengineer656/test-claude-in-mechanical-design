"""Generates SolidCraft command scripts for ONE leg (LEFT side, rev 2 refit), emitted in WORLD coordinates (M15). Mirror about world XZ for the right leg.
Run:  python3 build_leg.py OUT.json --parts thigh,coupler,... [--h 195]   (h = hip height above axle; nominal 195, floor 140, max 289)
      python3 build_leg.py --check                                       (numerical clearance table at 140..289)
      solidcraft-cli run OUT.json --save cad/parts/leg.solidcraft --out exports/stl/leg/<part>.stl
Math frame (hip-relative): X = world x - 28 (fwd), Y = world z - 280 (up), Z = world y (lateral, outboard +); Cad class maps to world (X+28, Z, Y+280).
Parts are built at pose h in assembly position (re-orient in the slicer; print orientation in docs/parts/leg.md).
"""
import json, math, sys
import numpy as np

T, S, CP, KC, BEND = 121., 189., 113., 42., 175.
B = np.array([39., 31.])            # rev 2 refit (CoM): hip 10.6 mm ahead of the axle at h195 (rev 1: B 46,30 -> 37.1 mm)
ANCH = np.array([97.4, 70.9])       # rev 2: solved for spring span 154.5 (h140) / 111.0 (h289) -> 43.5 mm stroke, 125 N max
CRANK = 40.
R_HOUSING = 52.1
# rev 2 Y stack (world y): M4 thigh +1, M10 shank face 79 (hub 80.5), M11 coupler 1 mm each side, M12 spring band 104.5..117.5 (axis 111) 2 mm below the arch plate
Y = dict(plate0=65, plate1=71, sh1=79, kpad1=93.5, cpad1=125.5, th0=94, th1=104, stub1=126.5, arch0=119.5, arch1=126.5,
         cp0=127.5, cp1=141.5, strap0=142.5, strap1=148.5, cr0=105, cr1=117)
SPR_Y0, SPR_Y1, SPR_AX = 104.5, 117.5, 111.0
BOW = 14.0
BOLTS = [(94.5, 42.0), (94.5, 66.0), (122.5, 42.0), (122.5, 66.0)]   # C9: world (x, y) of the 4 x M5 through-bolts, 28 x 24 pattern, centred on the 47 x 32 foot
POSTR = 82.0; POSTA = (142, 162)   # arch post radius: outside the housing ears (r 64 + ear radius 5)
U = lambda a: np.array([math.cos(math.radians(a)), math.sin(math.radians(a))])


def bis(f, a, b):
    fa = f(a)
    for _ in range(70):
        m = (a + b) / 2; fm = f(m)
        if fa * fm <= 0: b = m
        else: a, fa = m, fm
    return (a + b) / 2


def pose_th(th):
    K = T * U(th)
    f = lambda s: np.linalg.norm(K + KC * U(s + BEND) - B) - CP
    ss = np.linspace(-180, -60, 481); v = [f(s) for s in ss]
    for i in range(480):
        if v[i] * v[i + 1] < 0:
            s = bis(f, ss[i], ss[i + 1]); break
    else:
        return None
    return dict(th=th, sh=s, K=K, C=K + KC * U(s + BEND), W=K + S * U(s), h=-(K + S * U(s))[1])


def pose_h(h):
    prev = None
    for t in np.linspace(10, -85, 381):
        p = pose_th(t)
        if p is None: continue
        if prev is not None and (prev[0] - h) * (p['h'] - h) <= 0:
            return pose_th(bis(lambda x: pose_th(x)['h'] - h, prev[1], t))
        prev = (p['h'], t)
    raise ValueError("hip height unreachable %s" % h)


def hull(pts):
    pts = sorted(set(map(tuple, np.round(pts, 4))))
    cr = lambda o, a, b: (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def circ(c, r, n=36): return [(c[0] + r * math.cos(2 * math.pi * i / n), c[1] + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def hull_c(*items):
    P = []
    for it in items: P += circ(it[1], it[2]) if it[0] == 'c' else [it[1]]
    return hull(P)


def tf(pts, ang, org):
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    return [(round(org[0] + c * x - s * y, 4), round(org[1] + s * x + c * y, 4)) for x, y in pts]


def rect(x0, y0, x1, y1): return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
def hexpts(af, ang=0): r = af / math.sqrt(3); return [(r * math.cos(math.radians(ang + 60 * k)), r * math.sin(math.radians(ang + 60 * k))) for k in range(6)]


class Cad:
    """Rev 2: emits WORLD coordinates (left leg). Leg frame (X fwd, Y up, Z lateral) -> world (X+28, Z, Y+280); keeps handedness (M15)."""
    def __init__(s): s.C = []
    def cmd(s, c, **p): s.C.append({"command": c, "params": p})
    def poly(s, name, z0, z1, pts, body=None, op="new", targets=None):
        sk = name + "_sk"
        s.cmd("sketch.create", plane={"origin": [0, z1, 0], "x_dir": [1, 0, 0], "y_dir": [0, 0, 1]}, name=sk)   # normal = -y: extrudes from y=z1 down to z0
        s.cmd("sketch.line", points=[[round(float(x) + 28, 3), round(float(y) + 280, 3)] for x, y in pts], closed=True, connect=False)
        s.cmd("sketch.finish")
        p = dict(sketch=sk, distance=z1 - z0, operation=op, name=name)
        if targets: p["targets"] = targets
        if body: p["body_name"] = body
        s.cmd("solid.extrude", **p)
    def cyl(s, name, d, z0, z1, c, body=None, op="new", targets=None):
        p = dict(diameter=d, height=z1 - z0, base=[round(float(c[0]) + 28, 3), z0, round(float(c[1]) + 280, 3)], axis="Y", operation=op, name=name)
        if body: p["body_name"] = body
        if targets: p["targets"] = targets
        s.cmd("solid.cylinder", **p)
    def tube(s, body, do, di, z0, z1, c):
        s.cyl(body + "_o", do, z0, z1, c, body=body); s.cyl(body + "_i", di, z0 - .01, z1 + .01, c, op="cut", targets=[body])
    def box(s, name, x0, y0, z0, lx, ly, lz, body=None, op="new", targets=None):   # leg-frame args: x0,y0(up),z0(lateral), extents lx,ly(up),lz(lateral)
        p = dict(length=lx, width=lz, height=ly, corner=[x0 + 28, z0, y0 + 280], operation=op, name=name)
        if body: p["body_name"] = body
        if targets: p["targets"] = targets
        s.cmd("solid.box", **p)


def geom(p):
    th, sh = p['th'], p['sh']; K, C, W = p['K'], p['C'], p['W']
    G = {}
    G['thigh'] = tf(hull_c(('c', (0, 0), 22), ('p', (73, 26)), ('p', (73, -34)), ('c', (T, 0), 20)), th, (0, 0))
    G['crank'] = tf(hull_c(('c', (0, 0), 17), ('c', (-CRANK, 0), 8)), th, (0, 0))
    G['crank_slot'] = tf(rect(-CRANK - 3, -9, -CRANK + 12, 9), th, (0, 0))
    G['crank_pin'] = tf([(-CRANK, 0)], th, (0, 0))[0]
    loc = lambda s_, t_: tuple(np.round(K + s_ * U(sh) + t_ * U(sh + 90), 4))
    M = loc(94.5, BOW)
    G['sh_a'] = hull_c(('c', tuple(K), 22), ('c', M, 15))
    G['sh_b'] = hull_c(('c', M, 15), ('c', tuple(W), 16))
    G['sh_foot'] = circ(tuple(W), 36, 56)
    G['sh_c'] = hull_c(('c', tuple(K), 22), ('c', tuple(C), 19))   # C3: R19 carries the O36 flange + 4 x M5 on O28
    G['sh_kpad'] = hull_c(('c', tuple(K), 17), ('c', tuple(C), 14))
    G['strap'] = hull_c(('c', tuple(K), 17), ('c', tuple(C), 14))
    d = (C - B) / np.linalg.norm(C - B); n = np.array([-d[1], d[0]])
    G['cp_bar'] = [tuple(B + n * 8), tuple(C + n * 8), tuple(C - n * 8), tuple(B - n * 8)]
    G['cp_eyeB'] = circ(tuple(B), 14, 40); G['cp_eyeC'] = circ(tuple(C), 14, 40)
    p140 = pose_h(140.0)     # end stop engages at the 140 mm floor (A3, M17)
    ct = tf([(73, 26)], p140['th'], (0, 0))[0]
    G['ct'] = ct
    G['pad_rect'] = rect(ct[0] - 5, ct[1], ct[0] + 5, ct[1] + 15)
    G['arch'] = hull_c(('c', (0, 0), 28), ('c', tuple(B), 12), ('p', (ct[0] - 8, ct[1])), ('p', (ct[0] + 8, ct[1])), ('p', (ct[0] - 8, ct[1] + 20)), ('p', (ct[0] + 8, ct[1] + 20)))
    G['arch_up'] = hull_c(('c', (ct[0] - 5, ct[1] + 14), 10), ('c', tuple(ANCH), 10))
    G['arch_tab'] = hull_c(('c', tuple(ANCH), 10), ('p', (ANCH[0] - 14, 87.5)), ('p', (ANCH[0] + 14, 87.5)), ('p', (ANCH[0] - 14, ANCH[1])), ('p', (ANCH[0] + 14, ANCH[1])))   # lug for the box beam end
    G['arch_posts'] = hull_c(('c', (0, 0), 28), ('c', tuple(POSTR * U(POSTA[0])), 12), ('c', tuple(POSTR * U(POSTA[1])), 12))
    return G, p140


def poly_dist(Pa, Pb):
    def dense(P, step=0.5):
        out = []
        for i in range(len(P)):
            a, b = np.array(P[i]), np.array(P[(i + 1) % len(P)]); n = max(2, int(np.linalg.norm(b - a) / step))
            out += [a + (b - a) * k / n for k in range(n)]
        return np.array(out)
    def inside(P, q):
        P = np.array(P); s = 0
        for i in range(len(P)):
            a, b = P[i], P[(i + 1) % len(P)]
            s += (b[0]-a[0])*(q[1]-a[1])-(b[1]-a[1])*(q[0]-a[0]) > 0
        return s == len(P) or s == 0
    A, Bn = dense(Pa), dense(Pb)
    d = np.min(np.linalg.norm(A[::2, None, :] - Bn[None, ::2, :], axis=2))
    return -d if (inside(Pa, Bn[0]) or inside(Pb, A[0])) else float(d)


def check():
    for h in (140, 160, 195, 240, 289):
        p = pose_h(h); G, _ = geom(p)
        sp = np.array([-CRANK * U(p['th']), ANCH]); dv = sp[1] - sp[0]; nn = np.array([-dv[1], dv[0]]) / np.linalg.norm(dv) * 6.5
        spoly = [tuple(sp[0] + nn), tuple(sp[1] + nn), tuple(sp[1] - nn), tuple(sp[0] - nn)]
        ring = circ((0, 0), R_HOUSING, 90)
        shank_ring = min(poly_dist(G[k], ring) for k in ('sh_a', 'sh_b', 'sh_c'))
        bsp = poly_dist(circ(tuple(B), 5, 24), spoly)
        arch_sp = poly_dist(G['arch'], spoly)
        thC = poly_dist(G['thigh'], circ(tuple(p['C']), 10.5, 40)); padsp = poly_dist(G['pad_rect'], spoly)
        print('   thigh-Cpad %.1f  stop pad-spring %.1f' % (thC, padsp))
        cp_k = poly_dist(circ(tuple(p['K']), 5, 24), G['cp_bar'])
        sp_th = poly_dist(G['thigh'], spoly)
        posts = [circ(tuple(POSTR * U(a)), 9, 16) for a in POSTA]
        Wc0 = circ(tuple(p['W']), 85, 90)
        wpost = min(poly_dist(Wc0, q) for q in posts)
        post_sh = min(poly_dist(q, G[k]) for q in posts for k in ('sh_a', 'sh_b', 'sh_c'))
        post_th = min(poly_dist(q, G['thigh']) for q in posts)
        post_cr = min(poly_dist(q, G['crank']) for q in posts)
        Wc = circ(tuple(p['W']), 85, 90)
        wh = {k: poly_dist(Wc, G[k]) for k in ('thigh', 'crank', 'cp_bar', 'cp_eyeC', 'strap', 'sh_kpad', 'arch', 'arch_posts')}
        wh['housing'] = poly_dist(Wc, circ((0, 0), R_HOUSING, 90)); wh['spring'] = poly_dist(Wc, spoly); wh['posts'] = wpost
        print("   wheel R85 (y 80.5..151) in-plane clearance:", {k: round(v, 1) for k, v in wh.items()})
        depth = p['C'][0] + 28 + 14 + 125
        print("h%4d th %7.2f sh %7.2f C(%6.1f,%6.1f) spr %.1f | shank-ring %5.1f Bpin-spring %5.1f arch-spring %5.1f cpl-Kpin %5.1f spring-thigh %5.1f post-shank %5.1f post-thigh %5.1f post-crank %5.1f depth %.0f" % (
            h, p['th'], p['sh'], p['C'][0], p['C'][1], np.linalg.norm(dv), shank_ring, bsp, arch_sp, cp_k, sp_th, post_sh, post_th, post_cr, depth))


def build_part(cad, name, h):
    p = pose_h(h); G, p140 = geom(p); K, C, W = p['K'], p['C'], p['W']; th, sh = p['th'], p['sh']
    y = Y
    if name == "thigh":
        b = "Leg_Thigh"
        cad.poly("th_plate", y['th0'], y['th1'], G['thigh'], body=b)
        cad.poly("th_crank", y['cr0'], y['cr1'], G['crank'], op="join", targets=[b])
        cad.poly("th_slot", SPR_AX - 2, SPR_AX + 2, G['crank_slot'], op="cut", targets=[b])
        cad.cyl("th_crankpin", 5.0, y['cr0'] - 1, y['cr1'] + 1, G['crank_pin'], op="cut", targets=[b])
        cad.poly("th_lug", y['th1'] - .01, 112, tf(rect(66, 16, 80, 26), th, (0, 0)), op="join", targets=[b])   # striker lug for the TPU stop
        cad.cyl("th_stub", 30, y['th1'] - .01, y['stub1'], (0, 0), op="join", targets=[b])
        cad.cyl("th_stubbore", 24, y['th1'], y['stub1'] + .01, (0, 0), op="cut", targets=[b])
        cad.cyl("th_sleeve_pk", 38, y['th0'] - .01, 98, (0, 0), op="cut", targets=[b])   # C5: round O38 x 4 steel sleeve (y 94-98), hex 26.3 A/F broached inside
        cad.cyl("th_relief", 32, 97.9, 100, (0, 0), op="cut", targets=[b])               # relief behind the sleeve (output hex 26 A/F, 30 across corners)
        cad.cyl("th_m4", 9, 99.9, y['th1'] + .01, (0, 0), op="cut", targets=[b])      # gearbox rev 1: ONE central M4 clamp screw (head/washer from the stub bore side)
        cad.cyl("th_kbore", 12, y['th0'] - .01, y['th1'] + .01, tuple(K), op="cut", targets=[b])
        cad.poly("th_chan", y['th0'] - .01, y['th0'] + 3, tf(rect(24, 6, 100, 14), th, (0, 0)), op="cut", targets=[b])
    elif name == "coupler":
        b = "Leg_Coupler"
        cad.poly("cp_bar", y['cp0'], y['cp1'], G['cp_bar'], body=b)
        cad.poly("cp_eB", y['cp0'], y['cp1'], G['cp_eyeB'], op="join", targets=[b])
        cad.poly("cp_eC", y['cp0'], y['cp1'], G['cp_eyeC'], op="join", targets=[b])
        cad.cyl("cp_bB", 14, y['cp0'] - .01, y['cp1'] + .01, tuple(B), op="cut", targets=[b])
        cad.cyl("cp_bC", 14, y['cp0'] - .01, y['cp1'] + .01, tuple(C), op="cut", targets=[b])
    elif name == "shank":
        b = "Leg_Shank"
        cad.poly("sh_a", y['plate1'], y['sh1'], G['sh_a'], body=b)
        cad.poly("sh_b", y['plate1'], y['sh1'], G['sh_b'], op="join", targets=[b])
        cad.poly("sh_c", y['plate1'], y['sh1'], G['sh_c'], op="join", targets=[b])
        cad.poly("sh_foot", y['plate1'], y['sh1'], G['sh_foot'], op="join", targets=[b])
        cad.poly("sh_kpad", y['sh1'] - .01, y['kpad1'], G['sh_kpad'], op="join", targets=[b])
        cad.cyl("sh_kbore", 14, y['sh1'], y['kpad1'] + .01, tuple(K), op="cut", targets=[b])
        cad.cyl("sh_cstand", 21, y['sh1'] - .02, y['kpad1'] + .01, tuple(C), op="cut", targets=[b])   # C3: steel stand-off passes through the K pad
        cad.cyl("sh_cflange", 36, y['sh1'] - .02, y['sh1'] + 4, tuple(C), op="cut", targets=[b])
        for k in range(4):
            cad.cyl(f"sh_cm5{k}", 5.5, y['plate1'] - .01, y['sh1'] + 4, tuple(C + 14 * U(sh + 45 + 90 * k)), op="cut", targets=[b])
        cad.cyl("sh_axle", 38.2, y['plate1'] - .01, y['sh1'] + .01, tuple(W), op="cut", targets=[b])   # wheel axle neck D38 (wheel.md)
        for k in range(4):
            cad.cyl(f"sh_cb{k}", 4.5, y['plate1'] - .01, y['sh1'] + .01, tuple(W + 23 * U(45 + 90 * k)), op="cut", targets=[b])
        cad.poly("sh_chan", 76, y['sh1'] + .01, tf(rect(40, -5, 140, 5), sh, tuple(K)), op="cut", targets=[b])
    elif name == "plate":
        b = "Leg_ShankPlate"
        cad.poly("pl_a", y['plate0'], y['plate1'], G['sh_a'], body=b)
        cad.poly("pl_b", y['plate0'], y['plate1'], G['sh_b'], op="join", targets=[b])
        cad.poly("pl_c", y['plate0'], y['plate1'], G['sh_c'], op="join", targets=[b])
        cad.poly("pl_f", y['plate0'], y['plate1'], G['sh_foot'], op="join", targets=[b])
        for k in range(4):
            cad.cyl(f"pl_cm5{k}", 5.5, y['plate0'] - .01, y['plate1'] + .01, tuple(C + 14 * U(sh + 45 + 90 * k)), op="cut", targets=[b])
        cad.cyl("pl_ax", 38.2, y['plate0'] - .01, y['plate1'] + .01, tuple(W), op="cut", targets=[b])
        for k in range(4):
            cad.cyl(f"pl_cb{k}", 4.5, y['plate0'] - .01, y['plate1'] + .01, tuple(W + 23 * U(45 + 90 * k)), op="cut", targets=[b])
    elif name == "strap":
        b = "Leg_KneeStrap"
        cad.poly("st", y['strap0'], y['strap1'], G['strap'], body=b)
        cad.cyl("st_k", 14, y['strap0'] - .01, y['strap1'] + .01, tuple(K), op="cut", targets=[b])
        cad.cyl("st_c", 14, y['strap0'] - .01, y['strap1'] + .01, tuple(C), op="cut", targets=[b])
    elif name == "arch":
        b = "Leg_ArchPlate"
        cad.poly("ar_a", y['arch0'], y['arch1'], G['arch'], body=b)
        cad.poly("ar_u", y['arch0'], y['arch1'], G['arch_up'], op="join", targets=[b])
        cad.poly("ar_p", y['arch0'], y['arch1'], G['arch_posts'], op="join", targets=[b])
        cad.poly("ar_t", y['arch0'], y['arch1'], G['arch_tab'], op="join", targets=[b])   # lug that carries the beam end (M7)
        cad.cyl("ar_brg", 42, y['arch0'] - .01, y['arch1'] + .01, (0, 0), op="cut", targets=[b])
        cad.cyl("ar_B", 10, y['arch0'] - .01, y['arch1'] + .01, tuple(B), op="cut", targets=[b])
        cad.cyl("ar_anch", 5, y['arch0'] - .01, y['arch1'] + .01, tuple(ANCH), op="cut", targets=[b])
        for a in POSTA:
            cad.cyl(f"ar_post{a}", 18, y['arch0'] - .01, y['arch1'] + .01, tuple(POSTR * U(a)), op="cut", targets=[b])
    elif name == "beam":      # rev 2 (M7): 6061 BOX beam 40 (x) x 8.5 (up) x 2 wall, lateral y 52..119.5, abuts the arch-plate lug; solid 6 mm foot plate on the body (y 38..52)
        b = "Leg_OutriggerBeam"
        cad.box("bm_a", 57, 79, 38, 47, 6, 32, body=b)                         # C9: foot 47 x 32 (lateral y 38-70)
        cad.box("bm_r", 77, 79, 51.9, 40, 8.5, 18.2, op="join", targets=[b])   # 8.5 root stub on the foot (the Body shelf is below z 359 there)
        cad.box("bm_b", 77, 75.5, 69.9, 40, 12, 49.6, op="join", targets=[b])  # C9: 12 high box beam, Y 75.5-87.5
        cad.box("bm_bi", 79, 77.5, 70, 36, 8, 49.7, op="cut", targets=[b])     # 2 mm walls
        cad.box("bm_sp", 83, 75.4, 103.5, 28, 2.2, 16, op="cut", targets=[b])  # spring relief in the bottom wall (envelope reaches Y 77.4)
        for i, (bx, by) in enumerate(BOLTS):
            cad.cmd("solid.cylinder", diameter=5.5, height=8, base=[bx, by, 358.5], axis="Z", operation="cut", targets=[b], name=f"bm_h{i}")
    elif name == "cstand":      # C3: S355 stand-off O21 y 79-125.5, O36 x 4 flange, 4 x M5 on O28 (through shank), bush O14 x 12 pressed in
        b = "Leg_CStandoff"
        cad.cyl("cs_o", 21, y['sh1'], y['cpad1'], tuple(C), body=b)
        cad.cyl("cs_f", 36, y['sh1'], y['sh1'] + 4, tuple(C), op="join", targets=[b])
        cad.cyl("cs_bore", 14, y['cpad1'] - 12, y['cpad1'] + .01, tuple(C), op="cut", targets=[b])
        for k in range(4):
            cad.cyl(f"cs_m5{k}", 5.5, y['sh1'] - .01, y['sh1'] + 4.01, tuple(C + 14 * U(sh + 45 + 90 * k)), op="cut", targets=[b])
    elif name == "bplate":      # C9: 3 mm Al backing plate under the Body shelf (world z 350-353), 4 x M5
        b = "Leg_BeamBackplate"
        cad.box("bp_a", 60, 70, 40, 41, 3, 28, body=b)
        for i, (bx, by) in enumerate(BOLTS):
            cad.cmd("solid.cylinder", diameter=5.5, height=8, base=[bx, by, 349.5], axis="Z", operation="cut", targets=[b], name=f"bp_h{i}")
    elif name == "tpu":
        cad.poly("pad", 109.5, 119.5, G['pad_rect'], body="Leg_StopPad_TPU")
        cad.cyl("bump1", 10, 97.5, 103.5, tf([(60, 26)], th, (0, 0))[0], body="Leg_Bumper_Thigh_TPU")
        cad.cyl("bump2", 10, 74, 80, tuple(K + 70 * U(sh)), body="Leg_Bumper_Shank_TPU")
        cad.cyl("bump3", 6, y['cpad1'] + .1, y['cp0'] - .1, tuple(C), body="Leg_Dot_TPU")
    elif name == "hw":
        for nm, c, z0, z1 in (("Leg_Pin_K", K, 80, 149), ("Leg_Pin_C", C, 113.5, 149), ("Leg_Pin_B", B, 119.5, 149)):
            cad.cyl(nm, 10, z0, z1, tuple(c), body=nm)
        cad.cyl("Leg_Pin_Crank", 5, 105, 117, tf([(-CRANK, 0)], th, (0, 0))[0], body="Leg_Pin_Crank")
        cad.cyl("Leg_Pin_Anchor", 5, 105, 119.5, tuple(ANCH), body="Leg_Pin_Anchor")
        for nm, c, z0, z1 in (("Leg_Bush_K_shank", K, 81.5, 93.5), ("Leg_Bush_K_thigh", K, 94, 104), ("Leg_Bush_K_strap", K, 142.5, 148.5),
                              ("Leg_Bush_C_shank", C, 113.5, 125.5), ("Leg_Bush_C_coupler", C, 127.5, 141.5), ("Leg_Bush_C_strap", C, 142.5, 148.5),
                              ("Leg_Bush_B_coupler", B, 127.5, 141.5)):
            cad.tube(nm, 12 if nm == "Leg_Bush_K_thigh" else 14, 10, z0, z1, tuple(c))   # C4: thigh bush DU-type 10x12x10
        cad.tube("Leg_Brg_6806_outer", 42, 30, 119.5, 126.5, (0, 0))
        cad.tube("Leg_Spacer_K", 14, 10, 104.2, 142.3, tuple(K))
        cad.cyl("Leg_HexSleeve", 38, 94, 98, (0, 0), body="Leg_HexSleeve")   # C5: round-OD O38 x 4 steel insert
        cad.poly("Leg_HexSleeve_i", 93.99, 98.01, tf(hexpts(26.3, 0), th, (0, 0)), op="cut", targets=["Leg_HexSleeve"])
        a0 = np.array(tf([(-CRANK, 0)], th, (0, 0))[0]); v = ANCH - a0; n = np.array([-v[1], v[0]]) / np.linalg.norm(v) * 6.5
        cad.poly("Leg_Spring_env", SPR_Y0, SPR_Y1, [tuple(a0 + n), tuple(ANCH + n), tuple(ANCH - n), tuple(a0 - n)], body="Leg_Spring_env")
    elif name == "posts":
        for a in POSTA:
            cad.tube(f"Leg_ArchPost_{a}", 18, 12, 40, y['arch0'], tuple(POSTR * U(a)))   # 16 x 3 steel tube
    elif name == "refs":
        cad.cyl("ref_ring", 2 * R_HOUSING, 59.5, 93.5, (0, 0), body="REF_HipHousing")
        cad.cyl("ref_skirt", 122, 40, 59.5, (0, 0), body="REF_HipSkirt")
        cad.cyl("ref_wheel", 170, 80.5, 151, tuple(W), body="REF_Wheel")
    else:
        raise SystemExit("unknown part " + name)


if __name__ == "__main__":
    if "--check" in sys.argv: check(); sys.exit()
    out = sys.argv[1]; parts = sys.argv[sys.argv.index("--parts") + 1].split(",")
    h = float(sys.argv[sys.argv.index("--h") + 1]) if "--h" in sys.argv else 195.0
    cad = Cad()
    for pt in parts: build_part(cad, pt, h)
    json.dump({"commands": cad.C}, open(out, "w")); print(len(cad.C), "commands")
