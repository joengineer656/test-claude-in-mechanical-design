"""Rev 2 formal structural check of the leg (A1-A11): arch plate/posts/beam, knee+C pins, shank dog-leg, C pad, hex sleeve, body ties.
Hand calc, in-plane rigid-body statics from the real 4-bar geometry (cad/parts/src/build_leg.py). Not FEA.
Run: python3 structural_leg_rev2.py > structural_leg_rev2_output.txt
shortcut: quasi-static, loads from theory.md 6.4/6.9 kg re-run (vertical ground force; slide add-on mu=0.8 in-plane), printed parts isotropic
in-plane, Kt from handbook lug charts; upgrade with FEA on the arch plate and shank."""
import sys, math, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "cad", "parts", "src"))
import build_leg as L
pi = math.pi
U = L.U
# ---- allowables (materials_gears.md A9/A10 derates, 50 C) ----
PAHT = 65 * 0.9 * 0.7        # 40.95 MPa in-plane
PETG = 34 * 0.75 * 0.7       # 17.85
IL = 0.4                     # interlayer (Z) factor, structural.md rev 1
AL_Y, ST_Y, PIN_Y = 240., 355., 1100.
E_AL, E_PA, G_AL, G_PA = 69000., 5000., 26000., 1900.
SF_MIN = 1.5
def sf(a, s): return a / s if s > 0 else 99.
# ---- loads, theory.md "Re-run at CAD mass": knee pin LC-A/C/B/D, axle N, hip height used for the pose ----
LC = {  # name: (axle N @6.4, knee pin @6.4, knee pin @6.9, hip height h)
    'A': (210, 490, 530, 210), 'C': (266, 810, 820, 205), 'B': (324, 1540, 1680, 140), 'D': (456, 2640, 2810, 140)}
SPR = 180.      # spring design load at the anchor / crank
MU = 0.8

def leg_statics(h, Wv, Tw=0.):
    """Shank free body: ground/axle force Wv=(fx,fz) at W, coupler force along C-B, K force = remainder. Returns F_C vec, F_K vec (on shank)."""
    p = L.pose_h(h); K, C, W, B = p['K'], p['C'], p['W'], L.B
    d = (B - C) / np.linalg.norm(B - C)            # coupler line, force on shank at C = s*d (s<0 means push)
    cross = lambda a, b: a[0] * b[1] - a[1] * b[0]
    # moment about K: (W-K)x Fw + (C-K)x (s d) = 0
    Fw = np.array(Wv, float)
    s = -(cross(W - K, Fw) + Tw) / cross(C - K, d)
    Fc = s * d; Fk = -(Fw + Fc)
    return p, Fw, Fc, Fk

print("== 0. Load table and consistency of the 4-bar statics (vertical axle force only) ==")
print("LC  h    axle N  FK(statics)  FK(theory 6.4)  FC(statics)  ratio theory/statics")
SC = {}
for k, (ax, fk64, fk69, h) in LC.items():
    p, Fw, Fc, Fk = leg_statics(h, (0, ax))
    r = fk64 / np.linalg.norm(Fk)
    SC[k] = r
    print(f"{k}  {h:3d}  {ax:5d}   {np.linalg.norm(Fk):8.0f}     {fk64:8d}      {np.linalg.norm(Fc):8.0f}      {r:5.2f}")
print("(ratio >1: theory includes leg-link inertia/spring/horizontal parts not in a vertical-only static; loads below use the THEORY knee pin value and scale the statics vectors to it)")

def case_vectors(k, mass, slide=0., Tw=0.):
    """Return pose, Fw, Fc, Fk scaled so |Fk| = theory knee pin for the mass (conservative scale applied to all three)."""
    ax, f64, f69, h = LC[k]; fk = f64 if mass == 6.4 else f69
    p, Fw0, Fc0, Fk0 = leg_statics(h, (0, ax))
    s = fk / np.linalg.norm(Fk0)
    p, Fw, Fc, Fk = leg_statics(h, (slide * ax, ax), Tw)      # slide: horizontal ground force mu*axle (+-), Tw: wheel reaction torque Nmm
    return p, Fw * s, Fc * s, Fk * s


# ======================================================================================
print("\n== 2. Knee pin K (D10, 42CrMo4 12.9, yield 1100), thigh bush, thigh knee boss ==")
yK = dict(pad=87.5, thigh=99.0, strap=145.5)       # bush centres (shank bush 81.5-93.5, thigh 94-104, strap 142.5-148.5)
d = 10.
def pin_bend(F, ya, yl, yb):
    Ra = F * (yb - yl) / (yb - ya); Rb = F - Ra
    return Ra, Rb, Ra * (yl - ya)           # M in N mm
print("mass LC  FK kN | pad/strap N  M Nm  sigma  SF pin | SF pin if strap cannot take the transverse part (cantilever from pad) | bush p MPa (SF vs 28 sintered bronze static) | thigh boss R17 net sect. MPa SF PAHT")
ST_ = {}
for mass in (6.4, 6.9):
    for k in LC:
        p, Fw, Fc, Fk = case_vectors(k, mass)
        F = np.linalg.norm(Fk)
        Ra, Rb, M = pin_bend(F, yK['pad'], yK['thigh'], yK['strap'])
        sg = 32 * M / (pi * d ** 3); sg2 = 32 * F * (yK['thigh'] - yK['pad']) / (pi * d ** 3)
        pb = F / (10 * 10); sn = F / (2 * 10 * 10) * 2.2
        ST_[(mass, k)] = F
        print(f"{mass} {k}  {F/1000:5.2f} | {Ra:5.0f}/{Rb:4.0f} {M/1000:5.1f} {sg:5.0f} {sf(PIN_Y, sg):5.2f} | {sf(PIN_Y, sg2):5.2f} | p={pb:5.1f} SF={sf(28, pb):4.2f} | {sn:5.1f} SF={sf(PAHT, sn):4.2f}")
for F in (2000, 2640):
    print(f"pin at {F} N: sigma {32*pin_bend(F,87.5,99,145.5)[2]/(pi*d**3):.0f} MPa; cantilever bound {32*F*11.5/(pi*d**3):.0f} MPa")

# ======================================================================================
print("\n== 3. Shank dog-leg and C pad ==")
def arm_geometry(h):
    p = L.pose_h(h); K, W, sh = p['K'], p['W'], p['sh']
    M = K + 94.5 * U(sh) + L.BOW * U(sh + 90)
    return p, K, M, W
def width_at(s_frac_seg, seg):
    # seg 0: K(R22)->M(R15); seg 1: M(R15)->W(R16)  (hull widths)
    return (44 + (30 - 44) * s_frac_seg) if seg == 0 else (30 + (32 - 30) * s_frac_seg)
TAL = 3.0   # Al shank plate thickness (mm), y (71-TAL)..71; PAHT 71..79
def section(w, notch=True):
    """strips (y0,y1,width,E,G) for Al 3 mm + PAHT 8 mm (10x3 phase channel on the outboard face where the arm runs)."""
    return w
def props(w, notch):
    # in-plane (axis out of plane): EI_in, EA ; out-of-plane via strips about the transformed NA
    nw = 10. if notch else 0.
    EA = E_AL * TAL * w + E_PA * (8 * w - 3 * nw)
    EIin = E_AL * TAL * w ** 3 / 12 + E_PA * (8 * w ** 3 / 12 - 3 * nw ** 3 / 12)
    ys = np.arange(71 - TAL + 0.05, 79, 0.1)
    bw = np.array([w if y < 76 or not notch else w - nw for y in ys]); Ee = np.array([E_AL if y < 71 else E_PA for y in ys])
    ya = np.sum(Ee * bw * ys) / np.sum(Ee * bw)
    EIoop = np.sum(Ee * bw * (ys - ya) ** 2) * 0.1
    cmax = max(ya - 68, 79 - ya)
    # torsion: thin rectangles, G share
    Gs = np.array([G_AL if y < 71 else G_PA for y in ys]); y0 = np.sum(Gs * ys) / np.sum(Gs)
    GJ = 2 * np.sum(Gs * bw * (ys - y0) ** 2) * 0.1 * 0.97     # bonded laminate, thin-plate torsion tau = 2 G theta (y-y0)
    return dict(EA=EA, EIin=EIin, EIoop=EIoop, ya=ya, GJ=GJ, y0=y0)
Y_LOAD, Y_MID = 115.75, 73.5
def shank_stress(h, F2, Fy, Tw, bow=True):
    """Free body from the foot: in-plane force F2=(fx,fz) at W, lateral Fy, wheel reaction torque Tw (Nmm about y). Stations along the arm centreline."""
    p, K, M, W = arm_geometry(h)
    pts = [(K, M, 0), (M, W, 1)]
    if not bow:     # straight K->W reference arm
        pts = [(K, W, 0)]
    out = []
    stations = [0.1, 0.35, 0.65, 0.9] if bow else [0.1, 0.35, 0.65, 0.9]
    for a, b, seg in pts:
        for f in (stations if bow else stations):
            P = a + f * (b - a); t = (a - b) / np.linalg.norm(a - b)   # tangent pointing foot->K... section outward normal
            n = np.array([-t[1], t[0]])
            r = np.array([W[0] - P[0], W[1] - P[1], Y_LOAD - Y_MID])   # (x, z, y)
            Fv = np.array([F2[0], F2[1], Fy])
            rg = r - np.array([0, 85., 0])                                     # lateral force acts at the tyre contact, 85 mm below the axle
            Mv = np.cross(r, np.array([F2[0], F2[1], 0.])) + np.cross(rg, np.array([0, 0, Fy]))   # components (x,z,y)
            Mv_y = Mv[2] + Tw / 1.0                                            # about the out-of-plane axis (in-plane bending), N mm
            Mxz = np.array([Mv[0], Mv[1]])
            Mt = Mxz @ t; Mn = Mxz @ n                                         # torsion about arm axis, out-of-plane bending
            Nax = -(np.array(F2) @ t)                                          # axial (compression positive when foot pushes up the arm)
            Vin = np.array(F2) @ n; Vy = Fy
            w = width_at(f if bow else f, seg) if bow else 44 + (32 - 44) * f
            pr = props(w, notch=(np.linalg.norm(P - K) > 40))
            # stresses
            sig_in_al = E_AL * Mv_y * (w / 2) / pr['EIin']; sig_in_pa = E_PA * Mv_y * (w / 2) / pr['EIin']
            sig_ax_al = E_AL * Nax / pr['EA']; sig_ax_pa = E_PA * Nax / pr['EA']
            sig_o_al = E_AL * Mn * max(pr['ya'] - (71 - TAL), 0) / pr['EIoop']
            sig_o_pa = E_PA * Mn * (79 - pr['ya']) / pr['EIoop']
            sig_o_pa_in = E_PA * Mn * (71 - pr['ya']) / pr['EIoop']
            th_ = Mt / pr['GJ']; tau_al = abs(2 * G_AL * th_ * max(abs(71 - TAL - pr['y0']), abs(71 - pr['y0']))); tau_pa = abs(2 * G_PA * th_ * max(abs(71 - pr['y0']), abs(79 - pr['y0'])))
            s_al = abs(sig_in_al) + abs(sig_ax_al) + abs(sig_o_al); s_pa = abs(sig_in_pa) + abs(sig_ax_pa) + abs(sig_o_pa)
            out.append(dict(s=np.linalg.norm(P - K), w=w, Min=Mv_y, Mt=Mt, Mn=Mn, s_al=s_al, s_pa=s_pa, tau_al=tau_al, tau_pa=tau_pa,
                            vm_al=math.sqrt(s_al ** 2 + 3 * tau_al ** 2), vm_pa=math.sqrt(s_pa ** 2 + 3 * tau_pa ** 2), in_pa=abs(sig_in_pa)))
    return out
print("Arm = 8 mm PAHT-CF (71-79, 10x3 phase channel) + 3 mm 6061 plate (68-71) bonded; ground load plane y 115.75, section mid-plane y 73.5; stresses = |in-plane| + |axial| + |out-of-plane| (worst fibre).")
print("case              dist from K | w | Min Nm Mt Nm Mn Nm | Al MPa (SF/240) | PAHT MPa (SF/41 ; SF PETG/17.9)  | tau Al, PAHT")
WORST = {}
for mass in (6.4, 6.9):
    for k, sl, fy, tw, tag in (('D', 0., 0., 0., 'vertical'), ('D', 0.8, 0., 9200., 'slide +x, wheel torque 9.2 Nm'), ('D', -0.8, 0., -9200., 'slide -x'),
                               ('D', 0., 0.8, 0., 'lateral slide Fy=0.8Fax'), ('C', 0.8, 0.8, 9200., 'LC-C slide + lateral'), ('B', 0., 0., 0., 'vertical')):
        ax = LC[k][0] * (LC[k][2] / LC[k][1] if mass == 6.9 else 1)
        p, Fw, Fc, Fk = case_vectors(k, mass, sl, tw)
        r = shank_stress(LC[k][3], (Fw[0], Fw[1]), fy * Fw[1] if fy else 0., tw, bow=True)
        mx = max(r, key=lambda q: q['s_pa'] / 41 + q['s_al'] / 240)
        WORST[(mass, k, tag)] = mx
        print(f"{mass} {k} {tag:30s} s={mx['s']:5.0f} w={mx['w']:4.1f} | {mx['Min']/1000:5.1f} {mx['Mt']/1000:5.1f} {mx['Mn']/1000:5.1f} | Al {mx['s_al']:5.0f} SF {sf(AL_Y, mx['vm_al']):4.2f} | PAHT {mx['s_pa']:5.1f} SF {sf(PAHT, mx['vm_pa']):4.2f} (PETG {sf(PETG, mx['vm_pa']):4.2f}) | {mx['tau_al']:4.1f} {mx['tau_pa']:4.1f}")
# dog-leg effect: in-plane moment, bowed vs straight arm
for k in ('D',):
    p, Fw, Fc, Fk = case_vectors(k, 6.4)
    rb = shank_stress(140, (Fw[0], Fw[1]), 0., 0., True); rs = shank_stress(140, (Fw[0], Fw[1]), 0., 0., False)
    print("dog-leg effect LC-D in-plane M at stations (Nm), bowed:", [round(q['Min'] / 1000, 1) for q in rb], " straight:", [round(q['Min'] / 1000, 1) for q in rs])

print("\nShank plate thickness study (6.4 kg, LC-D): worst section, SF = allowable / von-Mises-type combined stress")
for tal in (3., 4., 5., 6.):
    TAL = tal
    row = []
    for tag, sl, fy, tw in (('vert', 0., 0., 0.), ('slide-x', -0.8, 0., -9200.), ('lat', 0., 0.8, 0.)):
        p, Fw, Fc, Fk = case_vectors('D', 6.4, sl, tw)
        r = shank_stress(140, (Fw[0], Fw[1]), fy * Fw[1] if fy else 0., tw, True)
        mx = max(r, key=lambda q: q['s_pa'] / 41 + q['s_al'] / 240)
        row.append(f"{tag}: Al {sf(AL_Y, mx['vm_al']):.2f} PAHT {sf(PAHT, mx['vm_pa']):.2f}")
    print(f"Al plate {tal:.0f} mm | " + " | ".join(row))
TAL = 3.0
print("\nPlate study, LC-C controlled with slide + lateral (S6 on S3), 6.4 kg, and LC-D vertical at 6.9 kg")
for tal in (3., 5., 6., 8.):
    TAL = tal
    out = []
    for k, mass, sl, fy, tw in (('C', 6.4, 0.8, 0.8, 9200.), ('C', 6.4, -0.8, 0., -9200.), ('D', 6.9, 0., 0., 0.)):
        p, Fw, Fc, Fk = case_vectors(k, mass, sl, tw)
        r = shank_stress(LC[k][3], (Fw[0], Fw[1]), fy * Fw[1] if fy else 0., tw, True)
        mx = max(r, key=lambda q: q['s_pa'] / 41 + q['s_al'] / 240)
        out.append(f"{k}{mass} sl{sl} fy{fy}: Al {sf(AL_Y, mx['vm_al']):.2f} PAHT {sf(PAHT, mx['vm_pa']):.2f}")
    print(f"Al plate {tal:.0f} mm | " + " | ".join(out))
TAL = 3.0

# ---- C pad: printed column R10.5 from y 79 to the bush centre y 119.5 ----
# The strap is pinned to the shank at K and C only: it can carry only a force pair ALONG the K-C line. So the pad takes the
# transverse component of F_C in full and 0.42 of the axial component (pin-C reaction split 0.42 pad / 0.58 strap).
print("\n== 3b. C pad (R10.5 column y 79-113.5, bush 113.5-125.5, Ø14 bush -> 3.5 mm wall) ==")
ZC = pi * 21 ** 3 / 32
yC = dict(pad=119.5, cp=134.5, strap=145.5)
shr = (yC['strap'] - yC['cp']) / (yC['strap'] - yC['pad'])
def cpad_load(k, mass, **kw):
    p, Fw, Fc, Fk = case_vectors(k, mass, **kw)
    kc = (p['C'] - p['K']) / np.linalg.norm(p['C'] - p['K']); Fa = Fc @ kc; Ft = Fc[0] * -kc[1] + Fc[1] * kc[0]
    return np.linalg.norm(Fc), math.hypot(Ft, shr * Fa), Fa, Ft
print("mass LC  FC N (axial/transverse to K-C) | pad load N | root bending MPa | SF PAHT in-plane | SF across layers (x0.4) | bush wall net section MPa SF")
CP = {}
for mass in (6.4, 6.9):
    for k in LC:
        F, P, Fa, Ft = cpad_load(k, mass); M = P * (yC['pad'] - 79); sg = M / ZC; sw = P / (2 * 3.5 * 12) * 2.6
        CP[(mass, k)] = (P, sg, sw)
        print(f"{mass} {k} {F:6.0f} ({Fa:6.0f}/{Ft:6.0f}) | {P:5.0f} | {sg:6.1f} | {sf(PAHT, sg):5.2f} | {sf(PAHT*IL, sg):5.2f} | {sw:5.1f} {sf(PAHT, sw):4.2f}")
P = CP[(6.4, 'D')][0]
for lab, al in (('in-plane layers', PAHT), ('across layers x0.4', PAHT * IL)):
    print(f"R needed for SF 1.5 at 6.4 kg LC-D ({lab}): {(32*P*40.5*SF_MIN/(pi*al))**(1/3)/2:.1f} mm radius for a printed column (now 10.5, no room: thigh clearance 4.2 mm)")
sg_s = P * 40.5 / ZC
print(f"Steel S355 stand-off Ø21 (y 79-125.5, bush pressed in, Ø36 flange, 4 x M4): bending {sg_s:.0f} MPa SF {sf(ST_Y, sg_s):.2f}; 6061 {sf(AL_Y, sg_s):.2f}")
M_ = P * 40.5; T_b = M_ / (2 * 14 * 0.9)
print(f"   root moment {M_/1000:.0f} Nm on a Ø28 bolt circle, 4 x M4: bolt tension {T_b:.0f} N each (M4 8.8 proof ~ 5 kN): SF {5000/T_b:.1f}; 3 mm Al plate pull-through shear {T_b/(pi*8*3):.0f} MPa")
# K pad (thigh pin reaction into the shank), lug net section R17 vs Ø14 bush, 12 mm bush, Kt 2.2
print("K pad lug (R17, bush 12 long, pad share 0.80 of F_K):")
for mass in (6.4, 6.9):
    F = ST_[(mass, 'D')]; sn = 0.80 * F / (2 * 10 * 12) * 2.2
    print(f"   {mass} kg LC-D F_K {F:.0f}: net section {sn:.1f} MPa SF PAHT {sf(PAHT, sn):.2f}; across layers n/a (in-plane load)")

# ======================================================================================
print("\n== 1. Arch plate + posts + 6061 box beam (rigid-plate share model, 2D in the leg plane) ==")
# supports: post 1 (r82,142), post 2 (r82,162): Ø16x3 steel cantilever L=79.5 (y 40 -> 119.5); beam tip at the lug x~97, up 83: 40x8.5x2 box, cantilever 67.6 (y 52 -> 119.5)
Ls = 79.5; Ip = pi / 64 * (16 ** 4 - 10 ** 4); kp = 3 * 200000 * Ip / Ls ** 3
Lb = 67.6; Ibx = (8.5 * 40 ** 3 - 4.5 * 36 ** 3) / 12; Ibz = (40 * 8.5 ** 3 - 36 * 4.5 ** 3) / 12
kbx = 3 * 69000 * Ibx / Lb ** 3; kbz = 3 * 69000 * Ibz / Lb ** 3
Zp = Ip / 8; Zbz = Ibz / 4.25; Zbx = Ibx / 20
print(f"post k = {kp:.0f} N/mm each (cantilever, conservative: no end-rotation restraint); beam kx {kbx:.0f}, kz {kbz:.0f} N/mm (rigid root); post Z {Zp:.0f} mm3; beam Zz {Zbz:.0f}, Zx {Zbx:.0f} mm3")
sup = [(L.POSTR * U(142), kp, kp), (L.POSTR * U(162), kp, kp), (np.array([97.0, 83.0]), kbx, kbz)]
def arch_solve(loads):
    """loads: list of (pos, force vec). Rigid plate: translation u, rotation th. Returns reactions on the plate supports (force the support exerts) """
    A = np.zeros((3, 3)); b = np.zeros(3)
    for pos, kx, kz in sup:
        G = np.array([[1, 0, -pos[1]], [0, 1, pos[0]]]); Kk = np.diag([kx, kz]); A += G.T @ Kk @ G
    for pos, F in loads:
        b += np.array([F[0], F[1], pos[0] * F[1] - pos[1] * F[0]])
    u = np.linalg.solve(A, b)
    R = []
    for pos, kx, kz in sup:
        G = np.array([[1, 0, -pos[1]], [0, 1, pos[0]]]); R.append(np.diag([kx, kz]) @ G @ u)   # support force on plate is -R; magnitude R
    return R
def arch_loads(k, mass, spring=SPR, r2mode='A'):
    p, Fw, Fc, Fk = case_vectors(k, mass)
    FB = -Fc                                                   # coupler pulls the B pin with minus the force it applies to the shank
    Fkt = -Fk                                                  # thigh load at K (force of shank on thigh)
    Ft = np.linalg.norm(Fkt)
    yh = 87.5 if r2mode == 'A' else 96.0
    R1 = (Ft * (121.0 - 99.0) + spring * (121.0 - 110.0)) / (121.0 - yh); R2 = Ft + spring - R1
    r2dir = Fkt / Ft
    a0 = (-L.CRANK) * U(p['th']); sp = (L.ANCH - a0) / np.linalg.norm(L.ANCH - a0)
    loads = [(L.B, FB), (np.zeros(2), R2 * r2dir), (L.ANCH, spring * sp)]
    return p, loads, R2, np.linalg.norm(FB)
print("\nmass LC  |FB| N  R2 N (ideal A / sleeve B)  | post reactions N (P1,P2)  moment Nm@base  sigma MPa  SF S355 | beam tip N (x,z)  M_z-weak Nm  sigma MPa  SF 6061")
AR = {}
for mass in (6.4, 6.9):
    for k in LC:
        p, loads, R2, FBm = arch_loads(k, mass)
        R = arch_solve(loads); R2b = arch_loads(k, mass, r2mode='B')[2]
        Pm = [np.linalg.norm(R[0]), np.linalg.norm(R[1])]; Mb = Pm[0] * Ls / 1000; sg = Mb * 1000 / Zp
        bx, bz = R[2]; Mz = abs(bz) * Lb; Mx = abs(bx) * Lb
        sgb = Mz / Zbz + Mx / Zbx
        AR[(mass, k)] = (R, Pm, sg, sgb, R2, FBm)
        print(f"{mass} {k}  {FBm:5.0f}  {R2:5.0f}/{R2b:4.0f} | {Pm[0]:5.0f} {Pm[1]:5.0f}   {max(Pm)*Ls/1000:5.1f}  {max(sg for sg in [max(Pm)*Ls/Zp]):6.0f} {sf(ST_Y, max(Pm)*Ls/Zp):5.2f} | ({bx:5.0f},{bz:5.0f})  {(abs(bz)*Lb)/1000:5.1f}  {sgb:5.0f} {sf(AL_Y, sgb):5.2f}")
# worst direction sweep for the B-pin force (+-45 deg) at LC-D 6.4 / 6.9
print("\nsweep: B-pin force direction +-60 deg about the computed one, LC-D (worst post bending, beam stress)")
for mass in (6.4, 6.9):
    p, loads, R2, FBm = arch_loads('D', mass); worst_p = 0; worst_b = 0; worst_bz = 0
    for da in range(-60, 61, 10):
        c, s_ = math.cos(math.radians(da)), math.sin(math.radians(da))
        Fb = loads[0][1]; Fb2 = np.array([c * Fb[0] - s_ * Fb[1], s_ * Fb[0] + c * Fb[1]])
        R = arch_solve([(L.B, Fb2)] + loads[1:]); Pm = max(np.linalg.norm(R[0]), np.linalg.norm(R[1]))
        sgb = abs(R[2][1]) * Lb / Zbz + abs(R[2][0]) * Lb / Zbx
        worst_p = max(worst_p, Pm); worst_b = max(worst_b, sgb); worst_bz = max(worst_bz, abs(R[2][1]))
    print(f"{mass} kg: post shear max {worst_p:.0f} N -> sigma {worst_p*Ls/Zp:.0f} MPa SF(S355) {sf(ST_Y, worst_p*Ls/Zp):.2f}; beam {worst_b:.0f} MPa SF {sf(AL_Y, worst_b):.2f}; beam z-force {worst_bz:.0f} N, root moment {worst_bz*Lb/1000:.0f} Nm")

# ---- arch plate local checks ----
print("\n== 1b. Arch plate local sections (6061, 7 mm), B pin, bearing ring, body-side post collar ==")
for mass in (6.4, 6.9):
    R, Pm, sg, sgb, R2, FB = AR[(mass, 'D')]
    # B pin Ø10 cantilever from the plate outer face 126.5, coupler centre y 134.5 (conservative lever from plate mid 123)
    Mpin = FB * (134.5 - 123.0); sgp = 32 * Mpin / (pi * 10 ** 3)
    bear = FB / (10 * 7)                              # pin on plate bore 7 mm
    lig_b = FB / (2 * 7 * 7) * 2.5                    # R12 boss round Ø10: 7 mm ligament, Kt 2.5
    Fnet = max(np.linalg.norm(R[0] + R[1]), 1.0)      # total force the two posts take from the plate
    lig_r = Fnet / (2 * 7 * 7) * 3.0                  # bearing ring R28 / bore R21: two 7 mm ligaments, Kt 3, tension case (bearing carries compression)
    lig_r2 = R2 / (2 * 7 * 7) * 3.0
    print(f"{mass} kg LC-D: B pin {FB:.0f} N: pin bending {sgp:.0f} MPa SF {sf(PIN_Y, sgp):.2f}; plate bore bearing {bear:.0f} MPa SF {sf(1.5*AL_Y, bear):.1f}; "
          f"B boss ligament {lig_b:.0f} MPa SF {sf(AL_Y, lig_b):.2f}; ring ligaments (post force {Fnet:.0f} N) {lig_r:.0f} MPa SF {sf(AL_Y, lig_r):.2f}; R2 {R2:.0f} N on ring {lig_r2:.0f} MPa SF {sf(AL_Y, lig_r2):.2f}")
    # plate web between ring and posts: width ~34 mm x 7
    Vmax = max(np.linalg.norm(R[0]), np.linalg.norm(R[1])); Mweb = Vmax * 0  # in-plane force to posts: tension/shear in a 22-34 mm wide web
    print(f"      web to the posts (min width 22 mm at the post boss R11 -> 11 mm ligament each side): {Vmax/(2*11*7)*2.5:.0f} MPa SF {sf(AL_Y, Vmax/(2*11*7)*2.5):.1f}")
    # collar of the body side plate: D18 hole, D30 collar 5 mm (y 60-65), post D16 -> if collar is the guide: reaction = V*(119.5-40)/(62.5-40)
    Vc = Vmax * (119.5 - 40.0) / (62.5 - 40.0); pc = Vc / (16 * 5)
    print(f"      if the side-plate collar (y 60-65, D18 hole) acts as the intermediate support with the base at y 40: collar load {Vc:.0f} N, bearing {pc:.0f} MPa SF PAHT {sf(PAHT, pc):.2f} (PETG {sf(PETG, pc):.2f}); base seat at y 40 is NOT defined in body.md")

# ---- M5 tie of the beam, and 4 x M4 plate-to-body ----
print("\n== 4b. Ties to the body: beam foot 2 x M5 and hip Al plate 4 x M4 (through-bolts + washer assumed; heat-set insert rule < 150 N) ==")
for mass in (6.4, 6.9):
    for tag, lat in (('realistic direction', None), ('worst-direction sweep', 'sweep')):
        R, Pm, sg, sgb, R2, FB = AR[(mass, 'D')]
        bx, bz = R[2]
        if lat == 'sweep':
            p, loads, R2_, FBm = arch_loads('D', mass); bxm = bzm = 0
            for da in range(-60, 61, 10):
                c, s_ = math.cos(math.radians(da)), math.sin(math.radians(da)); Fb = loads[0][1]
                Rr = arch_solve([(L.B, np.array([c * Fb[0] - s_ * Fb[1], s_ * Fb[0] + c * Fb[1]]))] + loads[1:])
                if abs(Rr[2][1]) > bzm: bxm, bzm = Rr[2]
            bx, bz = bxm, bzm
        Fy_ = 0.0
        T_pair = abs(bz) * Lb / 7.0                      # foot plate 14 mm lateral wide: bolt line to compression edge 7 mm
        T_bolt = T_pair / 2 + abs(bz) / 2
        S_bolt = math.hypot(abs(bx) * Lb / 30.0, abs(bx) / 2)    # in-plane moment on 2 bolts 30 mm apart
        print(f"{mass} kg {tag}: beam tip (x {bx:.0f}, z {bz:.0f}) N: M5 tension {T_bolt:.0f} N each (insert rule 150 N -> SF {sf(150, T_bolt):.2f}); shear {S_bolt:.0f} N each; "
              f"M5 8.8 shear SF {sf(6800, S_bolt):.1f}; bearing on 4 mm printed rib {S_bolt/(5*4):.0f} MPa SF PAHT {sf(PAHT, S_bolt/20):.2f}; slip friction (preload 5.5 kN, mu 0.3, 2 bolts) {2*5500*0.3:.0f} N vs {math.hypot(bx, S_bolt*0):.0f} N")
# 4 x M4 hip plate (at +-44 -> 4 bolts), loads: post base moments + shear + 20 Nm torque
for mass in (6.4, 6.9):
    R, Pm, sg, sgb, R2, FB = AR[(mass, 'D')]
    Mx = sum(np.linalg.norm(r) for r in R[:2]) * Ls / 1000     # Nm, worst alignment
    T = Mx * 1000 / 176.0; S = (sum(np.linalg.norm(r) for r in R[:2]) / 4 + 20000 / (4 * 62.2))
    print(f"{mass} kg LC-D hip plate 4 x M4 (+-44), IF the posts are based on the plate: out-of-plane moment {Mx:.0f} Nm -> tension {T:.0f} N/bolt; shear {S:.0f} N/bolt (incl. 20 Nm torque); "
          f"bearing on 4 mm PAHT pad {S/(4.5*4):.1f} MPa SF {sf(PAHT, S/18):.2f}; M4 8.8 tension SF {sf(5000, T):.1f}; heat-set insert rule SF {sf(150, T):.2f} -> through-bolt + washer needed")

# ---- thigh sleeve ----
print("\n== 4a. Thigh hex sleeve (steel 26.3/29 A/F, 4 mm at y 94-98) -> bearing 1 and hex contact ==")
import math as m_
C0_, Z_, dm_, B_, d_in = 2900., 15, 36., 7., 30.; Q0 = 5 * C0_ / Z_; al_ = m_.radians(20); E_s = 2000.
def ball(F, arm):
    M = F * arm / 1000.; Qr = 5 * F / (Z_ * m_.cos(al_)); Qn = 4 * M * 1000 / (Z_ * dm_) / m_.sin(al_)
    p0 = M * 1000 / (pi * d_in * B_ ** 2 / 12); Kth = (E_s / 5.) * pi * d_in * B_ ** 3 / 24 / 2 / 1000
    return M, Q0 / (Qr + Qn), PAHT / p0 if p0 else 99, m_.degrees(M / Kth)
print("sleeve length / centre y -> bearing 1 (87.5): R1 N, M1 Nm, ball SF, seat SF, tilt deg  (spring 180 N, thigh load at y 99, spring at 110, brg 2 at 121)")
for Ls_ in (0.0, 4.0, 6.0, 8.0):
    yh = 87.5 if Ls_ == 0 else 94.0 + Ls_ / 2
    for mass in (6.4, 6.9):
        out = []
        for k in ('A', 'C', 'B', 'D'):
            Fk_ = LC[k][1] if mass == 6.4 else LC[k][2]
            R1 = (Fk_ * 22. + SPR * 11.) / (121. - yh); R2 = Fk_ + SPR - R1
            arm = yh - 87.5
            if arm > 0: M, sb, ss, th = ball(R1, arm)
            else: M, sb, ss, th = 0, Q0 / (5 * R1 / (Z_ * m_.cos(al_))), 99, 0
            out.append(f"{k}: R1 {R1:5.0f} M {M:4.1f} ball {sb:4.2f} seat {ss:5.2f} {th:3.1f}deg R2 {R2:4.0f}")
        print(f"L={Ls_:.0f} mm yc={yh:5.1f} {mass} kg | " + " | ".join(out))
print("\nHex contact stress (steel sleeve against PAHT-CF; torque on 3 flats at half length, radial on projected 26 x L):")
print("mass LC  T Nm  R1 N  | L=4 carrier hex 26 A/F p_t+p_r MPa SF | thigh pocket 29.2 A/F | L=6 carrier | L=8 carrier")
for mass in (6.4, 6.9):
    for k, T in (('C', 13.0), ('B', 17.2), ('D', 20.0), ('D', 5.0)):
        Fk_ = LC[k][1] if mass == 6.4 else LC[k][2]
        res = []
        for Ls_ in (4.0, 6.0, 8.0):
            yh = 94.0 + Ls_ / 2; R1 = (Fk_ * 22. + SPR * 11.) / (121. - yh)
            pt = T * 1000 / (3 * 13.0 * (26 / m_.sqrt(3)) / 2 * Ls_); pr = R1 / (26 * Ls_)
            pt2 = T * 1000 / (3 * 14.6 * (29.2 / m_.sqrt(3)) / 2 * Ls_); pr2 = R1 / (29.2 * Ls_)
            res.append((pt + pr, pt2 + pr2, R1))
        print(f"{mass} {k}  {T:4.1f}  {res[0][2]:5.0f} | {res[0][0]:5.1f} SF {sf(PAHT, res[0][0]):4.2f} | {res[0][1]:5.1f} SF {sf(PAHT, res[0][1]):4.2f} | {res[1][0]:5.1f} SF {sf(PAHT, res[1][0]):4.2f} | {res[2][0]:5.1f} SF {sf(PAHT, res[2][0]):4.2f}")
# sleeve itself: steel 1.5 mm wall hex, 4 mm long: bending of the wall between flats under contact load (small); skip. Thigh hub: ligament between pocket 29.2 A/F vertex (r 16.86) and hub R22
print(f"thigh hub ligament at hex vertex: R22 - 16.86 = {22-16.86:.1f} mm; hoop tension from radial 2.4 kN on the pocket ~ {2365/(2*5.1*10)*2.0:.0f} MPa (Kt 2, t 10) SF {sf(PAHT, 2365/(2*5.1*10)*2.0):.2f}")
print("\nBearing 1 at the 2.0 kN design load (LC-D capped by a compliant stop), sleeve 4 mm (yc 96) and 6061/6906 option")
for Fk_ in (2000., 2640.):
    R1 = (Fk_ * 22. + SPR * 11.) / (121. - 96.); M, sb, ss, th = ball(R1, 8.5)
    C0_save = C0_
    print(f"F_K {Fk_:.0f}: R1 {R1:.0f} N M1 {M:.1f} Nm ball SF {sb:.2f} seat SF {ss:.2f} tilt {th:.1f} deg | 6906 (C0 ~5.0 kN) ball SF ~{sb*5.0/2.9:.2f}")
print("Sleeve at 2.0 kN + thigh plane moved inboard by 2 mm (yc 94, i.e. sleeve y 92-96): ", end="")
R1 = (2000 * 22. + SPR * 11.) / (121. - 94.); M, sb, ss, th = ball(R1, 6.5); print(f"ball {sb:.2f} seat {ss:.2f}")
