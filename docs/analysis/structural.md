# Structural review: hip gearbox (rev 0, 2026-11-04)

Owner: Structural Analysis Engineer. Hand calculation only (no CAD, no FEA). Script: `calc/structural_hip_gearbox.py` -> `calc/structural_hip_gearbox_output.txt`.
Inputs: DECISIONS.md, design_targets.md rev 2 (frozen), docs/parts/hip_gearbox.md, theory.md (O13 re-run, P3 spring re-fit), materials_gears.md.

## Summary

**SF rule used:** SF = allowable at 50 °C / stress at the unfactored load, pass >= 1.5. Allowable PAHT-CF = 65 x 0.9 x 0.7 = 41 MPa; PETG = 34 x 0.75 x 0.7 = 17.9 MPa (materials A9/A10).

| # | Item | Worst case | SF | Verdict |
|---|---|---|---|---|
| 1 | **Single 6806, 10.5 mm overhang** | LC-D fault: Fr 2.13 kN, M 22 Nm | ball 0.78, seat 0.70, carrier tilt about 4.8° | **FAIL** (LC-B 1.2-1.3 also fails; LC-C 2.1-2.3 passes) |
| 1b | Carrier tilt -> planet meshes | LC-D: about 800 N radial on the ring teeth = 5.5 x the torque load | tooth SF falls below 1 | **FAIL** |
| 1c | Normal landing LC-A (Fr 0.47 kN, M 4.9 Nm) | seat tilt 1° (seat softness), mesh load 1.2 x torque load | marginal | **FAIL on tilt**, strength OK |
| 2a | Hex 26 A/F x 6 (16 Nm + radial) | 22.8 MPa | PAHT-CF 1.80, **PETG 0.78** | OK only if the thigh socket is PAHT-CF or steel-lined |
| 2b | M4 steel inserts (3 on Ø15) | clamp only; pull-out unknown | not verifiable | **Open**, test |
| 2c | Planet pins Ø5 hardened | 123 MPa at 16 Nm (154 at 20) | 8.1 (6.5 at 20 Nm) | OK |
| 2d | Housing stack bolts 5 x M3, ears | torque path | 3.8-8.8; washer bearing 1.5 | OK, washers required |
| 2e | Skirt in bending (carries the bearing moment to the plate) | LC-D, Kt 2.5 at the windows | 1.41 | **FAIL (marginal)** |
| 2f | Al plate -> body, 4 x Ø4.5 at +-44 | torque only: 80 N shear/bolt. If the plate carries the radial load: 940 N tension + 540 N shear | PAHT-CF 1.83, **PETG 0.80** | OK only if the side plate takes the radial load (see Q3) |
| 2g | Gear torque (reference) | 16 Nm fault / 20 Nm design | materials SF 2.15 at 20 Nm | OK **only if the tilt moment stays out of the teeth** |
| 2h | Lateral slide landing (not in theory's table) | roll moment 33-58 Nm, axial couple 1.0-1.7 kN | cover lip SF 1.1 | **Open / FAIL if 1.7 kN is real** |

**Answer to OQ-2.** One 6806 on a 10.5 mm overhang is not acceptable. A touching pair of 6806 is worse (outer bearing 5.3 kN = 1.8 C0, lever only 7 mm). A second bearing is needed, spaced so the thigh plane sits between the two bearings:
- Spacing >= 21 mm (2 x 10.5), 2nd bearing centre at y >= 108.5. Each bearing then sees F/2 = 1.07 kN at LC-D: static SF (C0/Fr) 2.7, no moment.
- Fallback: 2nd bearing inboard at the carrier-in (span 45.5 mm). Outer bearing 1.23 F = 2.6 kN at LC-D (C0/Fr 1.1), inner 0.5 kN reversed. Moment gone but outer bearing still marginal, and it does not fit (Ø81.5 carrier-in, sun flange Ø50 in the Ø52 bore, rotor bell, 5.5 mm to the planets).
- **Recommended:** a thigh outboard bearing (6806 or smaller, 3 x 3 kN class is enough) on a body-fixed stub at y about 108, reached by a bracket that arches over the top (outboard of y 103, clear of the thigh, coupler, spring, B pin). Mechanical Design must check the arch; the carrier then runs on bearing 1, the thigh on bearings 1 + 2.

## Assumptions

1. Loads from theory.md (O13 re-run, fixed TPU end stop): hip bearing radial = knee pin force: LC-A 345, LC-C 597, LC-B 1125, LC-D 2011 N. Spring crank force 122 N (design 180 N) added arithmetically, which is conservative.
2. Hip gearbox torque: design 20 Nm, worst fault 16 Nm (LC-B 16.1 Nm with the 10 kN/m stop). Normal LC-A/C 6-13 Nm. LC-D gives 4.9 Nm.
3. Load lever on the bearing: bearing centre y 87.5, thigh mid-plane y 98 -> 10.5 mm (hip_gearbox.md OQ-2). The moment is F x 10.5 mm.
4. **6806-2RS real ratings.** Listed values range C 4.45-4.55 kN, C0 2.9-3.44 kN (FAG 61806-2RSR 4.45/3.44; SMT 4.55/3.40; FBJ 4.49/2.9). VXB lists 5.35/3.8 for what appears to be a different variant. I used the **low end: C 4.45 kN, C0 2.9 kN**, since the brand is not fixed. Estimated ball count Z = 15, pitch dm 36 mm, from f0 and C0 (not catalogue data).
5. Ball model: contact angle 20° under load, moment carried as axial ball forces on opposite sides (lever dm), allowable ball load 5 C0/Z = 967 N. Free axial play about 0.11 mm -> free tilt 3 mrad = 0.18°. All indicative.
6. Printed seats: Winkler layer 5 mm, E_eff = 2 GPa (PAHT-CF, conditioned, 50 °C), cosine pressure around the seat and linear across the 7 mm width. This probably **under-estimates seat stiffness by 2-3x**, so the tilt numbers are upper bounds; the pressures are not affected by the stiffness choice.
7. Planet-mesh share: radial stiffness of a tooth pair 2.5 kN/mm (plastic, b 20), lever 25 mm from bearing to planet mid-plane (z 47.5 vs 22), three planets weighted 1.5. Once the 0.12 mm backlash is taken up, the meshes (about 2300 Nm/rad) stiffen the carrier far more than the seats (about 270 Nm/rad). So the meshes take about 90 % of the tilt moment.
8. Hex: 3 flats engaged at half length, apothem 13 mm, 6 mm engagement. Radial load over 26 x 6 mm projected.
9. Plate-to-body path: stack assumed cantilevered from the Al plate at y about 10 to the bearing at y 87.5 (77.5 mm), the worst case. Skirt wall 2.4 mm, 6 windows of 10 x 10 mm (20 % loss), Kt 2.5.
10. M3 preload 800 N (about 0.5 Nm in printed seats), friction 0.3, 50 % creep loss.
11. Lateral slide landing: F_y = mu x F_axle (mu 0.8, theory's own rule), ground contact 215 mm below the hip, hip-B pin lever 34 mm.

## Calculations

### 1. Bearing and carrier (LC load Fr includes the 122 N spring)

| Case | Fr N | M Nm | C0/Fr | Max ball load / allowable (SF) | Seat peak p MPa (SF vs 41) | Seat tilt | Mesh radial N |
|---|---|---|---|---|---|---|---|
| A controlled | 467 | 4.9 | 6.2 | 3.56 | 12.7 (3.2) | 1.0° | 176 (x1.2) |
| C one wheel, ctrl | 719 | 7.5 | 4.0 | 2.31 | 19.6 (2.1) | 1.6° | 271 (x1.9) |
| B fault sym | 1247 | 13.1 | 2.3 | 1.33 | 34.0 (1.2) | 2.8° | not run (x3) |
| D fault 1 wheel | 2133 | 22.4 | 1.4 | **0.78** | **58.2 (0.70)** | **4.8°** | **804 (x5.5)** |

- Fatigue (A, C): equivalent radial load with the moment 0.8 and 1.3 kN, (C/P)^3 = 162 and 45 Mrev. The hip swings about 75° and rarely, so bearing life is not the problem. **Tilt and seat pressure are.**
- "x" = worst-planet wedge normal force on the ring flanks versus the torque-only tangential load per planet at 16 Nm (141 N with K_share 1.3, K_v 1.1). The wedge factor is 1.46 (20° flank angle, two flanks).
- Effect on the meshes: the planets, being gears in a printed carrier, become a second bearing 25 mm from the first. Misalignment over the 20 mm ring face is 0.06 mm at the free tilt of 0.18° and 0.35 mm at 1°, against 0.12 mm backlash per mesh. The lateral wedge force on the teeth in LC-D is 5.5 x the torque load. The materials SF of 2.15 at 20 Nm would fall below 1 (stress is dominated by that component). The same applies to the planet bearings and pins, which see the radial force added on top of the torque force.
- Two-bearing options (LC-D, F = 2133 N): touching pair: outer 5.3 kN (1.84 C0), fails. Spaced 21 mm centred: 1.07 kN each, 0.62 x C0 equivalent, SF 2.7 (static C0/Fr), no moment. Inboard span 45.5 mm: outer 2.6 kN, C0/Fr 1.1, marginal.
- At the unfactored load, the single bearing fails only in LC-B and LC-D. The tilt in LC-A and LC-C is a gearbox-function problem (mesh misalignment), not a bearing-strength problem.
- With the ×1.5 ultimate factor on LC-D (3.2 kN), even the spaced pair is at 1.6 kN each = 0.55 C0 (fine).

### 2. Output interface and inserts
- **Hex 26 A/F x 6, 20 Nm:** torque contact 11.4 MPa, radial LC-D 13.7 MPa, sum 25.1 MPa. SF PAHT-CF 1.63 at 20 Nm (1.80 at 16 Nm). **PETG thigh: 0.71-0.78 -> fail.** The thigh socket must be PAHT-CF or have a steel/brass hex sleeve. Hex torsion shear 5.8 MPa, SF 4.1. Layers are normal to the hex axis, so the shear is in-plane (good).
- **M4 steel inserts:** they only clamp (thigh against the shoulder), they do not carry torque. M4 8.8 bolt capacity 5 kN, not limiting. The problem is the insert in PAHT-CF. Pull-out is not known (materials only gives the order of 1 kN for M3 heat-set in PLA and the rule of <150 N per heat-set insert). A tightening torque of 1.5 Nm gives about 1.9 kN of preload, above that rule. **Limit tightening to about 0.4 Nm (about 500 N) and test pull-out; SF cannot be stated yet.** Any lateral moment on the thigh also loads these inserts (see LC-L). Lateral loads must go through the shoulder face, not the inserts.
- **Planet pins Ø5 hardened, span 40 mm, loads K-factored:** at 16 Nm F_sun 85 N, F_ring 141 N, reactions 109/117 N, sigma 123 MPa, SF 8.1 against 1000 MPa. At 20 Nm: 154 MPa, SF 6.5. Cheek bearing pressure 5.8-7.3 MPa, SF 5.6-7. This neglects the extra radial force of item 1.
- **Housing stack (5 x M3 x 35, ears at r 64):** ring torque 312 N at 20 Nm. Shear 21 MPa per bolt with 3 sharing, ear bearing 5.8 MPa (SF 7.1), tear-out 2.6 MPa (SF 9.0), friction capacity 154 Nm (77 Nm after 50 % creep, SF 3.8). **Under the M3 head, bearing pressure 27 MPa with a Ø7 washer (SF 1.51); with the bare DIN 912 head (Ø5.5) it is about 55 MPa (SF 0.75): washers are mandatory.** Ear edge distance 5 mm = 1.7 d, below the 2.5 d rule, but tear-out SF is 9.
- **Skirt:** shear 0.7 MPa from torque (negligible). In bending the skirt carries the moment F x 77.5 mm: 165 Nm at LC-D -> 11.6 MPa, with Kt 2.5 at the windows 29 MPa, SF 1.41 (fail, marginal). At LC-A: SF 6.5. The two big windows near the plate should not both be on the load axis.
- **Al plate and body bolts (4 x Ø4.5 at +-44, r 62.2):** torque only, 20 Nm: 80 N shear per bolt, body-plate bearing 3.3 MPa (SF 5.3 PETG). If the plate carries the whole radial load (LC-D, 2.13 kN, moment 165 Nm): bolt shear 537 N, tension 939 N, M4 shear 43 MPa (fine), Al bearing 40 MPa (fine), but body side plate bearing 22.4 MPa (SF 1.83 PAHT-CF, 0.80 PETG); the 939 N tension also exceeds heat-set insert rules, so a through bolt with a washer plate is required. If the housing seat in the side plate carries the radial load, the plate bolts see only torque (SF > 5).
- **LC-L lateral slide landing:** F_y = 0.8 x 192 = 154 N (LC-C) or 0.8 x 337 = 270 N (LC-D). Roll moment 33-58 Nm. Resisted by the couple hip / B pin (34 mm apart): about 0.97-1.7 kN axial on the hip bearing. Cover lip (1.5 mm x Ø42): shear 4.9-8.6 MPa, SF 1.9 / 1.1 with the interlayer factor 0.4 (printed lip). Stack bolt tension 0.2-0.34 kN per bolt is fine. Roll moment on the thigh/hex joint is not computed (needs a 3D leg analysis).
- **Gear reference (materials):** ring mesh SF 2.15 and sun mesh 2.09 at 20 Nm, 50 °C (K 1.3 x 1.1 included); at 16 Nm 2.7 and 2.6. These hold only if no radial/tilt load reaches the teeth.

### 3. Load cases and pass criteria for the later review (legs, wheel hub, body)

Use theory.md O13 re-run values (4.31 kg, fixed end stop). Criteria: SF >= 1.5 on unfactored loads at 50 °C (printed, static), SF >= 2 on fatigue allowables for LC-A/C/5, metals SF >= 1.5 on yield; bearing seats p <= 41 MPa PAHT-CF / 18 MPa PETG at 50 °C.

| ID | Case | Load | Apply to | Pass criteria |
|---|---|---|---|---|
| S1 | Standing, static + spring 122 N | 21 N per wheel, spring 122 N sustained 24 h at 50 °C | body anchors, thigh crank, side plate | creep: anchor strain < 0.2 mm after 24 h; pin bearing < 10 MPa; anchor design load 180 N, SF 1.5 |
| S2 | LC-A controlled landing (fatigue) | axle 156 N, leg 93 N, knee pin 345 N, hip 11.4 Nm | legs, hub, body | fatigue allowable (0.22-0.3 x UTS), SF >= 2 for 10^5 cycles |
| S3 | LC-C one wheel first, controlled | axle 192 N, knee pin 597 N, hip 19.9 Nm (motor 17.7), wheel gear 4.3 Nm | all legs | SF >= 1.5 static, >= 2 fatigue |
| S4 | LC-B fault symmetric | axle 220 N, leg 188 N, knee pin 1125 N, hip gear 16.1 Nm | thigh, coupler, knee pin, end stop | SF >= 1.5 on yield / static allowable; end stop travel >= 30 mm, no bottoming |
| S5 | LC-D worst abuse | axle 337 N, knee pin 2011 N, hip gear 4.9 Nm | knee/C/B pins, shank, thigh, end-stop lugs (92-120 Nm stop torque per materials, with stop force about 300 N) | SF >= 1.5; no pin bending permanent; PETG bearing <= 18 MPa |
| S6 | Sliding landing add-on | F_y = 0.8 x axle (154-270 N) at the tyre, 215 mm below the hip | shank, wheel axle, hub bearing seat, B pin, thigh | include with S3/S5; roll moment 33-58 Nm; hub axle bearing seat p <= 41 MPa |
| S7 | Fall on side, 0.5 m (21 J) | to be derived: stop distance and impulse from the TPU tyre, housing corner and shank | wheel side face, hip housing, body corner | no fracture; axle 2-bearing span >= 20 mm; hip housing no contact with ground, or contact on a rib |
| S8 | Single-leg climb | 1.5 x W on one wheel = 63 N + roll moment on the side plate | side plate, body | SF >= 1.5 |
| S9 | Motor stall at the current limit | hip 20 A = 17 Nm; wheel 15 A = 7 Nm into a locked output | gear stages, hub carrier, hex | SF >= 1.5 at 50 °C |
| S10 | Jump push-off | hip 40 A = 17.3 Nm for 71-85 ms, spring 122 N | thigh, hex, spring anchors | SF >= 1.5; spring hooks fatigue life 500 jumps |
| S11 | Wheel hub (spin-up) | LC-C spin-up 4.3 Nm through the gear, fault 8.7 Nm, axle radial <= 388 N (LC-D) into the axle bearings, never the gears; magnets and bearings 20 g | hub (PETG, <= 40 °C, 50 °C check), axle, stator carrier | gear SF >= 1.5 at 9 Nm; hub rim no creep at 50 °C; axle steel yield SF >= 1.5 |
| S12 | Body | hip housing reactions (item 1), battery 6 S pack 9 g deceleration, side-plate seats | body shell, side plates | side plate seat carries the radial (Q3); bearing p <= 41 MPa; battery retention 15 g with SF 1.5 |
| S13 | Thermal | housing 50-60 °C under S2/S3/S9 | all PAHT-CF / PETG parts | allowable at actual temperature; PETG not within 5 mm of the motor can |

## Sources
- theory.md sections 3.6, O13 re-run, P3 spring re-fit (landing loads, spring and anchor loads, end stop).
- materials_gears.md (PAHT-CF allowables A9/A10, Lewis check, pin results, insert and bolt rules, LC1-LC7).
- docs/parts/hip_gearbox.md (geometry, OQ-2).
- 6806-2RS ratings (web search, retrieved 2026-11-04): https://vxb.com/products/6806-2rs-bearing-6806-2rs ; https://www.sp-spareparts.de/en/p/61806-2rsr-fag ; https://govets.com/smt-bearings-281-76334b18.html ; https://www.qualitybearingsonline.ca/6806-2rs-fbj-thin-section-bearing-30x42x7mm/ ; https://www.zoro.com/ezo-deep-groove-30mm-bore-42mm-od-sealed-6806-2rsc0srl/i/G2080051
- Standard references (not fetched, from memory): ISO 76 static capacity C0 (Qmax = 5 C0/Z), Hertz ball loads, Lewis. Ratings of the actual purchased brand must be checked against the catalogue.

## Open questions
1. **Q1 (Mech Design):** feasibility of the outboard stub and arch at y about 108 (clearance to thigh, coupler, spring, B pin, wheel), or an alternative that puts the thigh plane between two bearings. Alignment tolerance of two bearings on a rigid thigh (printed parts, +-0.2 mm): the carrier is constrained twice; one bearing may need a floating fit.
2. **Q2 (Materials):** pull-out of M4 steel (Ensat-type) inserts in PAHT-CF (coupon test); PAHT-CF compressive allowable (used 41 MPa as tensile-based); creep of the seats at 50 °C.
3. **Q3 (Mech Design / Body):** where is the housing radial load reacted? The housing sits at y 34-99, the plate at y about 10, the body wall at y 63. The side-plate seat must carry the radial load; if not, the 4 plate bolts see 940 N tension.
4. **Q4 (Theory):** the theory load table has no horizontal/lateral ground force. LC-L numbers above are my estimate. Please add sliding-landing and side-fall load cases with 3D pin forces.
5. **Q5 (Control / Electrical):** confirm that a stuck end stop or phases-floating assumptions hold; a stiff stop would put 30-77 Nm in the teeth (materials O4).
6. Bearing brand and clearance class (C3?) are not fixed. Seat stiffness model is crude; a coupon test of the tilt stiffness of a printed 6806 seat under 5 Nm is recommended.
7. Skirt wall thickness (2.4 mm) and the window positions are from the text; check against the CAD.

## Changes to design assumptions
| Was | Now |
|---|---|
| Single 6806 carries the thigh load (assumption 5 of hip_gearbox.md) | **Rejected.** Needs a second bearing with the thigh plane between the two (spacing >= 21 mm), or an equivalent. A touching 6806 pair does not work. |
| Gear SF valid at 20 Nm | Valid only if the carrier tilt moment is kept out of the meshes. With a single bearing it is not. |
| Thigh material PETG with a hex socket | Thigh socket (hex) must be PAHT-CF or steel-lined (PETG SF 0.78). |
| M3 stack bolts with plain DIN 912 head | Add Ø7 washers (SF 0.75 -> 1.51). |
| M4 inserts as thigh clamp | Limit preload torque (about 0.4 Nm) until pull-out is tested; lateral moment must go through the shoulder face. |
| Plate-to-body bolts carry the housing | Radial load to the body must go through a seat in the side plate, not through the 4 plate bolts. |
| Landing cases vertical only | Add lateral slide LC-L and a side fall (S6, S7). |


## Rev 2 re-check (2026-11-05): one gearbox 6806 at y 87.5 + the leg's outer 6806 at y 121 (assembly review A2/M1)

Script `calc/structural_hip_gearbox_rev2.py` -> `structural_hip_gearbox_rev2_output.txt`. Same ball and seat model, spring 180 N (design) at the crank y 110, thigh load at y 99, supports: the hex on the carrier (bearing 1, y 87.5) and the stub bearing at y 121 (spacing 33.5 mm). Pass SF >= 1.5.

| Hex contact on the hub | Case | R1 on brg 1 N | M1 Nm | ball SF | seat SF | tilt | R2 on brg 2 N |
|---|---|---|---|---|---|---|---|
| A ideal (support at bearing 1, no moment) | LC-D | 1380 | 0 | 1.98 | - | 0 | 811 |
| B inboard end of hub, y 94 | LC-A / C / B / D | 354 / 560 / 990 / 1712 | 2.3 / 3.6 / 6.4 / 11.1 | 5.5 / 3.5 / 1.97 / **1.14** | 6.8 / 4.3 / 2.45 / **1.42** | 0.5 / 0.8 / 1.4 / 2.4 deg | 171-479 |
| C hub centre, y 99 (rigid thigh on the whole hex) | LC-A / C / B / D | 435 / 687 / 1215 / 2101 | 5.0 / 7.9 / 14.0 / 24.2 | 3.7 / 2.3 / 1.32 / **0.76** | 3.2 / 2.0 / 1.13 / **0.65** | 1.1 / 1.7 / 3.0 / 5.1 deg | 90 |

- **Finding.** The 33.5 mm spacing does not by itself relieve bearing 1: the thigh load enters the carrier at the hex, 11.5 mm from bearing 1 (rev 0: 10.5), and the outer bearing carries only what the stiff thigh transfers by tilting. If the hex bears over the whole hub (C), bearing 1 is **worse than rev 0** (LC-D 24 Nm; mesh wedge load worse than the 5.5x of rev 0). The rev 1 pair was better because the carrier journal ran in both bearings.
- **Fix (Leg + Gearbox):** make the steel sleeve (inner 26.3 A/F) only 3-4 mm long at the inboard end of the hub pocket (y 94-98) and relieve the rest of the pocket by >= 0.5 mm. That gives B: LC-A/C/B pass (SF >= 1.97 ball, >= 2.45 seat), LC-D (fault, 2.0 kN) still **marginal fail** (ball 1.14, seat 1.42, tilt 2.4 deg = half of rev 0). A hex-free alternative (thigh carried by the stub bearing and a bearing on the carrier, i.e. a pilot of the stub into the carrier) is not possible without bringing bearing 2 back.
- **Outer bearing (leg):** 90-811 N, C0/R2 >= 3.6: fine. It sits on the leg arch plate and the posts (leg.md), whose stiffness decides how much of the load really goes there; not analysed here (Leg/Structural: post bending at 811 N plus the 180 N spring path of A6).
- **Carrier planet loads.** With B the carrier tilt is 0.5/0.8/1.4/2.4 deg (A/C/B/D) vs 1.0/1.6/2.8/4.8: the mesh wedge load halves (about 400 N on the ring teeth at LC-D vs 800 N); LC-D still above the torque load (about 2.8x). Gear SF 2.15 (at 20 Nm) holds for A/C; B/D not yet.
- **Hex.** 25.4 MPa at 20 Nm + 2.19 kN radial: SF 1.61 PAHT-CF (steel sleeve/inserts in the hub: no change). Skirt bending (stack moment F x 77.5): LC-D SF 1.37 with the old 2.4 mm wall, 2.27 with the CAD wall 3.4 mm: pass.
- **Cover lip after the M4 trim (1 mm, was 2 mm).** Axial 0.97 / 1.7 kN: SF **1.29 / 0.73** (2 mm: 2.57 / 1.47). **Fail at 1.7 kN.** Use a 2 mm lip (do not trim; move the thigh plane +1 mm per A5) or add a circlip retention of the race.
- **Cover lip restored (rev 3.1, 2026-11-05):** boss trimmed at y 93 (z 53), lip 2 mm (z 51-53). SF 2.57 / **1.47** at 0.97 / 1.7 kN: **pass (>= 1.4)**. Needs thigh plane at y >= 94. The 1 mm trim result above is superseded.
- Open: sleeve-length requirement above; insert pull-out coupon (unchanged); seat stiffness model remains crude.


## Rev 2 formal check (2026-11-05): leg arch/posts/beam, knee/C pins, shank, C pad, thigh sleeve, body ties (A1-A11)

Owner: Structural. Script `calc/structural_leg_rev2.py` -> `calc/structural_leg_rev2_output.txt` (imports the real 4-bar geometry from `cad/parts/src/build_leg.py`). Hand calc, **not FEA**; thermal skipped by client decision (A11).
**Loads:** theory.md "Re-run at CAD mass" 6.4 / 6.9 kg: knee pin LC-A/C/B/D = 0.49/0.81/1.54/2.64 and 0.53/0.82/1.68/2.81 kN; axle 210/266/324/456 N. Directions come from in-plane 4-bar statics scaled to the theory pin force (vertical-only statics gives 0.66-1.29 x theory); spring 180 N; hip radial from the rev-2 bearing model. S6 slide add-on: horizontal 0.8 x axle with wheel-reaction torque +-9.2 Nm, lateral 0.8 x axle at the tyre (85 mm below the axle). S7 (side fall) has no derived impulse: **not evaluated**. S1, S8, S9, S10 are below LC-B/C everywhere in the leg (spring anchor pin Ø5 in double shear 5 MPa; jump = hip 13 Nm + 169 N) and are not repeated.
**Allowables (50 C):** PAHT-CF 65 x 0.9 x 0.7 = 41 MPa in-plane, x 0.4 across layers = 16.4; PETG 34 x 0.75 x 0.7 = 17.9 (so **every loaded leg part must be PAHT-CF; PETG fails everywhere below**); 6061-T6 yield 240; S355 355; 42CrMo4 12.9 pin 1100; sintered bronze static 28 MPa. Pass SF >= 1.5.

### Results (SF, 6.4 kg / 6.9 kg, governing case LC-D unless stated)
| # | Item | Result | SF | Verdict |
|---|---|---|---|---|
| 1a | Arch plate: B pin Ø10 bending (FB 2.56 / 2.72 kN) | 300 / 319 MPa | 3.7 / 3.5 | PASS |
| 1b | Arch plate: B boss ligament 7 mm, bearing ring R28 (R2 811 N rev-2 ideal; 1.03 / 1.09 kN at 6.4 / 6.9), web to posts | 65, 31, 7 MPa | 3.7, 7.6 / 7.2, > 30 | PASS (811 N case: SF > 10) |
| 1c | 2 posts Ø16x3 S355, cantilever 79.5 mm, rigid-plate sharing with beam (post shear 310/410 N, M 33 Nm) | 96 / 102 MPa | 3.7 / 3.5; B direction swept +-60 deg: **1.58 / 1.49** | PASS at 6.4, **marginal 6.9 (worst direction)** |
| 1d | 6061 box beam 40x8.5x2: realistic direction (tip 1005 N x, 252 N z, M 17 Nm weak axis) / +-60 deg sweep (tip z 1.2 kN, 81 Nm) | 90 / 242 MPa (6.4) | 2.7 / 2.5; **0.99 / 0.93 sweep** | PASS realistic, **FAIL sweep** |
| 1e | Beam foot 2 x M5 into the body top rib (47x14 mm foot) | tension 1.3-1.4 kN per bolt (6.4 kN in sweep), shear 2.3-2.5 kN, bearing 116-123 MPa on a 4 mm printed rib | heat-set rule (150 N) 0.11; bearing PAHT **0.33-0.35** | **FAIL** |
| 1f | Post seats: Al plate 104x104 reaches r 73.5 max, posts are at r 82; body.md has only a D18 hole + D30 collar (y 60-65), no base at y 40 | collar load 1.45 / 1.54 kN if it is the guide | PAHT 2.3 / 2.1, PETG 0.99 | **OPEN/FAIL (no base seat)** |
| 2a | Knee pin K Ø10 (reactions 0.80/0.20, M 24 / 26 Nm) | 248 / 264 MPa (cantilever bound 309) | **4.4 / 4.2** (3.6 / 3.3 bound); at the 2.0 kN design load 5.9 | PASS: the pin is not the weak link |
| 2b | Thigh bush (sintered bronze, 10 mm long, p = 26.4 / 28.1 MPa) | | **1.06 / 1.00** (B: 1.82 / 1.67) | **FAIL** |
| 2c | Thigh knee boss R17 round Ø14 bush, ligament 10 mm, Kt 2.2 | 29 / 31 MPa | **1.41 / 1.32** (B 2.4 / 2.2) | **FAIL** |
| 2d | K pad lug (R17, 12 mm bush, 0.8 F) | 19 / 21 MPa | 2.1 / 2.0 | PASS |
| 3a | Shank arm (8 mm PAHT-CF + 3 mm Al bonded, 10x3 channel), LC-D vertical, worst section 86 mm from K: in-plane 47 Nm, **out-of-plane 21 Nm + torsion 14 Nm** (ground load plane is 42 mm outboard of the plate) | Al 173 / 185, PAHT 31 / 33 MPa | Al 1.16 / 1.09, **PAHT 0.95 / 0.89**, PETG 0.41 | **FAIL** |
| 3a2 | same, LC-B vertical | | Al 1.98 / 1.82, PAHT 1.62 / 1.49 | PASS / marginal |
| 3a3 | S6 slide on LC-C (+0.8 x, lateral 0.8) / LC-D slide -x / LC-D lateral | | PAHT **0.74** / **0.59** / **0.29** (Al 1.17 / 0.76 / 0.43) | **FAIL** |
| 3a4 | Dog-leg itself (BOW 14 mm) | peak in-plane M 71.7 Nm vs 67.3 Nm for a straight arm: **+7 %** only; the failure is the out-of-plane moment, not the bow | | |
| 3b | C pad, printed Ø21 column y 79-113.5, lever 40.5 mm (strap can only carry the force along K-C, so the pad takes the transverse part: 1.94 / 2.07 kN at D) | 87 / 92 MPa root bending; bush wall 60 / 64 MPa | in-plane **0.47 / 0.44**, across layers 0.19; B 0.81 / 0.74; C 1.41 / 1.39 (across layers 0.56); A 2.3 (0.93 across layers); wall D 0.68 | **FAIL, all landing cases** |
| 4a | Thigh sleeve 4 mm (y 94-98, load centre y 96, not 94): bearing 1 ball / seat / tilt, LC-A, C, B, D | M1 4.3 / 6.7 / 12.2 / 20.4 Nm (6.4 kg) | A 3.5 / 3.6, C 2.3 / 2.3, **B 1.25 / 1.29, D 0.75 / 0.77** (6.9: B 1.15, D 0.70); at 2.0 kN D 0.98 / 1.01 | **FAIL B, D** (the rev-2 re-check assumed contact at y 94; the 4 mm sleeve centre is 2 mm further out) |
| 4b | Hex contact (steel on carrier PAHT hex 26 A/F, torque + radial), D at 20 Nm / B / C | 40.2 / 28.5 / 18.7 MPa | **1.02 / 0.98**, **1.44 / 1.38**, 2.2 | **FAIL D, marginal B** |
| 4c | Thigh hub ligament at the hex vertex (R22 - 16.9 = 5.1 mm) under 2.4 kN | 46 MPa | **0.88** | **FAIL** |
| 4d | Hip plate -> body 4 x M4 (+-44), IF the posts are based on this plate: 57 / 61 Nm out of plane, 20 Nm torque | tension 325 / 345 N, shear 260 / 271 N per bolt, bearing 14.5 MPa on 4 mm PAHT | 2.8 / 2.7 (bearing), M4 tension 15; heat-set rule 0.45 | PASS with through-bolts + washers, FAIL with heat-set inserts |
Findings that matter: (1) the 2.6 kN knee-pin question is answered: **the Ø10 steel pin has SF 4.4; the weak links at 2.64 kN are the thigh bush (1.06), the thigh boss (1.41), the C pad (0.47) and the shank arm (0.95)**. (2) The shank is governed by the **out-of-plane moment from the tyre plane (y 115.75) being 42 mm outboard of the 3 mm plate**, which also drives the S6 lateral case. (3) The 4 mm sleeve does not keep bearing 1 out of trouble at LC-D (see 4a/4b).

### Concrete changes for every SF < 1.5 (owner + dimension)
| # | Owner | Change | Resulting SF (6.4 / 6.9) |
|---|---|---|---|
| C1 | Leg | Shank Al plate **3 -> 6 mm** (y 65-71; printed arm stays y 71-79; SPI cable face moves to y 65). Body to confirm >= 1 mm to the side-plate pad ring | LC-D vertical Al 1.96 / 1.85, PAHT 1.95 / 1.83; LC-C slide + lateral Al 1.90, PAHT 1.56 |
| C2 | Manager/Theory | **S6 sliding landing is checked at LC-C level, not LC-D.** LC-D + lateral 0.8 x axle (motors off, one wheel) stays < 1.5 even at 6 mm (0.71 / 0.61): accept as an abuse case with no fracture, or limit it by the compliant stop and a slip assumption | |
| C3 | Leg | **C pad:** replace the printed Ø21 column by an S355 (or 17-4) stand-off Ø21 x y 79-125.5 with a Ø36 x 4 flange, **4 x M5 on Ø28** through the shank plate (nuts on the inboard Al face), bush Ø14 pressed directly in (wall 3.5 mm steel). A printed column would need R15.4 (in-plane) / R20.9 (across layers) and there is no room (thigh clearance 4.2 mm) | stand-off bending 87 MPa SF 4.1; root moment 79 Nm -> M5 tension ~3.1 kN each, SF 2.6 (M4: 1.6) |
| C4 | Leg | **Thigh knee boss R17 -> R20** (ligament 10 -> 13 mm); **thigh bush -> flanged steel-backed PTFE/bronze (DU type) ID10 x 10, static >= 100 MPa** instead of sintered bronze | boss 1.83 / 1.72; bush p 26 MPa vs >= 100 -> > 3.5 |
| C5 | Leg | **Thigh sleeve:** round-OD steel insert **Ø38 x 4 mm** (hex 26.3 A/F broached inside, knurled/epoxied in the hub) instead of a 29 A/F hex sleeve, so the hub wall is steel-backed (hub R22 stays; the 5.1 mm ligament goes) | radial bearing on the PAHT hub 15.8 MPa -> SF 2.6 (was 0.88) |
| C6 | Theory/Control + Manager | Cap LC-D knee pin at **<= 2.0 kN** (compliant TPU stop, as already planned in 5c); then bearing 1 ball/seat SF 0.98 / 1.01 and the thigh bush/boss pass with C4 | |
| C7 | Gearbox | Bearing 1: **6806 -> 6906 (30x47x9, C0 about 5 kN)**, seat Ø42 -> Ø47, width 7 -> 9 (cover lip and carrier shoulder move accordingly). With C6 the ball SF is 1.68; without C6 (2.64 kN) 1.29. Alternative: move the thigh plane/sleeve so the load centre is y 94 (sleeve y 92-96): 2.0 kN ball 1.15, seat 1.42 (still < 1.5) | 1.68 (with C6) |
| C8 | Leg | Posts **Ø16x3 -> Ø18x3** (Z +35 %), post hole in the body D18 -> D20 (collar D30 -> D32) | worst direction 2.0 / 2.0 |
| C9 | Leg + Body | **Beam foot 47x14 -> 47x32 (lateral y 38-70) with 4 x M5 through-bolts** (28 x 24 pattern) into a 3 mm Al backing plate inside the top rib, steel washers; beam height **8.5 -> 12 mm** (Y 75.5-87.5; check the spring, 3.5 mm lower) | tension per bolt ~180 N, shear ~1.1 kN, slip friction 6.6 kN; beam sweep stress SF ~1.7 |
| C10 | Body | Define the post base seat: the Al plate (r 73.5 max) does not reach r 82. Add a 3 mm Al tab (or a 4 mm PAHT-CF boss) at y 40 for each post with 2 x M4 through-bolts, and make the side-plate collar D16.4 x 10 mm long (y 55-65) so it guides the post (effective cantilever 79.5 -> about 57 mm) | collar bearing 18 MPa PAHT-CF SF 2.3 (PETG 0.99: the collar must be PAHT-CF) |
| C11 | Gearbox | Use through-bolts + washers on the 4 x M4 plate-to-body (insert pull-out rule 150 N is exceeded at 325 N) | 4d: 2.8 |

Not done / needs FEA or test: shank foot ring and axle neck (Ø38.2, 4 x M4 pcd 46), the shank K-C hull, S7 side fall, wheel hub; the post/beam sharing assumes a rigid root and a flat cantilever (conservative for the posts, optimistic for the beam if the rib flexes); coupon tests for the bush and the bonded Al plate remain open. Rev 1 text above that quotes "pin SF 6-7" and the Rev 2 re-check of the hex sleeve (contact at y 94) are superseded where they disagree.
