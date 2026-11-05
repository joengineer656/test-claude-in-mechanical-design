# Materials & Gears: P1 Report (Materials Eng., with Structural Eng.)

Status: P1 calculations only. No CAD (Gate A conditional). Rev 0, 2026-11-04.
Script: `docs/analysis/calc/gear_lewis.py`. Run `python3 gear_lewis.py` to regenerate every table in §3.

---

## 1. Summary

**Gear stages (baseline)**

| Stage | Ratio / teeth (Zs/Zp/Zr) | Module | Face width | Tooth form | Gear material | Lewis SF at peak torque |
|---|---|---|---|---|---|---|
| Wheel hub, single stage, 3 planets | **4.94:1 (17/25/67)**, or 3.91:1 (23/22/67) or 6.0:1 (13/26/65) | **1.25** | **15 mm** | Herringbone, 20° PA, ψ = 20–25° | **PAHT-CF** for sun and planets, PAHT-CF ring insert | 3.8 at 6 Nm (PETG fallback: 2.0) |
| Hip output mesh (2-stage, or compound with stepped planets), 3 planets | about 9:1 total | **1.5** | **20 mm** | Herringbone (spur if a steel sun is used) | **PAHT-CF**, no PLA/PETG | 2.3 at 15 Nm at 50 °C, ring pitch Ø96 (2.0 at Ø84) |
| Hip input stage | about 3:1 | 1.0–1.25 | 12 mm | Herringbone | PAHT-CF (or a steel sun) | sees 15/3 ≈ 5 Nm, same as the wheel stage, SF > 3 |

**Metal is required for:**
- Planet pins: hardened steel dowels Ø5 h6. Ø4 is acceptable for the wheel only.
- All bearings: planets, carrier/output, and the wheel hub.
- Hip output shaft or flange interface: steel D-shaft or bolted steel bushing.
- Wheel axle: stationary steel tube or shaft. Wheel loads must not pass through the motor bearings.
- Through-bolts plus steel washers or bushings at every spring and hip pivot.
- Optional, recommended if bench tests show wear: a steel sun pinion (catalogue MOD1.0 or MOD1.5) on the motor rotor. The sun runs hottest (it is bolted to the rotor), is the smallest gear and sees the most cycles.

**Key findings**
1. For a simple planetary, the tooth force is Ft = 2·T_out/(Np·D_ring). It does not depend on the ratio, so the ring pitch diameter is the main strength lever. Make the ring as large as the motor diameter allows (Ø84–96 mm).
2. PLA is not acceptable for any gear or housing that touches the motor. It loses about 55 % of its strength at 50 °C and creeps at the 55–60 °C glass transition. PETG works only for the wheel stage at ≤ 40 °C. The hip needs PAHT-CF (or PA-CF) or metal.
3. **The motor can break the gears.** With KV90 (Kt ≈ 0.106 Nm/A), 30 A gives about 26 Nm at a 9:1 hip and 14 Nm at a 5:1 wheel. Firmware current limits are a gear-protection feature: hip ≤ 20 A (≈ 17 Nm), wheel ≤ 15 A (≈ 7 Nm).
4. Landing torque fed back from the output side is **not** limited by motor current. The hip gearbox needs the snapper spring in series and/or a slip limit. The structural load cases must cover this.
5. A published benchmark supports the approach. Urs et al. (2022) ran an all-FDM-PLA 7.5:1 planetary, about 90 mm OD (same scale as the 8308), at 19 Nm peak for 2 s. It survived a 57 h / 420k-stride life test with only 26 mrad of backlash growth. Our hip target (15 Nm) is at the same level, but our motors run hotter, which is why we use PAHT-CF instead of PLA.

---

## 2. Assumptions

| # | Assumption | Value | Basis / owner to confirm |
|---|---|---|---|
| A1 | Hip peak output torque (jump/landing) | 8–15 Nm (design at 15) | Brief. Theory Eng. to confirm |
| A2 | Wheel peak output torque | 3–6 Nm (design at 6) | Brief. Theory Eng. |
| A3 | Continuous / reversing torque (balance) | Wheel 1.5 Nm, fully reversed. Hip 4 Nm with ripple | Estimate. Control Eng. to give an rms spectrum |
| A4 | Motor | Eaglepower 8308, Ø92 × 28.5, 336 g, 22 A cont. listed, KV90 **not confirmed** (DECISIONS.md) | Retailer listing (robu.in). Theory Eng. verifying |
| A5 | Gear/housing temperature | Wheel ≤ 40 °C, hip ≤ 50 °C (motor case can exceed 60 °C under jump/stall) | Thermal Eng. to confirm |
| A6 | Number of planets | 3, load-share factor K_share = 1.3 | Printed tolerance ±0.1 mm |
| A7 | Dynamic factor | K_v = 1.1 (pitch-line speed < 3 m/s) | Sun Ø21 mm at ~1900 rpm ≈ 2.1 m/s |
| A8 | Lewis form factor | 20° full depth, weakest gear in mesh (sun or planet). Herringbone treated as spur (no credit for helix overlap) | Conservative by about 1.3–1.5× |
| A9 | Printed allowable stress | UTS_XY × k. k = 0.70 static peak, 0.30 one-way fatigue (10⁷), 0.22 fully reversed fatigue | Engineering derate, see §3.1 |
| A10 | PAHT-CF strength | 65 MPa (moisture-conditioned) vs 92 MPa dry TDS | Nylon absorbs water. Use conditioned values |
| A11 | Print orientation of gears | Gear axis = print Z, so teeth bend in the strong XY plane | Urs et al. 2022 |

---

## 3. Calculations

### 3.1 Material allowables used (100 % infill, axis = Z)

| Material | UTS_XY (MPa) | Static allowable 25 °C (×0.70) | Reversed fatigue (×0.22) | Strength retained at 40 / 50 °C | HDT 0.45 MPa | Verdict for gears |
|---|---|---|---|---|---|---|
| PLA (Bambu Basic) | 39 | 27 | 8.6 | 0.80 / 0.45 | ~57 °C | Prototype gears only, away from motors |
| PETG | 34 | 24 | 7.5 | 0.88 / 0.75 | 69 °C | Wheel stage fallback, housings |
| PAHT-CF (Bambu) | 65 (cond.), 92 (dry) | 45.5 | 14.3 | 0.95 / 0.90 | 194 °C | **Gears baseline** |
| POM (Delrin) | n/a printed | n/a | n/a | n/a | n/a | Very hard to print on an open A1 (no bed adhesion, warps). Buy machined POM gears if needed |
| ABS/ASA | ~33–40 | ~25 | ~8 | good to 80 °C | ~95 °C | Warp risk on the open A1. Not recommended for gears |

Derate rationale:
- Layer seams and perimeter/infill interfaces sit at the tooth root.
- Z-direction weakness matters for helix and herringbone teeth (each layer is a slice, but the load stays in-plane, so this is acceptable).
- Polymer S-N curves fall to about 25–35 % of UTS at 10⁷ cycles. Fully reversed bending is lower again.
- Planets are idlers, so their teeth always see **fully reversed** bending, even in one-way drive. Balance reversals make the sun and ring reversed too.

### 3.2 Lewis bending: equations

```
Ft     = 2·T_out / (Np · D_r) · K_share · K_v      [N]   (per mesh, worst planet)
sigma  = Ft / (b · m · Y(z_min))                   [MPa]
SF     = sigma_allow(material, kind, T) / sigma
Hertz  sigma_H = Z_H·Z_E·sqrt(Ft/(b·d_sun)·(u+1)/u), Z_H = 2.49, Z_E(plastic/plastic, E=3 GPa) = 23.6 √MPa
```

Output of `calc/gear_lewis.py` (sigma in MPa, SF = allowable/actual, Hertz in MPa):

#### Wheel stage (simple planetary, Np=3, ring pitch <= 84 mm)

| m | ratio | Zs/Zp/Zr | i actual | D_r | b | sigma@6Nm | SF PLA | SF PETG | SF PAHT-CF | sigma@1.5Nm cont. | SFfat(rev) PAHT-CF 40C | Hertz@6Nm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1.0 | 4 | 27/27/81 | 4.00 | 81 | 10 | 20.2 | 1.4 | 1.2 | 2.3 | 5.1 | 2.7 | 43 |
| 1.0 | 4 | 27/27/81 | 4.00 | 81 | 15 | 13.5 | 2.0 | 1.8 | 3.4 | 3.4 | 4.0 | 35 |
| 1.0 | 5 | 20/31/82 | 5.10 | 82 | 10 | 21.7 | 1.3 | 1.1 | 2.1 | 5.4 | 2.5 | 45 |
| 1.0 | 5 | 20/31/82 | 5.10 | 82 | 15 | 14.4 | 1.9 | 1.6 | 3.2 | 3.6 | 3.8 | 36 |
| 1.0 | 6 | 16/32/80 | 6.00 | 80 | 10 | 24.2 | 1.1 | 1.0 | 1.9 | 6.0 | 2.2 | 48 |
| 1.0 | 6 | 16/32/80 | 6.00 | 80 | 15 | 16.1 | 1.7 | 1.5 | 2.8 | 4.0 | 3.4 | 39 |
| 1.25 | 4 | 23/22/67 | 3.91 | 84 | 10 | 16.5 | 1.7 | 1.4 | 2.8 | 4.1 | 3.3 | 41 |
| 1.25 | 4 | 23/22/67 | 3.91 | 84 | 15 | 11.0 | 2.5 | 2.2 | 4.1 | 2.8 | 4.9 | 33 |
| 1.25 | 5 | 17/25/67 | 4.94 | 84 | 10 | 18.0 | 1.5 | 1.3 | 2.5 | 4.5 | 3.0 | 43 |
| 1.25 | 5 | 17/25/67 | 4.94 | 84 | 15 | 12.0 | 2.3 | 2.0 | 3.8 | 3.0 | 4.5 | 35 |
| 1.25 | 6 | 13/26/65 | 6.00 | 81 | 10 | 21.6 | 1.3 | 1.1 | 2.1 | 5.4 | 2.5 | 47 |
| 1.25 | 6 | 13/26/65 | 6.00 | 81 | 15 | 14.4 | 1.9 | 1.7 | 3.2 | 3.6 | 3.8 | 39 |
| 1.5 | 4 | 18/18/54 | 4.00 | 81 | 10 | 15.2 | 1.8 | 1.6 | 3.0 | 3.8 | 3.6 | 43 |
| 1.5 | 4 | 18/18/54 | 4.00 | 81 | 15 | 10.2 | 2.7 | 2.3 | 4.5 | 2.5 | 5.3 | 35 |
| 1.5 | 5 | 13/20/53 | 5.08 | 80 | 10 | 18.4 | 1.5 | 1.3 | 2.5 | 4.6 | 3.0 | 46 |
| 1.5 | 5 | 13/20/53 | 5.08 | 80 | 15 | 12.3 | 2.2 | 1.9 | 3.7 | 3.1 | 4.4 | 37 |
| 1.5 | 6 | no fit | | | | | | | | | | |

#### Hip output mesh (2-stage or compound), weakest gear z_min=14, Np=3

| D_r | m | b | sigma@8Nm | sigma@15Nm | SF@15 PLA 25C | SF@15 PETG 40C | SF@15 PAHT-CF 50C | T_max PAHT-CF 50C (SF=1.5) | sigma@4Nm cont. | SFfat(rev) PAHT-CF 50C |
|---|---|---|---|---|---|---|---|---|---|---|
| 84 | 1.0 | 12 | 27.3 | 51.2 | 0.53 | 0.41 | 0.80 | 8.0 | 13.7 | 0.94 |
| 84 | 1.0 | 16 | 20.5 | 38.4 | 0.71 | 0.55 | 1.07 | 10.7 | 10.2 | 1.26 |
| 84 | 1.0 | 20 | 16.4 | 30.7 | 0.89 | 0.68 | 1.33 | 13.3 | 8.2 | 1.57 |
| 84 | 1.25 | 12 | 21.9 | 41.0 | 0.67 | 0.51 | 1.00 | 10.0 | 10.9 | 1.18 |
| 84 | 1.25 | 16 | 16.4 | 30.7 | 0.89 | 0.68 | 1.33 | 13.3 | 8.2 | 1.57 |
| 84 | 1.25 | 20 | 13.1 | 24.6 | 1.11 | 0.85 | 1.67 | 16.7 | 6.6 | 1.96 |
| 84 | 1.5 | 12 | 18.2 | 34.1 | 0.80 | 0.61 | 1.20 | 12.0 | 9.1 | 1.41 |
| 84 | 1.5 | 16 | 13.7 | 25.6 | 1.07 | 0.82 | 1.60 | 16.0 | 6.8 | 1.88 |
| 84 | 1.5 | 20 | 10.9 | 20.5 | 1.33 | 1.02 | 2.00 | 20.0 | 5.5 | 2.36 |
| 96 | 1.0 | 12 | 23.9 | 44.8 | 0.61 | 0.47 | 0.91 | 9.1 | 12.0 | 1.08 |
| 96 | 1.0 | 16 | 17.9 | 33.6 | 0.81 | 0.62 | 1.22 | 12.2 | 9.0 | 1.44 |
| 96 | 1.0 | 20 | 14.3 | 26.9 | 1.02 | 0.78 | 1.52 | 15.2 | 7.2 | 1.79 |
| 96 | 1.25 | 12 | 19.1 | 35.9 | 0.76 | 0.58 | 1.14 | 11.4 | 9.6 | 1.35 |
| 96 | 1.25 | 16 | 14.3 | 26.9 | 1.02 | 0.78 | 1.52 | 15.2 | 7.2 | 1.79 |
| 96 | 1.25 | 20 | 11.5 | 21.5 | 1.27 | 0.97 | 1.90 | 19.0 | 5.7 | 2.24 |
| 96 | 1.5 | 12 | 15.9 | 29.9 | 0.91 | 0.70 | 1.37 | 13.7 | 8.0 | 1.62 |
| 96 | 1.5 | 16 | 12.0 | 22.4 | 1.22 | 0.93 | 1.83 | 18.3 | 6.0 | 2.15 |
| 96 | 1.5 | 20 | 9.6 | 17.9 | 1.52 | 1.17 | 2.28 | 22.8 | 4.8 | 2.69 |

#### Steel planet pin (2*Ft on pin, d=4/5 mm, span b+4) and printed cheek bearing pressure

| case | T_out | D_r | b | F_pin N | d=4: sigma MPa | d=5: sigma MPa | cheek p (d=4, t=5) MPa |
|---|---|---|---|---|---|---|---|
| wheel peak | 6 | 84 | 15 | 136 | 103 | 53 | 3 |
| hip peak | 15 | 96 | 16 | 298 | 237 | 121 | 7 |
| hip peak | 15 | 84 | 20 | 340 | 325 | 166 | 9 |

KV90 -> Kt ~ 0.106 Nm/A. Output torque at motor current I (eta 0.9):
  wheel 5:1: 10 A -> 4.8 Nm, 20 A -> 9.6 Nm, 30 A -> 14.3 Nm, 40 A -> 19.1 Nm
  hip 9:1: 10 A -> 8.6 Nm, 20 A -> 17.2 Nm, 30 A -> 25.8 Nm, 40 A -> 34.4 Nm

### 3.3 Reading the tables

- **Wheel:** m1.25, b = 15 mm, ring pitch Ø84 gives Lewis SF 3.8 (PAHT-CF) or 2.0 (PETG) at 6 Nm peak, and reversed-fatigue SF 4.5 at 1.5 Nm and 40 °C. All three candidate ratios fit:
  - 4:1 → 3.91 (23/22/67)
  - 5:1 → 4.94 (17/25/67)
  - 6:1 → 6.00 (13/26/65). The 13-tooth sun needs a positive profile shift (x ≈ +0.3) to avoid undercut.
  The choice of ratio is a Theory/Control decision. Strength does not decide it.
- **Hip:** at 15 Nm only m1.5 × b20 (Ø84: SF 2.0) or m1.25–1.5 × b16–20 (Ø96: SF 1.5–2.3) in PAHT-CF at 50 °C give SF ≥ 1.5. PETG and PLA are below 1.2 in every row, so they are **rejected for the hip.**
- **Hertz contact:** 33–49 MPa at peak. This is at the level of published plastic contact limits (VDI 2736-type σ_Hlim for PA about 35–50 MPa at 10⁷ cycles), so **wear, not breakage, is the life limiter.** Grease the gears and use a dissimilar or metal sun if wear shows up in test 6a.
- **Planet pins:**
  - Ø5 hardened dowel at hip peak: 121–166 MPa, against > 1000 MPa yield. SF > 6.
  - Ø4 at the wheel: 103 MPa.
  - Printed cheek bearing pressure: 3–9 MPa. Acceptable for PAHT-CF/PETG, but use a 6 mm cheek and ≥ 2.5 × d edge margin.
- **Current limits (gear protection):**
  - Hip, Ø96 m1.5 b20, T_max = 22.8 Nm at SF 1.5 → I_max ≈ 22.8/(0.106·9·0.9) ≈ 26 A. Recommend a **20 A** firmware limit.
  - Wheel m1.25 b15 PAHT-CF: T_max ≈ 15 Nm → about 32 A. The traction limit is lower anyway; recommend 15 A.

### 3.4 Backlash and wear under balance torque reversals

- Backlash sits **outside** the motor-encoder loop (the AS5047P is on the motor).
  - At the wheel, it creates a dead-zone and a limit cycle in balancing.
  - At the hip, 1° of backlash on a 0.2 m leg is about 3.5 mm of foot error.
  - Target: ≤ 0.5° at the wheel output and ≤ 0.5° at the hip after run-in.
- Measured reference: Urs et al., PLA planetary: 56 → 82 mrad (3.2 → 4.7°) across 2 actuators after 57 h, i.e. about 13 mrad (0.75°) growth each. Plan for **about 1° growth over life** and re-shimming.
- Mitigations:
  1. Herringbone teeth: higher contact ratio (≈ 2.5), self-centring axially, no axial thrust on bearings.
  2. Print the ring 0.05–0.1 mm undersize on tooth thickness (profile shift) and calibrate with a test coupon. The A1 holds about ±0.05 mm in XY.
  3. Run in with the gears loaded for 30–60 min, then clean and re-grease.
  4. Grease: PTFE-based synthetic (e.g. Super Lube 21030) or silicone grease. Avoid petroleum grease on PETG (stress cracking).
  5. Avoid the same CF-filled material against an unfilled softer gear (the CF abrades it). Use PAHT-CF on PAHT-CF, or a steel sun on PAHT-CF planets (the classic low-wear steel/plastic pair).
  6. Control: add backlash compensation, or use an output-side encoder for the hip (open question).
- Dust: Urs saw fine plastic dust. Seal the wheel-hub gearbox with a lip or labyrinth because floor grit gets in.

---

## 4. Recommendation per gear stage

| Item | Wheel stage | Hip input stage | Hip output stage |
|---|---|---|---|
| Material | PAHT-CF (sun, planets, ring insert). Fallback PETG | PAHT-CF | PAHT-CF, ring insert keyed into a PETG/PAHT-CF housing |
| Module / b | 1.25 / 15 | 1.0–1.25 / 12 | 1.5 / 20 |
| Tooth form | Herringbone 20° PA, helix 20–25°, 0.5 mm root fillet r ≥ 0.38 m | Herringbone | Herringbone. Spur if a catalogue steel sun is used |
| Print orientation | Axis = Z, flat on bed. Herringbone is printable without support | same | same |
| Settings | 0.4 mm hardened nozzle (A1 option), 0.12–0.16 mm layers, **100 % infill** (or 5–6 walls so teeth are all perimeters), filament dried 80 °C/8 h, printed from a dry box. Bed 100 °C, textured PEI + glue, brim for rings | same | same |
| Bearings | Planets: 2× 685ZZ (5×11×5) or 2× MR105ZZ per planet. Carrier: 6806-2RS (30×42×7) | Planets 684ZZ/685ZZ | Planets 2× 685ZZ. Output: 6808-2RS (40×52×7) or 61808 (thin) |
| Pins | Ø4 or Ø5 × 20–24 mm hardened dowel (ISO 8734 / DIN 6325) | Ø4 | **Ø5 × 30 mm** hardened dowel |
| Metal sun option | Catalogue steel spur pinion MOD1.0 (15–20T) or MOD1.5 (13–15T), C45 / S45C, bolted or pressed to a flange on the rotor's 4×M3 Ø40 holes. Examples: Misumi GEABM/GEAKB series, KHK SS series, generic "MOD1 45# steel gear" (AliExpress). **Verify part numbers in P3.** This forces a re-pick of tooth counts to catalogue counts and spur teeth throughout the stage | | |

**Why not POM?** Moulded or machined POM is the textbook plastic gear, but the A1 cannot print it reliably (no adhesion, warping, no enclosure). If the bench test fails, the next step is **bought** POM or steel gears, not printed POM.

**Can the A1 print PAHT-CF?** Bambu lists PA/PAHT-CF as possible on the A1 with the hardened 0.4 nozzle, but it is not ideal without an enclosure. Small round parts such as gears (< 100 mm) are usually fine; long flat parts warp. If PAHT-CF prints fail, the fallback order is:
1. PETG-CF or PETG for the wheel.
2. A metal sun plus a larger face width for the hip.
3. Outsourced SLS PA12 or MJF gears (cheap, isotropic, about 48 MPa).

---

## 5. Material selection per printed part class

Infill percentages assume gyroid unless stated. Mass = ρ × solid volume × effective fill fraction.

| Part class | Material | Why | Density g/cm³ | Walls / infill | Orientation | Notes |
|---|---|---|---|---|---|---|
| Gears (all) | PAHT-CF (fallback PETG for the wheel only) | Strength, temperature, wear | 1.06 (PAHT-CF), 1.27 (PETG) | 100 % | Axis = Z | Dry before printing, store sealed |
| Gear housings / motor mounts | **PETG** (PAHT-CF near the hip motor if the Thermal Eng. reports > 55 °C) | PLA softens at 55–60 °C next to motor and driver | 1.27 | 5 walls, 40–60 % | Bearing bores in XY | Leave a ≥ 2 mm air gap or vent slots between the motor can and housing |
| Body shell / lid | PLA+ or PETG | Stiff, cheap, little heat away from drivers | 1.24 / 1.27 | 3 walls, 15 % gyroid | Large faces flat | Split > 250 mm parts with dovetail + M3 bolts |
| Side plates / hip mounts | **PETG** or PAHT-CF | Carry hip torque + landing. Must not creep | 1.27 | 6 walls, 50–60 % | Plate flat (loads in XY) | Bolt pattern for motor 4×M4 Ø40 through steel washers |
| Legs / linkages (thigh, coupler, shank) | **PETG** (PAHT-CF for the thigh if the mass allows) | Tough under impact. PLA is brittle in a fall | 1.27 | 5–6 walls, 40 % | **Long axis in XY**, never along Z | Pivots: steel shoulder bolts + flanged bearings (F684/F688) or bushings |
| Wheel hub / rim | PLA+ (client: PLA/ABS). **PETG preferred** because the hub motor heats it | PLA hub sits on the motor rotor and may soften | 1.24 / 1.27 | 4 walls, 30–40 % | Axis = Z | ABS not recommended on the open A1 (warp). Castellated rim tabs ≥ 4 mm thick |
| Tyre | **TPU 95A** | Prints well on the A1, keeps its shape on the rim tabs, wears slower | 1.21 | 3 walls, cells open | Axis = Z | Cell/hole pattern: see below |
| Spring mounts / snapper anchors | **PAHT-CF or PETG + steel** | Constant preload → creep. PLA creeps visibly under sustained stress | 1.06 / 1.27 | 100 % around the anchor, 6 walls | Load in XY | Load path must be bolt-in-shear / steel pin, never insert pull-out |
| Electronics trays, lidar mast, camera mount | PLA+ | Low load | 1.24 | 2–3 walls, 15 % | as convenient | Lidar mast: avoid a tall thin Z column (snaps at layer lines in a fall) |
| Battery rail / straps | PETG + Velcro straps | Impact | 1.27 | 4 walls, 40 % | flat | |

**TPU tyre, Shore 95A vs 85A**
- 95A (Bambu TPU 95A HF):
  - Prints at normal speed on the A1.
  - Stiff enough that the slot-and-tab interface does not roll off under lateral (cornering or one-leg-climb) loads.
  - Wears slower.
- 85A:
  - More grip and damping.
  - Very slow to print and stringy.
  - The tyre squirms on the tabs.
- **Recommend 95A** and get compliance from geometry: radial or angled through-holes ("airless" cells).
- What the cells do:
  1. Radial compliance that cuts peak landing g at the hub, which protects the gears and bearings.
  2. A larger contact patch.
  3. Lower mass.
  4. Tunable stiffness by cell wall thickness. Start with 1.2–1.6 mm walls.
- **Mass warning.** A solid tyre Ø170/Ø130 × 30 mm is 283 cm³ ≈ 340 g each. Use Ø170/Ø146 × 25 mm with about 40 % voids instead: ≈ 110 g each. See §7.

---

## 6. Fasteners into plastic

| Item | Recommendation |
|---|---|
| Heat-set inserts M3 | Ruthex-type M3 × 5.7 mm. Hole Ø4.0 mm, depth ≥ 6 mm, **wall around insert ≥ 1.6 mm** (≥ 2 mm in PETG/PA). Edge distance ≥ 2× insert OD |
| Heat-set inserts M4 | M4 × 8.1 mm. Hole Ø5.6 mm, depth ≥ 8.5 mm, wall ≥ 2.5 mm |
| Insert temperature | PLA 210 °C, PETG 240 °C, PAHT-CF 280 °C (iron setting). Insert perpendicular to the layers so the knurl engages several layers |
| When to use inserts | Covers, trays, electronics, housing halves: anything **assembled repeatedly with low load** |
| When to bolt through | Every **primary load path**: hip motor mount, leg pivots, spring anchors, carrier-to-leg, hub-to-carrier. Bolt + nut + steel washer (or a metal plate) clamps the plastic in compression |
| Creep / preload | Polymers relax under bolt clamp. PLA loses a large share of clamp in weeks, PETG less, PA least. Use wide washers (≥ 2× bolt dia), Nyloc nuts or threadlocker (Loctite 243 is safe with PA; **avoid on PETG/PC/ABS**, which crack from it. Use Nyloc there). Re-torque after run-in. Low torque: M3 ≈ 0.5–0.7 Nm into plastic |
| Spring preload | Never anchor a preloaded spring on an insert in pull-out. Use a steel pin or bolt in double shear through ≥ 6 mm of plastic each side, with a pressed steel bushing so the plastic sees bearing pressure < 10 MPa |
| Motor bolts | 8308 stator 4×M4 on Ø40 and rotor 4×M3 on Ø40: bolt through printed flanges into the motor's own threads. Thread engagement ≤ the motor thread depth (check before P3) |
| Pull-out data | CNC Kitchen insert tests: M3 heat-set inserts in PLA fail around the 1 kN level (insert-type dependent). Treat as order-of-magnitude only and design for < 150 N per insert |

---

## 7. Preliminary structural notes (for the Structural Engineer, P4)

**Load cases to analyse later**

| LC | Case | Load |
|---|---|---|
| LC1 | Landing, 20 cm drop, legs compliant | 3–5 g on 4 kg → 120–200 N total, ~100 N per wheel, plus hip back-drive torque. Hip peak 15 Nm. Check with the Theory Eng. spring rate |
| LC2 | Spring (snapper) preload, sustained | Preload force × hours → creep of anchors, side plates and housing bolt clamp |
| LC3 | Fall on side (tip over from 0.5 m) | Impact on the wheel side face and hip housing. Lateral bending of the shank and wheel axle. Body corner impact |
| LC4 | Single-leg climb | Asymmetric load, one wheel carries ~1.5× W, plus a roll moment on the side plate |
| LC5 | Balance reversals, fatigue | ±1.5 Nm wheel, 10⁷ cycles over life |
| LC6 | Motor stall at the current limit | Hip 20 A ≈ 17 Nm, wheel 15 A ≈ 7 Nm into a locked output |
| LC7 | Thermal | Hip housing at 50–60 °C under LC1/LC6 loads |

**Weakest expected parts**
1. Hip output gear teeth, then the hip carrier (planet pin bosses).
2. Wheel axle/hub bearing seat under side fall (moment on a thin plastic seat). Use a steel axle and a 2-bearing span ≥ 20 mm.
3. Leg shank near the wheel (bending + torsion on landing), and pivots (bearing bores ovalising).
4. Spring anchors (creep).
5. The PLA wheel hub near the hub motor (heat + creep).
6. Lidar mast in a fall.

**Design rules for CAD (P3)**
- Min wall: 1.6 mm (4 lines at 0.4 mm). Load-bearing ≥ 2.4 mm (6 lines). Bearing bores ≥ 3 mm wall.
- Fillets:
  - Internal fillets on load paths ≥ 2 mm.
  - Tooth root fillet ≥ 0.38·m.
  - Leg section changes r ≥ 5 mm.
  - Chamfer bed-side edges 0.5 mm (elephant foot).
- Bolt edge distance ≥ 2.5 × d from the hole centre to the edge (M3 ≥ 7.5 mm, M4 ≥ 10 mm). Pitch between bolts ≥ 3 × d.
- Layers: orient so tension and bending stay in XY. Never load across layers in tension (Z strength is ~60–90 % of XY for PLA and much less for CF filled). Legs and plates flat, gears axis-Z, mast lying down if possible.
- Bearing bores: print +0.05 to +0.10 mm (calibrate with a test coupon). Press fits only into PETG/PA, not PLA (creep loosens them). Add a retaining lip or circlip.
- Clearances: sliding 0.2 mm, press 0 to −0.05 mm, gear centre-distance per the calibration coupon.
- Split lines for > 250 mm parts: away from max-bending regions, with dowel/key + ≥ 2 bolts.
- Vent gap ≥ 2 mm between the motor can and any printed part. No PLA within 10 mm of a motor or driver heatsink.

---

## 8. Sources

- Urs, Enninful Adu, Rouse, Moore, "Design and Characterization of 3D Printed, Open-Source Actuators for Legged Locomotion", arXiv:2202.12395 (2022): https://arxiv.org/pdf/2202.12395. FDM-PLA 7.5:1 planetary, 19.1 Nm peak (2 s), 7.5 Nm (20 s), 482 g, 90×70 mm, 57 h life test, 26 mrad backlash growth, steel dowel pins, gears printed axis-Z.
- Yoshida et al., QDD actuator with a 3D-printed planetary reducer, Science Tokyo (2023): https://t2r2.star.titech.ac.jp/rrws/file/CTT100885960/ATD100000413/
- OpenTorque Actuator (8:1 printed planetary, 1150 g): https://hackaday.io/project/159404-opentorque-actuator
- Caden Kraft printed QDD actuator, measured 29.4 Nm: https://www.hackster.io/news/caden-kraft-s-3d-printable-quasi-direct-drive-actuators-cost-as-little-as-40-each-b1f5fa7376d7
- Budget QDD inspired by Mini Cheetah: https://hackaday.com/2025/07/14/a-budget-quasi-direct-drive-motor-inpired-by-mits-mini-cheetah
- Hackaday, "Studying the finer points of 3D printed gears" (material comparison PLA/PETG/ASA/nylon/CF): https://hackaday.com/2024/06/12/studying-the-finer-points-of-3d-printed-gears
- Shaaya, review of 3D-printed gear manufacturing issues: https://real.mtak.hu/211910/1/08-Shaaya.pdf and https://ojs.uni-miskolc.hu/index.php/dms/article/view/3626
- PMC review on 3D-printed polymer gears (wear: PETG most wear-resistant of ABS/PLA/PETG): https://pmc.ncbi.nlm.nih.gov/articles/PMC9147857/
- Zhang et al., "A physical investigation of wear and thermal characteristics of 3D printed nylon spur gears", Tribology International 141 (2020) 105953 (cited by Urs et al.)
- Bambu PLA Basic TDS: https://cdn.shopify.com/s/files/1/0380/5149/files/Bambu_PLA_Basic_Technical_Data_Sheet.pdf
- Bambu PAHT-CF TDS: https://cdn.shopify.com/s/files/1/0380/5149/files/Bambu_PAHT-CF_Technical_Data_Sheet.pdf and https://uwaterloo.ca/rapid-prototyping-centre/sites/default/files/uploads/documents/bambu_paht-cf_technical_data_sheet_v2.pdf
- Bambu PETG-CF TDS: https://cdn.shopify.com/s/files/1/0380/5149/files/Bambu_PETG-CF_Technical_Data_Sheet.pdf
- Filament-for-gears overview (vendor, qualitative): https://siraya.tech/blogs/news/best-filament-for-gears
- Eaglepower LA 8308 KV90 listing (336 g, 22 A cont., 0.186 Ω, 6–12S): https://robu.in/product/eaglepower-la-8308-kv90-motor/
- Standard references (not fetched): Lewis form factor table and the Barth dynamic factor (Shigley's Mechanical Engineering Design, ch. 14), VDI 2736 (thermoplastic gears), ISO 8734 dowel pins.

Values marked "estimate" (fatigue fractions, temperature retention, insert pull-out ~1 kN) are engineering judgement and are **not** taken from a single test source. They must be confirmed by the P6a bench test.

---

## 9. Open questions

1. **Motor KV and Kt** (Theory Eng.). All current-limit numbers scale with Kt. KV90 is assumed.
2. **MKS XDrive Mini current limit** (Electrical Eng.). If the driver peak is < 20 A, the hip torque target may be motor-limited before it is gear-limited.
3. **Hip gearbox topology:** 2-stage simple (3×3) vs compound stepped-planet vs Wolfrom. Axial length budget: motor 28.5 mm + gearbox ~45–55 mm. Decide with the Mech. Design Eng.
4. **Gear temperatures** (Thermal Eng.). If the hip case exceeds 60 °C, even PETG housings fail. Use PAHT-CF or an aluminium motor plate.
5. Can the client's A1 print PAHT-CF acceptably (warp, hardened nozzle purchase)? → Print a test ring and gear coupon before Gate C.
6. Landing back-drive torque on the hip: does the snapper spring sit in series with the gearbox (good) or in parallel (gearbox sees the full impact)? (Theory + Structural Eng.)
7. Is an output-side encoder needed on the hip to remove backlash from the control loop? (Control Eng.)
8. Is a steel sun wanted from day 1 (cost, catalogue tooth counts) or only after the bench test?

---

## 10. Changes to design assumptions

| Was (PLAN.md rev 0/1) | Now proposed | Reason |
|---|---|---|
| "PLA/ABS/PETG structure", gears unspecified | **Gears in PAHT-CF; PLA banned near motors** (gears, housings, motor-side hub) | Temperature + creep. PLA strength falls ~55 % at 50 °C |
| Wheel hub PLA/ABS | **PETG preferred** (PLA+ only if the Thermal Eng. confirms hub < 45 °C). ABS not recommended (open printer) | Hub is bolted to the hub motor |
| Risk mitigation: "herringbone, PETG/PA, wide face, steel pins" | Confirmed, plus: ring pitch as large as possible (Ø84–96), hip m1.5 × 20 mm, wheel m1.25 × 15 mm, Ø5 hardened pins, firmware current limits hip ≤ 20 A / wheel ≤ 15 A | §3 |
| Gear ratio decided by strength? | No: tooth force is independent of ratio at a fixed ring size. Choose the wheel ratio (3.91/4.94/6.0) on speed/torque grounds only | §3.2 |
| Tyre mass not budgeted | Tyre Ø170/Ø146 × 25 mm, 40 % voids ≈ 110 g each (solid thick tyre would be ~340 g) | BOM/mass budget |
| — | Hip gearbox needs a back-drive load limit (series spring / slip) | Landing torque is not limited by motor current |
| — | Metal parts list added to BOM: dowel pins Ø4/Ø5, 685ZZ ×12–18, 6806/6808 ×4, steel axles ×2, shoulder bolts, M3/M4 inserts, optional MOD1/MOD1.5 steel suns ×4 | §4, §6 |

Rough printed gearbox mass for the BOM: wheel stage ≈ 90–120 g each, hip ≈ 150–200 g each, including bearings and pins, excluding the motor.

---

## P1 follow-up (O3, O4)

Rev 1, 2026-11-04. Inputs from `docs/design_targets.md` and `theory.md`:
- Motor KV130, Kt 0.0636 Nm/A.
- Hip 8:1, wheel 3.91:1 (23/22/67).
- Gear design torques: hip **20 Nm**, wheel **10 Nm**.
- Landing cases LC-A…D (theory §3.6).

Scripts:
- `calc/gear_lewis.py`: the `followup()` and `compound_search()` tables.
- `calc/gear_landing.py`: the O4 table.

All safety factors are at **50 °C, PAHT-CF (conditioned), Lewis static allowable 0.7·UTS**, with the same K_share 1.3 and K_v 1.1 as §3.

This section **supersedes** the hip layout in §1 and §4 (a 9:1 2-stage at 15 Nm).

### O3. Gear re-check at the theory design torques

**Wheel, 3.91:1 (23/22/67), m1.25, ring pitch Ø83.75, 10 Nm**

| b (mm) | σ (MPa) | SF PAHT-CF 50 °C | SF PETG 50 °C | b needed for SF 1.5 |
|---|---|---|---|---|
| **15** | 18.3 | **2.23** | 0.97 | 10.1 mm |
| 18 | 15.3 | 2.68 | 1.17 | |
| 20 | 13.8 | 2.98 | 1.30 | |

The baseline m1.25 × 15 mm still holds (SF 2.2). **PETG is no longer an acceptable fallback** for the wheel at 10 Nm and 50 °C (SF < 1.0 at b = 15 mm). The wheel gears must be PAHT-CF, or a 20 mm PETG face run only at ≤ 40 °C.

**Hip 8:1 at 20 Nm: three candidate layouts**

| Layout | Mesh | Teeth (Zs/Zp/Zr) | m | D_r | b | σ (MPa) | SF | b for SF 1.5 |
|---|---|---|---|---|---|---|---|---|
| Single-stage | sun/planet/ring | 12/36/84 | 1.0 | 84 | 20 | 46.3 | 0.88 | 34 mm |
| Single-stage | sun/planet/ring | 12/36/84 | 1.25 | 105 | 20 | 29.6 | 1.38 | 22 mm (housing Ø ≈ 115 mm) |
| 2-stage 3.0 × 2.667 | input | 24/12/48 | 1.25 | 60 | 12 | 32.4 | 1.26 | 14 mm |
| 2-stage 3.0 × 2.667 | output | 36/12/60 | 1.5 | 90 | 24 | 24.0 | 1.70 | 21 mm |
| **Compound stepped planet** | sun → big step | 18 / 36 | 1.25 | — | 14 | — | **2.09** | — |
| (ring fixed, carrier out) | small step → ring | 18 / 63 | 1.5 | 94.5 | 20 | — | **2.15** | — |

Why the simple layouts are weak:
- An 8:1 simple stage needs a 12-tooth sun (Lewis Y = 0.245).
- A 2-stage 8:1 needs two stages of about 2.8:1, and those force 12-tooth planets.
- In a compound stage, the ring mesh carries only T·(1 − 1/i) = 0.875·T and uses an 18-tooth step (Y = 0.309).

**Recommended hip stage: compound stepped-planet, i = 8.000 exactly**
- Sun Zs = 18 (m1.25) drives the big planet step Zp1 = 36 (m1.25, b ≈ 14 mm).
- The small planet step Zp2 = 18 (m1.5, b = 20 mm) meshes with a fixed ring Zr = 63 (m1.5, pitch Ø94.5, housing OD ≈ 106 mm).
- 3 planets, carrier = output. Ratio check: i = 1 + Zr·Zp1/(Zs·Zp2) = 1 + 63·36/(18·18) = 8.000.
- Geometry checks:
  - Both centre distances are 33.75 mm exactly, so no profile shift is needed.
  - Big planets: tip Ø47.5 < planet spacing 58.5 mm.
  - Equal-spacing condition: (18·18 + 63·36)/(3·18) = 48, an integer.
  - **Verify the planet step phasing in CAD.** Each planet is one printed part with both steps, so tooth phase must be matched across the 3 planets.
- Variant compatible with a catalogue steel sun: m1.0 27/45 + m1.5 15/63, i = 8.000, SF 2.27 / 2.02.
- Advantages over 2-stage: one carrier, about 40–45 mm axial length, and a single output bearing (6808).
- Disadvantage: lower efficiency (about 0.80–0.85, still back-drivable at 8:1).
- Planet pin load ≈ Ft1 + Ft2 ≈ 106 + 177 = 283 N. Ø5 hardened dowel, SF > 6, unchanged.
- Planet bearings: 2× 685ZZ inside the small step (root Ø ≈ 23 mm).

**Current limits at 20 Nm, KV130**
- 40 A gives 40·0.0636·8 = 20.4 Nm at the output, so the 40 A jump-phase limit sits exactly at the design torque.
- With SF 2.1 the gear tolerates this. Keep **40 A only in the push-off phase** and **≤ 20 A (10.2 Nm) at all other times**, including landing.
- Wheel: 15 A gives 15·0.0636·3.91 = 3.7 Nm. Theory's 10 Nm landing spin-up case gives SF 2.2.

### O4. Landing load path: back-driven torque at the hip teeth

With the spring in parallel (body → thigh), spring force never crosses the teeth. Only two things reach them:
1. Motor torque × N, which is current-limited.
2. The torque needed to decelerate the motor rotor through the gear, N²·J_r·α.

Case 2 peaks when the leg hits the end stop with the motor unpowered. Model (`gear_landing.py`):
- One degree of freedom, rigid gear.
- Reflected rotor inertia N²J_r = 0.0128 kg m², which is 15 % of I_tot = 0.085 kg m² (leg 0.029 + rotor + 1.08 kg body × J²).
- End stop at 120 mm hip height (J = 0.201 m/rad).
- Gear torque = stop torque × rotor share.

| Case | v at stop | Stop stiffness (axle-referred) | Stop torque | **Gear torque** | SF (allowable 42 Nm) | Stop travel |
|---|---|---|---|---|---|---|
| LC-A controlled (theory) | — | — | — | 6.3 | 6.6 | — |
| LC-C one wheel first, controlled (theory) | — | — | — | 12.9 | 3.2 | — |
| LC-B-like, motors off, TPU bumper | 2.0 m/s | 25 kN/m | 92 Nm | 13.8 (theory: 17.2) | 3.0 (2.4) | 18 mm |
| same, J_r +40 % | 2.0 | 25 | 95 | 18.8 | 2.2 | 19 mm |
| same, faster (2.6 m/s) | 2.6 | 25 | 120 | 18.0 | 2.3 | 24 mm |
| LC-D-like, full body on one leg (knee pin 1572 N case) | 2.0 | 25 | 114 | 11.3 (theory: 4.5) | 3.7 | 23 mm |
| Soft bumper | 2.0 | 10 | 58 | 8.8 | 4.8 | 29 mm |
| **Stiff printed end stop** | 2.0 | 250 | 292 | **43.8** | **0.95** | 6 mm |
| Stiff stop, fast, J_r +40 % | 2.6 | 250 | 391 | **77** | **0.54** | 8 mm |
| End stop acting **through the gearbox** (theory LC-D hip torque) | — | — | 50.8 | **50.8** | **0.82** | — |
| Motor phases **shorted** as a fault brake, leg at 2 m/s (ω_m 80 rad/s, R-limited ≈ 57 A) | — | — | — | **≈ 29** (≈ 20 with inductance) | 1.4–2.1 | — |
| Motor at 40 A (jump phase) / 20 A | — | — | — | 20.4 / 10.2 | 2.1 / 4.1 | — |

What the numbers show:
- In every **normal** case (LC-A, LC-C) the gear torque is 6–13 Nm and SF ≥ 3.
- In the **fault** cases with a compliant end stop the gear sees 11–19 Nm, which is inside the 20 Nm design torque (SF ≥ 2.2).
- The gear fails only if:
  (a) the end stop is stiff (printed plastic on plastic), or
  (b) the end stop or the spring reacts through the gearbox output instead of directly from thigh to body, or
  (c) the driver short-circuits the phases on a fault.
- The 1572 N knee-pin case is a **structural** load (pins, coupler, end-stop lugs). It does not load the teeth, as long as rule (b) is kept.

**Recommendation: option 1, parallel spring plus landing controller.** A series elastic element and a slip clutch are **not needed**, provided these four conditions are written into the design rules:
1. **Compliant end stop between thigh and body**, never through the gearbox. TPU (85A–95A) bumper or block, axle-referred stiffness ≤ 25 kN/m (hip angular stiffness ≲ 1000 Nm/rad), with **≥ 20 mm of axle travel (≈ 0.1 rad / 6° at the hip)** before any hard contact. A progressive (conical or cellular) TPU shape is preferred.
2. **Spring anchors body → thigh** (as theory §3.4), never on the carrier or output flange.
3. **Driver fault state = phases floating** (ODrive IDLE). No short-circuit or active brake on a fault or e-stop. Regen goes to the brake resistors only while in closed loop at the current limit. (→ Electrical, Control.)
4. **Current schedule:** 40 A only during push-off. Landing and everything else ≤ 20 A. The landing controller (virtual spring-damper, LC-A) should be active before touchdown.

Why not the alternatives:
- **Series elastic element:** it would cut the rotor-inertia spike further. But it adds compliance and backlash at the hip, against the control targets (hip backlash ≤ 0.5°, high bandwidth for jump timing), and it adds parts and mass. Not justified while the compliant-stop numbers give SF ≥ 2.2.
- **Slip clutch:** a printed friction clutch's slip torque drifts as the plastic creeps under the clamp load (see §6). A metal clutch adds about 50–80 g per hip. Keep it only as a **fallback**, if the bench test (P6a drop test) shows gear torque > 20 Nm with the real bumper.

**Open items from O3/O4**
- Measure rotor inertia J_r. The fault spike scales with J_r (+40 % gives +36 % gear torque).
- Electrical must confirm the XDrive Mini fault behaviour (floating vs braking).
- Structural should size the end-stop lugs and pins for 92–120 Nm stop torque at the hip (LC-B/D-like) and the 1572 N knee pin.
- P5/P6a: drop test the hip with a torque estimate from motor current and an output encoder, to validate the 1-DOF model. The model ignores gear torsional compliance, which can overshoot up to about 2×.

**Changes to design assumptions (rev 1)**

| Was | Now | Reason |
|---|---|---|
| Hip ~9:1 2-stage, output m1.5 × 20, design 15 Nm | **Hip 8:1 compound stepped planet**: m1.25 18/36 + m1.5 18/63, b 14/20 mm, ring Ø94.5, SF 2.1 at 20 Nm and 50 °C | Theory 8:1 and 20 Nm; simple 8:1 layouts need 12-tooth gears |
| Wheel PETG fallback | **PAHT-CF only** for wheel gears (PETG SF 0.97 at 10 Nm, 50 °C) | 10 Nm design torque |
| Hip current ≤ 20 A always | 40 A only in push-off (20.4 Nm = design torque), ≤ 20 A otherwise | Theory jump requirement |
| Open: series spring or clutch? | Parallel spring + landing controller + **compliant end stop (≤ 25 kN/m, ≥ 20 mm travel), floating-phase fault state** | O4 table |

---

## P1 follow-up (O9 wheel gear)

Rev 2, 2026-11-04. The wheel motor is now the **T-Motor MN5008 KV170** (128 g, Ø55.6 × 32, 6 mm shaft, 15 A limit), with a single-stage planetary of about 3.5:1 (theory O9).

Design torques at the wheel output:
- 2.3 Nm fatigue (reversing 3–5 Hz)
- 4.5 Nm max operating
- 8.5 Nm ultimate

Criteria at 50 °C:
- SF ≥ 1.5 at 4.5 Nm and SF ≥ 1.2 at 8.5 Nm, both against the static allowable 0.7·UTS (conservative for an ultimate case).
- Also, my criterion: reversed-fatigue SF ≥ 1.5 at 2.3 Nm. The planets are idlers and the balance torque reverses.

Script: `calc/gear_lewis.py` → `o9_wheel()`. This section **supersedes** the 8308 wheel stage (3.91:1, m1.25 × 15) in O3 and §1.

### Tooth counts

**Theory's 20/15/50 cannot be assembled with 3 equally spaced planets:** (Zs + Zr)/3 = 70/3 is not an integer. Valid 3-planet sets near 3.5:1:

| Zs/Zp/Zr | i | Notes |
|---|---|---|
| **24/18/60** | **3.500** | exact ratio, **recommended** |
| 22/17/56 | 3.545 | |
| 26/19/64 | 3.462 | |
| 17/13/43 | 3.529 | small planets |
| 20/16/52 | 3.600 | closest to theory's 20-tooth sun |

### Strength at 50 °C (Lewis, K_share 1.3, K_v 1.1)

| Zs/Zp/Zr | m | Ring pitch Ø | b | PAHT-CF SF @4.5 / @8.5 / fatigue @2.3 | PETG SF @4.5 / @8.5 / fatigue | PLA SF @4.5 |
|---|---|---|---|---|---|---|
| 24/18/60 | 1.0 | 60 | 12 | 2.12 / **1.12** / **1.31** ✗ | 0.93 / 0.49 / 0.57 | 0.64 |
| 24/18/60 | 1.25 | 75 | 8 | 2.21 / **1.17** / 1.36 ✗ | 0.96 / 0.51 / 0.59 | 0.66 |
| 24/18/60 | **1.25** | **75** | **10** | **2.77 / 1.46 / 1.70 ✓** (minimum) | 1.21 / 0.64 / 0.74 | 0.83 |
| 24/18/60 | **1.25** | **75** | **12** | **3.32 / 1.76 / 2.04 ✓** (recommended) | 1.45 / 0.77 / 0.89 | 1.00 |
| 20/16/52 | 1.25 | 65 | 12 | 2.75 / 1.46 / 1.69 ✓ | 1.20 / 0.64 / 0.74 | 0.83 |

**Material: PAHT-CF.**
- PETG and PLA fail in every row, mainly on ultimate and reversed fatigue at 50 °C. There is no cheaper material that passes.
- PAHT-CF (1.06 g/cm³) is also the **lightest** option. PETG is 1.27 g/cm³.
- Housing and cover: PETG (no tooth loads).
- If the Thermal Engineer confirms the hub stays ≤ 40 °C, PETG still fails ultimate (about 0.85), so the answer does not change.
- Optional metal sun: a catalogue **MOD1.25 24T** steel spur gear is uncommon. If a steel sun is wanted, use **m1.0 31/23/77** (i = 3.484, ring Ø77; re-check SF, about −10 % vs m1.25) with a catalogue **MOD1 31T** gear. Otherwise keep it all printed.

### Recommended wheel stage

| Item | Value |
|---|---|
| Teeth | sun 24 / planet 18 / ring 60, 3 planets, **i = 3.500** |
| Module / pressure angle / form | m1.25, 20°, herringbone, helix 20° (spur if a steel sun is used) |
| Face width | **12 mm** (10 mm minimum) |
| Pitch Ø | sun 30, planet 22.5, ring 75 mm |
| Centre distance | 26.25 mm. Planet tip Ø25 < planet spacing 45.5 mm ✓ |
| Ring insert | root Ø ≈ 78.1, OD ≈ 86 mm (3–4 mm wall), keyed into the PETG housing. Fits inside the Ø170 wheel with ≈ 15 mm radial room to the rim inner Ø (~120 mm) |
| Axial length | about 12 gear + 2 × 4 carrier + 2 clearance ≈ **22–24 mm**. Motor 32 mm, so motor + gearbox ≈ 56 mm inside the hub |
| Sun mounting | Printed sun with flange, bolted to the MN5008 rotor's prop-mount threaded holes (**verify the pattern on the part**) and centred on the 6 mm shaft. No set screw into plastic |
| Planet pins | hardened dowel **Ø5 × 20 mm** (ISO 8734). Load at 8.5 Nm ≈ 216 N, σ ≈ 70 MPa, SF > 10. Ø4 would also pass |
| Planet bearings | **2 × 685ZZ (5 × 11 × 5) per planet**: 4.2 mm wall to the planet root. Light option: 1 × 685ZZ + 0.2 mm-clearance plain bore (−6 g total) |
| Carrier | PAHT-CF, two cheeks ≥ 4 mm with 3 bridges, pins pressed. **Best: carrier integrated into the wheel hub** (torque only). Theory: the axle bearings carry all radial load (≤ 312 N), never the gear |
| Carrier / sun centring | one thin bearing (e.g. 6704-2RS, 20 × 27 × 4, ≈ 5 g) between carrier and stator mount if the carrier is a separate part |
| Print | axis = Z, 100 % infill, 0.12–0.16 mm layers, dried PAHT-CF, hardened nozzle (as §4) |
| Driver current limit | 15 A (theory) gives 2.3 Nm. Gear SF at that torque: static 6.5, fatigue 2.0 |

### Gearbox mass estimate (per wheel)

| Part | Mass (g) |
|---|---|
| Sun with flange (PAHT-CF) | 10 |
| 3 planets (PAHT-CF, bearing bores) | 12 |
| Ring insert (PAHT-CF) | 15 |
| 3 steel pins Ø5 × 20 | 9 |
| 6 × 685ZZ | 12 |
| Fasteners, grease | 5 |
| **Gear core subtotal** | **≈ 63** |
| Carrier as a separate part (PAHT-CF) + 6704 bearing | +23 |
| Separate PETG housing/cover (if not shared with hub/motor mount) | +25 |
| **Total, separate carrier and housing** | **≈ 110** |

Totals:
- **Integrated design** (carrier = hub, ring held by the motor-mount sleeve): ≈ 65–80 g.
- Theory assumed 60–75 g, so it is consistent only for the integrated design.
- A standalone gearbox adds about **+35 g per side** of unsprung mass.

Weight options:
- b10 instead of b12: −6 g
- 1 bearing per planet: −6 g
- Ø4 pins: −3 g

### Open items (O9 gear)

1. **Theory must update the example teeth to 24/18/60.** 20/15/50 cannot be assembled with 3 planets.
2. Measure the MN5008 rotor prop-mount bolt pattern and thread depth (sun mounting).
3. Thermal: hub temperature. 50 °C is assumed; PAHT-CF passes up to about 80 °C.
4. Mechanical: integrate the carrier into the hub to hit about 70 g. The encoder magnet on the stator-side shaft end (theory) needs a path past the carrier and sun. Check in P2.

### Changes to design assumptions (O9)

| Was | Now | Reason |
|---|---|---|
| Wheel 3.91:1 23/22/67 m1.25 × 15, 10 Nm (8308) | **3.500:1, 24/18/60, m1.25 × 12 mm, ring Ø75, PAHT-CF** | MN5008 hub motor, O9 torques |
| Theory example 20/15/50 | 24/18/60 | 3-planet assembly condition |
| Wheel gearbox 60–75 g | 65–80 g integrated; ≈ 110 g standalone | Mass estimate above |

---

## Hip 6:1 option

Rev 3, 2026-11-05. Reason (DECISIONS.md, theory at 6.0 kg): 8:1 jumps 16 cm and fails; 6:1 jumps 21.6 cm. Goal: a 6:1 compound stepped-planet set that fits the **existing** hip housing (docs/parts/hip_gearbox.md). Script: `calc/gear_hip6.py` (run it to regenerate every number below). Landing numbers: `calc/gear_landing.py` re-run with N = 6 and N = 8.

### Result: change only the sun and the planet big step

Ratio = 1 + (Zp1/Zs)·(Zr/Zp2) = 6 with the ring stage kept (Zr 63, Zp2 18, m1.5, b20, centre distance 33.75 with no shift) gives **Zp1/Zs = 10/7**. Stage-1 candidates at the fixed centre distance 33.75:

| Zs/Zp1 | m1 | a0 | shift needed (x1+x2) | contact ratio | planet tip R (limit 57.5) | verdict |
|---|---|---|---|---|---|---|
| 21/30 | 1.25 | 31.88 | +1.78 | 1.46 | 54.6 | reject (huge shift, 27° working PA) |
| **28/40** | **1.0** | 34.00 | **−0.243** | **1.75** | **54.7** | **use** |
| 35/50 | 0.8 | 34.00 | −0.304 | 1.80 | 54.5 | reject (teeth too fine for a printed part) |

Because the ring, carriers, bearings, pins, 6806 seat and housing are untouched, the **tooth counts of the ring stage stay 63 / 18**.

### Exact parts to change in the CAD

| Part | Old (8:1) | New (6:1) |
|---|---|---|
| **HG_Sun** | 18 T, m1.25, spur, b 15.5, on Ø50 × 5 flange | **28 T, m1.0, 20° spur, b 15.5, x = −0.146** (sun pitch Ø28, tip Ø29.7, root Ø25.2). Flange Ø50 × 5, 4×M3 on Ø40 and the Ø14 × 2 relief unchanged (root Ø25.2 sits well inside the Ø40 bolt circle) |
| **HG_Planet big step** | 36 T, m1.25, spur, z 5.5–19.5 (b14) | **40 T, m1.0, 20° spur, b 14 (same z 5.5–19.5), x = −0.097** (pitch Ø40, tip Ø41.8, root Ø37.5). Tip swept radius 54.7 mm against the 57.5 mm already cleared by the housing, so **the skirt, cover and ring are unchanged**. Re-position the 6 × Ø7 lightening holes inside root Ø37.5 (keep ≥ 3 mm rim) |
| HG_Planet small step | 18 T, m1.5, herringbone ±20°, b20 | **unchanged** |
| HG_Ring (63 T m1.5 b20), carriers, pins Ø5 × 45, 685ZZ, 6806, housing | | **unchanged** |

Checks (all in `gear_hip6.py`):
- Ratio 1 + 40·63/(28·18) = **6.000000**.
- Centre distances: stage 1 works at 33.75 with the negative shift above, stage 2 is 1.5·(63 − 18)/2 = 33.75.
- Contact ratio stage 1 is 1.75 and stage 2 stays 1.79.
- Sun tip R 14.85, root R 12.6. Sun stays clear of the three planets.
- Tip gap between adjacent big steps is 16.7 mm (was 10.96).
- Backlash: thin each gear by 0.06 mm as before. The shift above gives zero backlash before thinning. Output lost motion stays about 0.2°.
- The sun core is larger (root Ø25.2 against about Ø19.7 for the 18 T sun), so it is stiffer on the rotor.

### Assembly condition and phasing offset
- General: (Zs·Zp2 + Zr·Zp1)/(3·gcd(Zp1, Zp2)) = (28·18 + 63·40)/(3·2) = **504, integer, OK**.
- Zs/3 = 9.33 is **not** an integer (it was 6 at 8:1), so the planets are not trivially identical. Checked: the phase term between the two steps is 120·k·(Zs/Zp1 + Zr/Zp2) = 120·k·4.2 = 504·k degrees, which is a whole number of degrees for every planet. The two steps' tooth pitches (9° and 20°) share a 1° lattice, so **all three planets are the same printed part with the same step offset**.
- **Offset: 0** (a big-step tooth centre and a small-step tooth centre on the same radial line; they coincide every 180°, because 9° and 20° share that period). Mark that line with a dot on the big-step face.
- Assembly order is unchanged: the sun goes in **last** and is turned until it drops into the three planets (it has 28 positions, and any step offset can be matched by turning it). Phasing in the CAD:
  - ring tooth centred on 0° (unchanged)
  - planet 0 at (33.75, 0), small-step gap facing the ring (as before)
  - big-step tooth centre on the planet's mesh line at the **same angle as the small-step tooth centre** (offset 0)
  - sun: place a tooth gap on the 0° line, then rotate it by a half pitch (6.43°) if the interference check shows contact.
  Re-run `hip_gear_mesh_check.py` with 6:1 kinematics.

### Strength at 20 Nm output, 50 °C, PAHT-CF (Lewis, K_share 1.3, K_v 1.1)

| Mesh | Gear / m / b | σ MPa | SF static at 20 Nm | SF reversed fatigue at 8 Nm | b needed for SF 1.5 |
|---|---|---|---|---|---|
| 8:1 sun-planet (old) | 18 T m1.25 b14 | 19.6 | 2.09 | 1.64 | 10.0 |
| **6:1 sun-planet** | **sun 28 T m1.0 b14** | 23.0 | **1.78** | **1.40** | 11.8 |
| 6:1 sun-planet, b16 | same, b16 | 20.1 | 2.04 | 1.60 | |
| 8:1 planet-ring (old) | 18 T m1.5 b20 | 19.0 | 2.15 | 1.69 | 14.0 |
| **6:1 planet-ring** | 18 T m1.5 b20 | 18.1 | **2.26** | 1.77 | 13.3 |

Minimum SF is **1.78** (sun mesh), which passes ≥ 1.5. The sun mesh is the weak one because m1.0 is smaller. If more margin is wanted, make the big step and sun b16 (the planet z-range grows by 2 mm; check the 1.5 mm axial gaps first). The 8:1 value for the sun mesh was also computed on the weakest gear (18 T planet small step), as then.

### New motor-side and carrier loads at the same 20 Nm output

| | 8:1 | 6:1 |
|---|---|---|
| Sun torque | 2.50 Nm | **3.33 Nm (+33 %)** |
| Tangential force, sun mesh (per planet, no K) | 74 N | **79 N (+7 %)**: sun is bigger (Ø28 against Ø22.5), so force rises less than torque |
| Tangential force, ring mesh | 123 N | **118 N (−4 %)** |
| Planet pin / carrier load (with K) | 282 N | **282 N, unchanged**: it depends on the output torque only. Pins, planet bearings, carrier and 6806 need no re-check |
| Motor torque for 20 Nm out (η 0.85) | 2.94 Nm (46 A) | **3.92 Nm (62 A)** |
| **Max forward output at 40 A** (Kt 0.0636) | 17.3 Nm | **13.0 Nm** |

Consequences:
- The motor **cannot** reach 20 Nm any more: at 40 A the output is 13 Nm, so the gears are now loaded to SF ≥ 2.7 by the motor in forward drive. The 20 Nm design case is only reached by back-driven shocks (below).
- The theory's needs are inside the 13 Nm: standing 3.8 Nm, single-leg climb 8.5 Nm. Continuous torque at 14 A is 14·0.0636·6·0.85 ≈ 4.5 Nm, below the 8.5 Nm single-leg case, so that case is brief use only (theory's own note).

### Reflected inertia at the motor
Reflected inertia scales with N²: output-side N²·J_r = 36·2.0e-4 = **0.0072 kg m²**, against 64·2.0e-4 = 0.0128 at 8:1 (**0.56×**, −44 %). J_r is the unmeasured estimate (±40 %). Consequences: the hip is easier to back-drive and impact tolerant, and the motors-off landing spike drops (next).

### Back-driven torque, motors-off fault landing (end-stop impact)
Same 1-DOF model as O4 (`gear_landing.py`: gear torque = stop torque × N²J_r/I_tot), v = 2 m/s at the end stop:

| Case | 8:1 gear torque | 6:1 gear torque | 6:1 / 8:1 |
|---|---|---|---|
| Layout mass, TPU bumper 25 kN/m | 13.8 Nm | **8.1 Nm** | 0.58 |
| Layout mass, stiff 250 kN/m | 43.8 | 25.5 | 0.58 |
| CAD mass 6.4 kg (I_leg 0.06, 2.2 kg/leg, J 0.18 at 140 mm), 25 kN/m | 10.7 | **6.1** | 0.57 |
| CAD mass 6.4 kg, stiff 250 kN/m | 33.7 | **19.3** | 0.57 |

- The 6:1 set takes **about 0.57× the 8:1 back-driven torque**. Applied to theory's fault number (**30 Nm at 8:1**), this gives **about 17 Nm at 6:1** against theory's 16 Nm limit: near the limit, no longer 2× over it.
- Against the Lewis capacity of this design (SF 1.0 at 1.78 × 20 = **about 36 Nm** static, 50 °C), 17 Nm leaves SF 2.1.
- The compliant TPU end stop from O4 (≤ 25 kN/m, ≥ 20 mm travel) still applies. With it the gear sees 6–8 Nm. With a stiff printed stop 19–26 Nm (SF 1.4–1.9), still safe for the teeth at 6:1, where 8:1 failed (34–44 Nm, SF 0.8–1.1).
- The load path conditions from O4 are unchanged (spring and end stop act body to thigh, never through the gearbox; phases floating on fault).

### Open items (6:1)
1. Update `hip_gear_geometry.py` / `build_hip_gearbox.py` with the sun 28 T x −0.146 and big step 40 T x −0.097; re-run the mesh interference check (the shift gives 0.12 mm backlash after thinning).
2. A 28-tooth m1.0 sun is the finest tooth in the stage. Print a sun coupon in PAHT-CF on the A1 (m1.0 teeth are 2.2 mm tall).
3. Hip current: 40 A jump-phase limit gives 13.0 Nm output (6:1) against 17.3 Nm at 8:1, but Theory's jump sim already includes this.
4. Theory's 16 Nm gearbox limit and my Lewis capacity (36 Nm static) differ; Structural/Theory should state which one governs.
5. Measure J_r. The fault torque scales with it.
