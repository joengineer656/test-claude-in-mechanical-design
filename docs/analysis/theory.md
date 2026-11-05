# Robot Theory — P1 Calculations (rev 1, 2026-11-04)

Author: Robot Theory Engineer. Scope: PLAN.md §4b items 1–4 (+ landing loads for Structural, CoM target).
Evidence: `docs/analysis/calc/theory_calc.py` (numpy only), full output in `docs/analysis/calc/theory_calc_output.txt`.
Re-run: `python3 theory_calc.py` (≈20 s; leg synthesis uses a fixed random seed, so the output does not change between runs).
No CAD was done. All numbers are per robot unless "per leg"/"per wheel" is stated.

---

## 1. Summary — recommended numbers

| Item | Recommendation | Basis / margin |
|---|---|---|
| **Motor variant** | **Eaglepower LA8308 KV130, all 4 motors** (one variant = interchangeable spares, one ODrive config) | KV90 cannot reach 12 km/h at 4–6:1 on ODrive v3.6 (70 % modulation limit), see §3.2 |
| Kt (KV130) | 8.27/130 = **0.0636 Nm/A** (KV90: 0.0919) | ODrive convention |
| Wheel diameter | **Ø170 mm** (r = 85 mm) | fits Ø92 motor + ~Ø100 ring gear + rim + 25–30 mm TPU tyre |
| **Wheel gearbox** | **4:1 single-stage planetary** (e.g. sun 18 / planet 18 / ring 54) | 13.3 km/h loaded at 19.8 V, 15.0 km/h at 22.2 V; peak wheel torque 9.2 Nm (7.6× traction limit) |
| **Hip gearbox** | **8:1** (single-stage, e.g. 12/36/84, or compound) | Jump sim 26.4 cm @19.8 V with springs (17.8 cm without); 6.1 Nm continuous, 17.3 Nm peak |
| Leg 4-bar | thigh 121, knee→wheel 189, coupler 113, knee→coupler pin 42 mm, body pivot B at (+46, +34) mm from hip | hip height above axle 100→290 mm over 74° hip rotation; wheel drifts only 18 mm horizontally |
| Leg heights (hip above axle) | crouch 100 / nominal 200 / extended 290 mm | robot height ≈ 85 + 290 + ~125 (body + lidar above hip) = 500 mm |
| **Snappers (springs)** | 1 extension spring per leg, body → thigh crank r_a = 40 mm: **k ≈ 2.7 N/mm, preload 8 N, max 146 N, working extension 52 mm**; 4.0 J/leg, 8 J total | ≈ 43 % of the 18.6 J jump energy; hip motors deliver the rest |
| Jump energy | 15.8 J ideal, **18.6 J** with 85 % linkage/spring efficiency | 3.6 kg, CoM rise 0.20 m, hub unsprung 1.44 kg |
| Landing design loads | see §3.6 load cases LC-A…LC-D | controlled landing 6.4 g on body, 18 g on hub; fault case 12 g |
| Hub vs belt | **Keep the hub** (client's choice) with the mitigations in §3.7 | belt saves 3.2 J of jump energy and 30 % axle load but adds 0.12 kg, a belt through two pivots and more parts |
| CoM target | body CoM 230 mm above axle (whole robot ≈ 140 mm), fore-aft over axle within ±5 mm, lateral ≤ 5 mm | §3.8 |
| Peak currents | 40 A per motor (limit set in ODrive), hips ≤ 56 A from battery for ≈ 70 ms in a jump | goes to the Electrical engineer |

**Fallback if the client already owns KV90 motors:** wheels **3:1** (12.7 km/h at 22.2 V, 11.1 km/h at 19.8 V loaded), hips **5:1** (25.4 cm jump @19.8 V with springs). With KV90, all of the requested 4/5/6:1 wheel ratios fail 12 km/h.

---

## 2. Assumptions

| # | Assumption | Value | Confidence / owner |
|---|---|---|---|
| A1 | Total mass | 3.6 kg (target), 4.0 kg checked | BOM eng. |
| A2 | Unsprung mass per side (hub) | 0.721 kg = motor 336 + gearbox 110 (steel pins) + rim+tyre 210 + axle/bearings 40 + ½ shank 25 g | estimate; **control sim uses 0.50 kg, so it must be updated** |
| A3 | Unsprung per side (belt alternative) | 0.315 kg, plus 0.06 kg/side of belt hardware on the body | estimate |
| A4 | Rotor inertia, one 8308 | 2.0e-4 kg m² (0.14 kg rotor at r_g 38 mm) | estimate ±40 %; measure |
| A5 | Wheel + tyre + carrier inertia | 1.0e-3 kg m² per wheel | estimate |
| A6 | Usable voltage | ODrive v3.6: max speed ≈ **KV × 0.7 × Vbus** (70 % modulation) | ODrive docs (source list) |
| A7 | Battery | 22.2 V nominal, 19.8 V loaded/low, 25.2 V full | client |
| A8 | Motor current | peak 40 A (few s, set in ODrive); continuous: wheel 11 A, hip 14 A (22 A drone rating derated, because there is no propeller airflow) | Electrical + Thermal to confirm the driver limit |
| A9 | Phase resistance | KV90: 0.186 Ω line-line (listing); KV130 scaled with 1/KV² → 0.089 Ω (assumes the same copper fill) | medium-low; measure with ODrive |
| A10 | Gear efficiency | wheel 1-stage printed planetary 0.90 forward / 0.85 back-drive; hip 0.85 | typical for greased printed planetary |
| A11 | Tyre | μ = 0.8, C_rr = 0.03, radial stiffness 12 kN/m per wheel | estimate; measure the printed TPU tyre |
| A12 | Aero | C_d·A = 0.9 × 0.30 × 0.45 m² | small effect |
| A13 | Body CoM | 230 mm above axle at nominal stance, pitch r_g 120 mm | layout target |
| A14 | Jump | "20 cm" = wheel clearance = CoM rise with the legs locked straight. Tucking the legs in flight is **not** counted (it is extra margin) | conservative |
| A15 | Motor model | DC-equivalent: V_eff = Ke·ω + I·R_ll, I ≤ 40 A; inductance ignored (unknown) | adequate for P1 |
| A16 | Balance headroom | at top speed, 30 % of peak torque stays free for balancing | design rule |

---

## 3. Calculations

### 3.1 Eaglepower 8308 — verified data

No manufacturer (Eaglepower) datasheet could be found online. All data comes from retailer and marketplace listings.

| Parameter | Value | Source | Confidence |
|---|---|---|---|
| Dimensions | Ø92 × 28.5 mm; stator 4×M4 on Ø40; rotor 4×M3 on Ø40; adapter Ø31, 4×Ø3 | client drawing 51fNBSpzq5L.jpg | high |
| Model name | "Eaglepower LA8308" ("8308" = stator/iron-core size) | robu.in listing | high |
| KV variants offered | **90, 130, 160, 180, 205** | accio.com / accio.ai marketplace listings | medium (more than one marketplace, not the manufacturer) |
| KV100 / KV150 | **not found** for the Eaglepower 8308 (those KVs belong to other brands, e.g. LigPower XU8) | searches | — |
| Internal resistance (KV90) | 0.186 Ω (very likely line-to-line) | robu.in | medium-low |
| Max continuous current (KV90) | 22 A | robu.in | medium-low (drone rating, with propeller cooling) |
| Max continuous power (KV90) | 900 W | robu.in | medium-low |
| Idle current | 0.6 A @ 24 V | robu.in | medium-low |
| Mass | 336 g (motor); 0.59 kg is the shipping weight | robu.in | medium |
| Voltage | 6–12S | robu.in | medium |
| Poles | 40 (20 pole pairs) | accio.ai page title only | **low** (8308 motors are often 36N40P or 36N42P, so check with ODrive calibration) |
| Inductance | not published | — | measure |

**Kt = 8.27 / KV** (ODrive `torque_constant`, Nm per A of Iq):

| KV | Kt Nm/A | T at 40 A | no-load rpm at 0.7×22.2 V | at 0.7×19.8 V |
|---|---|---|---|---|
| 90 | 0.0919 | 3.68 Nm | 1399 | 1247 |
| 130 | 0.0636 | 2.54 Nm | 2020 | 1802 |
| 160 | 0.0517 | 2.07 Nm | 2486 | 2218 |

**Why KV130:**
- The wheel needs 12 km/h ⇒ ω_w = 3.333/0.085 = 39.2 rad/s = 375 rpm.
- With KV90 on ODrive v3.6 at 19.8 V, the motor tops out at 1247 rpm no-load. So N ≤ 3.3 even before any load, and every requested ratio (4/5/6:1) misses the target.
- KV130 gives 1.44× the speed. The torque lost is irrelevant at the wheel because the **wheel torque is traction-limited**: μ·M·g·r/2 = 0.8·3.6·9.81·0.085/2 = **1.2 Nm per wheel**, while KV130 at 4:1 gives 9.2 Nm peak.
- The motor constant (Nm/√W) does not depend on KV for the same frame, so heat per Nm is the same. The cost of KV130 is 1.44× more current for the same torque. The Electrical engineer must confirm the 40 A driver limit.
- KV160 would also work but needs 1.8× the current. KV130 is the best compromise.
- Using one variant for hips and wheels keeps spares interchangeable.

### 3.2 Wheel gearbox comparison (KV130, Ø170, hub layout)

Formulas:
- no-load speed: v₀ = (KV·0.7·V)·(2π/60)/N · r
- loaded speed: the highest v at which min(40 A, (0.7V − Ke·ω_m)/R_ll)·Kt ≥ resistive torque/(Nη) + 0.3·Kt·40 A
- continuous wheel torque: T_c = Kt·11 A·N·η; peak wheel torque: T_p = Kt·40 A·N·η
- torque-limited acceleration: a = 2T_p/(r·m_eff), with m_eff = M + 2(I_w + N²I_r)/r²
- balance criterion (linearised wheel-inverted pendulum, θ̈ ≤ 0 reachable): τ ≥ m_b g l sinθ / (1 + m_b l/(m_eff r)); traction caps the tilt at atan μ = 39°

| N | V | no-load km/h | loaded km/h | T_wheel cont / peak Nm | a_torque / a_max m/s² | recoverable tilt (traction / torque) | torque margin 2T_p/(m_b g l) | reflected rotor N²J_r kg m² | ≥12 km/h? |
|---|---|---|---|---|---|---|---|---|---|
| **4:1** | 22.2 | 16.2 | **15.0** | 2.52 / 9.16 | 45 / 7.8 | 39° / 90° | 3.8 | 0.0032 | yes |
| **4:1** | 19.8 | 14.4 | **13.3** | | | | | | **yes** |
| 5:1 | 22.2 | 12.9 | 12.0 | 3.15 / 11.45 | 51 / 7.8 | 39° / 90° | 4.7 | 0.0050 | marginal |
| 5:1 | 19.8 | 11.5 | 10.6 | | | | | | no (≥10 only) |
| 6:1 | 22.2 | 10.8 | 10.0 | 3.78 / 13.74 | 55 / 7.8 | 39° / 90° | 5.6 | 0.0072 | no |
| 6:1 | 19.8 | 9.6 | 8.9 | | | | | | no |

KV90 for comparison (loaded km/h at 22.2 / 19.8 V): 4:1 → 9.6 / 8.4; 5:1 → 7.7 / 6.7; 6:1 → 6.4 / 5.6; 3:1 → 12.7 / 11.1.

**Recommendation: 4:1.**
- It is the only requested ratio that holds ≥ 12 km/h at low battery with 30 % balance headroom.
- All ratios have a torque surplus of 4–6×, so torque does not decide the choice.
- Back-drivability: 4:1 has the lowest reflected inertia (0.0032 vs 0.0072 kg m² at 6:1) and the lowest back-drive friction. This gives better impact tolerance and better torque transparency for balancing.
- A 1-stage 4:1 planetary (ring/sun = 3) is easy to print. Planet pins must be steel (see materials report).

### 3.3 Leg geometry (4-bar) and hip torque

Synthesis method:
- 120 000 random candidates were scored on wheel x-drift, transmission angle (35–145°), lever-arm ratio, links staying above the axle and reach ≤ 150 mm.
- The thigh is driven at hip H (0, 0). The coupler runs from body pivot B to point C on the shank. The shank is a rigid K–C–W lever (the C pin is 42 mm from the knee, 175° from the K→W line).

| hip height above axle (mm) | thigh angle | wheel x vs hip (mm) | J = dy/dφ (mm/rad) | knee K (mm) | pin C (mm) |
|---|---|---|---|---|---|
| 101 (crouch) | 0° | −38 | 219 | (121, 1) | (158, 21) |
| 150 | −14° | −28 | 172 | (117, −29) | (152, −5) |
| 199 (nominal) | −32° | −29 | 145 | (102, −64) | (134, −36) |
| 250 | −54° | −41 | 119 | (71, −98) | (99, −66) |
| 289 (extended) | −74° | −42 | 117 | (33, −116) | (53, −79) |

- The wheel stays 27–46 mm behind the hip, so the hip must be placed about 30 mm in front of the desired axle line (see CoM, §3.8).
- Transmission angle is 35–148°. This is acceptable but near the limit at crouch, so CAD should refine B by ±10 mm.
- These lengths are a P1 starting point for the P2 master layout, not frozen parts.

Hip torque per leg: T = F·J. This was cross-checked against full pin statics (1.538 = 1.538 Nm).

| Case | Leg force per leg | Hip torque crouch / nominal / extended | Worst |
|---|---|---|---|
| Standing, W_b/2 (m_b = 2.16 kg) | 10.6 N | 2.34 / 1.54 / 1.25 Nm | **2.3 Nm** |
| Height change at +0.5 g | 15.9 N | 3.51 / 2.31 / 1.87 | **3.5 Nm** |
| Single-leg climb (75 % W_b × 1.5 dyn) | 23.8 N | 5.26 / 3.46 / 2.81 | **5.3 Nm** |
| Jump push-off (sim, motor share) | — | — | up to 17.3 Nm (current-limited) |
| Landing LC-C (one wheel first) | 121 N | — | 15.2 Nm (12.9 Nm from the motor) |

**Hip ratio: 8:1 with KV130.**

| N_hip (KV130) | jump @22.2 V spring / none | jump @19.8 V spring / none | T_cont / T_peak (Nm) |
|---|---|---|---|
| 7:1 | 33.3 / 25.5 cm | 29.2 / 21.2 cm | 5.3 / 15.1 |
| **8:1** | **30.2 / 21.9** | **26.4 / 17.8** | **6.1 / 17.3** |
| 9:1 | 27.5 / 18.6 | 24.0 / 14.7 | 6.8 / 19.5 |
| 10:1 | 25.2 / 15.7 | 22.1 / 12.2 | 7.6 / 21.6 |

- Lower ratios jump higher, because the push-off is limited by speed and back-EMF, not by torque.
- 8:1 is the highest ratio that keeps ≥ 30 % jump margin at low battery with springs. The sim leaves out linkage friction and the energy of the leg links, so real heights will be about 15–20 % lower: ≈ 22 cm at 19.8 V.
- Continuous torque is 6.1 Nm, which is above the 5.3 Nm single-leg case.
- At 4.0 kg (hard limit) the sim gives 26.9 cm, because a heavier body loses less energy to the snatch.
- Without springs, 8:1 reaches ≈ 18–22 cm only. **The springs are needed for a reliable 20 cm.**

### 3.4 Snappers (springs)

Energy:
- take-off velocity v = √(2·g·0.20) = 1.98 m/s
- the body (2.16 kg) must reach v_b = v·M/m_b = 3.30 m/s before the 1.44 kg unsprung mass is snatched off the ground (inelastic momentum transfer)
- E = m_b·g·s + ½m_b·v_b² = 2.16·9.81·0.19 + ½·2.16·3.30² = **15.8 J**, of which 4.7 J is lost in the snatch
- with 85 % efficiency: **18.6 J**

Split:
- springs 8.0 J (43 %), hip motors 10–14 J (sim)
- Springs larger than this would push much harder than gravity at nominal stance, so the hips would have to hold them down continuously

Spring law (per leg, torsion-equivalent at the hip): T_s = T0 + k_θ·|φ − φ_ext|, with T0 = 0.30 Nm and k_θ = 4.27 Nm/rad over 74° of hip rotation.

| Point | Spring torque | Gravity torque | Hip motor must hold |
|---|---|---|---|
| Extended | 0.30 Nm | 1.25 Nm | — |
| Nominal | 3.41 Nm | 1.54 Nm | 1.89 Nm out → **4.4 A** continuous (≈ 1.7 W I²R per hip) |
| Crouch (loaded) | 5.85 Nm | 2.34 Nm | 3.53 Nm → 8.2 A (only for the ≈ 1 s before a jump) |

**Physical spring:** an extension spring between a body anchor and a crank arm on the thigh (r_a = crank radius, spring roughly ⟂ to the crank).

| r_a | k_lin | Preload F0 | F max (crouch) | Working extension |
|---|---|---|---|---|
| 30 mm | 4.7 N/mm | 10 N | 195 N | 39 mm |
| **40 mm (recommended)** | **2.7 N/mm** | **8 N** | **146 N** | **52 mm** |
| 50 mm | 1.7 N/mm | 6 N | 117 N | 65 mm |

- **Type:** extension spring, steel music wire. Or 2 parallel springs of 1.35 N/mm each per leg for redundancy and packaging. An extension spring is chosen because hooks are easy to attach to printed parts and it needs no guide rod. A torsion spring at the hip would put a 5.9 Nm reaction on printed lugs.
- **Placement:** body side plate to the thigh crank. **The spring must act directly between body and thigh, in parallel with the gearbox, so that spring load never passes through the gear teeth.**
- **Attachment loads:** 146 N max, 1.5× dynamic → **≈ 220 N design force** at each hook pin. This is a load for Structural (steel pins Ø3–4 mm, not printed hooks).
- Free length, wire size and fatigue life are chosen from a catalogue once the CAD gives the anchor geometry. Target: ≥ 10⁴ cycles at 146 N.
- **Safety:** with power off, the springs extend the legs. Add a mechanical pin-lock for transport and an e-stop procedure.

### 3.5 Jump cycle numbers (KV130, hip 8:1, 19.8 V, springs)

- Push-off time ≈ 71 ms, hip motors at the 40 A limit
- Battery current ≤ 56 A for ≈ 70 ms (hips only) → given to Electrical
- Body leaves at 3.3 m/s and the CoM rises 26 cm (simulated, idealised)

### 3.6 Landing load cases (for the Structural engineer)

Model:
- Drop from a 20 cm apex: v = 1.98 m/s, landing with the legs at 270 mm.
- Vertical 2-mass model. The tyre is 12 kN/m. The leg is the physical spring plus the motor's virtual spring-damper (k = 280·m_supported N/m, ζ = 0.6), capped by the motor torque.
- End stop: 25 kN/m bumper 5 mm before crouch.
- Pin forces come from 4-bar statics with a vertical ground force only. **Add a horizontal ground force of μ·F_axle for sliding landings.**

| LC | Case | Body g | Unsprung g | Axle N | Leg N | Hip torque total / motor (Nm) | Knee pin N | Coupler N | Hip bearing N | Stroke mm | Hip gear torque (Nm) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | symmetric, controlled (normal) | 6.4 | 18 | 171 | 68 | 8.5 / 6.3 | 252 | 193 | 252 | 60 | 6.3 |
| **B** | symmetric, motors off → end stop (fault) | 12.1 | 20 | 162 | 128 | 28.0 / 0 | 867 | 842 | 867 | 169 | 17.2 (rotor inertia) |
| **C** | one wheel first, controlled | 5.7 | 16 | 191 | 121 | 15.2 / 12.9 | 450 | 344 | 450 | 61 | 12.9 |
| **D** | one wheel first, motors off (worst abuse) | 10.9 | 20 | 293 | 232 | 50.8 / 0 | 1572 | 1528 | 1572 | 173 | 4.5 |
| A' | belt layout, controlled (comparison) | 5.5 | 24 | 121 | 83 | 10.0 / 8.1 | 311 | 235 | 311 | 61 | — |

Gear-tooth loads:
- **Hip gearbox:** design torque **17.3 Nm** (motor peak × 8 × η), plus LC-B rotor-inertia spike 17.2 Nm ⇒ use **20 Nm ultimate** at the output, cyclic 13 Nm (LC-C).
- **Wheel gearbox (4:1):**
  - Motor peak at the output is 9.2 Nm.
  - Spin-up at landing with slip: μ·F_axle·r = 0.8·191·0.085 = 13 Nm, of which 76 % goes through the gear (inertia share N²J_r/(N²J_r + J_w)) ⇒ **≈ 10 Nm design torque**.
  - The controller should match wheel speed to ground speed before touchdown.
- Vertical axle load (≤ 293 N, LC-D) must go **into the axle bearings, never into the gears or the motor bearings**.

The end-stop cases B/D give large pin forces because the 4-bar has its poorest leverage at crouch. Recommendation to Structural/Mechanical:
- Use LC-A/C as fatigue/normal loads and LC-D × SF 1.5 as the ultimate load.
- Put a compliant end stop (TPU bumper) at ~120 mm hip height, not at full crouch.

### 3.7 Hub motor vs motor-on-body + belt

| Quantity | Hub (client) | Body + belt | Effect |
|---|---|---|---|
| Unsprung per side | 0.721 kg (40 % of M) | 0.315 kg (17 %) | hub snatch loss 4.7 J vs 1.5 J |
| Total mass | 3.60 kg | 3.72 kg (+belt, pulleys, tensioner) | belt costs +0.12 kg against the 4 kg limit |
| Jump energy needed | 15.8 J | 14.5 J | hub needs +9 % |
| Leg inertia about hip | 0.029 kg m² (+0.013 reflected hip rotor) | 0.013 (+0.013) | hub legs swing 1.3× slower (t ∝ √I): 58 vs 45 ms for 40° at 17 Nm |
| Wheel-hop mode √(k_t/m_u) | 129 rad/s (20 Hz) | 195 rad/s (31 Hz) | both ≫ balance bandwidth (~4 Hz) |
| Wheel rotational inertia (incl. 16·J_r) | 4.2e-3 kg m² | same | reflected rotor inertia is the **same for belt and hub at the same ratio**, so it is not a hub drawback |
| Pendulum unstable pole | 7.2 rad/s | 8.1 rad/s | needed balance bandwidth ≈ 3× pole: ~22–25 rad/s; easy for both |
| Recoverable tilt | traction-limited 39° | 39° | same |
| Landing axle load (LC-A) | 171 N, 18 g on motor | 121 N, 24 g on the light wheel | hub motor magnets and bearings see ~20 g shocks |
| Complexity | wires (3 phase + 6 encoder) pass through 2 pivots | belt over 2 moving pivots, tension changes with the 4-bar, more parts | — |

**Recommendation: keep the hub.**
- The jump target is met with margin (sim 26 cm at low battery), and the balance dynamics are essentially unchanged.
- The belt's gains (−3 J, −50 N axle load) do not justify +0.12 kg and a belt routed through a moving 4-bar.

**Required mitigations for the hub:**
1. Wheel axle on 2 deep-groove bearings that take all radial/axial load. Motor bearings and gear teeth carry torque only.
2. Keep the unsprung mass ≤ 0.72 kg/side: hollow printed rim, light TPU tyre with lattice holes, no metal ring gear.
3. TPU tyre with ≥ 8–10 mm radial compliance (sets the 18 g figure; a stiffer tyre raises it).
4. Landing controller (virtual spring-damper, LC-A) and wheel-speed matching before touchdown.
5. Steel planet pins, glued/retained encoder magnet, motor magnets inspected after every jump test series.
6. Phase and encoder cables routed along the hip and knee pivot axes with strain relief (flex life). Consider putting the AS5047P on the hub with a short shielded cable.
7. Mechanical end stop at ~120 mm hip height (see §3.6).

### 3.8 Centre-of-mass target

- **Height:**
  - Body CoM 230 mm above the axle at nominal stance (hip 200 mm above axle) → about 315 mm above ground.
  - Whole robot (incl. 1.44 kg unsprung at axle height): (2.16·0.23)/3.6 ≈ **140 mm above axle** (≈ 225 mm above ground).
  - Do not lower the body CoM below ~180 mm above the axle: the unstable pole rises and the balance loop gets harder. Higher is easier to balance but needs more stroke for height changes.
- **Fore-aft:**
  - Body CoM over the wheel axle within **±5 mm** at nominal stance.
  - Because the axle sits 29 mm behind the hip (4-bar), the CoM must be 29 mm behind the hip axis.
  - Across the 100–290 mm stroke the axle moves 18 mm, so the controller compensates with ≤ 4.5° body pitch (atan(18/230)).
  - The battery rail gives ±20 mm trim.
- **Lateral:**
  - |y_CoM| ≤ **5 mm** from the mid-plane. On a 240 mm wheel track (centre to centre) this gives ≤ ±4 % wheel-load imbalance (2e/track).
  - Mirror the left/right drivers and run the cables symmetrically.

---

## 4. Sources

- Eaglepower LA8308 KV90 (robu.in): resistance 0.186 Ω, 22 A, 900 W, 336 g, 6–12S, 92×28.5. https://robu.in/product/eaglepower-la-8308-kv90-motor/ (page returns 403 to automated fetch; values taken from the search-engine index of the page)
- EaglePower 8308 90kV "40 poles", KV90/130/160/180/205 variants. https://www.accio.ai/find-product/eaglepower-8308-90kv-40-poles
- Eaglepower 90kV BLDC marketplace listing (KV variant list). https://fr.accio.com/plp/eaglepower-90kv-bldc-motor
- ODrive v0.5.4 specifications: max rpm ≈ KV × 0.7 × Vbus. https://docs.odriverobotics.com/v/0.5.4/specifications.html
- ODrive comparison table: v3.6 max modulation 70 %, v3.6 end-of-life. https://docs.odriverobotics.com/v/latest/hardware/odrive-comparison.html
- ODrive forum, v3.6 speed limit. https://discourse.odriverobotics.com/t/speed-limit-odrive-v3-6/11007
- ODrive forum, v3.6 R/L measurement accuracy (T-Motor R100). https://discourse.odriverobotics.com/t/difference-in-measurements-between-odrive-and-multimeter-t-motor-r100-kv90/9612
- ODrive torque constant convention Kt = 8.27/KV: ODrive docs, `motor.config.torque_constant`. https://docs.odriverobotics.com/v/latest/
- Reference robot (Ascento): https://www.inceptivemind.com/two-wheeled-jumping-robot-ascento-uneven-surfaces/13666/
- Client inputs: Requariment.txt, BOM File.txt, DECISIONS.md, 51fNBSpzq5L.jpg

---

## 5. Open questions

1. **Client:** which KV is printed on the motors you have, or will buy? This report recommends **KV130 for all 4**. If KV90 is already bought: wheels must be 3:1 (outside the requested 4/5/6 set) and hips 5:1.
2. **Client:** the hub layout is kept. The belt alternative is documented in §3.7, but no change is requested.
3. **Electrical:** can the MKS XDrive Mini supply 40 A peak per motor? Can the battery deliver ≥ 60 A bursts plus the wheel load? (KV130 needs 1.44× the current of KV90 for the same torque.) Does the Mini firmware keep the 70 % modulation limit? Is ODrive v3.6 being end-of-life a support risk? electrical.md uses 0.8×KV×Vbus, but this report uses the ODrive-documented 0.7. Agree on one value. Both reports independently conclude KV ≥ 130. electrical.md also reports 20 pole pairs from community configs and a ~40 A practical peak, which matches A8.
4. **Control:** update `sim_lqr_2d.py` m_wheel 0.50 → **0.72 kg**, N = 4, and use the motor KV130 Kt = 0.0636.
5. **BOM:** 4 motors = 1.34 kg (37 % of 3.6 kg) and unsprung mass is 1.44 kg. Confirm the 110 g gearbox and 210 g wheel+tyre budgets.
6. **Measure on arrival:** R, L, pole pairs (ODrive calibration), KV (spin-down test), rotor inertia (spin-down with a known torque), real continuous current inside the wheel (Thermal).
7. **Mechanical:** refine the 4-bar in CAD (transmission angle 35° at crouch). Choose the spring from a catalogue once the anchor points are fixed.

## 6. Changes to design assumptions

| Was (PLAN rev 0/1) | Now | Why |
|---|---|---|
| KV ≈ 90 assumed | **KV130 recommended** (KV90 = fallback with a 3:1 wheel) | ODrive v3.6 70 % modulation limit; KV90 cannot reach 12 km/h at 4–6:1 |
| Wheel ~4:1 first estimate | **4:1 confirmed** (KV130) | only requested ratio meeting 12 km/h at 19.8 V |
| Hip ~9:1 two-stage | **8:1** (single stage possible) | jump is speed-limited; 9–10:1 lose 3–5 cm |
| Jump energy ~16 J at 50 % efficiency | **15.8 J ideal / 18.6 J at 85 %**, of which 4.7 J is lost to hub unsprung mass | explicit two-mass momentum model |
| Wheel Ø160–180 | **Ø170** | — |
| Landing 3–5 g (PLAN §5) | **6.4 g body / 18 g hub (normal), 12 g body fault** | 2-mass landing sim; Structural must use §3.6 |
| Control sim m_wheel 0.50 kg | **0.72 kg/side** | itemised unsprung estimate |
| Spring "preloaded when leg folds" | spring acts in parallel to the gearbox, body→thigh, always engaged, 8 J total | keeps spring load off the gear teeth |

---

## P1 follow-up (O9) — wheel hub motor selection (rev 2, 2026-11-04)

Client decisions (DECISIONS.md):
- 8308 KV130 on the **hips only**
- a lighter (~170 g class) motor in each wheel hub
- one 6S 2200 mAh 50C pack

Evidence: `calc/o9_wheel_motor.py` → `calc/o9_output.txt` (reuses `theory_calc.py`).

### Requirements applied

| Requirement | Value | Source |
|---|---|---|
| Peak torque at the wheel | ≥ 2.0 Nm | control.md R-W1 |
| Continuous torque at the wheel | ≥ 0.6 Nm | control.md R-W1 |
| Top speed | 12 km/h at 19.8 V, with the ODrive v3.6 limit of 0.7·KV·Vbus | manager |
| Speed headroom (control rule) | N ≤ 0.85·(0.7·KV·19.8)·(2π/60)·r/(3.33 + 1.0) | control.md §9 |
| Torque oversizing | not needed: grip caps the total at ≈ 2.4–2.7 Nm | control.md §9 |
| Wheel | Ø170 kept (r = 85 mm) | — |
| Encoder | needs a shaft end or rotor centre for the diametric magnet | manager |

Model assumptions:
- Peak current = manufacturer 180 s rating (and ≤ 40 A).
- Continuous current = 40 % of that rating, because the motor is enclosed in the wheel.
- Printed 1-stage planetary: η = 0.90, 60–75 g with steel pins.
- Per-side unsprung mass = motor + gearbox + rim/tyre 210 g + axle/bearings 40 g + ½ shank 25 g.

### Candidates (sourced)

| Motor | KV | Mass | R (line-line) | Peak current (180 s) | Size / poles / shaft | Confidence |
|---|---|---|---|---|---|---|
| **T-Motor MN5008 KV170** | 170 | **128 g** | 270 mΩ | 15 A | Ø55.6 × 32 mm, 24N28P (14 pole pairs), 6 mm shaft | high: mass, R, size (T-Motor store); medium: peak current (retailer) |
| T-Motor MN5008 KV340 | 340 | 135 g | 55 mΩ | 35 A | same as above | high (T-Motor store) |
| T-Motor MN6007 II KV160 | 160 | 159 g | 227 mΩ | 18 A | Ø67.2 × 26.1 mm, 6 mm shaft | medium: the 227 mΩ / 18 A values come from the MN6007 / 6007II-X pages |
| iPower GM5208-12 (gimbal, direct drive) | ≈ 25 (estimated, **not listed**) | 195–209 g | 15.2 Ω | ~1.5 A | Ø63, 12N14P, 12 mm hollow shaft | medium: mass, R (iFlight) |

### Comparison at 19.8 V (selected rows; full table in o9_output.txt)

| Motor | N | Loaded km/h (30 % headroom) | Peak / cont at wheel (Nm) | R-W1 | Control rule (N_max) | Unsprung per side |
|---|---|---|---|---|---|---|
| Any motor, direct drive | 1:1 | — | 0.3–0.9 / ≤ 0.37 | **FAIL** | — | 0.40–0.48 kg |
| MN5008 KV170 | 3:1 | 22.4 | 1.97 / 0.79 | FAIL (just) | ok (4.11) | 0.463 kg |
| **MN5008 KV170** | **3.5:1** | **19.3** | **2.30 / 0.92** | **ok** | **ok (4.11)** | **0.465 kg** |
| MN5008 KV170 | 4:1 | 17.0 | 2.63 / 1.05 | ok | ok, but only 3 % margin | 0.468 kg |
| MN5008 KV170 | 5:1 | 13.6 | 3.28 / 1.31 | ok | FAIL | 0.473 kg |
| MN5008 KV340 | 4:1 | 35.6 | 3.06 / 1.23 | ok | ok (8.23) | 0.475 kg |
| MN5008 KV340 | 6:1 | 24.0 | 4.60 / 1.84 | ok | ok | 0.485 kg |
| MN6007 II KV160 | 3.5:1 | 18.3 | 2.93 / 1.17 | ok | ok (3.87) | 0.496 kg |
| MN6007 II KV160 | 4:1 | 16.0 | 3.35 / 1.34 | ok | FAIL | 0.499 kg |

**Direct drive is ruled out.** The best light outrunner gives ≤ 0.9 Nm, and gimbal motors give ≈ 0.3 Nm (15 Ω limits the current to < 1 A). R-W1 needs 2.0 Nm.

### Recommendation: T-Motor MN5008 KV170 + 3.5:1 single-stage planetary

**Why this motor:**
- It is the lightest candidate (128 g).
- Its lower current per Nm keeps it well inside the 40 A driver limit. KV340 would need ≈ 2× the current for the same torque.
- It meets R-W1 with 15 % margin. Grip caps the useful torque at ~1.3 Nm per wheel anyway.
- It meets the control headroom rule with 17 % margin (3.5 vs 4.11). 4:1 also passes, but with only 3 % margin, and a ±5 % KV tolerance would break it.

**Gearbox:**
- Example teeth: sun 20 / planet 15 / ring 50 (1 + 50/20 = 3.5), 3 planets, steel pins.
- Ring OD ≈ 60–70 mm. The Ø55.6 motor plus gearbox fits easily inside the Ø170 wheel.
- A smaller wheel is possible but not proposed, because it would change the control parameters and obstacle capability.

**Driver current limit:** set to **15 A** (the 180 s rating). Do not raise it, because extra torque is lost to grip.

**Encoder:**
- The MN5008 has a 6 mm shaft. A diametric magnet (6 × 2.5 mm) goes in a printed holder on the shaft end at the stator side.
- The XDrive Mini's on-board AS5047P **cannot sit behind a hub motor**, because the board lives in the body. A separate AS5047P breakout board is needed at the hub, with a cable through the leg (ABI or SPI, ~40 cm, shielded).
- **Electrical must confirm this** (noise and ODrive encoder mode).

**Mass:**
- Unsprung per side: **0.465 kg** (was 0.721).
- Robot saving: 2 × (336 − 128) + 2 × (110 − 62) ≈ **0.51 kg**.

### Jump re-run (hip 8308 KV130, 8:1, 8 J springs, unsprung 0.465–0.468 kg/side)

| M | Body mass | Ideal energy (85 % eff.) | Snatch loss (ideal) | Jump @22.2 V spring / none | Jump @19.8 V spring / none |
|---|---|---|---|---|---|
| 3.6 kg | 2.66 kg | 14.5 J (17.1 J) | 2.5 J (was 4.7) | 40.4 / 30.8 cm | **35.0 / 25.1 cm** |
| 3.2 kg | 2.26 kg | 13.1 J (15.4 J) | 2.6 J | 40.8 / 30.0 cm | 35.6 / 24.3 cm |

- 20 cm is now reached **without springs** (≈ 25 cm idealised, ≈ 20–21 cm after the 15–20 % real-world deduction).
- With springs there is ~75 % margin. The spring could be reduced to ≈ 4 J total, which halves the hip holding current (4.4 A → ~2 A).
- **Open for client/manager:** keep 8 J for margin, or reduce to 4 J? Recommended: design the anchors for 8 J and fit the 4 J spring first.
- These figures were computed with the 4:1 gearbox mass. 3.5:1 is 3 g lighter per side, which makes no difference.

### Wheel gearbox design torque (for the Materials engineer)

| Case | Output torque | Notes |
|---|---|---|
| Motor peak (15 A × Kt 0.0486 × 3.5 × 0.9) | **2.3 Nm** | normal operation, reversing at 3–5 Hz (fatigue, R-W5) |
| Continuous | 0.9 Nm | — |
| Landing spin-up with slip, LC-C (μ·F·r = 0.8·168·0.085 = 11.4 Nm at the tyre) | **≈ 4.5 Nm** through the gear (inertia share 0.39 at 4:1; ≈ 0.33 at 3.5:1, ≈ 3.8 Nm) | — |
| Fault LC-D (motors off, one wheel first, axle 312 N) | **≈ 8.3 Nm** | ultimate, SF 1.5 on top |

**Design values:**

| Use | Torque at the wheel output |
|---|---|
| Fatigue | 2.3 Nm |
| Max operating | 4.5 Nm |
| Ultimate | 8.5 Nm (× SF 1.5) |

The gearbox carries no radial load: the axle bearings take it (≤ 312 N).

### Landing with the light hub (M = 3.6 kg)

| Case | Axle | Unsprung | Body |
|---|---|---|---|
| LC-A | 142 N | 21 g | 6.0 g |
| LC-C | 168 N | 17 g | 5.2 g |
| LC-D | 312 N | 53 g (lighter unsprung mass bounces harder on the end stop) | 13.3 g |

These replace the hub rows of §3.6 for the new motor. The pin-force ratios scale with leg force.

### Sources (O9)

- T-Motor MN5008 (KV170/340/400: mass, R, size, 24N28P, shaft). https://store.tmotor.com/goods.php?id=999 , https://store.tmotor.com/goods.php?id=1000
- MN5008 KV170: 15 A peak, 270 mΩ (retailer). https://robotshop.com/products/tmotor-uav-brushless-motor-antigravity-mn5008-kv170
- T-Motor MN6007 / 6007II-X (KV160: 227 mΩ, 18 A). https://store.tmotor.com/goods.php?id=774 , https://store.tmotor.com/goods.php?id=1075
- MN6007 II: 159–161 g, Ø67.2 × 26.1 mm. https://RobotShop.com/products/tmotor-uav-brushless-motor-antigravity-mn6007ii-kv320 , https://vegadrones.in/?p=2429
- iPower GM5208-12: 15.2 Ω, 12N14P, Ø12 mm hollow shaft, ~195–209 g. https://shop.iflight.com/ipower-motor-gm5208-12-brushless-gimbal-motor-pro279
- Control requirements: `docs/analysis/control.md` R-W1/R-W2/§9.

### Open questions (O9)

1. **Electrical:** a remote AS5047P at the hub (cable length, ABI vs SPI, EMI next to the phase wires).
2. **Electrical:** MN5008 KV170 inductance and pole pairs (14) in the ODrive config.
3. **Thermal:** is 6 A continuous realistic for a 128 g motor enclosed in a printed wheel?
4. **Manager/client:** spring energy 8 J vs 4 J (see the jump re-run).
5. **Control:** update the sim with m_wheel = 0.465 kg, N = 3.5, J_rotor ≈ 4e-5 kg m² (estimate), Kt = 0.0486.

### Changes to design assumptions (O9)

| Was | Now |
|---|---|
| Wheel motor 8308 KV130, 4:1 | **T-Motor MN5008 KV170, 3.5:1** |
| Unsprung 0.721 kg/side | **0.465 kg/side** |
| Jump needs springs (18 cm without) | 25 cm without springs (idealised); springs are now margin |
| Wheel gear design torque 10 Nm | **4.5 Nm max operating / 8.5 Nm ultimate** |
| Wheel current limit 40 A | **15 A** |

---

## O13 re-run at 4.31 kg (rev 3, 2026-11-04)

Inputs (design_targets.md rev 2):
- total mass M = 4.31 kg
- unsprung 0.536 kg/side, so body m_b = 3.24 kg
- hips: 8308 KV130, 8:1
- wheels: MN5008 KV170, 3.5:1 (24/18/60)
- springs: 8 J kept

Evidence: `calc/o13_rerun.py` → `calc/o13_output.txt`. Control's `sim_lqr_2d.py` was imported unchanged and run with overridden parameters: m_wheel 0.536, N 3.5, KV 170, J_rotor 4e-5, i_max 15 A.

### Wheel speed and torque at 19.8 V

| R_ll (to be measured) | Loaded km/h (30 % headroom) | 2.0 Nm/wheel available up to | Peak / cont per wheel | Control N_max |
|---|---|---|---|---|
| 0.27 Ω | 19.3 | 16.1 km/h | 2.30 / 0.92 Nm | 4.11 ≥ 3.5 ✓ |
| 0.72 Ω | 15.7 | 6.9 km/h | 2.30 / 0.92 Nm | ✓ |

- Grip caps the torque at 1.44 Nm/wheel.
- With R = 0.72 Ω the motor still gives ≈ 1.3 Nm/wheel at 12 km/h, which is about 90 % of the grip cap. **This passes in practice. No fix is needed**, but measure R.
- If the measured R is 0.72 Ω and balance at top speed is weak, the smallest fix is the MN5008 **KV340** (55 mΩ, same size, +7 g) with the 15 A limit kept.

### Hip torque (per leg, m_b = 3.24 kg)

| Case | Hip torque | Motor current |
|---|---|---|
| Standing, worst pose | 3.5 Nm | 8.1 A (no spring) |
| At nominal, with the 8 J spring | 1.1 Nm | **2.6 A** |
| Height change at +0.5 g | 5.3 Nm | — |
| Single-leg climb | 7.9 Nm (spring gives ≈ 3.4 Nm, motor ≈ 4.5 Nm) | within 5.7 Nm continuous |

### Jump (hip I_peak 40 A; real estimate = sim × 0.80)

| V | Springs | Sim | **Real estimate** | Push time | Peak hip torque / current | Battery |
|---|---|---|---|---|---|---|
| 22.2 | 8 J | 36.9 cm | **29.5 cm** | 83 ms | 17.3 Nm / 40 A | ≤ 56 A |
| 22.2 | none | 29.2 | 23.3 | 96 ms | 17.3 / 40 | 56 |
| 19.8 | 8 J | 31.8 | **25.5 cm** | 85 ms | 17.3 / 40 | 56 |
| 19.8 | none | 23.9 | **19.1 (fails)** | 98 ms | 17.3 / 40 | 56 |

- Energy: 17.3 J ideal, 20.3 J at 85 % efficiency. Snatch loss 2.8 J.
- **20 cm holds with springs: +27 % margin at low battery.** Keeping the 8 J springs is necessary: without them the jump fails at 19.8 V.
- With the hip limit at 20 A instead of 40 A: 25.6 cm sim, ≈ 20.5 cm real (no margin). **The 40 A push-off limit must stay.**

### Landing load cases (updated; replaces §3.6 and O9 numbers)

| LC | Case | Body g | Unsprung g | Axle N | Leg N | Hip torque total / motor (Nm) | Knee pin = hip bearing (N) | Coupler N | Stroke mm | Wheel gear N·m | Hip gear (end-stop spike) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | symmetric, controlled | 5.8 | 19 | 156 | 93 | 11.4 / 9.3 | 345 | 263 | 61 | 3.5 | — |
| B | symmetric, motors off | 15.5 | 47 | 211 | 245 | 53.8 / 0 | 1665 | 1619 | 174 | 4.7 | **34.8 Nm ✗** |
| C | one wheel first, controlled | 5.1 | 15 | 192 | 161 | 19.9 / 17.7 | 597 | 454 | 62 | 4.3 | — |
| D | one wheel first, motors off | 13.0 | 43 | 388 | 412 | 90.4 / 0 | 2798 | 2720 | 180 | 8.7 | 30.4 Nm ✗ |

**Failure:** at 4.31 kg, the fault landings (B, D) on the 25 kN/m end stop at 105 mm back-drive the hip rotor. That puts a 30–35 Nm spike on the hip gearbox (20 Nm ultimate), and the knee pin reaches up to 2.8 kN.

**Smallest fix (tested, same script):** **TPU end stop of ≈ 10 kN/m that engages at 130 mm hip height, with ≥ 30 mm travel.**

| LC (fixed end stop) | Body g | Axle N | Leg N | Knee pin N | Hip gear spike |
|---|---|---|---|---|---|
| B | 11.9 | 220 | 188 | 1125 | **16.1 Nm** ✓ |
| D | 9.5 | 337 | 302 | 2011 | **4.9 Nm** ✓ |

**Design values for Structural/Materials:**
- **Fatigue:** LC-A/C.
- **Ultimate (× SF 1.5):** LC-B/D with the fixed end stop.
- **Wheel gear ultimate:** raise from 8.5 to **9 Nm** (LC-D 8.7).
- **Hip gear:** 20 Nm ultimate stays valid **only with the fixed end stop**.
- **LC-C:** needs 17.7 Nm from the hip motor (≈ 40 A). At the 20 A normal limit the controller uses more of the available ≥ 100 mm stroke instead (OK per the landing rules).

### Control LQR sim at 4.31 kg (torques are totals for both wheels)

| l | Tilt | Hold floor | LQR peak (unclipped) | Peak at limit | Min saturation that recovers | Δv | Max recoverable tilt |
|---|---|---|---|---|---|---|---|
| 0.15 m | 5° / 10° | 0.19 / 0.38 | 5.6 / 11.2 | 2.88 | 0.20 / 0.40 | 0.18 / 0.36 m/s | 45° |
| 0.23 m | 5° / 10° | 0.23 / 0.45 | 5.8 / 11.6 | 2.88 | 0.24 / 0.48 | 0.25 / 0.49 | 45° |
| 0.35 m | 5° / 10° | 0.26 / 0.51 | 6.1 / 12.1 | 2.88 | 0.27 / 0.55 | 0.34 / 0.68 | 43° |

- The usable limit is 2.88 Nm total. Grip sets it (motors at 15 A could give 4.34 Nm).
- All cases recover. **Balance passes at 4.31 kg.**

### Changes to design assumptions (O13)

| Was | Now |
|---|---|
| End stop ≤ 25 kN/m near crouch | **≈ 10 kN/m TPU, engages at 130 mm hip height, ≥ 30 mm travel** |
| Wheel gear ultimate 8.5 Nm | **9 Nm** |
| Jump margin at 19.8 V: 75 % (at 3.6 kg) | **+27 % with springs**; without springs it fails (19 cm), so the springs are mandatory |
| Hip push-off limit "40 A optional" | **40 A required** for the jump |

---

## P3 spring re-fit (rev 4, 2026-11-04)

Inputs:
- docs/layout.md P2: crank r = 40 mm opposite the thigh; body anchor at (47.3, 56.6) mm from the hip
- spring span ext / nom / crouch = 62.0 / 89.8 / 104.2 mm, so the stroke is 42.2 mm
- M = 4.37 kg, unsprung 0.536 kg/side
- hip 8308 KV130 8:1 at 40 A push-off, 19.8 V
- real jump = sim × 0.80

Evidence: `calc/p3_spring.py` → `calc/p3_output.txt`. The spring torque now uses the true layout geometry, T = F(L)·dL/dφ; the spring lengths reproduce the layout to 0.1 mm.

### Options at 4.37 kg (real jump, cm)

| Option | Stroke | F max | Energy per leg | From crouch 101: 19.8 V / 22.2 V | From 130 (end stop): 19.8 V | Hold current at nominal |
|---|---|---|---|---|---|---|
| **O0: keep 2.7 N/mm, 8 N preload, r 40** | 42.2 mm | 122 N | 2.74 J | **23.6 / 27.7** | 21.4 | 0.7 A |
| O1: 4.1 N/mm, 8 N preload | 42.2 | 181 | 3.99 | 25.9 / 29.8 | 23.2 | 3.5 A |
| O2: 3.5 N/mm, 20 N preload | 42.2 | 168 | 3.96 | 26.0 / 30.0 | 23.5 | 3.2 A |
| O3: 50 mm crank, 2.7 N/mm | 50.0 | 143 | 3.77 | 25.5 / 29.5 | 23.0 | 2.9 A |
| No spring | — | — | 0 | 19.1 / — | 17.7 | — |

- With the real geometry, the spring's leverage peaks where the push-off needs it. The **unchanged 2.7 N/mm spring already gives 23.6 cm real at 19.8 V (+18 %)** with only 5.5 J total (not 8 J).
- The 4.1 N/mm option gains just 2.3 cm. It also does not fit as a wire (see below).

**The real constraint is the anchor span, not the rate.**
- With a 62 mm span at full extension, the spring body (inside the hooks) must be ≤ ~46 mm.
- Music wire (DH, G = 81.5 GPa) that fits a Ø14 envelope:
  - 2.7 N/mm needs d 2.0 / D 11, n ≈ 45, body 93 mm. **Does not fit.**
  - 4.1 N/mm with a 48 mm body needs d 2.0 / D 12 at τ = 861 MPa against 900 MPa allowable. The hooks would be overstressed. **Rejected.**

### Recommendation (smallest fix)

**Keep the rate (O0) and move the body anchor 49 mm outward along the spring line**, to (94.1, 71.2) mm hip-relative (was 47.3, 56.6).

| Check | Value |
|---|---|
| New span ext / crouch | 111.0 / 152.0 mm |
| Stroke | 41.0 mm |
| F crouch | 119 N |
| Jump (real) | **23.5 cm at 19.8 V** from crouch 101 (+18 %); 27.5 cm at 22.2 V; 21.3 cm from 130 |

**Spring specification (per leg, 1 piece):**

| Parameter | Value |
|---|---|
| Type | extension spring, music wire EN 10270-1 DH (or 1.4310 stainless, +5 % d), German full loops (DIN) |
| Rate | **2.7 N/mm** (tolerance ±10 %) |
| Wire | **d = 2.0 mm**, mean D = 11.0 mm, **OD = 13.0 mm** (ID 9.0), C = 5.5 |
| Active coils | ≈ 45, body ≈ 92 mm |
| Free length (inside loops) | **≈ 110 mm** |
| Initial tension | ≈ 5 N |
| Preload at full extension | 8 N (installed at 111 mm) |
| Max extension | ≈ 42 mm (installed span 152 mm), **F max = 122 N** |
| Stress | τ ≈ 533 MPa at 122 N against ≈ 900 MPa allowable. Hook bending ≈ 1.0 GPa against ≈ 1.0 GPa fatigue allowable, so it is OK for ~10⁴ jump cycles but hooks are the life limit. Inspect after every 500 jumps. |
| Energy | 2.74 J/leg, **5.5 J total** |

**Catalogue part:**
- I could not find a verified catalogue part number for exactly this spec. Searches of Lee Spring (LE/LEM metric series) and Gutekunst turned up nothing that fits.
- Order with these filter values: OD 12.5–13.5 mm, d 2.0 mm, rate 2.4–3.0 N/mm, max load ≥ 125 N, free length 105–115 mm, max extended length ≥ 155 mm. Use the Lee Spring extension filter or a Gutekunst custom quote (they make custom springs in small quantities).
- If a catalogue spring has a slightly different free length, adjust the anchor position by the same amount. The anchor bracket should have a 3-hole slot at ±5 mm.

**Anchor loads (both ends: body anchor pin and thigh crank pin):**
- 122 N static along the spring line; **design 180 N** (×1.5 dynamic).
- Moment on the crank: 122 × 0.040 = 4.9 Nm.
- Use steel pins Ø4 mm in metal or heat-set-insert bosses. **The anchor must not be on the gearbox output** (layout §6 already complies).

**Clearance:**
- The spring OD drops from 14 to 13 mm, so spring ↔ B-pivot clearance goes from 3.3 to about 3.8 mm.
- Moving the anchor changes the spring line, so **Mechanical must re-run `com_layout.py` at all three poses** and keep ≥ 3 mm. If it is < 3 mm, offset the anchor ±3 mm in Y; the spring stays in the thigh plane.

**End stop (130 mm engage, 29 mm hip travel, ≈ 10 kN/m):**
- Compatible.
- Crouching for a jump to hip 101 compresses the pad by 9.9 mm: ≈ 99 N at r = 70 mm, so 6.9 Nm on the hip. The hip motor holds it at ≈ 16 A, plus ≈ 2 A for the spring and weight, so **≈ 18 A for ≤ 1 s, within the 20 A normal limit**.
- The pad gives back part of that energy at push-off. This was not credited, so the result is conservative.
- If crouch-into-pad is not wanted, jumping from 130 still gives 21.3 cm (+6 %, thin margin).

### Change to design assumptions (P3)

| Was | Now |
|---|---|
| 8 J springs (2.7 N/mm, 52 mm stroke) | Same 2.7 N/mm / 8 N preload, 41–42 mm stroke ⇒ **5.5 J**. Jump requirement met (23.5 cm real at 19.8 V). **Flag to client:** "8 J" cannot fit the layout's Ø14 envelope without overstressing the wire, and it is not needed. |
| Spring anchor at (47.3, 56.6) | **(94.1, 71.2) mm hip-relative**, slotted ±5 mm |
| Spring Ø14 envelope | **OD 13**, free length ≈ 110 mm |
| Jump crouch | to hip 101 (pad compressed), hold ≤ 1 s at ≈ 18 A |

---

## Re-run at CAD mass (6.4 kg) (rev 5, 2026-11-05)

Inputs (mass_actual.md, DECISIONS 2026-11-05):
- total mass 6.0 / **6.4** / 6.9 kg
- unsprung 0.84 kg/side, so body m_b = 4.32 / 4.72 / 5.22 kg
- minimum hip height 140 mm (stroke 140–289 mm, 150 mm)
- hips 8308 KV130 8:1 at 40 A push-off; wheels MN5008 KV170 3.5:1
- spring 2.7 N/mm, 8 N preload, 5.5 J, anchor as in P3 (span 111 → 148 mm at the 140 mm crouch)
- CoM +11 mm forward of the axle
- wheel inertia 2.0e-3 kg m² (was 1.0e-3), k_g 0.13

Evidence: `calc/o14_cad_mass.py` → `calc/o14_output.txt`. Real = sim × 0.80, as in O13/P3.

Model limits:
- Leg geometry is the P1 4-bar (B at (46,34); CAD has (46,30)), not re-synthesised.
- Leg-link kinetic energy and pad energy return are ignored.
- The wheel inertia of 2e-3 is an estimate.

### Requirement checks

| # | Requirement | 6.0 kg | **6.4 kg** | 6.9 kg | Verdict |
|---|---|---|---|---|---|
| 1 | Jump ≥ 20 cm real, 19.8 V, springs, from 140 mm | 16.1 cm | **16.2 cm** | 16.2 cm | **FAIL** |
| 1b | Same at 22.2 V, springs | 19.1 | **19.3** | 19.6 | **FAIL (marginal)** |
| 1c | No springs, 19.8 V / 22.2 V | 14.4 / 17.8 | 14.8 / 18.3 | 15.3 / 18.7 | FAIL |
| 2 | 12 km/h with 30 % balance headroom (loaded, 19.8 V) | 19.2 km/h (R 0.27 Ω), 15.6 (R 0.72 Ω) | 19.2 / 15.5 | 19.2 / 15.5 | **PASS**. Peak 2.30 / cont 0.92 Nm per wheel. Traction cap 2.0 / 2.13 / 2.30 Nm per wheel, so grip, not current, limits torque |
| 2b | CoM offset hold torque (+11 mm) | 0.65 Nm total | 0.69 | 0.74 | PASS: ≈ 38 % of the 0.92 Nm per-wheel continuous rating; it also adds a steady current and heat |
| 3a | Standing hip torque, worst pose | 3.8 Nm, 8.7 A without spring | **4.1 Nm / 9.5 A**; with spring 1.9 A at nominal, 3.7 A at crouch | 4.6 Nm; 2.7 / 4.7 A | PASS (5.7 Nm cont limit) |
| 3b | Single-leg climb (2.25 × leg force) | 8.5 Nm worst pose; at nominal with spring 4.4 Nm / 10.1 A | **9.3 Nm worst; at nominal 5.0 Nm / 11.6 A** | 10.3 Nm; 5.8 Nm / 13.5 A | **PASS at 6.4** (5.0 < 5.7 Nm thermal, peak well under 17.3 Nm). 6.9 kg: marginal (5.8 > 5.7) |
| 4 | Balance: max recoverable tilt; min torque for 5° / 10° (total) | 43–45°; 0.28–0.39 / 0.55–0.78 Nm | **41–45° (45° at l ≤ 0.23); 0.30–0.41 / 0.59–0.83 Nm**; LQR unclipped peak 5.7–6.2 / 11.4–12.5 Nm | 41–45°; 0.32–0.44 / 0.64–0.89 Nm | **PASS**. The usable limit is 4.0 / 4.27 / 4.34 Nm total, far above the 0.9 Nm needed |
| 5a | Landing, controlled (LC-A) hip torque vs 16 Nm gearbox limit | 15.6 Nm (13.5 motor) | **16.7 Nm (14.7)** | 18.1 Nm (16.1) | **6.0: PASS; 6.4: FAIL marginal (+4 %); 6.9: FAIL** |
| 5b | LC-C one wheel first, controlled | 26.2 Nm (23.9 motor, capped by 40 A) | 26.4 (23.9) | 26.5 (23.9) | **FAIL** unless the hip current is capped in landing |
| 5c | Fault landings B/D, motors off: back-driven rotor spike on the gearbox | 30.3 / 29.0 Nm | **29.5 / 28.8 Nm** | 28.5 / 28.6 Nm | **FAIL** (≈ 1.8× the 16 Nm limit), even with the 10 kN/m stop |
| 5d | Knee pin ≤ 2.0 kN design load: LC-A / C / B / D | 0.46 / 0.78 / 1.40 / 2.49 kN | **0.49 / 0.81 / 1.54 / 2.64 kN** | 0.53 / 0.82 / 1.68 / 2.81 kN | A, C, B **PASS**; D (worst abuse) **FAIL** (+32 % at 6.4 kg) |
| 5e | Wheel gear spin-up, LC-C / D (limit 9 Nm ultimate) | 3.4 / 5.7 | 3.6 / 6.1 | 3.7 / 6.6 | PASS |

Landing detail, 6.4 kg:

| LC | Body g | Unsprung g | Axle N | Leg N | Stroke mm |
|---|---|---|---|---|---|
| A | 5.7 | 15 | 210 | 133 | 61 |
| B | 12.8 | 36 | 324 | 295 | 138 |
| C | 4.7 | 12 | 266 | 216 | 66 |
| D | 9.7 | 40 | 456 | 448 | 154 |

### Why the 20 cm jump fails (and why mass is not the cause)

- The sim height barely changes with mass: 16.1–16.3 cm real from 4.4 to 7.0 kg. **Cutting weight does not make the jump pass.**
- The limit is hip speed. At 40 A and 19.8 V the 8:1 hip stalls against back-EMF during push-off.
- The crouch is now 140 mm, so the stroke is 150 mm instead of 188 mm. That removes about 30 % of the push-off energy. At 4.37 kg and a 101 mm crouch the same model gave 23.5 cm.
- Stiffer or larger springs do not fix it: 4.1 N/mm gives 17.0 cm, 5.5 N/mm gives 18.0 cm (6.4 kg, 19.8 V). The hips cannot push through the spring fast enough.
- Higher hip current does not help either, because the hips are already speed-limited at the stall current.

### Smallest fix: hip gearbox 6:1 instead of 8:1

| Option (6.4 kg, from 140 mm) | 19.8 V real | 22.2 V real | Spring F max |
|---|---|---|---|
| 8:1 + 2.7 N/mm (current) | 16.2 cm | 19.3 | 118 N |
| **6:1 + 2.7 N/mm (no spring change)** | **21.4 cm (+7 %)** | 23.9 | 107 N |
| 6:1 + 4.1 N/mm | 22.3 cm | 25.0 | 159 N |

- 6:1 passes at 6.0 kg (21.6) and at 6.9 kg (20.9). The margin over 20 cm is only +5–11 %.
- Costs and side effects of 6:1:
  - Hip torque at 40 A drops from 17.3 to 13.0 Nm. That is below the 16 Nm gearbox limit, so it fixes LC-A and LC-C (landing hip torque is motor-limited at ≈ 13 Nm).
  - Standing needs 33 % more current: 12.7 A against 9.5 A without spring (≈ 2.5 A with spring, still easy).
  - Single-leg climb at nominal: 11.6 A × 8/6 ≈ 15.5 A, inside the 20 A hip limit. The thermal margin is thinner. Brief use only.
- It also reduces the printed gearbox torque and probably its mass. Materials must redo the compound stage: ring ratio 6:1 needs, for example, sun 18 → planet 36, planet 18 → ring ≈ 45 (to be re-sized).
- Other options if 8:1 must stay:
  - 22.2 V full-charge only (6S fully charged, not a loaded pack): 4.1 N/mm gives 20.0 cm (marginal). Not recommended.
  - Reduce the hip height minimum back toward 101–110 mm (wheel clearance at the hip housing). Mechanical question: each 10 mm of extra stroke is worth ≈ +1.5 cm.
- **Not enough on their own:** mass cuts (no effect), stiffer springs (+2 cm).
- Mass is still worth cutting for other reasons (landing, climb thermal margin). Candidates, in order of saving:
  - legs ≈ 0.9 kg each against the 254 g planned: arch plate 135 g, posts 149 g, Al shank plate 83 g, knee strap 28 g, steel pins and bushings ≈ 220 g per leg
  - hip gearbox 413–435 g against 185 g planned
  - body printed shell ≈ 475 g against 297 g planned

### Landing fixes (all masses)

1. Cap hip current in the landing controller (LC-C, motor torque 23.9 Nm at 40 A): limit ≈ 27 A for 8:1, or use 6:1 (40 A = 13 Nm, automatic).
2. Fault cases B/D (28–30 Nm spike on a 16 Nm gearbox): add a **mechanical torque limiter or hard stop that takes the load before the rotor inertia is back-driven.** The TPU stop at 10 kN/m is not enough at this mass. Options: end stop at 160 mm raised to ≥ 170 mm engagement with ≥ 30 mm travel, or a slip clutch on the hip. Mechanical decision.
3. Knee pin LC-D 2.6–2.8 kN against the 2.0 kN design load: the knee pin and B-pin load path (SF 1.3 per leg.md) need a box beam or a tie into the body frame, as already noted.

### Changes to design assumptions

| Was | Now |
|---|---|
| Jump 23.5 cm real at 4.37 kg (101 mm crouch) | **16.2 cm at 6.4 kg (140 mm crouch): FAIL.** Not caused by mass. Due to the shorter stroke at 8:1 |
| Hip gearbox 8:1 | **6:1 recommended** (21.4 cm real, hip peak torque 13.0 Nm) |
| Hip torque gearbox limit 16 Nm vs 17.3 peak | At 6:1, the motor peak (13.0 Nm) stays under the limit |
| Standing hip hold at nominal 0.7 A | 1.9 A with spring (4.1 Nm without), still easy |
| Balance sim at 4.31 kg | **Unchanged: PASS at 6.0–6.9 kg** |
| Speed 12 km/h | **PASS at all masses** |

## Final robot (CAD rev 2, spring 3.5 N/mm): balance, jump with battery sag, spring check (rev 6, 2026-11-05)

Scripts (all in `calc/`): `final_balance_lqr.py` (balance, 12 km/h, hills; details in control.md §10), `final_jump_sag.py`, `final_spring_spec.py`, each with its `_output.txt`. Input geometry: `leg_refit_jump.py` (4-bar rev 2: B (39,31), anchor (97.4,70.9), hip 6:1, 40 A, unsprung 0.84 kg/side, minimum hip height 140 mm, real = sim × 0.80).

### Balance, 12 km/h (MN5008 KV170, 3.5:1, 15 A, 6S)
PASS at 6.4 and 6.9 kg. Highlights (control.md §10 has the full table): 20 N × 0.1 s push settles in 1.1–1.2 s with 4° peak and 0.8 N m; recovery from ≥ 45° tilt (torque limit 4.27 / 4.60 N m, traction); 12 km/h uses 34–35 % of the torque limit with 35 % speed headroom at 19.8 V; 15° slope uses 75–81 % of the continuous torque.

### Jump with battery sag (spring 3.5 N/mm, F0 15 N)
Pack model: V = Voc − R_int × I_bat. R_int = 40 mΩ (6 × 5 mΩ + 10 mΩ wiring, electrical.md), 80 mΩ for an aged or cold pack. Battery peak 56 A for ≈ 85 ms (current limited at 40 A per hip, speed-limited by back-EMF).

| Voc at rest | R_int | V under load | 6.4 kg real | 6.9 kg real |
|---|---|---|---|---|
| 25.2 V (full) | 40 mΩ | 23.0 V | 24.8 cm | 24.5 cm |
| 22.2 V (nominal) | 40 mΩ | 20.0 V | **21.7 cm** | **21.2 cm** |
| 22.2 V | 80 mΩ | 17.7 V | 20.7 | 20.3 |
| 20.5 V (3.4 V/cell, nearly empty) | 40 mΩ | 18.3 V | 19.9 | 19.5 |
| 20.5 V | 80 mΩ | 16.0 V | 18.9 | 18.4 |
| *no sag, fixed 19.8 V (old test value)* | 0 | 19.8 V | *20.2* | *19.7* |

- The old "19.8 V" test value was a good proxy for a nominal-charge pack with sag (20.0 V loaded).
- **20 cm real needs a rest voltage ≥ 20.6 V (6.4 kg) / 21.0 V (6.9 kg) with a healthy pack, ≥ 21.9 V (6.9 kg) with an aged one.** Gate: jump only with rest voltage ≥ 21.5 V (3.58 V/cell), 22.0 V for an aged pack. The control state machine and test plan use this.
- 56 A for 85 ms passes a 50 A slow-blow fuse by I²t, but test it (control.md 6a3).
- 6.9 kg is not marginal any more at 22.2 V (21.2 cm) but loses 1 cm at low charge.

### Spring check (full numbers in `final_spring_spec_output.txt`)
- Wire 2.0 mm A228 music wire, Sut ≈ 2000 MPa, OD 13 (D 11, C 5.5, Wahl Kw 1.278). Wire shear at 169 N: **757 MPa**, allowable 0.45 Sut = 900 MPa → **SF 1.19** (the A9 "~740" was a little low). At the 195 mm stance the spring already carries 132 N (592 MPa, 66 %).
- Over-travel: even at the mechanical reach of 116 mm the force is only 177 N (794 MPa, 88 % of allowable); the 900 MPa limit is at 201 N, 53 mm extension. The 180 N anchor design load holds.
- **Hooks are the critical part, not the body:** a plain full-loop hook gives 1423 MPa bending (allow 0.75 Sut = 1500, SF 1.05) and 740 MPa torsion at the bend (SF 1.08). Feasible only with **reduced-diameter hooks** (hook ID 6.5 for the Ø5 pins, mean D 8.5): estimated 1326 MPa (SF 1.13) and 603 MPa torsion (SF 1.33). This is an estimate (Shigley eq. with the mean of coil and hook diameter as moment arm): ask the supplier to confirm the hook stress and to stress-relieve after coiling.
- Fatigue (Zimmerli, unpeened): jump cycle 15 → 169 N body SF 1.21 at 1e7 cycles, stance cycle 15 → 132 N SF 1.56. Our need is ≈ 500 jumps (S10) plus thousands of stance cycles, so the body is safe. **Hook life is unverified**: plan 6 springs (2 + 4 spares), inspect hooks every 5 jumps, replace after 500 jumps.
- Verdict: **feasible, low margin (SF 1.1–1.2 static); not a design change.** If the bench test 6a2 shows hook cracking or set > 0.5 mm, the fallback is Cr-Si wire (A401/EN 10270-2 VDSiCr, same Ø, better fatigue and relaxation) with the same drawing. Going to 2.2 mm wire is infeasible: it needs 54 coils (body 121 mm > the 116 mm free length). A second spring in parallel does not fit the 13 mm band.

### Purchasable spring spec (2 per robot, order 6)
Extension spring, **custom, e.g. Lee Spring / Century Spring / Associated Spring custom extension**:
- Wire: **Ø2.00 mm ASTM A228 music wire** (EN 10270-1 SH); right-hand wind; **OD 13.0 mm** (ID 9.0, mean D 11.0), tolerance ±0.2.
- Coils: **≈ 34 active (≈ 33.6 close-wound body coils, body ≈ 69 mm)**, supplier to adjust the count to the rate.
- Rate **3.5 N/mm ±5 %**; **initial tension 15 N ±3 N** (τ_i 53 MPa, within the normal winding range).
- **Free length inside hooks 116.0 mm ±1.5 mm** (pin-centre distance 111.0 mm at full extension of the leg, plus the Ø5 pin). Load **169 N ±10 N at 159.5 mm inside hooks** (extension 43.5 mm). Max safe extension ≥ 53 mm (yield at 201 N).
- Ends: **extended, reduced-diameter full-loop hooks (closed, no gap), hook ID 6.5 mm for a Ø5 pin, hook plane perpendicular to the spring pin axis, both loops in the same plane (0° ±10°)**, bend radius at the transition ≥ 3 × wire diameter (6 mm), no tool marks.
- Finish: **stress-relieve after coiling and hook forming (230 °C, 30 min)**; plain or light oil; no zinc or chrome plating (hydrogen embrittlement); if plated, bake 190 °C for 4 h.
- Inspection: 100 % load test at 159.5 mm; certificate of material.
- Mass ≈ 33 g each. Request a first article before the batch.
- Part description line: "EXTENSION SPRING, A228 MUSIC WIRE 2.00 MM, OD 13.0 MM, FL 116.0 MM INSIDE HOOKS, RATE 3.5 N/MM, IT 15 N, REDUCED EXTENDED CLOSED FULL-LOOP HOOKS ID 6.5, STRESS-RELIEVED."

### Changes to design assumptions
| Was | Now |
|---|---|
| Jump 20.2 / 19.7 cm at 19.8 V fixed (A9) | 21.7 / 21.2 cm at 22.2 V rest with 40 mΩ sag; 19.9 / 19.5 at 20.5 V rest. Jump gate: rest voltage ≥ 21.5 V |
| Wire shear ~740 MPa | 757 MPa (SF 1.19); hook bending SF 1.05 plain, ~1.13 with reduced hooks |
| Spring "13 × 13 envelope, free ≈ 110 mm" | Free length inside hooks 116.0 mm (Ø5 pins), OD 13.0 |
| Balance sim at 3.6–4.0 kg | PASS at 6.4 / 6.9 kg with CAD inertia; l 177 mm, k_g 94 mm |
