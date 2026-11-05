# Actual mass roll-up from the CAD documents (rev 3)

Owner: BOM / Requirements Engineer · Date: 2026-11-05 · No CAD edits; masses are read from `docs/parts/*.md`, `bom/bom.md` and `electrical.md`.

Inputs:
- DECISIONS.md last rows (the client accepted weight growth)
- `docs/parts/wheel.md`, `body.md`, `leg.md`, `hip_gearbox.md`
- `docs/layout.md` §2 and `docs/analysis/calc/com_layout.py` for positions

## 1. Totals

| Case | Mass | vs BOM rev 2 (4.31 kg) | Meaning |
|---|---|---|---|
| **Solid CAD mass** | **6.86 kg** | +2.55 kg | 100 % solid volumes × density, as in the part docs |
| **Realistic sliced mass** | **6.41 kg** | +2.10 kg | Part docs' own sliced estimates (body 475 g, wheel 606 g, hip gearbox 413 g); legs at 0.68 × printed mass (850 g per leg) |
| Low case | 5.96 kg | +1.65 kg | Body 450 g, recovery options 1–5 on the hip gearbox (340 g), opened hip plate, pocketed arch plate and shank, thinner hub |

**Realistic mass range: 6.0–6.9 kg, central value ≈ 6.4 kg.**
- This is about 2.4 kg above the original 4.0 kg hard limit.
- The client has accepted weight growth (DECISIONS 2026-11-04). The limits are now soft.
- Function (20 cm jump, 12 km/h, balance) must be re-verified at this mass, because the client accepted weight growth and not loss of function.

### By subsystem (g)

| Subsystem | Solid | Sliced | Low | BOM rev 2 | Main reason |
|---|---|---|---|---|---|
| Legs (2) incl. leg cables and hip encoders | 1963 | 1777 | 1689 | ≈ 580 | Arch plate 135 g, posts 149 g, beam 34 g, Al shank plate 83 g, strap 28 g, Ø10 pins and bushings (≈ 220 g hardware) per leg |
| Hip actuators (2) | 1765 | 1723 | 1527 | 1278 | Gearbox 413–435 g vs 185 g; Al plate 80 g vs 32 g |
| Wheel modules (2) | 1304 | 1212 | 1140 | 994 | Al axle 60 g, spur ring sleeve, two-plate carrier, PETG hub 111–151 g, cover 38–45 g |
| Body printed + fasteners + Al seats | 831 | 695 | 650 | 297 + ≈ 160 | Solid 2.4 mm side plates, hip bulges, outriggers, tray floor |
| Power (battery, resistors, fuse, switch, e-stop, PDB, buck) | 470 | 470 | 445 | 465 | unchanged |
| Electronics (Pi, ESP32, fan, 4 drivers, lidar, camera) | 399 | 399 | 399 | 368 | unchanged |
| Wiring / misc | 131 | 131 | 110 | 177 | unchanged (leg cables are counted with the legs) |
| **Total** | **6863** | **6407** | **5960** | **4312** | |

## 2. Unsprung mass per side (wheel + shank)

| Part | Solid (g) | Sliced (g) | Source |
|---|---|---|---|
| Wheel module (MN5008, axle, gears, hub, cover, tyre, bearings, encoder) | 652 | 606 | wheel.md |
| Shank printed (PAHT-CF) | 156 | 106 | leg.md (sliced = 0.68 × solid) |
| Shank Al plate 3 mm | 83 | 83 | leg.md |
| Knee strap 6 mm (rigid with the shank) | 28 | 28 | leg.md |
| ½ leg cables (SPI + 3 phase wires) | 14 | 14 | electrical.md |
| **Unsprung per side** | **933** | **837** | |

- This is **1.8× the rev-2 figure (0.536 kg)** and about 2× what the jump and landing calcs used (0.465 kg).
- Theory's convention counted only half of a 50 g shank. The real shank is 267 g with its plate and strap.
- Not included: the K pin (Ø10 × 65, ≈ 40 g), the coupler and the spring share. Counting them adds about 50 g.
- **Theory and Control must re-run** jump, landing impact and balance (wheel inertia) at 0.84–0.93 kg per side.

## 3. Component table for the CoM script (`docs/analysis/calc/com_layout.py`)

Positions are world coordinates at the nominal pose (hip 195). x is fore-aft with the hip at x = 28 and the axle at x = 0. z is height with the axle at z = 85. Y is symmetric, so it does not change the CoM and is omitted.
- The positions are the layout values, updated only where `body.md` moved a part (battery z, Pi x, resistors).
- The positions of the leg sub-parts, the arch posts and the beam are **estimates** from the layout and the leg doc. **The CoM script should take real centroids from `cad/parts/*.solidcraft`.**
- Replace the old masses (layout total 4370 g) with the "sliced" column. Use "solid" for a conservative check.

| # | Component | Qty | Each solid (g) | Each sliced (g) | Total solid (g) | Total sliced (g) | Low (g) | x (mm) | z (mm) | Source / note |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Body printed (B1 sides, tray, cradle, Pi deck, lid, front, rear, mast) | 1 | 611 | 475 | 611 | 475 | 450 | -20 | 245 | body.md; sliced 450-500 |
| 2 | Body Al hip seat rings 2x22 + steel anchor dowels 2x8 | 1 | 60 | 60 | 60 | 60 | 60 | 28 | 290 | body.md (bought/cut) |
| 3 | Body fasteners, inserts, washers | 1 | 160 | 160 | 160 | 160 | 140 | -20 | 245 | layout value (BOM fasteners 209 less wheel/hip share) |
| 4 | Battery 6S 2200 mAh 50C + strap/foam | 1 | 355 | 355 | 355 | 355 | 330 | -104.5 | 216 | BOM 350 + 5; cradle is in the body print; pack raised 9.4 mm |
| 5 | Pi 4 + heatsink | 1 | 56 | 56 | 56 | 56 | 56 | -22.5 | 214 | body.md: Pi moved 20 mm forward |
| 6 | ESP32 PCB + ICM-42688-P | 1 | 25 | 25 | 25 | 25 | 25 | 25 | 190 | layout |
| 7 | PDB | 1 | 25 | 25 | 25 | 25 | 25 | 52 | 160 | layout |
| 8 | 5 V buck | 1 | 7 | 7 | 7 | 7 | 7 | 52 | 158 | layout |
| 9 | Fan 40 mm + grilles | 1 | 15 | 15 | 15 | 15 | 15 | 77 | 185 | layout |
| 10 | XDrive Mini x4 + Al plates (61 g each) | 4 | 61 | 61 | 244 | 244 | 244 | -85 | 235 | layout; 2 hip at z 275, 2 wheel at z 195 (mean 235) |
| 11 | Brake resistors x2 (+Al bracket) | 2 | 10 | 10 | 20 | 20 | 20 | -25.5 | 266.5 | body.md: moved to x -51..0, z 259-274 |
| 12 | E-stop | 1 | 30 | 30 | 30 | 30 | 30 | -100 | 335 | layout |
| 13 | Anti-spark switch | 1 | 18 | 18 | 18 | 18 | 18 | -100 | 332 | layout |
| 14 | Fuse 50 A + holder | 1 | 15 | 15 | 15 | 15 | 15 | -97.5 | 328 | layout |
| 15 | LD19 lidar | 1 | 52 | 52 | 52 | 52 | 52 | -40 | 382 | layout |
| 16 | Pi camera | 1 | 7 | 7 | 7 | 7 | 7 | 91 | 300 | layout |
| 17 | Harness / NTC / misc | 1 | 131 | 131 | 131 | 131 | 110 | -45 | 245 | layout (Electrical O9-d 110 + misc) |
| 18 | Hip stack per side: 8308 KV130 + screws 360.5 | 2 | 360.5 | 360.5 | 721 | 721 | 721 | 28 | 280 | BOM + layout |
| 19 | Hip stack per side: Al motor plate 3 mm | 2 | 79.9 | 79.9 | 160 | 160 | 110 | 28 | 280 | hip_gearbox.md (layout had 32); low = plate opened between bolts |
| 20 | Hip stack per side: printed gearbox + bearings/pins (no Al plate) | 2 | 434 | 413 | 868 | 826 | 680 | 28 | 280 | hip_gearbox.md 413-435; low = recovery options 1-5 (about 330-340) |
| 21 | Hip stack per side: motor-side encoder | 2 | 8 | 8 | 16 | 16 | 16 | 28 | 280 | layout |
| 22 | Leg per side: thigh (PAHT-CF) | 2 | 97 | 66 | 194 | 132 | 132 | 80 | 250 | leg.md; sliced = 0.68 x solid |
| 23 | Leg per side: coupler (PAHT-CF) | 2 | 39 | 27 | 78 | 54 | 54 | 119 | 280 | leg.md |
| 24 | Leg per side: shank printed (PAHT-CF) | 2 | 156 | 106 | 312 | 212 | 200 | 82 | 166 | leg.md |
| 25 | Leg per side: shank Al plate 3 mm | 2 | 83 | 83 | 166 | 166 | 140 | 82 | 166 | leg.md |
| 26 | Leg per side: Al knee strap 6 mm | 2 | 28 | 28 | 56 | 56 | 56 | 133 | 220 | leg.md |
| 27 | Leg per side: Al arch plate 7 mm (outer hip bearing seat) | 2 | 135 | 135 | 270 | 270 | 220 | 28 | 280 | leg.md; low = pocketed |
| 28 | Leg per side: steel arch posts 2 x tube | 2 | 149 | 149 | 298 | 298 | 298 | -43 | 318 | leg.md; position from r 82 at 142/162 deg, estimate |
| 29 | Leg per side: Al outrigger beam | 2 | 34 | 34 | 68 | 68 | 68 | 66 | 336 | leg.md |
| 30 | Leg per side: pins, bushings, spring, outer 6806, TPU stop (hardware) | 2 | 224 | 224 | 448 | 448 | 448 | 100 | 260 | leg.md ~220 + TPU 4; spring 35 at (34,318) |
| 31 | Leg side: hip leg-side encoder + leg cable | 2 | 36.5 | 36.5 | 73 | 73 | 73 | 50 | 200 | layout 8 + 28.5 |
| 32 | Wheel module per side (motor, gear, hub, cover, tyre, axle, bearings, encoder) | 2 | 652 | 606 | 1304 | 1212 | 1140 | 0 | 85 | wheel.md; hub/cover estimates until a slicer run |
| | **TOTAL** | | | | **6863** | **6407** | **5960** | | | |

Items removed from the layout's old table, because the CAD parts now carry them:

| Old layout item | Old mass (g) | Replaced by |
|---|---|---|
| Body shell + body fasteners | 282 + 160 | rows 1–3 |
| Thigh / shank / coupler per side | 33 / 63 / 31 | rows 22–29 |
| Knee / C / B / hip joint hardware per side | 40 / 25 / 16 / 16 | row 30 |
| Spring per side | 35 | row 30 |
| TPU end stop + bracket per side | 13 | row 30 (TPU 4 g) and the body print (seat arm) |
| Gearbox per side | 253 | row 20 |
| Al plate per side | 32 | row 19 |
| Wheel module per side | 497 | row 32 |
| Total | 4370 | **6407 (sliced)** |

### Rough CoM with these masses (nominal pose, x–z only; approximate)

| Case | Mass | CoM x vs axle | CoM height above axle |
|---|---|---|---|
| Solid | 6.86 kg | **+12.4 mm** | 138.9 mm |
| Sliced | 6.41 kg | **+11.0 mm** | 140.5 mm |
| Layout rev 0 (for comparison) | 4.37 kg | +2.1 mm | 130.8 mm |

- **The CoM moves forward by 9–10 mm.** That exceeds the ±5 mm target.
- The heavy new parts are all ahead of the axle: the hip gearboxes and Al plates, the arch plates and the front beams.
- The battery rail only trims 0 to +20 mm of pack travel (about 1.7 mm of CoM per 20 mm), so it cannot recover this.
- The controller can absorb it with body pitch, or ballast can go at the rear. The CoM script must be re-run with real centroids to confirm.

## 4. Assumptions
- **Solid** values are the part docs' volume × density figures (PAHT-CF 1.2, PETG 1.27, Al 2.70, steel as quoted).
- **Sliced** values:
  - body: mid of 450–500 g
  - wheel: 606 g (wheel.md)
  - hip gearbox: 413 g (housing at ~80 % fill, hip_gearbox.md)
  - leg printed PAHT-CF parts: 0.68 × solid. This reproduces the leg doc's "≈ 850 g with real infill".
  - Al and steel parts are unchanged.
- **Hip gearbox:** the second output bearing (outboard 6806, 19 g) and the arch are counted in the leg (arch plate 135 g, posts 149 g, bearing in the hardware). The recovery options (330 g per side) are not applied in the solid or sliced case; they appear in the low case.
- **Purchased parts** (motors, battery, drivers, Pi, ESP32, lidar, fan, resistors, wiring) use the BOM rev 2 / electrical.md values. Nothing was weighed.
- **Fasteners:** body 160 g (layout) plus the hip fasteners (24.5 g per side) and wheel fasteners (inside the 606 g). Possible overlap with the BOM's 209 g: about ±40 g.
- **Not yet in any CAD doc:** hip-gearbox ear relief, arch bracket envelope, box beam for the 2 kN B-pin path, wheel-to-housing clearance fixes, cable clips, grease. These add roughly 50–150 g.

## 5. Open questions
1. **Function at the real mass** (Theory/Control): jump, 12 km/h speed headroom, balance with 0.84–0.93 kg per wheel side. Hip torque and spring (5.5 J) may no longer give 20 cm at ≈ 6.4 kg.
2. **CoM** moves about +11 mm forward (above). Re-run `com_layout.py` with real centroids; decide on ballast or rail trim.
3. Hip gearbox rework: options 1–5 are approved but not applied (−75 to −95 g per side). Re-measure after the rework.
4. Weigh the first prints: wheel hub (111 g est.) and cover (38 g est.), body parts and the leg parts.
5. Thermal: the heavier legs, plates and hip plate raise the Al heat paths. Thermal's allowable currents are unaffected, but the thermal doc still uses the old masses.

## 6. Sources
- `docs/parts/wheel.md`, `body.md`, `leg.md`, `hip_gearbox.md`, `layout.md`, `DECISIONS.md` (rows 2026-11-04 / 2026-11-05)
- `bom/bom.md` rev 2, `docs/analysis/electrical.md` O9-d, `docs/analysis/calc/com_layout.py`
- Motor and pack masses: see `bom/bom.md` §6.

## 7. Changes to design assumptions
- The robot mass is **6.4 kg realistic (6.0–6.9 kg)**, not 4.31 kg. The 3.6 kg target and the 4.0 kg limit are given up by client decision.
- Unsprung mass per side is **0.84–0.93 kg**, not 0.536 kg.
- CoM at nominal is about +11 mm ahead of the axle, not +2 mm.
- The BOM rev-2 masses for the printed parts, hip gearbox, wheel module and legs are replaced by the CAD values.
