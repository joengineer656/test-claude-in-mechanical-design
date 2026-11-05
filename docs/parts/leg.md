# Leg CAD (ONE leg, left; right = mirror about world XZ) — rev 2 (CoM refit; see the REV 2 block below, sections 1-7 are rev 1 history where they disagree)

## REV 2b (A13 / structural C1-C9, 2026-11-05) — authoritative over everything below
Generator `cad/parts/src/build_leg.py` (new parts `cstand`, `bplate`); STL/STEP re-exported (world coords, left leg; right = mirror about XZ). **All loaded leg parts are PAHT-CF (printed) or metal as listed; PETG is not allowed anywhere in the leg.**
| Change | Done |
|---|---|
| C1 shank Al plate | **6 mm, y 65-71** (was 3 mm, 68-71). Printed arm still y 71-79, wheel hub 80.5: the wheel side is untouched. Inboard face (SPI cable) now y 65: **Body must keep >= 1 mm to the pad ring** |
| C3 C pad | printed column deleted. **Leg_CStandoff S355 O21, y 79-125.5, O36 x 4 flange (y 79-83), 4 x M5 on O28** through printed shank + Al plate (nuts on the inboard Al face), O14 bush pressed in (y 113.5-125.5). Shank C boss R16 -> R19 (flange bolt edge distance); O21 hole + O36 recess cut through the K pad |
| C4 thigh boss | **R20** (was 17); bush **DU-type (steel-backed PTFE/bronze) ID10 x OD12 x 10 long**, thigh bore O12 (was O14 sintered bronze). Thigh-to-C-stand-off in-plane clearance (check) 11.6 / 11.6 / 11.6 / 10.6 / **0.5 mm** at h140/160/195/240/289 (0.3 at h289 before this change: the tight spot is the thigh flank, not the boss; ensure the real part is built to size at h289) |
| C5 sleeve | **O38 x 4 round-OD steel insert, y 94-98** (hex 26.3 A/F broached inside, knurl + epoxy); thigh pocket O38 to y 98, O32 relief to y 100; hub R22 unchanged (3 mm PAHT ring) |
| C8 posts | **O18 x 3 S355** (was O16), same r 82 / 142, 162 deg / y 40-119.5; arch plate holes O18, ring R12 round the post holes |
| C9 beam | foot **47 x 32 (lateral y 38-70)**, **4 x M5 through-bolts at world x 94.5 / 122.5, y 42 / 66 (28 x 24)**, 3 mm Al **backing plate** `Leg_BeamBackplate` 41 x 28 at world z 350-353 (below the Body shelf z 353-359). Beam **12 high (Y 75.5-87.5 = z 355.5-367.5, top unchanged)** from lateral y 70 to 119.5, 2 mm walls; on the foot (y 52-70) a solid 8.5 high root stub (Y 79-87.5) because the Body shelf occupies z 353-359 there. A 28 x 16 relief is cut in the bottom wall under the spring band (envelope top Y 77.4). Structural: re-check the beam root (12 mm section starts at y 70, not 52) |
| C6/C7/C10/C11 | not Leg |
Mass (solid CAD, from STL volumes, g/leg): thigh 99, coupler 39, shank 122 (printed 260) · plate 170, strap 28, arch 147, beam 55, backplate 9 (Al 409) · posts 176, stand-off 130 (steel 306) · TPU 3 · hardware ~ 280 (was 220: + sleeve, 8 x M5 + washers, DU bush). **~1.26 kg/leg solid (was 0.95): +0.31 kg/leg, +0.62 kg robot.** Biggest: plate +87, stand-off 130, posts +27. (Weight saver not taken: bore the stand-off hollow / thin the plate outside the arm.)
Not done: pockets, M5 nut pockets, FEA of shank + arch plate (owed, A13).

## REV 2 (2026-11-05) — authoritative where it differs from the rev 1 text below
Numbers for other owners: `docs/parts/leg_interfaces_rev2.md`. Jump/CoM scripts: `docs/analysis/calc/leg_refit_jump.py`, `com_rev2.py` (+ `_output.txt`).
- **Refit (A4/M9):** B pin (46,30) -> **(39,31)**, anchor (94.1,71.2) -> **(97.4,70.9)** (spring span 154.5 mm at h140 / 111.0 at h289, stroke 44 mm). Hip is **10.6 mm ahead of the axle at h195** (was 37.1); axle world x 17.4. **Nominal thigh angle -24.26 deg** (was -33.19), -0.29 at h140, -77.09 at h289 (swing 76.8 deg, was 67). Reach 116..303; floor 140 kept (A3), stop pad re-seated for 140 (M17).
- **Jump:** the larger thigh swing lowers the hip mechanical advantage: with the old spring (2.7 N/mm, F0 8 N) the jump is 18.9 cm at 6.4 kg / 19.8 V (21.4 at 22.2 V) vs 21.2 for rev 1. **Spring changed to 3.5 N/mm, F0 15 N (Fmax 169 N < 180 N design, E 4.0 J/leg = 8.1 J both): 20.5 / 20.2 / 19.7 cm at 6.0 / 6.4 / 6.9 kg, 19.8 V real (x0.8); 23.1 / 22.7 / 22.2 at 22.2 V.** Hip peak 13 Nm (6:1). Hold at nominal: spring exceeds gravity by 0.95 Nm/leg (motor holds against it). New spring: 2.0-2.2 mm music wire, D 11, OD <= 13.5, free ~110 mm; wire shear ~740 MPa at 169 N (allow ~900) - Materials to confirm. 6.9 kg is marginal (19.7 cm).
- **CoM:** whole robot **+2.0 mm (solid 6979 g) / +0.9 mm (sliced 6350 g)** ahead of the axle (was +22.2 / +21.1). Leg 949 g/side. Wheels move +26.5 mm forward with the axle; hip, body and gearboxes unchanged.
- **Y stack (M4, M10, M11, M12):** shank 71-79 (hub 80.5), K pad 93.5, thigh 94-104, crank 105-117 / spring band 104.5-117.5 (axis 111), arch plate + outer 6806 119.5-126.5 (2 mm above the spring), coupler 127.5-141.5, strap 142.5-148.5. Pins/bushings follow (K pin 80-149, C 113.5-149, B 119.5-149).
- **M3:** hex sleeve inner 26.3 A/F, **only 4 mm long (y 94-98)** at the inboard end (Structural re-check: longer sleeve overloads gearbox bearing 1); pocket 29.2 A/F relieved to y 100. Hex vertices point along the thigh axis; gearbox homing tab = nominal thigh angle -24.26. Three pcd-15 M4 holes replaced by ONE central Ø9 clamp-screw hole (gearbox rev 1).
- **M7 load path (box beam):** body dowel deleted. Spring anchor pin carried by the arch plate, which has a lug (x 83-111 up to leg Y 87.5 = world z 367.5) abutting a **6061 box beam 40 x 8.5 x 2 wall** (y 52-119.5), foot plate 6 mm on the body (y 38-52), tied to the body frame by 2 x M5 into the Body top rib (Body to provide seats) and to the lug by 2 x M5 (axial). Hand checks (not FEA): beam, 169 N at the tab, M = 11 Nm -> 8 MPa; if it takes 0.5 kN of the B-pin load, 34 Nm -> 24 MPa (SF > 8). Posts: 2 x Ø16x3, 0.6 kN each x 79.5 mm = 48 Nm -> 140 MPa (SF 5 on 700). Arch ring around the Ø42 bearing seat widened to R28 (7 mm ligament; 811 N bearing reaction -> ~25 MPa with Kt 3). **Structural still owes the formal check of the 811 N + 180 N case.**
- **M16:** C pad radius 14 -> 10.5 (wall 3.5 round the Ø14 bushing); thigh-to-C-pad in-plane clearance at h289 was 0.2 mm, now 4.2; check also 11.0 at h140-195. **M12:** spring-to-arch gap 2 mm (Y). Stop pad shortened to 15 mm (clears the spring by 7.3 mm at 140).
- **M15:** all leg STEP/STL now in WORLD coordinates (left leg, nominal pose h195, x fwd, y lateral outboard +, z up; right = true mirror about XZ). Rev 1 files were Y-up / handed-swapped: Assembly must re-import.
- Wheel axle path in body frame (hip-relative x): -6.6 (h140), -10.6 (h195), -53.3 (h289) - Body's axle notch (A3) must be re-derived from this (the axle sits 26 mm further forward than rev 1 at h195, 26 mm at h140).
- Mass per leg 949 g solid (arch plate 70 g -> includes lug; beam 21 g). Remaining: spring ordering/wire check, FEA of the shank dog-leg and the arch plate, C-pad strength after the radius cut, bolt seats on Body.

Owner: Leg CAD Engineer · 2026-11-05 · built to leg_spec.md **Rev 1** (Ø10 pins, 3 mm Al shank plate, steel-lined hex hub, no mass cuts) and the wheel neck Ø38 (shank foot hole Ø38.2).
Files: `cad/parts/leg.solidcraft` (nominal pose, all bodies), generator `cad/parts/src/build_leg.py` (`--check` prints the clearance table; `--parts a,b --h 195` builds a JSON for `solidcraft-cli run`), STL `exports/stl/leg/*.stl`, STEP `exports/step/leg_*.step`, screenshots `docs/screenshots/leg_{195,101,289}_{top,iso}.png`.
Frame: X = world x − 28, Y(up) = world z − 280, sketch Z = world y. Parts are exported in assembly position at nominal (h 195); re-orient in the slicer.

## 1. Y stack (world y, mm)
Shank Al plate 68–71 · shank printed 71–80 (wheel hub starts 80.5) · K pad 80–93, C pad 80–123 · thigh hub/plate 93–103 · crank clevis 104–116 (spring axis 110) · arch plate 117.5–124.5 (outer hip bearing, stub y 103–124.5) · coupler 125–139 · knee strap (Al, 6 mm) 139.5–145.5.

## 2. Parts
| Part | Material / process | Volume cm3 | Mass (solid) |
|---|---|---|---|
| Leg_Thigh: hub R22, hex pocket 29.2 A/F for the steel sleeve, 3 x Ø4.5 on pcd 15, hollow stub Ø30/Ø24 to y 124.5 (bolt access), crank 40 mm with 4 mm slot, Ø5 pin hole, striker lug, knee boss R17 (Ø14 bushing), phase-wire groove | PAHT-CF | 80.9 | 97 g |
| Leg_Coupler: 16 deep bar, R14 eyes, Ø14 bushing bores | PAHT-CF | 32.3 | 39 g |
| Leg_Shank: arm with 14 mm dog-leg (clears hip housing), K pad, C pad, foot R36 with Ø38.2 hole, 4 x Ø4.5 on pcd 46, phase-wire channel | PAHT-CF | 130.0 | 156 g |
| Leg_ShankPlate 3 mm (inboard face, SPI cable rides on it) | 6061-T6 waterjet | 30.8 | 83 g |
| Leg_KneeStrap 6 mm (outer cheek of K and C: both pins pass, so it is rigid with the shank) | 6061-T6 | 10.5 | 28 g |
| Leg_ArchPlate 7 mm (outer 6806 seat Ø42, B pin, stop-pad seat, anchor pin, 2 post holes) | 6061-T6 | 50.0 | 135 g |
| Leg_OutriggerBeam 6 mm L (body front x 57 to anchor, out to y 124.5) | 6061-T6 | 12.6 | 34 g |
| 2 x Leg_ArchPost Ø16x3 steel tube, y 40–117.5, at r 82, 142 and 162 deg | 4140 / S355 | 19.0 | 149 g |
| TPU 95A: stop pad 10x10x25, 2 rest bumpers Ø10x6, dot Ø6 | TPU | 3.5 | 4 g |
Bought: pins K Ø10x65, C Ø10x35, B Ø10x28.5 (h6, 12.9 / 42CrMo4), crank pin Ø5, anchor pin Ø5; 7 sintered-bronze bushings ID10/OD14 (L6–14); K spacer tube; 6806-2RS (outer hip bearing); hex sleeve 1.5 mm steel 26/29 A/F x 6; M4 x 16 + washers; spring 2.7 N/mm (envelope only, 13x13); e-clips. Hardware about 220 g.
**Mass per leg ≈ 945 g solid-model (printed 292 + Al 281 + steel posts 149 + hardware/spring ≈ 220 + TPU 4); ≈ 850 g with real infill. Two legs ≈ 1.7–1.9 kg** (leg_spec rev 1 had 0.54 kg: the arch plate, posts, beam, strap and solid sections are new). Pockets/lightening were not modelled; solid is conservative.

## 3. Print and settings (Bambu A1, hardened nozzle, dried PAHT-CF)
Thigh: flat, inboard face (y 93) down, hex pocket on the bed side (0.12 layer), 5 walls, 40 % gyroid, 100 % around hub; layers lie in the bending plane. Coupler: flat on its side face. Shank: flat, plate face (y 71) down, pads up; diagonal on the bed (≈ 290 mm span; if it will not fit, split at the bow with a lap and 2 x M4). All: 4–5 walls, bushing bores printed Ø13.9 and reamed, steel inserts for the hex sleeve epoxied. TPU: flat, 15 % gyroid, 2 walls. Right leg: mirror in the slicer.

## 4. Clearances (`build_leg.py --check`, in-plane, same-Y parts)
| Pose h | 101 | 130 | 195 | 289 |
|---|---|---|---|---|
| thigh angle (deg) | −0.3 | −9.2 | −33.2 | −79.6 |
| shank ↔ hip housing R52.1 | 9.6 | 28.2 | 47.0 | 25.6 |
| B pin (R5) ↔ spring | 2.4 | 4.6 | 9.6 | 13.4 |
| coupler ↔ K pin | 9.9 | 16.8 | 27.9 | 33.9 |
| posts ↔ shank / thigh / crank | 107 / 52 / 30 | 135 / 52 / 27 | 170 / 52 / 26 | 139 / 52 / 43 |
| depth (C x + 28 + 14 + 125) | 325 | 323 | 301 | 210 |
**Spring ↔ B fix:** B moved 4 mm down (46, 34 → 46, 30): crouch clearance −1.3 → +2.4 mm (Ø10 pin). Larger moves (−6) lose the 289 mm extension (max hip 282). In addition the B pin starts at the arch plate (y 117.5) and the spring band is y 103.5–116.5, so the pin never enters the spring band (Y gap 1 mm). **The spring axis moved to y 110 (outboard of the thigh hub)** because the 13 mm spring envelope crosses the Ø44 hub at crouch (it passes 18.8 mm from the hip axis; hub R22 + spring 6.5).
Hip range now 80–290; thigh swing grows to −79.6 deg at 289 (was −72.7); nominal thigh −33.2 deg (was −30): gearbox homing tab is set for −29.99 (3.2 deg shift, Gearbox to confirm). End stop engages at hip 130 = thigh −9.2 deg.

## 5. Double-plate joints and loads (Rev 1 values, S1–S13)
- K: shank pad (y 80–93, bush centre 87) and strap (y 139.5–145.5) straddle the thigh (98): reactions 0.80 F / 0.20 F; S5 2011 N: bushing 1610 N / (10 x 12) = 13 MPa, pin bending (497 N x 44 mm) = 180 MPa, **SF 6 on 1100**. C: coupler (y 125–139) between C pad (bush 111–123) and strap: 0.37 F / 0.63 F, bushing 20 MPa. B: Ø10 pin cantilevered from the arch plate, M = 1955 x 7.5 = 14.7 Nm, 150 MPa, **SF 7**.
- Thigh at the stop station (10 x 60 solid): σ = 96.5 Nm / 6000 = 16 MPa, **SF 2.8** (S5, allowable 45.5); S3 fatigue SF 4. Crank: 180 N x 40 = 7.2 Nm, ear bearing 4.5 MPa, SF > 3. Hex: 17.3 Nm, flank bearing 4.9 MPa on the steel sleeve, **SF > 5**. Stub Ø30/24 PAHT: 1.1 kN at the outer bearing, σ 12.7 MPa, **SF 3.6** (needs a R2 fillet at the thigh).
- Shank: Al plate 3 mm share by stiffness (Rev 1 SF 2.7 S5+S6, 1.47 S7 placeholder). The dog-leg raises the bending moment in the arm: **needs FEA** (not done).
- Arch plate: bore section 49 MPa at 88 Nm (SF 4.9 on 240; ~2 with Kt). **The B-pin reaction (2 kN) goes through the arch plate into the posts and beam. Posts: 1 kN x 77 mm = 77 Nm, tube 227 MPa, SF 3 on 700. The outrigger beam (6 x 20 section) does NOT reach SF 1.5 for that load (about 1.3 on x, worse on z): needs a ribbed/box beam or a body-integrated frame.**

## 6. Cable routing
3 phase wires: groove 8 x 3 on the thigh inboard face (hub to knee), service loop R >= 20 in the 13 mm gap y 80–93... now y 103–139 at the knee (spacer Ø14 tube is the pivot; use a 40 mm slack loop on the inboard side), then the 10 x 4 channel on the outboard face of the shank arm (s 40–140) to the foot. Shielded SPI (~45 cm) rides on the **Al plate inboard face (y 68)** with P-clips, 15+ mm from the phase channel (y 76–80) by Y offset (≥ 8 mm plate+printed) — 15 mm separation holds only at the knee/foot, along the arm it is 8–12 mm: add shield braid grounding at the body end; cable passes the Ø14 axle bore at the wheel (SPI slot of rev 0 removed, encoder is in the wheel carrier now).

## 7. Open questions / changes to design assumptions
1. **Wheel vs hip housing/arch at crouch (layout-level):** tyre R85 spans y 80.5–151; housing cover R52 to y 93 and arch disc R24 overlap it when hip < ~137 mm (36 mm at 101; the end stop engages at 130). Needs a decision (wheel inboard cut-out, smaller cover, or hip floor 137).
2. **Axle foot:** carrier bolts pcd 46 are 1.65 mm from the Ø38.2 hole wall (needs shank foot boss; plate is the load path). Foot enlarged to R36.
3. Support structure (arch plate, posts, beam) is a concept: posts bolt to the hip Al plate at r 82 (142 and 162 deg, between the skirt ears at r 64) and the beam to the body front; body/gearbox engineers must provide seats. The B pin reaction path is the critical open item.
4. Y stack changed: thigh plane unchanged (93–103) but crank/spring y 110, coupler y 125–139, strap to y 145.5, stub to 124.5 (the gearbox doc said arch ≈ 108); outer bearing spacing 33 mm.
5. B (46, 30), thigh angles and homing tab (above); pins Ø10 (BOM item 21–23 to be replaced).
6. Not modelled: pockets/ribs and the 2 mm thigh cover (solid sections used), cable clips, e-clip grooves, threads. Bushing / press fits need a coupon (O16). PAHT-CF E ≈ 5 GPa assumed. S7 side-fall load still a placeholder. Mass is reported, not capped.
