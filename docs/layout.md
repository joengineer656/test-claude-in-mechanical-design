# P2 Master Layout — rev 0

Owner: Mechanical Design Engineer · Date: 2026-11-04 · Inputs: DECISIONS.md, PLAN.md, docs/design_targets.md rev 2 (+ manager update rev 2.1: end stop ≈10 kN/m, engages at hip 130 mm, ≥30 mm travel; knee pin design load ≤2.0 kN), theory/electrical/thermal/materials_gears/mass_budget, bom/bom.md, cad/vendor/SOURCES.md.

Files:
- SolidCraft design: `cad/assembly/master_layout.solidcraft` (59 envelope bodies, all named, pose and envelope driven by user parameters)
- STEP: `exports/step/master_layout.step`
- Screenshots: `docs/screenshots/master_layout_iso.png`, `master_layout_front.png`, `master_layout_side.png` (nominal), `master_layout_side_crouch.png`, `master_layout_side_extended.png`
- CoM + clearance script: `docs/analysis/calc/com_layout.py` → output `docs/analysis/calc/com_layout_output.txt`

Frame: X forward, Y left, Z up, mm. The origin is the ground under the robot centre at nominal stance. In the CAD and the script the **body stays fixed**: in other poses the legs and wheels move, and the ground is at axle z − 85.

Envelope blocks only (no teeth, fillets or holes). The vendor STEPs (LD19, Pi Camera 3, XT60, WROOM) were **not** imported. SolidCraft can write only to its sandbox folder, so the placement transforms could not be checked in this pass. Every bought part is an envelope block at the SOURCES.md size. The STEP import is planned for P3.

## 1. Parameters (SolidCraft user parameters)

| Name | Value | Meaning |
|---|---|---|
| wheel_d | 170 | tyre OD |
| tyre_w | 25 | tyre width (Ø170/Ø146 × 25, Materials §7) |
| track_w | 275 | wheel centre to wheel centre → **overall width 300** |
| hub_d | 86 | hub motor + 3.5:1 stack envelope (ring OD ≈ 86) |
| thigh / shank / coupler / knee_pin | 121 / 189 / 113 / 42 | 4-bar (theory §3.3) |
| shank_bend | 175° | angle between K→C and K→W |
| shank_full | √(shank² + knee_pin² − 2·shank·knee_pin·cos 175°) = 230.9 | C → W bar length |
| Bx, Bz | 46, 34 | coupler body pivot B relative to the hip |
| crank_r | 40 | spring crank on the thigh, opposite the thigh |
| hip_h | 195 | hip above the axle (middle of 100–290) |
| hip_x | 28 | hip ahead of the axle at nominal (from the 4-bar) |
| hip_z | wheel_d/2 + hip_h = 280 | |
| thigh_ang, shank_ang, coupler_ang, spring_ang, spring_len | pose set (below) | drive the pose; `com_layout.py` prints them |
| Kx/Kz, Cx/Cz, Wx/Wz, Px/Pz | expressions | knee, coupler pin, axle, crank pin |
| body_w × body_h × body_d | 126 × 190 × 210 | body shell box |
| body_x0, body_z0 | −125, 150 | rear and bottom of the body |
| bat_x | −104.5 | battery centre x (trim rail, 0 to +20 forward) |
| lidar_x, mast_h | −40, 25 | LD19 position and mast height |

Pose sets (deg; spring_len in mm). Set them with one `batch` of `parameters.change`:

| Pose | hip_h | thigh_ang | shank_ang | coupler_ang | spring_ang | spring_len |
|---|---|---|---|---|---|---|
| crouch | 101 | 0.482 | −148.240 | −6.851 | 33.141 | 104.23 |
| nominal (saved) | 195 | −29.987 | −135.530 | −36.533 | 24.105 | 89.75 |
| extended | 289 | −72.677 | −114.283 | −84.929 | 17.323 | 62.00 |

Lateral stack per side, outboard to inboard (Y, left side; the right side is mirrored):

| Item | Y range | Note |
|---|---|---|
| Tyre + hub rim | 125–150 | Ø170 |
| Hub motor + gear stack | 80–125 | Ø86. MN5008 32 + gear stage 22 = 54 axial, fits in 70 |
| Wheel encoder (Ø30 × 8) | 70–78 | in a pocket of the shank foot |
| Coupler | 93–101 | outboard of the thigh. C and B pins cross the thigh plane |
| Spring Ø14 | 81–95 | in the thigh plane, above and behind the hip |
| Thigh + crank | 81–91 | bolted to the hip output face |
| Shank | 68–80 | **inboard of the thigh**, inside the Y span of the gearbox; clears it in XZ |
| Hip gearbox Ø100 | 40–80 | 40 mm axial budget |
| 8308 Ø92 × 28.5 | 11.5–40 | |
| Hip Al plate Ø100 × 3 | 8.5–11.5 | thermal rule 3 |
| Hip motor-side encoder Ø30 × 8 | 0.5–8.5 | back to back across the mid-plane |
| Body shell wall | ±63 | |

## 2. Component placement (nominal; centroids from `com_layout.py`)

| Component | x | y | z | mass g |
|---|---|---|---|---|
| Battery 6S 2200 + cradle (**upright at the rear wall**, 35 × 45 × 107) | −104.5 | 0 | 206.5 | 365 |
| Pi 4 + heatsink (85 × 56 × 28) | −42.5 | 0 | 214 | 56 |
| ESP32 PCB 70 × 50 (+ IMU) | 25 | 0 | 190 | 25 |
| **IMU ICM-42688-P** | 0 | 0 | 187 | (in PCB) |
| PDB / 5 V buck | 52 / 52 | 0 / −35 | 160 / 158 | 25 / 7 |
| 40 mm fan (front inlet, low) | 77 | 0 | 185 | 15 |
| Inlet vent 60 × 55 (front, low) / outlet 70 × 50 (rear, top) | 85 / −125 | 0 | 185 / 310 | — |
| 4 × XDrive Mini on 70 × 70 × 1.5 Al plates (vertical, on the side walls) | −85 | ±46.75 | 275 (hip) / 195 (wheel) | 4 × 61 |
| 2 × brake resistor HS25 (on an Al bracket, ≥10 mm from plastic, at the outlet) | −72.5 | ±15 | 257.5 | 2 × 10 |
| E-stop Ø22, Ø40 head (top, rear corner) | −100 | 0 | 335 | 30 |
| Anti-spark switch (top) / 50 A fuse (top hatch) | −100 / −97.5 | +38 / −40 | 332 / 328 | 18 / 15 |
| LD19 lidar on a Ø20 × 25 mast (base z 365) | −40 | 0 | 382 | 52 |
| Pi camera 3 (front face) | 91 | 0 | 300 | 7 |
| Body shell + body fasteners | −20 | 0 | 245 | 282 + 160 |
| Harness / NTC / misc | −45 | 0 | 245 | 131 |
| Hip stack per side: encoder 8, Al plate 32, 8308 + fasteners 360.5, gearbox 253 | 28 | ±4 / ±10 / ±26 / ±60 | 280 | 653.5 |
| Thigh / shank / coupler (each side) | 80 / 82 / 119 | ±86 / ±74 / ±97 | 250 / 166 / 280 | 33 / 63 / 31 |
| Knee / C / B / hip joint hardware (each side) | 133 / 165 / 74 / 28 | ±86 / ±97 / ±97 / ±86 | 220 / 247 / 314 / 280 | 40 / 25 / 16 / 16 |
| Spring (each side) | 34 | ±88 | 318 | 35 |
| Spring body anchor | 75.2 | ±79 | 336.6 | (body) |
| TPU end stop + bracket (each side) | 100.3 | ±86 | 292.5 | 13 |
| Leg-side hip encoder / leg cable (each side) | 28 / 66 | ±85 / ±74 | 280 / 152 | 8 / 28.5 |
| Wheel module (each side) | 0 | ±125 | 85 | 497 |
| **Total** | | | | **4370** |

Mass = BOM 4312 g + 42 g (Al plates for the 2 hip drivers, which no longer sit on the hip plate) + 16 g (2 motor-side hip encoder kits). See §8.

## 3. Centre of mass (whole robot, 4.370 kg)

| Pose | Fore-aft vs axle | Lateral | Height above ground | Above axle | Target |
|---|---|---|---|---|---|
| Crouch (hip 101) | +10.9 | −0.04 | 148.7 | 63.7 | trim ±20 / pitch |
| **Nominal (hip 195)** | **+2.1** | **−0.04** | **215.8** | **130.8** | **±5 / ≤5 → PASS** |
| Extended (hip 289) | +5.7 | −0.04 | 283.3 | 198.3 | trim ±20 / pitch |

- The axle moves 10–11 mm aft relative to the body at crouch and at full extension (4-bar drift).
- The controller absorbs this with body pitch (≈ 1.6° at full extension, ≈ 9.7° at full crouch, where the CoM is only 64 mm above the axle), or with the battery rail. The script asserts ±5 mm only at nominal and ≤ 20 mm at the other poses.
- IMU: 2.1 mm fore-aft and 28.8 mm vertical from the nominal CoM (inside ±30). It is ≥ 47.9 mm from the nearest motor, driver, resistor or fan (rule ≥ 40). **PASS.**
- The script recomputes all of these values and asserts them (`python3 docs/analysis/calc/com_layout.py`).

## 4. Clearance checks (`com_layout.py`; XZ distance for parts whose Y ranges overlap; crouch, nominal and extended)

| Check | Result |
|---|---|
| Static interior blocks overlap | none |
| Leg clearances, worst | spring ↔ B pivot 3.3 · coupler ↔ spring 6.3 · shank ↔ hip gearbox 8.8 (at crouch) · B ↔ end stop 11 · all others > 16 mm |
| Overall height, extended (lidar top) | **492.5 ≤ 500 PASS** (398.5 at nominal, 304.5 at crouch) |
| Overall width | **300 ≤ 300 PASS** (tyre outer faces) |
| Overall depth | nominal 299.8 PASS, extended 221.5 PASS, **crouch 321 FAIL** (coupler pin C reaches x = 196) |
| Leg stroke (hip 101 → 289) | 188 mm. ≥ 100 mm landing stroke **PASS**. With 20 cm jump clearance plus a leg tuck in flight there is 188 mm of tuck available |
| Body bottom above ground | 150 nominal, 56 at crouch |
| Lidar 360° view | Lidar optics plane ≈ z 385–395; nothing in the body above z 360 (e-stop head top). **PASS** |
| Vents | inlet 33 cm² and outlet 35 cm² gross. Need ≥ 32 gross at a 50 % open grille. **PASS** |
| End stop (rev 2.1) | Engages at hip 130 (thigh −7.7°). Hip travel 130 → 101 = 29 mm (≈ 30). Pad compression at r = 70 mm is 9.9 mm |
| Spring stroke | 62 → 104 mm = **42 mm** (target 52) |

## 5. Bambu A1 split plan (256³, keep parts ≤ 250)

| Part | Envelope | Plan |
|---|---|---|
| Body (210 × 126 × 190) | fits | Print as 5 parts for assembly access, not for size: bottom tray with battery rail, 2 side plates (hip-housing seats), top lid (lidar mast, e-stop, switch, fuse hatch), front/rear covers (grilles) |
| Shank (230.9 between pins + bosses ≈ 255) | over 250 on X/Y | Print diagonally on the bed (diagonal 362 mm), flat. If bosses grow, split at mid-length with a bolted lap joint (2 × M4) |
| Tyre Ø170, hub Ø146, hip housing Ø110 | fit | one piece each |
| Thigh 121, coupler 113, brackets | fit | one piece each |

## 6. O11 resolution — axle-keyed Al hub carrier vs free-axis encoder magnet

The **Al stator carrier becomes a hollow stationary axle**:
- The carrier is a 6061 part with a Ø30 journal for the 2 × 6806 hub bearings. Its flange bolts to the shank foot (4 × M4) and to the MN5008 stator (4 × M3 on Ø25), so it is keyed to the leg by the bolt pattern. No separate steel axle is needed.
- It has a central **Ø14 bore through its full length**:
  - the MN5008 6 mm shaft end (stator side) projects into this bore and carries the Ø6 × 2.5 diametric magnet in an Al/printed holder
  - the AS5047P breakout (Ø30 × 8 envelope) closes the bore from the shank side, in a pocket of the shank foot, on axis ±0.25 mm, with a 1.5 mm gap set by shims
- The thermal fins are an annular finned cap on the leg side around the bore. The centre stays open for the encoder.
- Load path: tyre → hub → 6806 pair → carrier journal → shank. The gears never carry radial load (Materials rule).
- Use non-magnetic M2 screws (A2 or brass) within 10 mm of the sensor. Al does not disturb the magnet.
- The cable leaves radially through a slot in the shank foot, ≥ 15 mm from the phase leads.
- The same concept is used at the hips: motor-side AS5047P breakout on the 8308 back, through the Ø12 hole of the Al plate.

## 7. Assumptions
1. Hip gearbox envelope is Ø100 × 40 mm axial (task: ≈ Ø100 × 45; Materials: 40–45 mm). The mass budget shows a Ø110 housing; at Ø110 the B pivot lug (r = 57 mm) is buried in the housing and must be carried by it (see O-P2-3).
2. Masses are the BOM/mass-budget values, lumped at the envelope centroids. Printed parts are ±15 %, so the CoM uncertainty is about ±5 mm. The real trim is done on the battery rail.
3. LD19 is 38.6 × 38.6 × 33.5, camera 25 × 24 × 11.5, HS25 resistor 51 × 28 × 15, battery 107 × 45 × 35 (SOURCES.md).
4. Theory B pivot (46, 34) and the 175° shank bend are kept unchanged. The kinematics match theory.md to < 1 mm.
5. The end stop "≥30 mm travel" is read as **hip travel** (130 → 101 mm). The pad itself compresses ≈ 10 mm.

## 8. Changes to design assumptions (to log in DECISIONS.md)
1. **All 4 drivers in the body on their own 70 × 70 Al plates. Hip drivers are no longer coaxial on the 8308.**
   - Back-to-back coaxial drivers need ≈ 2 × 100 mm of hip stack, which breaks the 300 mm width.
   - Each hip now gets a remote AS5047P breakout on the motor back (same as the wheels): +16 g.
   - The hip drivers need 2 more Al plates: +42 g.
   - **Total mass 4.370 kg (+58 g over 4.31).**
2. **Battery stands upright against the rear wall (CoM z 206), not low and central.** The knee-forward 4-bar puts the hips (+28 mm) and the leg links (≈ +90 mm) ahead of the axle. Even with the battery at the rear, the nominal CoM is +2.1 mm.
3. **The shank runs inboard of the thigh**, inside the Y span of the hip gearbox. This is needed for 300 mm width. Clearance to the gearbox is ≥ 8.8 mm at crouch.
4. **The spring gives a 42 mm stroke, not 52.** With a 40 mm crank and a straight spring, the chord limit is about 48 mm. For the same 4 J per leg, k ≈ 2.7 × (52/42)² ≈ 4.1 N/mm. Alternatively, use a 50 mm crank. Theory must re-fit the spring.
5. **The ESP32 PCB sits on its own mounts at the CoM**, not as a Pi HAT. This puts the IMU at the CoM.
6. **The B pivot lug and the end-stop bracket are carried by the stationary hip housing / side plate.** The spring anchor goes on a body bracket (75, ±79, 337). None of them is on the gearbox output.

## 9. Open questions
- O-P2-1 **Depth at full crouch is 321 mm (> 300).** Pin C reaches x = 196. Options:
  - accept it (the requirement is for nominal stance)
  - move B by up to ±10 mm (theory allows this) and re-optimise
  - limit the usable crouch to the end stop (hip 130 gives depth ≈ 318)

  Decision needed from the manager/client.
- O-P2-2 Spring re-fit (k ≈ 4.1 N/mm or a 50 mm crank). The spring ↔ B-pivot clearance is only 3.3 mm. Move the anchor when the spring is chosen.
- O-P2-3 B lug at r = 57 vs a Ø100–110 hip housing: refine B outward by about 5–10 mm, or integrate the lug into the housing. Re-check the transmission angle (35° at crouch).
- O-P2-4 IMU sits 28.8 mm below the CoM (limit 30). The keep-out from the hip plate stops it moving up. Control should confirm, or allow a CoM-offset correction in the estimator.
- O-P2-5 Battery rail trim is only 0 to +20 mm (the pack is against the rear wall). Enough for the +2.1 mm result. If printed parts come out heavy at the front, there is no rearward trim.
- O-P2-6 Electrical: confirm the hip motor-side encoder change (remote breakout, cable ≤ 15 cm inside the body) and the 4-driver layout. Thermal: confirm the driver plates on the side walls in the inlet → outlet path, and the resistors at the outlet.
- O-P2-7 Knee pin ≤ 2.0 kN (rev 2.1): the Ø24 knee boss with 2 × 608 envelope is reserved. Structural to confirm in P3.
- O-P2-8 Import the vendor STEPs in P3 and re-measure (SolidCraft sandbox path: copy them into its allowed folder first).
