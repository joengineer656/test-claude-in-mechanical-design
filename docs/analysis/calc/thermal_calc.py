"""P1 thermal calculations (thermal.md). Run: python3 thermal_calc.py > thermal_output.txt
Lumped steady-state resistance networks + adiabatic bursts. All inputs are stated in thermal.md (Assumptions).
Copper loss under FOC (ODrive amplitude-invariant current, I = phase-current amplitude):
    P_cu = 1.5 * I^2 * R_ph,  R_ph = R_ll / 2 (wye)  ==  0.75 * I^2 * R_ll
"""
import math

T_AMB = 35.0          # design ambient, C
T_WIND_MAX = 100.0    # winding design limit (keeps magnets/varnish safe; see thermal.md A4)
ALPHA_CU = 0.00393    # copper tempco 1/K


def r_hot(r25, t):
    return r25 * (1 + ALPHA_CU * (t - 25))


def p_cu(i, r_ll, t):
    return 1.5 * i**2 * r_hot(r_ll / 2, t)


def steady(i, r_ll, r_th, p_other=0.0):
    """Fixed-point winding temperature with temperature-dependent R. Returns (T, P_total)."""
    t = T_AMB
    for _ in range(200):
        p = p_cu(i, r_ll, t) + p_other
        t_new = T_AMB + p * r_th
        if t_new > 400:          # thermal runaway / no solution in range
            return float("inf"), p
        if abs(t_new - t) < 1e-6:
            break
        t = t_new
    return t, p


def i_max(r_ll, r_th, p_other=0.0, t_lim=T_WIND_MAX):
    p_allow = (t_lim - T_AMB) / r_th - p_other
    return math.sqrt(max(p_allow, 0) / (1.5 * r_hot(r_ll / 2, t_lim)))


def par(*rs):
    return 1 / sum(1 / r for r in rs)


def conv(h, a):
    return 1 / (h * a)


# ---------------- Wheel: T-Motor MN5008 KV170 in an enclosed printed hub ----------------
W_RLL, W_KT, W_N, W_ETA = 0.270, 8.27 / 170, 3.5, 0.90
W_POLEPAIRS = 14
v = 10 / 3.6                                  # 10 km/h
w_wheel = v / 0.085                           # rad/s
w_mot = w_wheel * W_N
rpm_mot = w_mot * 60 / (2 * math.pi)
f_el = rpm_mot / 60 * W_POLEPAIRS
# iron + bearing loss from idle current 0.4 A @ 22 V (no-load rpm 170*22), scaled ~ f^1.5
P_FE_W = 0.4 * 22 * (rpm_mot / (170 * 22)) ** 1.5

A_MOT_W = math.pi * 0.0556 * 0.032 + 2 * math.pi * 0.0278**2   # motor outer surface
A_CAV = math.pi * 0.10 * 0.045 + 2 * math.pi * 0.05**2         # hub cavity wall, D100 x 45 mm
A_HUB_OUT = 0.040                                               # outer hub/disc area exchanging with ambient
R_WALL = 0.003 / (0.20 * A_CAV)                                 # 3 mm printed wall, k = 0.2 W/mK
R_W_JC = 1.5                                                    # winding -> motor surface (estimate)
H_RAD = 6.0
# rotating rotor convection (driving, ~1090 rpm): Nu = 0.133 Re^(2/3) Pr^(1/3)
nu_air, k_air = 1.7e-5, 0.027
re_rot = (w_mot * 0.0278) * 0.0556 / nu_air
h_rot = 0.133 * re_rot ** (2 / 3) * 0.89 * k_air / 0.0556
re_flat = v * 0.17 / nu_air
h_flat = 0.664 * re_flat**0.5 * 0.89 * k_air / 0.17

cases_w = {
    # name: (h motor->cavity air, h cavity air->wall, h outer)
    "sealed hub, standstill": (5 + H_RAD, 5, 6 + 5),
    "sealed hub, 10 km/h": (h_rot + H_RAD, 15, h_flat + 5),
}
R_AL_PATH = 0.5 + conv(11, 0.020)   # Al stator carrier (3 mm 6061) + axle contact 0.5 K/W, then ~200 cm2 finned Al cap outside the hub, still air
print("=== WHEEL MN5008 KV170 ===")
print(f"10 km/h: wheel {w_wheel:.1f} rad/s, motor {rpm_mot:.0f} rpm, f_el {f_el:.0f} Hz, P_iron+bearing ~{P_FE_W:.2f} W")
print(f"h_rotor(1090 rpm) = {h_rot:.0f} W/m2K, h_outer(2.78 m/s) = {h_flat:.0f} W/m2K, A_motor {A_MOT_W*1e4:.0f} cm2, A_cavity {A_CAV*1e4:.0f} cm2")
wheel_R = {}
for name, (h1, h2, h3) in cases_w.items():
    r_sealed = R_W_JC + conv(h1, A_MOT_W) + conv(h2, A_CAV) + R_WALL + conv(h3, A_HUB_OUT)
    r_al = R_W_JC + par(r_sealed - R_W_JC, R_AL_PATH)
    wheel_R[name] = (r_sealed, r_al)
    print(f"[{name}] R_wind-amb sealed = {r_sealed:.1f} K/W ; with Al heat path = {r_al:.1f} K/W")

# Wheel operating points (current = phase amplitude)
t_6a_drv = 6 * W_KT * W_N * W_ETA
p_gear_6a = (1 - W_ETA) * t_6a_drv * w_wheel
duty_tw = 0.30                                   # RMS wheel torque while balancing+driving (Nm), control: cont req 0.6
i_duty = duty_tw / (W_KT * W_N * W_ETA)
p_gear_duty = (1 - W_ETA) * duty_tw * w_wheel
print(f"6 A -> {t_6a_drv:.2f} Nm at wheel; duty RMS {duty_tw} Nm -> {i_duty:.2f} A")
for lbl, i, rkey, pother in [
    ("6 A standstill", 6, "sealed hub, standstill", 0),
    ("6 A @10 km/h", 6, "sealed hub, 10 km/h", P_FE_W + p_gear_6a),
    ("duty @10 km/h", i_duty, "sealed hub, 10 km/h", P_FE_W + p_gear_duty),
    ("duty standstill bal.", i_duty, "sealed hub, standstill", 0),
]:
    for j, tag in enumerate(("sealed", "Al path")):
        t, p = steady(i, W_RLL, wheel_R[rkey][j], pother)
        print(f"  {lbl:22s} {tag:8s}: P_cu25 {p_cu(i, W_RLL, 25):5.2f} W, P_tot {p:5.2f} W, T_wind {t:6.1f} C")
for rkey in wheel_R:
    po = P_FE_W + 0.25 if "km/h" in rkey else 0
    print(f"  I_max cont (T_wind {T_WIND_MAX:.0f} C) [{rkey}]: sealed {i_max(W_RLL, wheel_R[rkey][0], po):.1f} A,"
          f" Al path {i_max(W_RLL, wheel_R[rkey][1], po):.1f} A")
# sensitivity: retailer conflict 720 mOhm
print(f"  (if R_ll were 0.720: I_max sealed standstill {i_max(0.72, wheel_R['sealed hub, standstill'][0]):.1f} A)")
# temperatures of the cavity air / wall at the sealed limit (standstill)
h1, h2, h3 = cases_w["sealed hub, standstill"]
p_lim = (T_WIND_MAX - T_AMB) / wheel_R["sealed hub, standstill"][0]
t_case = T_AMB + p_lim * (wheel_R["sealed hub, standstill"][0] - R_W_JC)
t_air = T_AMB + p_lim * (conv(h2, A_CAV) + R_WALL + conv(h3, A_HUB_OUT))
t_wall_in = T_AMB + p_lim * (R_WALL + conv(h3, A_HUB_OUT))
print(f"  at sealed limit ({p_lim:.1f} W): motor can {t_case:.0f} C, cavity air {t_air:.0f} C, hub wall inner {t_wall_in:.0f} C")
C_MN = 0.128 * 500         # J/K lumped motor
C_CU_W = 0.025 * 385       # J/K copper only (estimate 25 g)
print(f"  tau sealed standstill = {wheel_R['sealed hub, standstill'][0]*C_MN/60:.0f} min (C = {C_MN:.0f} J/K)")
p15 = p_cu(15, W_RLL, 80)
print(f"  15 A peak: P_cu(80C) {p15:.0f} W -> copper-only adiabatic {p15/C_CU_W:.1f} K/s, whole motor {p15/C_MN:.2f} K/s")
# time at 6 A from 60 C before 100 C (lumped, standstill sealed)
r = wheel_R["sealed hub, standstill"][0]
t_inf, p6 = steady(6, W_RLL, r)
t6 = -r * C_MN * math.log((t_inf - 100) / (t_inf - 60)) if t_inf > 100 else float("inf")
print(f"  6 A from 60 C to 100 C (sealed, standstill): {t6:.0f} s")
assert 2 < wheel_R["sealed hub, standstill"][0] < 40

# ---------------- Hip: Eaglepower 8308 KV130, 8:1, printed housing ----------------
H_RLL, H_KT, H_N, H_ETA = 0.089, 8.27 / 130, 8, 0.85
A_MOT_H = math.pi * 0.092 * 0.0285 + 2 * math.pi * 0.046**2
R_H_JC = 0.8
r_free = conv(11, 0.6 * A_MOT_H)                          # exposed 60 % of can, still air + radiation
r_plate = 0.005 / (0.25 * math.pi * 0.025**2) + conv(11, 0.03)   # 5 mm printed mount (k 0.25) + side plate to air
r_gbox = 15.0                                               # rotor face -> printed gearbox -> air (estimate)
R_HIP = R_H_JC + par(r_free, r_plate, r_gbox)
r_alplate = 0.003 / (167 * math.pi * 0.025**2) + conv(11 + 3, 2 * 0.08 * 0.08)   # 3 mm Al 80x80 adapter, both faces
R_HIP_AL = R_H_JC + par(r_free, r_alplate, r_gbox)
R_HIP_DRV = R_H_JC + par(conv(20 + 5, 0.6 * A_MOT_H), r_plate, r_gbox)    # robot driving 2.8 m/s
print("\n=== HIP 8308 KV130 ===")
print(f"R_wind-amb: printed mount {R_HIP:.2f} K/W, with Al adapter plate {R_HIP_AL:.2f} K/W, printed + driving air {R_HIP_DRV:.2f} K/W")
for lbl, tq in [("6 Nm continuous", 6.0), ("30 % (1.8 Nm)", 1.8), ("standing 2.3 Nm", 2.3), ("climb 5.3 Nm", 5.3)]:
    i = tq / (H_N * H_ETA * H_KT)
    for tag, rr in (("printed", R_HIP), ("Al plate", R_HIP_AL)):
        t, p = steady(i, H_RLL, rr)
        t_can = T_AMB + p * (rr - R_H_JC)
        print(f"  {lbl:16s} I {i:5.1f} A {tag:8s}: P_cu25 {p_cu(i, H_RLL, 25):5.2f} W, T_wind {t:5.1f} C, can/housing {t_can:5.1f} C")
for tag, rr in (("printed", R_HIP), ("Al plate", R_HIP_AL)):
    im = i_max(H_RLL, rr)
    print(f"  I_max cont {tag}: {im:.1f} A -> {im*H_N*H_ETA*H_KT:.1f} Nm at hip")
i_k = 6.0 / (H_N * H_ETA * 0.8 * H_KT)
print(f"  (with measured-Kt derate 0.8: 6 Nm needs {i_k:.1f} A)")
assert R_HIP_AL < R_HIP

# ---------------- Jump burst (adiabatic) ----------------
C_CU_H = 0.050 * 385      # 8308 copper ~50 g (estimate)
C_HIP = 0.336 * 500
print("\n=== JUMP 40 A BURST (hip) ===")
for tb in (0.115, 0.3, 2.0):
    p40 = p_cu(40, H_RLL, 80)
    print(f"  {tb:5.3f} s at 40 A: P_cu(80C) {p40:.0f} W, E {p40*tb:.0f} J, copper-only dT {p40*tb/C_CU_H:.1f} K, whole motor {p40*tb/C_HIP:.2f} K")
for period in (5, 10, 20):
    print(f"  one 0.3 s push-off every {period:2d} s adds {p_cu(40, H_RLL, 80)*0.3/period:.1f} W average")

# ---------------- Driver (XDrive Mini, NTMFS5C628NL x6) ----------------
RDS_HOT = 2.4e-3 * 1.5     # 2.4 mOhm max @25 C, x1.5 at Tj ~100 C
F_PWM, V_BUS, T_SW = 24e3, 25.2, 60e-9   # 24 kHz, rise+fall ~60 ns per transition pair
def driver_loss(i):
    cond = 3 * (i / math.sqrt(2)) ** 2 * RDS_HOT
    sw = 3 * 0.5 * V_BUS * (2 * i / math.pi) * T_SW * F_PWM
    shunt = 2 * (i / math.sqrt(2)) ** 2 * 0.5e-3 * 0.5
    return cond, sw, shunt, cond + sw + shunt + 1.5
print("\n=== DRIVER ===")
R_BOARD_BARE = conv(11, 2 * 0.063 * 0.058)
R_BOARD_AL = par(R_BOARD_BARE, 0.5 + conv(11, 2 * 0.07 * 0.07))   # 1.5 mm Al 70x70 plate under FETs via pad
print(f"board->air: bare {R_BOARD_BARE:.1f} K/W, with 70x70x1.5 Al plate {R_BOARD_AL:.1f} K/W")
for i in (2, 4.2, 6, 14, 20, 40):
    c, s, sh, tot = driver_loss(i)
    print(f"  {i:4.1f} A: cond {c:5.2f} sw {s:4.2f} shunt {sh:4.2f} + logic 1.5 = {tot:5.2f} W;"
          f" rise bare {tot*R_BOARD_BARE:4.0f} K, Al {tot*R_BOARD_AL:4.0f} K")

# ---------------- Brake resistor ----------------
print("\n=== BRAKE RESISTOR 2 ohm ===")
for vb in (25.2, 28.0, 30.0):
    print(f"  {vb} V: peak {vb**2/2:.0f} W, {vb/2:.1f} A")
C_RES = 0.012 * 900
print(f"  25 J event -> {25/C_RES:.1f} K ; fault (318 W continuous) -> {318/C_RES:.0f} K/s, reaches 200 C in {165/(318/C_RES):.1f} s")

# ---------------- Body / Pi 4 ----------------
print("\n=== BODY ===")
p_drv_duty = 2 * driver_loss(4.2)[3] + 2 * driver_loss(i_duty)[3]
p_drv_hi = 2 * driver_loss(14)[3] + 2 * driver_loss(6)[3]
others = 6.0 + 0.9 + 0.7     # Pi 4 SLAM, buck, ESP32+CAN+IMU (camera on front face, lidar outside)
for lbl, pd in (("duty", p_drv_duty), ("high (hip 14 A, wheel 6 A)", p_drv_hi)):
    print(f"  {lbl}: drivers {pd:.1f} W + others {others:.1f} W = {pd+others:.1f} W")
A_BODY = 2 * (0.25 * 0.15 + 0.25 * 0.20 + 0.15 * 0.20)
R_BODY = conv(6, A_BODY) + 0.003 / (0.2 * A_BODY) + conv(10, A_BODY)
for lbl, pd in (("duty", p_drv_duty), ("high", p_drv_hi)):
    P = pd + others
    print(f"  sealed body ({A_BODY:.3f} m2, R {R_BODY:.2f} K/W) {lbl}: air {T_AMB + P*R_BODY:.0f} C")
P = p_drv_duty + others
for dT in (5, 8):
    Q = P / (1.15 * 1005 * dT)
    print(f"  fan flow for dT_air {dT} K: {Q*1e3:.2f} L/s = {Q*2118.9:.1f} CFM; free vent area at 1.5 m/s: {Q/1.5*1e4:.0f} cm2 each")
H, dTn = 0.15, 15
vel = 0.6 * math.sqrt(2 * 9.81 * H * dTn / 308)
print(f"  natural chimney (H {H} m, dT {dTn} K): v {vel:.2f} m/s, free area each {P/(1.15*1005*dTn*vel)*1e4:.0f} cm2")
# Pi SoC rise over local air (Raspberry Pi whitepaper class values, see thermal.md)
for lbl, d in (("bare", 50), ("passive heatsink", 35), ("heatsink + fan", 18)):
    for air in (T_AMB + P * R_BODY, T_AMB + 6):
        print(f"  Pi SoC {lbl:16s} at local air {air:4.0f} C -> {air + d:4.0f} C")
