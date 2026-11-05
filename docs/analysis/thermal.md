# Thermal Analysis — P1 (rev 0, 2026-11-04)

Author: Thermal Engineering Specialist. Scope: P1 calculations only, no CAD (DECISIONS.md, Gate A).
Evidence: `calc/thermal_calc.py` produces `calc/thermal_output.txt`. Every number below comes from that output.

## Summary

| # | Question | Answer |
|---|---|---|
| 1 | Is 6 A continuous realistic for the MN5008 inside a **sealed printed hub**? | **No.** R(winding to ambient) is about 19.7 K/W at standstill and 8.3 K/W at 10 km/h. Holding the winding at 100 °C with 35 °C ambient allows only **3.5 A (standstill) or 4.9 A (10 km/h)** continuous. At 6 A there is no steady state below 100 °C. From 60 °C the winding reaches 100 °C in about **170 s**. |
| 1b | Fix for the wheel | Add an **aluminium heat path**: a 3 mm 6061 stator carrier, clamped to the axle, ending in a finned aluminium cap (about 200 cm²) **outside** the hub on the leg side. This gives 5.4 / 4.4 K/W and **I_max = 6.7 A (standstill) / 7.1 A (10 km/h)**. Real duty is about 2 A RMS: winding 49–62 °C. |
| 1c | Hip 8308 (8:1) | 6 Nm continuous needs 13.9 A, which gives a 109 °C winding and a 95 °C can on a printed mount. **Printed mount limit: 5.7 Nm.** With a 3 mm Al adapter plate (80×80): 89 °C winding, 77 °C can, limit 6.5 Nm. At 30 % load (1.8 Nm, 4.2 A) the winding is only about 40 °C. |
| 2 | Drivers | 1.6–1.9 W each at duty, 3.1 W at hip 14 A, 4.5 W at 20 A, 12 W at 40 A. A bare board rises 55 K at 20 A, so it **needs a 70×70×1.5 mm Al plate** (rise 24 K). |
| 2b | Brake resistor | Peak 318 W at 25.2 V and 392 W at 28 V. A 25 J event heats it only about 2 K, but a fault (full V²/R for 5–6 s) reaches 200 °C. Mount it on metal, off plastic, and monitor it. |
| 2c | Pi 4 in a closed body | A sealed body runs at 52 °C air (duty) and 56 °C (high). The Pi then reaches 87 °C with a heatsink, so it throttles. **Use a 40 mm fan (≥ 3.3 CFM) with ≥ 10–16 cm² free inlet and outlet each, plus a Pi heatsink.** SoC: about 59 °C. |
| 3 | Materials | **PLA is out** for any part in the hub cavity: cavity air reaches 66 °C and the motor can 95 °C at the sealed limit. Use PAHT-CF (HDT 170 °C at 1.8 MPa) for the sun adapter, ring and carrier, and **PETG minimum (ASA preferred) for the hub shell**. Hip housing: PAHT-CF next to the can, or an Al plate. |
| 4 | 40 A jump burst | 130 W in the winding. 0.3 s gives **+2 K** in the copper (adiabatic), so the burst is harmless. A jump every 10 s adds 3.9 W average. |
| 5 | Sensors | Fit a 10 k NTC in the end-turns of all 4 motors, wired to the ODrive `motor_thermistor`, with derating from 80 °C and cut-off at 100 °C. |

## Assumptions

| # | Assumption | Value | Confidence / check |
|---|---|---|---|
| A1 | Ambient | 35 °C | client brief |
| A2 | Copper loss, FOC | P = 1.5·I²·R_ph, with R_ph = R_ll/2 (wye) and I = phase-current **amplitude**. ODrive `current_lim` / Iq use this convention. Note: 1.5·I²·R_ll/2 = 0.75·I²·R_ll. Using I²·R_ll would overstate the loss by 33 %, and 3·I²·R_ll would overstate it 4×. | high |
| A3 | Tempco | R(T) = R25·(1 + 0.00393·(T − 25)), solved by iteration | high |
| A4 | Winding limit | **100 °C design**. T-Motor / Eaglepower publish no insulation class. Typical drone-motor N-grade magnets begin to lose flux above about 80–120 °C. The 100 °C limit is therefore a magnet/epoxy limit, not a wire limit. | medium |
| A5 | MN5008 KV170 | R_ll 0.270 Ω, 128–135 g, Ø55.6×32, 24N28P (14 pp), idle 0.4 A at 22 V. A retailer lists 0.720 Ω; this is rejected because the KV340 version is 55 mΩ and R ∝ 1/KV² gives about 0.22 Ω. Sensitivity: at 0.72 Ω the sealed limit drops to 2.2 A. | medium (measure) |
| A6 | 8308 KV130 | R_ll 0.089 Ω (theory A9, scaled), Kt 0.0636, hip 8:1, η 0.85. Copper ≈ 50 g (estimate). | low-medium (measure) |
| A7 | Iron + bearing loss | Idle power 0.4 A × 22 V = 8.8 W at 3740 rpm, scaled as rpm^1.5. At 1092 rpm this gives **1.4 W** (wheel at 10 km/h). The hip runs nearly at standstill, so its iron loss ≈ 0. | medium |
| A8 | Gear loss | (1 − η)·T_out·ω_out. Wheel η 0.90. At a held position (ω ≈ 0) the gear loss is ≈ 0. | medium |
| A9 | Duty cycle | Hip balancing = 30 % of the 6 Nm rating = 1.8 Nm. Wheel at 10 km/h: 0.30 Nm RMS at the wheel = **1.96 A** (rolling resistance ≈ 0.05 Nm plus balancing). This is half of control's 0.6 Nm continuous requirement. | medium (log in P6c) |
| A10 | Convection | Still air plus radiation: h ≈ 11 W/m²K. Rotating rotor (1090 rpm): Nu = 0.133·Re^(2/3)·Pr^(1/3) → 27 W/m²K. Hub outer surface at 2.78 m/s (flat plate, laminar): 16 W/m²K. Radiation is ≈ 5–6 W/m²K. | textbook correlations, ±30 % |
| A11 | Hub geometry | Cavity Ø100 × 45 mm (298 cm²), 3 mm printed wall (k 0.2 W/mK), 400 cm² outer area | placeholder until P2 layout |
| A12 | Driver | 6 × NTMFS5C628NL at 2.4 mΩ max, ×1.5 hot. 24 kHz PWM, 60 ns switching per cycle, 25.2 V. Two 0.5 mΩ shunts. Logic 1.5 W (electrical §3.9). | medium |
| A13 | Driver location | Hip drivers sit coaxially behind the hip motors (on-board AS5047P). Wheel drivers are **in the body** with a remote encoder at the hub (theory O9). **No driver heat inside the wheel.** | per theory O9 |
| A14 | Body | 250 × 150 × 200 mm shell (0.235 m²), 3 mm printed wall, h_in 6, h_out 10 → 1.2 K/W. Internal loads: Pi 4 6 W, buck 0.9 W, ESP32 0.7 W, all 4 drivers (6.7 W at duty, 10 W high). Lidar and camera sit outside or on the shell. | placeholder until P2 |
| A15 | Pi 4 SoC rise over local air | bare ≈ 50 K, passive heatsink ≈ 35 K, heatsink + fan ≈ 18 K under sustained load (order of magnitude from RPi white paper RP-010139 and published tests) | medium |
| A16 | Motor lumped heat capacity | 500 J/kgK × mass: MN5008 64 J/K, 8308 168 J/K | medium |

## Calculations

### 1. Motor losses and steady temperatures

**Wheel MN5008 KV170, 3.5:1.** At 10 km/h: wheel 32.7 rad/s, motor 1092 rpm, f_el 255 Hz.

| Case | I (A) | P_cu at 25 °C | P_total (hot) | T_winding sealed | T_winding Al path |
|---|---|---|---|---|---|
| 6 A, standstill | 6 | 7.3 W | — | **runaway (> 100 °C, no steady state)** | 84 °C |
| 6 A, 10 km/h (+1.4 W iron, +2.9 W gear) | 6 | 7.3 W | 13.7–15.7 W | **166 °C** | 95 °C |
| Duty, 10 km/h | 1.96 | 0.8 W | 3.2 W | 62 °C | 49 °C |
| Duty, standstill balancing | 1.96 | 0.8 W | 0.9 W | 52 °C | 40 °C |

Thermal resistance, winding → ambient: R = R_wc (1.5) + 1/(h₁·A_motor) + 1/(h₂·A_cavity) + t/(k·A) + 1/(h₃·A_out).
- Sealed: **19.7 K/W** at standstill, **8.3 K/W** at 10 km/h.
- Al path: 0.5 K/W contact + a 200 cm² finned cap at 11 W/m²K, in parallel, gives **5.4 / 4.4 K/W**.

**Max continuous current (winding 100 °C):**

| Configuration | Standstill | 10 km/h |
|---|---|---|
| Sealed | **3.5 A** | **4.9 A** |
| Al path | **6.7 A** | **7.1 A** |

At the sealed limit (3.3 W): motor can 95 °C, cavity air 66 °C, hub inner wall 44 °C. Time constant is about 21 min (sealed). 15 A peak: 55 W, i.e. 5.8 K/s in the copper alone or 0.9 K/s for the whole motor, so **15 A only for ≤ 3–5 s bursts**.

**Verdict for 6 A:** it is **not realistic as a true continuous rating in a sealed printed hub**. It is fine as a ≤ 2–3 min rating, and the actual duty needs only about 2 A. Two options:
- Set `current_lim` = 15 A (bursts only), rely on the thermistor, and **rate the sealed hub at 3.5 A continuous**.
- Or fit the Al heat path to make 6 A truly continuous.

Venting the hub (open spokes) instead was considered. With h ≈ 14 W/m²K directly on the motor, R ≈ 8 K/W at standstill, which reaches only ≈ 5 A, and it lets floor grit into the gears (materials_gears §5). **The Al path is preferred.**

**Hip 8308 KV130, 8:1.**
- Printed mount: R = 4.3 K/W (driving air 2.95 K/W).
- 3 mm Al adapter plate: 3.4 K/W.

| Case | I | P_cu at 25 °C | T_winding printed / Al | Can / housing printed / Al |
|---|---|---|---|---|
| 6 Nm continuous | 13.9 A | 12.8 W | **109** / 89 °C | **95** / 77 °C |
| Single-leg climb 5.3 Nm | 12.3 A | 10.0 W | 89 / 76 °C | 79 / 66 °C |
| Standing 2.3 Nm | 5.3 A | 1.9 W | 44 / 42 °C | 42 / 40 °C |
| 30 % load 1.8 Nm | 4.2 A | 1.2 W | 40 / 39 °C | 39 / 38 °C |

- I_max continuous: 13.2 A (5.7 Nm) with the printed mount, 14.9 A (6.5 Nm) with the Al plate.
- **If the measured Kt is 0.8 × nominal** (electrical §3.2 cross-check), 6 Nm needs 17.3 A. **Then 6 Nm is not continuous even with the Al plate.** Treat 6 Nm as a ≤ 5 min rating and 5.3 Nm (climb) as the continuous design point.

### 2. Driver, brake resistor, body, Pi 4

**Driver loss** (per board): conduction 3·(I/√2)²·R_DS,hot; switching 3·½·V·(2I/π)·t_sw·f; shunts; logic 1.5 W.

| I_phase | Loss | Rise, bare board (12.4 K/W) | Rise, 70×70×1.5 Al plate (5.5 K/W) |
|---|---|---|---|
| 2 A (wheel duty) | 1.6 W | 20 K | 9 K |
| 6 A | 1.9 W | 24 K | 10 K |
| 14 A (hip cont.) | 3.1 W | 38 K | 17 K |
| 20 A | 4.5 W | 55 K | 24 K |
| 40 A (burst) | 11.9 W | 148 K steady | 65 K steady |

The 40 A row is steady state. A 0.3 s burst is negligible because the board heat capacity is several J/K. With 52–56 °C body air (sealed), a bare board at 20 A would sit about 110 °C, above the 80 °C `fet_thermistor` derate. **The Al plate is mandatory for the hip drivers.** The wheel drivers need it only if the body stays sealed.

**Brake resistor 2 Ω:**
- Peak power: 318 W (25.2 V), 392 W (28 V, OV ramp), 450 W (30 V trip).
- Electrical's realistic events are ≤ 25 J, which heats a 12 g Al-clad body by only 2.3 K. Average power is < 5 W.
- In a fault (a lab PSU that cannot sink current plus a stuck regen, or a wrong `brake_resistance`), it takes the full V²/R. It heats at 29 K/s and reaches 200 °C in about 6 s.

**Body (sealed):** 14.3 W at duty → 52 °C air; 17.6 W (hip 14 A, wheel 6 A) → 56 °C.

**Pi 4 SoC** (soft throttle 80 °C, hard 85 °C):

| Cooling | Sealed body air (52 °C) | Ventilated body air (41 °C) |
|---|---|---|
| Bare | 102 °C | 91 °C |
| Passive heatsink | 87 °C | 76 °C |
| Heatsink + fan | 70 °C | **59 °C** |

**A sealed body fails. Use forced ventilation.**
- Flow: Q = P/(ρ·c_p·ΔT). For ΔT_air 8 K: 1.54 L/s (**3.3 CFM**). For 5 K: 2.5 L/s (5.2 CFM).
- Free vent area at ≤ 1.5 m/s: **10–16 cm² per opening (inlet and outlet)**. With a 50 % open grille that is ≈ 20–32 cm² gross.
- A 40 mm 5 V fan (about 5–7 CFM free air) is enough.
- Natural chimney alternative (0.15 m height, ΔT 15 K): 36 cm² free area each. It still leaves 50 °C air, which is not enough for a bare Pi.

### 3. Material temperature check

| Part | Expected max temp | Limit (HDT at 0.45 MPa, or practical) | Material decision |
|---|---|---|---|
| Wheel sun adapter on the rotor bell | = motor can, up to 95 °C at the sealed limit | PLA 57, PETG 69, ASA ~95, PAHT-CF 194 (170 at 1.8 MPa) | **PAHT-CF** (or Al) |
| Wheel planets, ring, carrier (in cavity air) | 50–66 °C | PAHT-CF; materials_gears derate 0.90 at 50 °C | **PAHT-CF** (PETG fallback **not** allowed if sealed and ≥ 4 A) |
| Wheel hub shell / spokes | inner wall 44 °C (limit case), motor-side boss 60+ °C | PLA creeps at about 50 °C under tyre preload | **PETG minimum, ASA preferred** (needs a draft shield on the open A1). **PLA rejected** for the hub. PLA only for a separate outer rim ring ≥ 40 mm from the motor, if the client insists. |
| Tyre | ≤ 45 °C | TPU 95A fine | TPU 95A (no change) |
| Hip motor mount / gearbox housing touching the can | 77 °C (Al plate) to 95 °C (printed) at 6 Nm continuous; 40 °C at duty | PETG 69 °C fails at continuous load | **PAHT-CF** for the mount and housing. Add a 3 mm Al adapter plate. Keep a ≥ 2 mm air gap at the rotor. PETG is only acceptable ≥ 10 mm from the can. |
| Hip gears | ≤ 60–70 °C (heat soaks from the rotor through the sun) | PAHT-CF; nylon stiffness drops above about 60–80 °C | PAHT-CF. **Materials must re-check the hip SF at 70 °C** (only 50 °C was checked). |
| Body near the drivers / brake R | 56 °C air; FET plate up to 80 °C | PLA marginal | Body shell PETG near the drivers. Driver standoffs ≥ 5 mm off plastic. Brake R ≥ 10 mm from any printed part. |

PAHT-CF (Bambu TDS V2.0): HDT 194 °C at 0.45 MPa, 170 °C at 1.8 MPa; Vicat 220 °C. Moisture lowers the stiffness. Bambu suggests annealing at 80–130 °C for 5–12 h, which is recommended for the gears.

### 4. Jump / push-off transient (adiabatic, hip)

P_cu(40 A, 80 °C) = 1.5·40²·0.0445·1.216 = **130 W**. Copper heat capacity ≈ 50 g × 385 = 19 J/K.

| Burst | Energy | ΔT copper only | ΔT whole motor |
|---|---|---|---|
| 0.115 s (control thrust) | 15 J | 0.8 K | 0.09 K |
| 0.3 s | 39 J | 2.0 K | 0.23 K |
| 2 s (stall fault) | 260 J | 13.5 K | 1.6 K |

The burst is not a thermal issue. The repetition rate is the issue: one 0.3 s push-off every 5 / 10 / 20 s adds 7.8 / 3.9 / 1.9 W average. **Rule: ≤ 1 jump per 10 s, and only while the winding is < 80 °C** (thermistor gate in the jump state machine).

### 5. Design rules for CAD (P2/P3)

1. **Wheel heat path:** 3 mm 6061 stator carrier, clamped by the stator M3 pattern, keyed to the steel axle. The axle ends in a finned Al cap (≥ 200 cm² fin area) outside the hub on the leg side. Use thermal paste or a pad at both joints. No printed part sits between the stator and the cap.
2. **Hub sealing:** keep the labyrinth seal. Do not vent the gear cavity to the floor side.
3. **Hip:** 3 mm Al adapter plate (≥ 80 × 80 mm, exposed to air) between the 8308 stator (4×M4 Ø40) and the PAHT-CF side plate. The rotor bell is open to air where the gearbox allows. Air gap ≥ 2 mm can-to-plastic.
4. **Drivers:** 70 × 70 × 1.5 mm Al plate under the FET area with a 1 mm thermal pad. Board standoffs ≥ 5 mm. Place the plate in the fan airflow path. The hip driver plate can double as the hip Al adapter plate (one part).
5. **Body vents:** a low inlet at the front/bottom (cool side, battery first) and a high outlet at the rear/top under the lidar mast. Each ≥ 16 cm² free (≥ 32 cm² gross at 50 % open), with a fine mesh against grit. One 40 mm 5 V fan pulls air **in** across the battery → Pi heatsink → drivers → out. Do not place the outlet where it blows on the IMU.
6. **Pi 4:** stick-on Al heatsink set. Place it directly in the fan stream, not above the drivers.
7. **Battery:** at the inlet (coolest air), not downstream of the drivers. LiPo ≤ 60 °C.
8. **Brake resistors:** outside the body, or bolted to the driver Al plate edge only if that plate is outside the IMU zone. ≥ 10 mm from printed parts. Leads ≥ 18 AWG silicone.
9. **IMU keep-out:** ≥ 40 mm from any motor, driver, Al driver plate, brake resistor and the fan outlet (control.md). The IMU sits in the inlet half of the airflow, so its air temperature changes slowly.
10. **Wiring:** route the thermistor pair with the encoder cable (shielded, twisted). It needs 2 extra conductors through hip and knee for the wheel motors.

### 6. Motor thermistor recommendation

- **Part:** 10 kΩ NTC, B ≈ 3950, glass-bead or 0402 on fine leads. Pot it into the stator end-turns with thermally conductive epoxy (1 per motor, 4 total).
- **Wiring:** to an ADC-capable GPIO on each XDrive Mini, with a pull-up of about 2.2 kΩ to 3.3 V. That is the geometric mean of R_NTC at 25 °C and 120 °C, for best resolution in the 60–110 °C band.
- **fw 0.5.1 config:**
  - path `axisN.motor_thermistor.config` (0.5.2+ moved it to `axisN.motor.motor_thermistor`)
  - `gpio_pin` = the chosen pin
  - set coefficients with `set_motor_thermistor_coeffs`
  - `temp_limit_lower = 80`, `temp_limit_upper = 100`, `enabled = True`
  - the stock limits are 100/120 °C, which is too high for these magnets
- **Verify it reads a value, not NaN, before trusting it** (known 0.5.1 forum issue).
- **Firmware rules:**
  - The ESP32 reads `motor_thermistor.temperature` over CAN and blocks jumps above 80 °C.
  - Wheel `current_lim` 15 A stays a burst limit. Add an ESP32-side I²t budget: e.g. a 3.5 A² RMS window over 60 s sealed, or 6.7 A with the Al path.
- Keep `fet_thermistor` at 80/100 °C (electrical §3.3).
- Brake resistor: a 10 k NTC epoxied to the resistor body, read by the ESP32 ADC. Alarm at 120 °C and open the anti-spark switch at 150 °C.

## Sources

- Bambu Lab PAHT-CF TDS (HDT 194 °C @0.45 MPa, 170 °C @1.8 MPa, annealing): https://cdn.shopify.com/s/files/1/0380/5149/files/Bambu_PAHT-CF_Technical_Data_Sheet.pdf ; V2 copy with Vicat 220 °C: https://uwaterloo.ca/rapid-prototyping-centre/sites/default/files/uploads/documents/bambu_paht-cf_technical_data_sheet_v2.pdf (verified by web search 2026-11-04)
- Raspberry Pi thermal white paper RP-010139 (Pi 4 soft throttle 80 °C, hard 85 °C): https://pip-assets.raspberrypi.com/categories/685-app-notes-guides-whitepapers/documents/RP-010139-WP-1-Use-case-specific%20thermal%20performance%20of%20Raspberry%20Pi%20SBCs.pdf ; docs PR: https://github.com/raspberrypi/documentation/pull/1348/files ; bare-Pi test throttling about 81 °C: https://www.hackster.io/news/do-you-need-to-use-a-fan-for-cooling-with-the-new-raspberry-pi-4-6d523ca12453
- onsemi NTMFS5C628NL (60 V, 2.4 mΩ, RθJC ≈ 1.3 K/W family value): https://www.onsemi.com/products/discrete-power-modules/mosfets/low-medium-voltage-mosfets/ntmfs5c628nl , https://www.onsemi.com/pdf/datasheet/ntmfs5c628nl-d.pdf
- T-Motor MN5008 (size, 24N28P, mass): https://store.tmotor.com/goods.php?id=999 ; KV170 270 mΩ, idle 0.4 A @22 V, 15 A/180 s: https://robotshop.com/products/tmotor-uav-brushless-motor-antigravity-mn5008-kv170 ; conflicting 720 mΩ listing: https://www.robozar.com/product/t-motor-antigravity-mn5008-kv170/
- ODrive motor thermistor (0.5.1 config, stock 100/120 limits, NaN issue, 0.5.2 path change): https://discourse.odriverobotics.com/t/axis-error-over-temp/6785 , https://discourse.odriverobotics.com/t/motor-thermistor-temperature-reads-nan-without-any-errors/5514 , https://www.github.com/odriverobotics/ODrive/releases/tag/v0.5.2-rc_2
- Project inputs: theory.md (O9, A9, hip torques), electrical.md (§3.2, §3.3, §3.9), materials_gears.md (A5, material table), control.md (IMU ≥ 40 mm).
- Convection correlations (rotating cylinder, laminar flat plate, chimney flow): standard heat-transfer texts (Incropera, *Fundamentals of Heat and Mass Transfer*). Not web-verified.

## Open questions

1. **Electrical:** which XDrive Mini header pins are ADC-capable for the motor thermistor? Is `AUX_TEMP` an on-board sensor or a free input? This could not be confirmed (Makerbase manual returns HTTP 403).
2. **Measure on arrival (P6a):** R_ll of MN5008 KV170 (270 vs 720 mΩ), and 8308 KV130 R and Kt. Run a heat-run: 30 min at 3.5 A in a sealed prototype hub with the thermistor, and fit R_th and τ. All R_th values here are ±30–50 %.
3. **Materials:** re-check the hip gear SF at 70 °C, and the wheel gears at 66 °C cavity air (currently 40/50 °C).
4. **Mechanical (P2):** is there room for the Al stator carrier plus an external finned cap within the wheel width and the leg clearance? The added mass is about 25–35 g per side (unsprung), which BOM must log.
5. **Control:** confirm the 0.30 Nm RMS wheel duty and the 1.8 Nm hip duty from the P5 sim and P6c logs.
6. **Client:** the hub material changes from PLA/ABS to PETG/ASA (PLA only for a separate outer rim ring). Approval is needed.

## Changes to design assumptions

| Was | Now |
|---|---|
| Wheel continuous 6 A (O9, 40 % of the 15 A rating) | **3.5 A continuous in a sealed printed hub**. 6 A only with the Al heat path (6.7 A), or for ≤ 2–3 min |
| Wheel 15 A current limit | Kept, but as a **≤ 3–5 s burst** limit plus an ESP32 I²t budget |
| Hip 6.1 Nm continuous (theory) | **5.7 Nm** with a printed mount; 6.5 Nm with a 3 mm Al adapter plate. If Kt = 0.8 × nominal: ≈ 5.3 Nm |
| Hip/wheel gear temperature 50 / 40 °C (materials A5) | **Hip ≤ 70 °C, wheel ≤ 66 °C** (sealed limit) → re-check SF |
| Wheel hub PLA/ABS (client), PETG preferred (materials) | **PETG minimum, ASA preferred; PLA rejected near the motor.** Sun adapter, ring and carrier in PAHT-CF |
| Gear/motor-mount housings PETG | **PAHT-CF where in contact with the motor can** |
| Closed electronics bay (passive) | **Ventilated bay: 40 mm fan ≥ 3.3 CFM, inlet/outlet ≥ 16 cm² free each, Pi heatsink** |
| Driver heatsink "≥ 1.5 mm Al plate" (electrical) | Confirmed: **70 × 70 × 1.5 mm**, mandatory for the hips |
| Motor thermistor "if fitted" (control) | **Mandatory on all 4 motors**, limits 80/100 °C, jump gated at 80 °C |
| No brake resistor temperature monitoring | **NTC on each brake resistor**, cut-off at 150 °C |
