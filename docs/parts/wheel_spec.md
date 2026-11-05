# Wheel assembly (x2) — build spec, rev 0 (spec only, no CAD yet)

Owner: Wheel Design Engineer (under Mechanical Design) · Date: 2026-11-04
Inputs: DECISIONS.md, design_targets.md rev 2 (frozen), layout.md §1/§6, materials_gears.md (O9 wheel gear, §5/§7), thermal.md, electrical.md, theory.md §3.6, mass_budget.md, cad/vendor/SOURCES.md, hip_gearbox.md (house style).
Status: numbers below are hand-derived (gear numbers re-checked in Python). Nothing was drawn. SolidCraft was **not** used.
Planned outputs (for the CAD session): `cad/parts/src/build_wheel.py`, `cad/parts/wheel.solidcraft`, `exports/step/wheel.step`, `exports/stl/wheel/WH_*.stl`, `docs/analysis/calc/wheel_gear_geometry.py`.

## 0. Concept in one paragraph
The MN5008 stator is bolted to the end of a hollow Al carrier (fixed axle, Ø14 bore). The ring gear is fixed to the same axle through a PAHT-CF sleeve. The motor rotor drives the sun; the planet carrier is the output and bolts to the hub cover. The hub (PETG) turns on 2 x 6806 on the carrier journal and carries every radial load. The gears carry torque only. Ratio = 1 + 60/24 = **3.500** (ring fixed, carrier out).

**Frame.** Local axis **u** (outboard +), u = 0 at the carrier journal shoulder. World (left wheel): Y = 80 + u (layout Y 80 = outboard face of the shank foot), X = 0, Z = 85 (axle height above ground). Right wheel = mirror about the XZ plane; every part is symmetric, so the same STL is used (the tyre and the hub are rotationally symmetric, only the tab handedness-free design applies).

## 1. Parameters (names for the CAD script)

### 1.1 Gear (checked)
| Name | Value | Note |
|---|---|---|
| m | 1.25 | module |
| zs / zp / zr | 24 / 18 / 60 | i = 1 + zr/zs = 3.500 |
| pa, psi | 20°, 20° herringbone | each half 6 mm, same hand rules as hip (ring turned by tanψ·6/(π·75/…); compute in `wheel_gear_geometry.py`) |
| d_sun / d_pl / d_ring | 30 / 22.5 / 75 | pitch Ø |
| a_c | 26.25 | centre distance = m(zs+zp)/2 = m(zr−zp)/2, no profile shift |
| N_pl | 3 | at 120° |
| Assembly | (zs+zr)/N = 28 integer, zs/N = 8 and zr/N = 20 integer | **OK, all planets identical, same phase, 120° apart** |
| Neighbour clearance | planet tip Ø25.0 vs planet spacing 45.47 | 20.5 mm gap, OK |
| sun_root / sun_tip | 26.88 / 32.5 | |
| pl_root / pl_tip | 19.38 / 25.0 | |
| ring_tip (inner, addendum) / ring_root | 72.5 / 78.4 | |
| ring_OD | 86 | wall 3.8 at root. Matches layout hub_d |
| gear_b | 12 | face width (SF 3.3 @4.5 Nm, 1.76 @8.5 Nm, PAHT-CF, 50 °C) |
| bl_flank | 0.06 per flank | each tooth thinned 0.06, ring spaces +0.06 (as hip). Expect lost motion ≈ 0.3° (target ≤ 1°); `wheel_gear_geometry.py` must report it |
| tooth_pts | 10 per flank + 2-point root | polylines, same method as hip |

### 1.2 Bought parts / fits
| Name | Value | Note |
|---|---|---|
| mot_D / mot_L / mot_body | 55.6 / 32 / 27 | 27 mm body + 5 mm shaft out of the **base** (stator) side. SOURCES.md drawing |
| mot_shaft_D | 6 (inner shaft), 5 mm projects on the stator side | the Ø4 stub on the rotor top is under the sun collar |
| mot_stator_pcd, n | Ø25, 4 x M3 | tapped in the motor base |
| mot_rotor_pcd, n | Ø18 (4 x M3 used) and Ø12 (spare) | **verify depth/pattern on arrival (O14)** |
| mot_cap | Ø20 x 2.4 raised on the rotor top | sun collar needs a Ø21 x 2.6 recess |
| brg_hub | 2 x 6806-2Z, 30 x 42 x 7 | cc = 7 (touching pair, see §3) |
| brg_pl | 6 x 685ZZ, 5 x 11 x 5 | 2 per planet |
| pin | 3 x Ø5 x 20 hardened dowel (ISO 8734), h6 | |
| mag | Ø6 x 2.5 diametric NdFeB | |
| enc_board | Ø30 x 8 envelope (AS5047P breakout) | |
| fasteners | see §6 | A2 non-magnetic within 10 mm of the sensor |

### 1.3 Axial stack (u, mm). Total 71 → wheel outboard face Y = 151 (layout 150; O-W1)
| Feature | u range |
|---|---|
| Shank foot (layout) | −12 … 0 |
| Carrier flange (Al, outside the shank face, see §4) | −16 … −12 |
| Carrier neck Ø34 through the shank foot | −12 … 0 |
| Journal shoulder face | 0.5 |
| Hub inboard face (labyrinth, gap 0.5 to shank) | 0.5 |
| B1 6806 | 0.5 … 7.5 |
| B2 6806 | 7.5 … 14.5 |
| Journal end (Ø30), sleeve flange (3) sandwiched | 14.5 … 17.5 |
| Motor base | 17.5 |
| Motor rotor top face | 44.5 |
| Sun collar + carrier plate A | 44.5 … 49.5 (plate A 45.0 … 49.5) |
| Sun teeth / planets / ring teeth | 49.5/50.0 … 62.0 / 62.5 |
| Carrier plate B | 62.5 … 67.0 |
| Hub cover (centre disc), recessed Ø30 boss for plate B | 66.5 … 70.5 (Y 146.5-150.5), screws Ø6 head recess |
| Tyre | u 46 … 71 (Y 126-151 → 125-150 nominal; set tyre_u0 so the outboard tyre face = hub cover face + 0.5) |

## 2. Gear stage parts (PAHT-CF, dried 80 °C/8 h, hardened 0.4 nozzle, axis = Z, flat on bed)
| Part | Spec |
|---|---|
| WH_Sun | 24T b12, collar Ø26 x 5 (u 44.5–49.5) with Ø21 x 2.6 recess for the motor cap, bore Ø6.2 (shaft stub Ø4 clears), 4 x Ø3.4 through on Ø18 PCD, counterbore Ø5.8 x 2.5 from the gear side; M3 x 8 A2 into the rotor (check thread ≥ 6 mm). No set screw. |
| WH_Planet x3 | 18T b12, centre pocket 2 x Ø11 (+0.1) x 5.1 deep from each face, 2 mm web between (bearing wall 4.2 mm to root Ø19.38) |
| WH_Carrier | plate A Ø58 x 4.5 (centre hole Ø28 round the sun collar, 1 mm running gap) + 3 integral posts Ø12 x 13 at r26.25, **at 60°+120k** between planets + plate B Ø58 x 4.5 printed separate or split; blind Ø5 pin holes 3.5 deep in both plates; plate B has 4 x M3 clearance on Ø40 PCD to the hub cover. Plate gap 13 = planet 12 + 2 x 0.5. Pin 20 = 3.5 + 13 + 3.5 |
| WH_RingSleeve | one part: flange Ø60 x 3 (u 14.5–17.5, 4 x Ø3.4 on Ø25 to line up with the motor screws, plus Ø34 pilot ring), tube OD 63 / ID 59 (motor 55.6 + 3.4) to u 49.5, ring zone OD 86 u 49.5–62.5 (teeth 12 + 0.5), herringbone teeth inside. Printed flange-down. 3 x M3 radial anti-rotation not needed (clamped by the 4 motor screws) |
Tolerances for PAHT-CF on the A1: pin holes Ø5.05 (press, tap with a mallet), 685 pockets Ø11.10, shaft bore Ø6.20, free running gaps 0.5 axial, 0.4 radial. Gear tip/root polylines as for the hip gears. Print a coupon first (O15).

## 3. Bearings and load path
| Item | Value |
|---|---|
| Choice | 2 x 6806-2Z (61806, 30 x 42 x 7, C ≈ 4.4 kN, C0 ≈ 2.9 kN, verify in the SKF table) |
| Layout | touching pair (DB), cc 7 mm, 0.1 mm preload shim (outer race against a hub shoulder) |
| Why not 6808 | needs a Ø40 journal; bore Ø14 would leave a 13 mm wall, hip uses 6808 already; mass +10 g each |
| Tyre load plane | u ≈ 58 (centre of the tyre). B1 centre u 4, B2 centre u 11, lever 54 mm |
| Reaction (F = axle load) | R_B2 = F·54/7 = 7.7 F, R_B1 = F·47/7 = 6.7 F, in opposite directions |
| LC-A 171 N (normal landing) | R_B2 1.32 kN, R_B1 1.15 kN. L10 ≈ (4.4/1.32)³ = 37 M rev ≈ 20,000 km |
| LC-C 191 N | 1.47 / 1.28 kN |
| LC-D 293 N (motors off abuse) | **2.26 / 1.97 kN, static SF ≈ 1.3 on C0 = 2.9 kN** (one shot, acceptable, not for fatigue) |
| Side fall LC3 | not quantified. The hub tilt in a touching pair is poor. **O-W2** |
| Better option (needs layout) | move the tyre inboard by ≈ 18 mm (centre u ≈ 40): R_B2 5.1 F, or space the bearings to cc 15 (costs +8 mm of stack). Decision needed |
| Fits | hub bore Ø42.10 (PETG, printed, then ream/sand; or press in with Loctite 641), journal Ø30 k5 (machined/bought Al), hub shoulder 1 mm, retained by a PETG cover lip |
| Gear protection | gears and motor bearings see torque only (Materials rule). 0.5 mm labyrinth at the hub inboard face, hub cover has a 0.4 mm overlap lip (grit) |

## 4. Carrier = hollow fixed axle (6061-T6, CNC or turned, not printed)
| Name | Value |
|---|---|
| car_bore_D | 14 through, Ø31.2 counterbore from u −16 to 5 for the encoder board (Ø30 x 8 envelope) |
| car_journal_D | 30 k5, u 0.5 … 14.5 (shoulder Ø40 at u 0.5) |
| car_neck_D | 34, through the Ø34.2 hole in the shank foot (12 thick) |
| car_flange | Ø56 x 4 inboard of the shank foot (u −16 … −12), 4 x M4 on Ø46 PCD, clamps the shank foot. The tapped holes are in the shank foot (M4 steel inserts, same as hip) |
| car_fins | annular fin ring Ø62 / Ø34 on the flange's inboard face (u −24 … −16), 12 radial fins 1.2 thick x 14 radial x 8 high |
| car_motor_holes | 4 x Ø3.4 on Ø25 (r12.5 sits in the 8 mm wall, r 7 … 15), counterbore Ø5.8 x 2.2 from the Ø31.2 step at u 5 (M3 x 14 DIN 7984 A2, screw into the motor base through the sleeve flange) |
| Encoder | magnet holder Ø12.6 OD / Ø5.95 ID on the shaft end (Loctite 648), pocket Ø6.1 x 2.5; magnet face at u 6.5; board chip face at u 5.0 → **gap 1.5** (shim stack 0.1/0.2/0.5 under the board, A2 M2 x 4 screws); on axis ±0.25 |
| Cable | radial slot 4 x 8 mm at u −14 through the flange side, then along the shank, ≥ 15 mm from the phase wires; phase wires leave through a second Ø8 radial hole 90° away at u −14 |
| Mass | ≈ 65 g (fins and pocketed flange); thermal budget was 30 g → **O-W3** |

## 5. Hub (PETG, 4 walls, 30 % gyroid; ASA preferred if a draft shield is available)
Two printed parts: **WH_Hub** (inboard bell) and **WH_Cover** (outer centre disc).

| Name | Value |
|---|---|
| hub_boss | OD 52 / ID 42.10 x 14 (u 0.5 … 14.5), bearing seat, shoulder 1 at u 14.5 |
| hub_web | Ø52 → Ø76 x 3 at u 0.5 … 3.5 |
| hub_drum | OD 74.8 / ID 70 (2.4 wall) u 3.5 … 44, clears the sleeve (OD 63) by 3.5 radial and the sleeve flange Ø60 |
| hub_flare | 12 radial spokes 2.4 thick x 12 axial, Ø74.8 → Ø132, at u 40 … 52, and an annular rib Ø132 |
| hub_cavity | gear zone ID 90 from u 46 to 66 (ring OD 86, 2 mm gap) |
| hub_rim_ring | OD 138 / ID 132 x 25 (u 46 … 71) |
| hub_tabs | **12 castellated tabs**, 4 mm radial (Ø138 → Ø146), tangential 18 mm, gaps 8.6 mm, full 25 axial. Print Ø146 +0.0 / −0.2 |
| hub_lip_in | inboard flange Ø150 x 2 at u 44 … 46 (tyre stop) |
| hub_cover | centre disc Ø146 x 2.5 + 4 thick ring Ø120–146; **hole pattern**: 5 x 4... 12 x Ø16 holes on Ø100 PCD (lightening, also the client's "disc with a hole pattern"), Ø30 boss for the carrier plate B (4 x M3 on Ø40), 8 x M3 inserts on Ø124 PCD into the rim ring, lip overlapping the tyre face by 3 |
| Cover bolts | 8 x M3 x 10 into heat-set inserts (Ø4 x 5.7) in the rim ring ribs |
| Thermal | motor-side boss reaches 60 °C+: PETG minimum. Never PLA |
| Mass | hub body ≈ 80 g, cover ≈ 30 g (estimates ±15 %) |

## 6. Tyre (TPU 95A, Bambu TPU 95A HF, 3 walls, one piece per side)
| Name | Value |
|---|---|
| tyre_OD / tyre_ID / tyre_w | 170 / 146 / 25 |
| tyre_slots | 12 inner ribs (slot clearance for hub tabs): rib 8.0 tangential x 4 radial (Ø146 → Ø138) x 25 axial, fits the gaps between tabs. **Interference**: rib 8.0 vs gap 8.6 → 0.3 each side loose; TPU stretches over the tabs; tab tip OD vs tyre ID: tyre ID 145.6 (0.4 interference, "plug and play, no glue") |
| tyre_retain | inboard bead: lip Ø142 x 2 hooks behind hub_lip_in; outboard retained by the cover lip |
| tread_wall / inner_wall | 2.4 / 2.0 |
| cell zone | R 75 … 82.6 radial height 7.6, N = 30 axial through-cells, each 14.9 tangential (rounded slot R3), web 1.6 |
| tread | 24 chevron grooves 1 deep x 2 wide, 45°, across the width; two 1 mm side chamfers |
| Mass (calc) | solid ring 180 g; cells remove 57 % of the annulus → ≈ 77 g + ribs 12 g = **≈ 90 g (≤ 110 ✓)** |
| Print | axis = Z (stand on one face), 0.2 layer, 3 walls, 0 % infill, slow outer wall, cells need no support, 0.15 mm seam on the inboard face. Ø170 x 25 fits A1 (256) easily |
| Check | radial stiffness target 12 kN/m (theory A11) → print one, measure (O16); thicken webs to 2.0 if softer |

## 7. Hub-to-leg interface (shank foot)
| Item | Value |
|---|---|
| Datum | shank foot outboard face, Y = 80. Shank 12 thick (Y 68–80) |
| Foot hole | Ø34.2 for the neck; 4 x M4 steel insert holes on Ø46 PCD from the inboard side (flange sits against Y 64–68) |
| Encoder pocket | in the carrier (not the shank) counterbore, Ø31.2; layout's Y 70-78 pocket is **replaced** (the board is deeper at u 5, Y 85) |
| Fin ring | outside the shank: Y 56–64, clear of the body wall (body bottom z 150 vs axle z 85) |
| Load | shank → 4 x M4 flange clamp (steel washers) → neck → journal. Lateral moment from side fall: flange Ø56, M4 x 20, A2 70, torque 2.5 Nm |
| Phase/cable | per §4 |

## 8. Bought parts and masses
| Part | Qty | g each | g |
|---|---|---|---|
| MN5008 KV170 | 1 | 128 | 128 |
| 6806-2Z | 2 | 19 | 38 |
| 685ZZ | 6 | 1.3 | 8 |
| Dowel Ø5 x 20 | 3 | 3.1 | 9 |
| M3 x 8 / x 10 / x 14 A2 + inserts + M4 flange screws | ~30 | | 15 |
| Encoder PCB + magnet + holder | 1 | | 8 |
| M3 inserts Ø4 x 5.7 (8) + M4 inserts (4, in shank) | | | 4 |

## 9. Mass per wheel vs 0.536 kg unsprung target
| Item | g (est) | mass_budget g |
|---|---|---|
| Bought (above) | 210 | 128+38+... |
| WH_Sun / 3 planets / carrier | 11 / 12 / 24 | gear core 72 |
| WH_RingSleeve (PAHT-CF) | 41 | sleeve 16 |
| Carrier + fins (6061) | 65 | 30 |
| WH_Hub + WH_Cover (PETG) | 80 + 30 | 87 |
| Tyre | 90 | 110 |
| ½ shank, ½ cables (not in this spec) | 39 | 39 |
| **Total** | **≈ 600** | **536** |

**≈ +65 g/side over the 0.536 kg** (≈ +130 g robot, ±15 %). Recovery in order: (1) merge the sleeve and the carrier flange, thin the ring zone (−15 g); (2) 2 mm Al carrier flange with window cut-outs, fins only 6 high (−15 g); (3) hub spokes/drum 3 walls, gyroid 20 % (−15 g); (4) cover 2 mm (−8 g); (5) tyre N = 32 cells, 2.0 mm tread (−8 g). Total ≈ −60 g, back to ≈ 540 g.

## 10. Print plan (A1, 256^3, hardened nozzle, dryer)
| Part | Material | Orientation | Notes |
|---|---|---|---|
| WH_Sun, Planet x3, Carrier A/B | PAHT-CF 100 % | gear axis Z, tooth face on bed | no supports; carrier posts printed with plate A |
| WH_RingSleeve | PAHT-CF 5 walls | flange down | ring teeth at top, outside OD 86, 49 tall |
| WH_Hub | PETG | rim ring up (cover side up), boss down | needs tree supports under the flare spokes only. Ø150 x 71 fits |
| WH_Cover | PETG | flat | |
| WH_Tyre | TPU 95A | one face down | 250 g max/spool |
No part needs splitting (largest Ø170).

## 11. SolidCraft build script plan (do not run; `cad/parts/src/build_wheel.py`, JSON like `build_hip_gearbox.py`)
1. Import `wheel_gear_geometry.py` (new): involute polylines for sun/planet/ring, ring turned by herringbone; assert assembly, no interference through one tooth pitch, report lost motion.
2. Parameters (§1) via `parameters.change`; local frame Z = axle, outboard +.
3. Bought blocks: MN5008 cylinder Ø55.6 x 27 + shaft Ø6 x 5 (base side) + Ø20 x 2.4 cap + hole patterns, 6806 x2 (revolve Ø30/Ø42 x 7), 685ZZ x6, pins x3, board Ø30 x 8, magnet Ø6 x 2.5. SOURCES.md says no STEP exists, so use blocks.
4. Carrier (Al): revolve profile (journal, neck, flange), bore Ø14, counterbore Ø31.2, 4 holes on Ø25 + counterbores, 4 M4 holes on Ø46, fins (12 extrudes + circular pattern), cable slots.
5. WH_RingSleeve: tube, flange, ring OD; ring teeth by a polyline extrude cut, herringbone as two 6 mm halves.
6. WH_Sun, WH_Planet (one + circular pattern x3 at 120°), WH_Carrier (plate A + posts + plate B, pin holes, M3 holes).
7. WH_Hub: revolve base profile (boss/web/drum), spokes by pattern, rim ring + 12 tabs by pattern, inserts holes, cover holes.
8. WH_Cover: disc, 12 holes pattern, boss, lip.
9. WH_Tyre: ring, 30 cells pattern, 12 ribs pattern, tread grooves, bead lip.
10. Assemble (positions from §1.3), mirror not needed. Interference check: gear mesh, sleeve vs rotor (0.5), hub drum vs sleeve (3.5), tab vs rib, encoder gap = 1.5.
11. `measure` mass of each printed part; fill §9 with the real values, update this spec.
12. Export STEP + STL; screenshots iso/exploded/section XZ/gear cut at u 56.

## 12. Open questions
- O-W1 Stack is 71 mm, outboard wheel face Y 151 (layout 150). Do we trim 1 mm or accept 301 mm total width?
- O-W2 Touching-pair 6806 gives an overhung moment; tilt, side-fall (LC3) and bearing-seat stiffness unverified. Move the tyre inboard (layout change) or increase cc?
- O-W3 Thermal asked for ≥ 200 cm² of fin area; this carrier has ≈ 60 cm². Thermal to re-check allowable continuous current (the 7 A figure may drop to ≈ 5 A).
- O-W4 MN5008 rotor thread depth and the real bolt patterns (O14). Rotor Ø18 pattern is used for the sun.
- O-W5 Carrier machined from 6061: who makes it? (Printing is not an option; "everything 3D printed" needs the client's OK for Al parts, already accepted in the BOM.)
- O-W6 Mass +65 g/side over target. Cuts in §9.
- O-W7 Tyre inner interference and rib clearance need a print test; TPU shrinkage.
- O-W8 Right/left sides identical, but the rotation direction of the phasing mark is irrelevant (symmetric gears).
- O-W9 Encoder cable run next to the phase leads (≥ 15 mm) in a shank foot of 12 mm: needs the shank design to confirm.
