"""P1 Robot Theory calculations (wheel ratio, leg 4-bar, hip ratio, snappers, landing, hub vs belt).
Run: python3 theory_calc.py   -> prints the markdown tables used in ../theory.md
numpy only. All SI units. Every assumed number is in the INPUTS block with its basis.
"""
import math
import numpy as np

g = 9.81
# ---------------- INPUTS ----------------
KV = 90.0                 # rpm/V, Eaglepower LA8308 KV90 (retailer listing; verify on arrival)
R_LL = 0.186              # ohm, line-line (retailer "internal resistance"); ODrive phase R ~ R_LL/2
KT = 8.27 / KV            # Nm/A (ODrive convention, A = Iq amplitude)
KE = 1.0 / (KV * 2 * math.pi / 60)   # V/(rad/s), DC-equivalent back-EMF constant
K_MOD = 0.70              # ODrive v3.6 max modulation 70 %: max rpm ~ KV*0.7*Vbus (ODrive docs 0.5.4 specs)
I_PEAK = 40.0             # A, peak motor current (few s). Driver limit to be confirmed by Electrical
I_CONT_WHEEL = 11.0       # A, continuous: 22 A drone rating halved (no prop airflow, enclosed in wheel)
I_CONT_HIP = 14.0         # A, continuous: hip motor in open air on body side plate
I_ROTOR = 2.0e-4          # kg m2, 8308 rotor (estimate 0.14 kg @ r_g 38 mm; same as control sim)
I_WHEEL = 1.0e-3          # kg m2, rim + TPU tyre + carrier, one wheel (estimate)
R_W = 0.085               # m, wheel radius (D 170)
ETA_W = 0.90              # printed single-stage planetary, greased, forward
ETA_W_BACK = 0.85         # backdrive
ETA_H = 0.85              # hip gearbox forward (single stage, larger ratio)
MU = 0.8                  # tyre-ground friction (TPU on concrete/lino)
CRR = 0.03                # rolling resistance, soft TPU airless tyre
CDA = 0.9 * 0.30 * 0.45   # Cd * frontal area (0.30 x 0.45 m)

M_TOT = 3.6               # kg, budget target (hard limit 4.0 checked separately)
# per-side unsprung (moves with the wheel) - hub layout
MU_HUB = 0.336 + 0.110 + 0.210 + 0.040 + 0.025   # motor, gearbox, rim+tyre, axle+bearings, 1/2 shank = 0.721
MU_BELT = 0.210 + 0.060 + 0.020 + 0.025         # rim+tyre, axle+pulley+bearings, belt, 1/2 shank = 0.315
BELT_EXTRA = 0.060        # kg per side: belt, 2 pulleys, tensioner, idler shafts
L_BODY = 0.23             # m, body CoM above axle at nominal stance
KG_BODY = 0.12            # m, body pitch radius of gyration

MOTOR_KV, WHEEL_N, HIP_N = 130, 4, 8   # P1 recommendation (see theory.md)
Y_CROUCH, Y_NOM, Y_EXT = 0.10, 0.20, 0.29   # hip height above wheel axle (m)
JUMP_H = 0.20             # m, required wheel clearance (CoM rise, no tuck credit)
V_KMH_REQ = 12.0


def set_motor(kv):
    """Switch motor variant. R scaled ~1/KV^2 from the KV90 listing (same copper fill) - ESTIMATE for KV!=90."""
    global KV, R_LL, KT, KE
    KV = kv
    R_LL = 0.186 * (90.0 / kv) ** 2
    KT = 8.27 / kv
    KE = 1.0 / (kv * 2 * math.pi / 60)


def wheel_speed_table():
    rows = []
    v_req = V_KMH_REQ / 3.6
    for N in (3, 4, 5, 6):   # 3:1 shown only as KV90 fallback
        for V in (22.2, 19.8):
            veff = K_MOD * V
            w0 = veff / KE                    # motor rad/s no load
            v0 = w0 / N * R_W * 3.6           # km/h
            # loaded: resistive (rolling + aero) + 30 % of peak wheel torque kept as balance headroom
            def need(vms):
                F = CRR * M_TOT * g + 0.5 * 1.2 * CDA * vms**2
                return F * R_W / 2 / (N * ETA_W) + 0.3 * KT * I_PEAK   # motor torque per motor
            vms = 0.0
            for vv in np.arange(0, 15, 0.005):
                wm = vv / R_W * N
                Iavail = min(I_PEAK, (veff - KE * wm) / R_LL)
                if KT * Iavail < need(vv):
                    break
                vms = vv
            rows.append((N, V, w0 * 60 / 2 / math.pi, v0, vms * 3.6))
    return rows


def wheel_torque_table(m_u, label):
    """Torque, acceleration, balance recovery, back-drive for each ratio."""
    out = []
    mb = M_TOT - 2 * m_u
    for N in (3, 4, 5, 6):
        Tc = KT * I_CONT_WHEEL * N * ETA_W
        Tp = KT * I_PEAK * N * ETA_W
        I_eff = I_WHEEL + N**2 * I_ROTOR
        A = M_TOT + 2 * I_eff / R_W**2          # effective translational mass
        a_tq = 2 * Tp / R_W / A
        a_max = min(a_tq, MU * g)
        # balance: theta_dd <= 0 needs tau >= mb g l sin(th) / (1 + mb l /(A r))
        tau = 2 * Tp
        s = tau * (1 + mb * L_BODY / (A * R_W)) / (mb * g * L_BODY)
        th_tq = math.degrees(math.asin(min(1.0, s)))
        th_trac = math.degrees(math.atan(MU))
        margin = tau / (mb * g * L_BODY)
        Irefl = N**2 * I_ROTOR
        out.append(dict(N=N, Tc=Tc, Tp=Tp, a_tq=a_tq, a_max=a_max, th=min(th_tq, th_trac), th_tq=th_tq,
                        margin=margin, Irefl=Irefl, Ieff=I_eff, A=A))
    return out


# ---------------- leg 4-bar synthesis (random search, fixed seed) ----------------
def leg_points(p, phi):
    L1, L2, L3, Lkc, al, bx, by, br = p
    K = np.stack([L1 * np.cos(phi), L1 * np.sin(phi)], -1)
    B = np.array([bx, by])
    d_vec = B - K
    d = np.linalg.norm(d_vec, axis=-1)
    a = (Lkc**2 - L3**2 + d**2) / (2 * d)
    h2 = Lkc**2 - a**2
    ok = h2 > 0
    h = np.sqrt(np.where(ok, h2, 0))
    u = d_vec / d[..., None]
    perp = np.stack([-u[..., 1], u[..., 0]], -1)
    C = K + a[..., None] * u + br * h[..., None] * perp
    kc = (C - K) / Lkc
    ca, sa = math.cos(al), math.sin(al)
    dirw = np.stack([kc[..., 0] * ca - kc[..., 1] * sa, kc[..., 0] * sa + kc[..., 1] * ca], -1)
    W = K + L2 * dirw
    # transmission angle at C between coupler (C->B) and shank (C->K)
    v1 = B - C
    v2 = K - C
    cosmu = np.sum(v1 * v2, -1) / (np.linalg.norm(v1, axis=-1) * np.linalg.norm(v2, axis=-1) + 1e-12)
    mu = np.degrees(np.arccos(np.clip(cosmu, -1, 1)))
    return K, C, W, ok, mu


def eval_leg(p, phi):
    K, C, W, ok, mu = leg_points(p, phi)
    y = W[:, 1]
    if not ok.any() or y[ok].min() > -Y_EXT or y[ok].max() < -Y_CROUCH:
        return None
    best = None
    n = len(phi)
    i = 0
    while i < n - 1:
        if not (ok[i] and ok[i + 1]):
            i += 1
            continue
        sgn = np.sign(y[i + 1] - y[i])
        j = i
        while j < n - 1 and ok[j + 1] and np.sign(y[j + 1] - y[j]) == sgn:
            j += 1
        seg = slice(i, j + 1)
        ys = y[seg]
        if ys.min() <= -Y_EXT and ys.max() >= -Y_CROUCH:
            m = (ys <= -Y_CROUCH + 1e-9) & (ys >= -Y_EXT - 1e-9)
            idx = np.arange(i, j + 1)[m]
            if len(idx) > 5:
                xs = W[idx, 0]
                Jy = np.abs(np.gradient(y[idx], phi[idx]))
                low = min(K[idx, 1].min(), C[idx, 1].min()) - y[idx].min()
                reach = max(np.abs(K[idx, 0]).max(), np.abs(C[idx, 0]).max())
                pen = 0.0
                pen += max(0, 35 - mu[idx].min()) * 0.002 + max(0, mu[idx].max() - 145) * 0.002
                pen += max(0, Jy.max() / Jy.min() - 2.5) * 0.02
                pen += max(0, 0.03 - low) * 2 + max(0, reach - 0.15) * 2
                pen += 0.2 * max(0, Jy.mean() - 0.13)   # keep hip lever short (torque)
                score = (xs.max() - xs.min()) + 0.3 * abs(xs.mean()) + pen
                cand = (score, idx, xs, Jy, mu[idx])
                if best is None or score < best[0]:
                    best = cand
        i = j + 1 if j > i else i + 1
    return best


def synth_leg(n=120000, seed=1):
    rng = np.random.default_rng(seed)
    phi = np.radians(np.arange(-180, 180, 0.5))
    lo = np.array([0.08, 0.12, 0.08, 0.025, -math.pi, -0.06, -0.02])
    hi = np.array([0.16, 0.20, 0.18, 0.070, math.pi, 0.06, 0.05])
    best = None
    for _ in range(n):
        q = lo + (hi - lo) * rng.random(7)
        p = tuple(q) + (1.0 if rng.random() < 0.5 else -1.0,)
        r = eval_leg(p, phi)
        if r and (best is None or r[0] < best[1][0]):
            best = (p, r)
    return best, phi


def leg_tables(p, phi, idx):
    K, C, W, ok, mu = leg_points(p, phi)
    ph = phi[idx]
    y = -W[idx, 1]   # hip height above axle (positive)
    order = np.argsort(y)
    return ph[order], y[order], W[idx, 0][order], K[idx][order], C[idx][order], W[idx][order], mu[idx][order]


def statics(p, Kp, Cp, Wp, F):
    """Vertical ground force F (N, up) at wheel. Returns hip torque, coupler force, knee pin force."""
    B = np.array(p[5:7])
    u = (Cp - B) / np.linalg.norm(Cp - B)      # coupler direction (two-force member)
    Fw = np.array([0.0, F])
    cross = lambda a, b: a[0] * b[1] - a[1] * b[0]
    # shank moments about K: (W-K) x Fw + (C-K) x (fc*u) = 0
    fc = -cross(Wp - Kp, Fw) / cross(Cp - Kp, u)
    Fk = -(Fw + fc * u)                       # force from thigh on shank at knee
    T_hip = cross(Kp, -Fk)                    # thigh: shank pushes thigh with -Fk at K
    return T_hip, abs(fc), np.linalg.norm(Fk)


# ---------------- jump simulation ----------------
def motor_torque(wm, V):
    veff = K_MOD * V
    I = min(I_PEAK, max(0.0, (veff - KE * abs(wm)) / R_LL))
    return KT * I, I


def jump(Nh, V, m_b, m_u_total, spring, legs):
    """1-DOF push-off from Y_CROUCH to Y_EXT, both legs. spring(phi) -> hip torque per leg (Nm)."""
    ph, y, J = legs
    yy, v, t, dt = Y_CROUCH, 0.0, 0.0, 2e-5
    Imax, Pmax, Es, Em = 0.0, 0.0, 0.0, 0.0
    while yy < Y_EXT:
        Jy = np.interp(yy, y, J)
        phi = np.interp(yy, y, ph)
        wm = Nh * v / Jy
        Tm, I = motor_torque(wm, V)
        Ts = spring(phi)
        F_leg = (Tm * Nh * ETA_H + Ts) / Jy
        a = 2 * F_leg / m_b - g
        Es += 2 * Ts / Jy * v * dt
        Em += 2 * Tm * Nh * ETA_H / Jy * v * dt
        Imax = max(Imax, I)
        Pmax = max(Pmax, 2 * (KE * abs(wm) * I + I**2 * R_LL))
        v += a * dt
        yy += v * dt
        t += dt
        if t > 1.0:
            return None
    M = m_b + m_u_total
    v_to = m_b * v / M                       # inelastic snatch of the unsprung mass
    h = v_to**2 / (2 * g)
    lost = 0.5 * m_b * v**2 - 0.5 * M * v_to**2
    return dict(t=t, v_b=v, v_to=v_to, h=h, Es=Es, Em=Em, lost=lost, Imax=Imax, Pbat=Pmax, Ibat=Pmax / V)


def make_spring(ph, y, J, F_static_leg, E_leg, T0_min=0.3):
    """Linear torsion-equivalent: T = T0 + k*(|phi - phi_ext|). Solve gravity-balance at nominal and energy."""
    phi_ext = np.interp(Y_EXT, y, ph)
    phi_cr = np.interp(Y_CROUCH, y, ph)
    phi_nom = np.interp(Y_NOM, y, ph)
    D = abs(phi_cr - phi_ext)
    dn = abs(phi_nom - phi_ext)
    if E_leg is None:     # pure gravity compensation with given preload
        T0 = T0_min
        k = (F_static_leg * np.interp(Y_NOM, y, J) - T0) / dn
    else:
        T0 = T0_min
        k = (E_leg - T0 * D) / (0.5 * D**2)
    f = lambda phi: T0 + k * abs(phi - phi_ext)
    return f, T0, k, D, phi_ext


# ---------------- landing simulation (vertical 2-mass) ----------------
def landing(m_body, m_unsprung, legs, spring, Nh, mode, y0=0.27, v0=None, k_tyre=12000.0):
    ph, y, J = legs
    v0 = math.sqrt(2 * g * JUMP_H) if v0 is None else v0
    Tmax_hip = KT * I_PEAK * Nh / ETA_W_BACK      # motor torque reflected (backdriven, braking)
    yu, vu = 0.0, -v0          # tyre contact point height (0 = touching)
    L = y0                     # leg length (hip height above axle)
    vL = 0.0                   # leg extension rate
    dt = 1e-5
    pk = dict(Ft=0, Fl=0, Th=0, Tm=0, ab=0, au=0, s=0, y_at=y0, Tgear_es=0)
    yb_v = -v0
    for _ in range(int(0.4 / dt)):
        Jy = np.interp(L, y, J)
        phi = np.interp(L, y, ph)
        Fs = spring(phi) / Jy
        Fm = 0.0
        if mode == "controlled":
            # virtual spring-damper toward Y_NOM, stopping body within ~0.08 m
            kv = 280.0 * m_body                       # ~0.09 m stroke for any supported mass
            cv = 2 * 0.6 * math.sqrt(kv * m_body)
            Fm = kv * (y0 - L) - cv * vL - Fs + m_body * g
            Fm = float(np.clip(Fm, -Tmax_hip / Jy, Tmax_hip / Jy))
        Fes = 25000.0 * max(0.0, (Y_CROUCH + 0.005) - L)    # printed/rubber end stop, 5 mm before crouch
        Fl = Fs + Fm + Fes
        Ft = k_tyre * max(0.0, -yu) + (40.0 * max(0.0, -vu) if yu < 0 else 0.0)
        ab = Fl / m_body - g
        au = (Ft - Fl) / m_unsprung - g
        # integrate
        vb = yb_v + ab * dt
        vu2 = vu + au * dt
        aL = ab - au
        vL_new = vb - vu2
        Tgear_es = I_ROTOR * Nh**2 * abs(aL) / Jy if Fes > 0 else 0.0
        yb_v, vu = vb, vu2
        L += vL_new * dt
        vL = vL_new
        yu += vu * dt
        pk["Ft"] = max(pk["Ft"], Ft)
        if Fl > pk["Fl"]:
            pk["Fl"], pk["y_at"] = Fl, L
        pk["Th"] = max(pk["Th"], Fl * Jy)
        pk["Tm"] = max(pk["Tm"], abs(Fm) * Jy)
        pk["ab"] = max(pk["ab"], ab / g + 1)
        pk["au"] = max(pk["au"], abs(au) / g)
        pk["s"] = max(pk["s"], y0 - L)
        pk["Tgear_es"] = max(pk["Tgear_es"], Tgear_es)
        if yb_v > 0 and vu >= 0 and yu >= 0:
            break
    return pk


def balance_pole(m_u):
    mb = M_TOT - 2 * m_u
    A = M_TOT + 2 * (I_WHEEL + WHEEL_N**2 * I_ROTOR) / R_W**2
    Bm = mb * L_BODY
    Cm = mb * (L_BODY**2 + KG_BODY**2)
    return math.sqrt(mb * g * L_BODY / (Cm - Bm**2 / A))


def main():
    global M_TOT
    set_motor(MOTOR_KV)
    print(f"## Motor constants (chosen KV{KV:.0f}; R scaled from KV90 listing)")
    print(f"Kt = 8.27/KV = {KT:.4f} Nm/A, Ke = {KE:.4f} V/(rad/s), R_ll = {R_LL} ohm")
    for kv in (90, 130, 160):
        print(f"KV{kv}: Kt={8.27/kv:.4f} Nm/A, T@{I_PEAK:.0f}A={8.27/kv*I_PEAK:.2f} Nm, "
              f"no-load @22.2V*{K_MOD}={kv*22.2*K_MOD:.0f} rpm, @19.8V={kv*19.8*K_MOD:.0f} rpm")

    for kv in (90, 130):
        set_motor(kv)
        print("\n## Wheel speed (KV%d, R_ll=%.3f ohm, D=%.0f mm)" % (kv, R_LL, 2e3 * R_W))
        print("| N | Vbus V | motor no-load rpm | no-load km/h | loaded km/h (rolling+aero + 30 % torque headroom) |")
        print("|---|---|---|---|---|")
        for N, V, rpm, v0, vl in wheel_speed_table():
            print(f"| {N}:1 | {V} | {rpm:.0f} | {v0:.1f} | {vl:.1f} |")
        print("\n## Wheel torque / acceleration / balance (KV%d, hub layout, m_u=%.3f kg/side)" % (kv, MU_HUB))
        print("| N | T_wheel cont Nm | T_wheel peak Nm | a_torque m/s2 | a_max (traction cap) | max recoverable tilt deg | torque margin 2Tp/(m_b g l) | N^2 J_rotor kg m2 | m_eff kg |")
        print("|---|---|---|---|---|---|---|---|---|")
        for r in wheel_torque_table(MU_HUB, "hub"):
            print(f"| {r['N']}:1 | {r['Tc']:.2f} | {r['Tp']:.2f} | {r['a_tq']:.1f} | {r['a_max']:.1f} | "
                  f"{r['th']:.0f} (torque-only {r['th_tq']:.0f}) | {r['margin']:.1f} | {r['Irefl']:.4f} | {r['A']:.2f} |")
    print(f"Traction limit per wheel (static, mu*M*g*r/2) = {MU*M_TOT*g*R_W/2:.2f} Nm")
    set_motor(MOTOR_KV)

    print("\n## Leg 4-bar synthesis")
    (p, res), phi = synth_leg()
    score, idx, xs, Jy, mu = res
    L1, L2, L3, Lkc, al, bx, by, br = p
    print(f"L1 thigh={L1*1e3:.0f} mm, L2 knee->wheel={L2*1e3:.0f} mm, L3 coupler={L3*1e3:.0f} mm, "
          f"Lkc knee->coupler pin={Lkc*1e3:.0f} mm, shank angle KC->KW={math.degrees(al):.0f} deg, "
          f"coupler body pivot B=({bx*1e3:.0f},{by*1e3:.0f}) mm from hip, branch={br:+.0f}")
    ph, y, x, K, C, W, mus = leg_tables(p, phi, idx)
    J = np.abs(np.gradient(-W[:, 1], ph))
    print(f"wheel x drift over stroke: {xs.min()*1e3:.1f} .. {xs.max()*1e3:.1f} mm; hip rotation over stroke "
          f"{math.degrees(abs(ph[-1]-ph[0])):.0f} deg; J=dy/dphi {J.min()*1e3:.0f}..{J.max()*1e3:.0f} mm/rad; "
          f"transmission angle {mus.min():.0f}..{mus.max():.0f} deg")
    print("| hip height above axle mm | thigh angle deg | wheel x mm | J mm/rad | knee (x,y) mm | coupler pin C (x,y) mm |")
    print("|---|---|---|---|---|---|")
    for yt in (0.10, 0.15, 0.20, 0.25, 0.29):
        i = int(np.argmin(abs(y - yt)))
        print(f"| {y[i]*1e3:.0f} | {math.degrees(ph[i]):.0f} | {x[i]*1e3:.1f} | {J[i]*1e3:.0f} | "
              f"({K[i,0]*1e3:.0f},{K[i,1]*1e3:.0f}) | ({C[i,0]*1e3:.0f},{C[i,1]*1e3:.0f}) |")
    legs = (ph, y, J)

    m_b = M_TOT - 2 * MU_HUB
    F_stat = m_b * g / 2
    print(f"\nSprung (body) mass m_b = {m_b:.2f} kg; static leg force per leg = {F_stat:.1f} N")

    print("\n## Hip torque cases (per leg, output side), from statics")
    cases = [("standing (W_b/2)", F_stat), ("height change, +0.5 g (1.5 W_b/2)", 1.5 * F_stat),
             ("single-leg climb: 75 % W_b x1.5 dyn", 1.125 * m_b * g)]
    print("| case | leg force N | hip torque @crouch Nm | @nominal Nm | @extended Nm | worst Nm |")
    print("|---|---|---|---|---|---|")
    for name, F in cases:
        Ts = []
        for yt in (Y_CROUCH, Y_NOM, Y_EXT):
            i = int(np.argmin(abs(y - yt)))
            Ts.append(abs(statics(p, K[i], C[i], W[i], F)[0]))
        worst = max(abs(statics(p, K[i], C[i], W[i], F)[0]) for i in range(len(y)))
        print(f"| {name} | {F:.1f} | {Ts[0]:.2f} | {Ts[1]:.2f} | {Ts[2]:.2f} | {worst:.2f} |")
    # cross-check virtual work
    i = int(np.argmin(abs(y - Y_NOM)))
    print(f"(check: statics T={abs(statics(p,K[i],C[i],W[i],F_stat)[0]):.3f} vs virtual work F*J={F_stat*J[i]:.3f} Nm)")

    # jump energy budget
    v_req = math.sqrt(2 * g * JUMP_H)
    stroke = Y_EXT - Y_CROUCH
    for lab, mu_side in (("hub", MU_HUB), ("belt", MU_BELT)):
        M = M_TOT + (2 * BELT_EXTRA if lab == "belt" else 0)
        mb_ = M - 2 * mu_side
        vb = v_req * M / mb_
        E = mb_ * g * stroke + 0.5 * mb_ * vb**2
        print(f"\nJump energy ({lab}): M={M:.2f} m_b={mb_:.2f} v_takeoff={v_req:.2f} v_body={vb:.2f} m/s "
              f"E_actuators={E:.1f} J (snatch loss {0.5*mb_*vb**2-0.5*M*v_req**2:.1f} J); /0.85 losses = {E/0.85:.1f} J")

    print("\n## Hip ratio sweep: jump push-off simulation (two legs, I_peak=%.0f A)" % I_PEAK)
    spr, T0, k, D, phi_ext = make_spring(ph, y, J, F_stat, E_leg=4.0)
    print(f"Spring (per leg, torsion-equivalent at hip): T0={T0:.2f} Nm preload at full extension, "
          f"k={k:.2f} Nm/rad, stroke {math.degrees(D):.0f} deg, T@crouch={T0+k*D:.2f} Nm, "
          f"T@nominal={spr(np.interp(Y_NOM,y,ph)):.2f} Nm vs gravity {F_stat*np.interp(Y_NOM,y,J):.2f} Nm, "
          f"energy/leg={T0*D+0.5*k*D**2:.2f} J")
    nospr = lambda phi: 0.0
    print("| N hip | V | spring | jump h cm | push time ms | spring J | motor J | snatch loss J | peak I/motor A | peak battery A |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for kv, Ns in ((90, (5, 6, 7, 8)), (130, (6, 7, 8, 9, 10, 11, 12))):
      set_motor(kv)
      for Nh in Ns:
        for V in (22.2, 19.8):
            for sl, sf in (("8 J", spr), ("none", nospr)):
                r = jump(Nh, V, m_b, 2 * MU_HUB, sf, legs)
                if r is None:
                    print(f"| {Nh} | {V} | {sl} | fail | | | | | | |")
                    continue
                print(f"| KV{kv} {Nh}:1 | {V} | {sl} | {r['h']*100:.1f} | {r['t']*1e3:.0f} | {r['Es']:.1f} | {r['Em']:.1f} | "
                      f"{r['lost']:.1f} | {r['Imax']:.0f} | {r['Ibat']:.0f} |")
    set_motor(MOTOR_KV)
    Nh = HIP_N
    Tm_cont = KT * I_CONT_HIP * Nh * ETA_H
    Tm_pk = KT * I_PEAK * Nh * ETA_H
    print(f"\nHip N={Nh}: output torque cont {Tm_cont:.1f} Nm, peak {Tm_pk:.1f} Nm")
    i_nom = int(np.argmin(abs(y - Y_NOM)))
    hold = abs(spr(ph[i_nom]) - F_stat * J[i_nom])
    print(f"Hip motor holding torque at nominal with spring: {hold:.2f} Nm out -> "
          f"{hold/(Nh*ETA_H)/KT:.1f} A")
    i_cr = 0
    holdc = abs(spr(ph[i_cr]) - F_stat * J[i_cr])
    print(f"Holding at full crouch (spring loaded): {holdc:.2f} Nm out -> {holdc/(Nh*ETA_H)/KT:.1f} A")

    # linear spring conversion
    for ra in (0.030, 0.040, 0.050):
        kl = k / ra**2
        print(f"crank r_a={ra*1e3:.0f} mm: linear k={kl:.0f} N/m ({kl/1000:.2f} N/mm), preload F0={T0/ra:.0f} N, "
              f"F@crouch={(T0+k*D)/ra:.0f} N, working extension={ra*D*1e3:.0f} mm")

    print("\n## Landing from %.0f cm apex (v=%.2f m/s)" % (JUMP_H * 100, math.sqrt(2 * g * JUMP_H)))
    print("| case | body g (peak) | unsprung g | tyre/axle N | leg force N | hip torque total Nm | hip motor part Nm | leg stroke mm | hip gear torque from end-stop Nm |")
    print("|---|---|---|---|---|---|---|---|---|")
    LC = {}
    for name, mbody, mun, mode in (("A symmetric, controlled", m_b / 2, MU_HUB, "controlled"),
                                   ("B symmetric, motors off -> end stop", m_b / 2, MU_HUB, "off"),
                                   ("C one wheel first, controlled", m_b, MU_HUB, "controlled"),
                                   ("D one wheel first, motors off", m_b, MU_HUB, "off"),
                                   ("A' belt layout, controlled", (M_TOT + 2*BELT_EXTRA - 2*MU_BELT) / 2, MU_BELT, "controlled")):
        pk = landing(mbody, mun, legs, spr, HIP_N, mode)
        LC[name] = pk
        print(f"| {name} | {pk['ab']:.1f} | {pk['au']:.0f} | {pk['Ft']:.0f} | {pk['Fl']:.0f} | {pk['Th']:.1f} | "
              f"{pk['Tm']:.1f} | {pk['s']*1e3:.0f} | {pk['Tgear_es']:.1f} |")
    print("\nPin forces at peak leg force (statics, vertical ground force only):")
    print("| case | leg force N | pose hip h mm | hip torque Nm | knee pin N | coupler N | hip bearing radial N | wheel axle N |")
    print("|---|---|---|---|---|---|---|---|")
    for name, pk in LC.items():
        i = int(np.argmin(abs(y - pk["y_at"])))
        T, fc, fk = statics(p, K[i], C[i], W[i], pk["Fl"])
        print(f"| {name} | {pk['Fl']:.0f} | {y[i]*1e3:.0f} | {abs(T):.1f} | {fk:.0f} | {fc:.0f} | {fk:.0f} | {pk['Ft']:.0f} |")
    # wheel gear landing torque (spin-up slip, traction limited)
    for name in ("A symmetric, controlled", "C one wheel first, controlled"):
        Ft = LC[name]["Ft"]
        T_tyre = MU * Ft * R_W
        frac = WHEEL_N**2 * I_ROTOR / (WHEEL_N**2 * I_ROTOR + I_WHEEL)
        print(f"Wheel gear spin-up torque ({name}): mu*F*r={T_tyre:.1f} Nm, through gear (N=WHEEL_N inertia share {frac:.2f}) = {T_tyre*frac:.1f} Nm")

    print("\n## Hub vs belt")
    for lab, mu_side, extra in (("hub", MU_HUB, 0), ("belt", MU_BELT, BELT_EXTRA)):
        Mt = M_TOT + 2 * extra
        mb_ = Mt - 2 * mu_side
        I_leg = mu_side * Y_NOM**2
        p_ = balance_pole(mu_side)
        r5 = [r for r in wheel_torque_table(mu_side, lab) if r["N"] == WHEEL_N][0]
        print(f"{lab}: unsprung/side {mu_side:.3f} kg ({2*mu_side/Mt*100:.0f} % of M), body {mb_:.2f} kg, "
              f"leg inertia about hip {I_leg:.4f} kg m2, unstable pole {p_:.1f} rad/s, "
              f"N=WHEEL_N recoverable tilt {r5['th_tq']:.0f} deg, eff. mass {r5['A']:.2f} kg")

    print("\n## Mass-limit check: jump at M=4.0 kg (hub, chosen hip N, 19.8 V, spring)")
    M_TOT = 4.0
    m_b4 = M_TOT - 2 * MU_HUB
    r = jump(HIP_N, 19.8, m_b4, 2 * MU_HUB, spr, legs)
    print(f"m_b={m_b4:.2f}: jump {r['h']*100:.1f} cm, peak I {r['Imax']:.0f} A")


if __name__ == "__main__":
    main()
