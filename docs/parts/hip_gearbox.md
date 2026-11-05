# Hip gearbox 6:1 — P3a detailed CAD (rev 3: single output bearing, leg owns the outer bearing; rev 2: 6:1 gear set)

Owner: Gearbox Design Engineer (under Mechanical Design) · Date: 2026-11-04
Inputs: DECISIONS.md, docs/design_targets.md rev 2 (frozen), docs/layout.md rev 0, docs/analysis/materials_gears.md (O3, CAD rules), thermal.md (hip 3 mm Al plate), electrical.md (hip encoder).

## Files

| What | Path |
|---|---|
| SolidCraft design (multi-body; saved with the SolidCraft save tool) | `cad/parts/hip_gearbox.solidcraft` |
| Generator script (rebuilds the design: `python3 build_hip_gearbox.py hg.json && solidcraft-cli run hg.json --save hip_gearbox.solidcraft`) | `cad/parts/src/build_hip_gearbox.py` |
| Gear geometry, phasing, contact ratio and backlash checks (asserted) | `docs/analysis/calc/hip_gear_geometry.py` → `hip_gear_geometry_output.txt` |
| 2D mesh interference check of the CAD tooth polylines (asserted) | `docs/analysis/calc/hip_gear_mesh_check.py` |
| Envelope vs layout (leg clearances, body box) | `docs/analysis/calc/hip_gearbox_envelope.py` → `hip_gearbox_envelope_output.txt` |
| STEP of the full gearbox (printed parts, Al plate, bearings, pins, encoder envelope) | `exports/step/hip_gearbox.step` |
| STL per printed part (left side; assembly position, re-centre in the slicer) | `exports/stl/hip_gearbox/HG_*.stl` |
| Screenshots | `docs/screenshots/hip_gearbox_iso.png`, `_section.png` (XZ cut), `_ring_stage_z30.png` (cut through the ring stage), `_arch.png` (rev 1, stale: the arch is gone in rev 3; the old exploded view was removed as stale) |

**CAD frame.** Z is the gearbox axis (outboard is +), z = 0 is the 8308 rotor face, and X is world X. Left side: world = (28 + x, 40 + z, 280 − y). The right side is the same stack mirrored about the world XZ plane:
- Sun, planets, carrier parts, Al plate: identical parts.
- Skirt, ring and cover: use the **mirrored** STL (mirror in Bambu Studio), because the ear and stop-block angles are set in world XZ.

## REV 3.2 (2026-11-05): A13 / C7 bearing 1 6806 -> 6906 (30x47x9) and C11
Patched in one small run (`cad/parts/src/patch_hip_gearbox_6906.py`, ~85 s; backup `hip_gearbox.solidcraft.pre6906.bak`; `build_hip_gearbox.py` still builds the 6806 state).
- **Bearing 1 = B_6906**, local z **42-51** (outboard face stays at z 51, so the cover lip z 51-53, cover face y 93 and the thigh plane y >= 94 are unchanged; 7 -> 9 mm width grows inboard by 2 mm). Seat Ø42 -> **Ø47** (cover bore z 42-51), cover boss wall r 23.5-26.5 (down to z 42.5), carrier groove floor z 43 -> **41.5** out to r 27.5 (wall to the pin holes 3.3 mm, was 6.25; floor 1.5 mm over the hub-to-pin web, shear 7 MPa at 20 Nm), inner-race shoulder top z 44 -> 42. Cover lip (r 19.02-23.3) untouched: bite on the outer race 2.7 mm. Boolean interference B_6906 vs cover 0.1 mm3 (coaxial contact only), vs carrier 0.
- **Mass per side:** bearing 19 -> 45 g (+26, catalogue 6906-2RS), CarrierOut 58.8 -> 52.7 g (-6.1), Cover 41.1 -> 41.4 g (+0.3): **+20 g/side, +40 g for the pair** (gearbox about 454 g without / 534 g with the Al plate).
- **C11 (plate -> body):** the 4 x M4 are through-bolts M4 x 55 + nut (body side plate nut pockets) with **a washer under the head on the Al plate and a washer under the nut** (Body: washer step O9.6 in the pocket). No heat-set inserts. Bolt length unchanged.
- STL re-exported: `HG_Cover_L.stl`, `HG_CarrierOut.stl`; `hip_gearbox.step`. Open: calibration coupon for the O47 seat; structural re-run for the thinner carrier groove floor (hand estimate only).

## REV 3 (2026-11-05): assembly review A1-A7 (M1, M3, M4, M6)

Patched in small runs on the saved design (`cad/parts/src/patch_hip_gearbox_rev3.py`, ~55 s; no rebuild; the previous state is `hip_gearbox.solidcraft.bak`). `build_hip_gearbox.py` was NOT updated for rev 3 (it still builds the rev 2 arch/bearing 2): the .solidcraft/STEP/STL are the reference.
- **M1 (done).** Deleted: bearing 2 (B_6806_2), HG_Arch (bar, ring, post, M3 x 60 arch bolt), the Ø30 journal extension (z 65-73). The leg's outer 6806 (y ~121) and its arch plate on the posts replace them. Kept: the 26 A/F hex (z 53-65) and the M4 clamp insert, whose hole moved into the hex (Ø5.6 x 10, **z 55-65**, was z 63-73). The 5th ear at world 105 deg is now an ordinary stack ear (M3 x 35 + washer like the others). Clear zone of rev 1 (strip y 104-116 along 105 deg) is released: the gearbox keeps nothing outboard of y 92 (cover trim) except the hex end at y 105 (z 65).
- **M3 (done, re-settable).** The gearbox hex stays 26 A/F; the Leg's steel sleeve inner is **26.3 A/F** (Leg owner; sleeve OD must grow with it, 1.5 mm wall). Homing tab moved from centre 209.99 deg (thigh -29.99) to **213.19 deg local (thigh -33.19)**; the old tab outside r 40.8 was cut off and a new 8 mm tab joined (r 39.5-47.5, z 40-48.5). The cover stop blocks are in thigh-angle terms and unchanged (crouch +1.5, extension -74.7 deg). **To re-set for another thigh angle:** `python3 src/patch_hip_gearbox_rev3.py out.json <thigh_deg>` is for the original rev 2 state only (it also does M1/M4); for a later re-set, edit the `TabOld`/`TabNew` pair in that script (old = last angle, new = final angle) and run it on a design that has only the tab step (3 commands, < 10 s). `leg_interfaces_rev2.md` (Leg owner) was not available when this was done: -33.19 deg is the A5 value, **re-check against the final thigh angle**.
- **M3b (rev 3.1, 2026-11-05).** Final nominal thigh angle **-24.26 deg** (leg_interfaces_rev2.md): homing tab / hex index re-set from 213.19 to **204.26 deg local** (tab-only step, same quad/cut-then-join as `patch_hip_gearbox_rev3.py`, run from a scratch copy; the script itself still holds -33.19 as default, pass -24.26 only on a pre-M1 design). Hex repeats each 60 deg. Leg sleeve engages the hex only 4 mm (inboard end, y 94-98).
- **M4 (superseded by rev 3.1).** Cover trim to z 52 (1 mm lip) failed the 1.7 kN axial case. **Rev 3.1: cover boss/lip back to z 53 (world y 93); 2 mm lip z 51-53, r 19.02-23.3** (r 19.02 not 19.0: a boolean at exactly r 19 fails in this kernel; bite 1.98 mm). Lip SF (structural.md Rev 2 re-check): 2.57 at 0.97 kN, **1.47 at 1.7 kN** (>= 1.4). Needs thigh plane at y >= 94 (A5, 1 mm clearance to the cover). Backup of the pre-fix design: `cad/parts/hip_gearbox.solidcraft.pre_lip.bak`. Re-exported: `HG_Cover_L.stl`, `HG_CarrierOut.stl` (tab), `hip_gearbox.step`.
- **M6 (not done, by decision).** Body has not confirmed it keeps the end-stop/TPU seat arm (body.md still lists it to y 92, x 90-95). Rotating the ear set +5 deg (15/75/105/165/195 -> 20/80/110/170/200) would mean rebuilding Ring (ears are inside the lofted tooth sections, which hang this kernel), Cover and Skirt. `EARS` in `build_hip_gearbox.py` is the one parameter; the ears also have to stay >= 25 deg from the body posts (45/135/225/315), 20 and 200 deg give 25 deg. Do this only if Body keeps the arm.
- **Mass per side (CAD, 1.2 g/cm3).** Arch -23 g, 6806 #2 -19 g (bought), M3 x 60 -> x 35 -1 g, CarrierOut -6.8 g (58.8 g), Cover -0.7 g (41.1 g): **about 434 g/side without the Al plate, 514 g with it** (was 484 / 564). Two sides about 1.03 kg (-0.10 kg).
- **Structural (docs/analysis/structural.md "Rev 2 re-check").** Spacing is 33.5 mm (87.5 -> 121), but the thigh sits only 11.5 mm from bearing 1, and the hex is where the thigh load goes into the carrier. With a rigid thigh and hex contact over the whole hub, bearing 1 is worse than before (LC-D ball SF 0.76, seat 0.65, tilt 5.1 deg). The outer bearing only helps if the hex contact is moved to the inboard end of the hub (y 94-97): then LC-D ball SF 1.14, seat 1.42, tilt 2.4 deg (half of rev 0), LC-A/B/C pass. **Requirement on the Leg:** steel sleeve (26.3 A/F) only 3-4 mm long at the inboard end of the hub (y 94-98), the rest of the pocket relieved radially (>= 0.5 mm), so the radial load goes to the stub bearing.

## REV 2 (2026-11-05): 6:1 gear set (DECISIONS.md, materials_gears.md "Hip 6:1 option")

Only the **sun and the planet big step** changed: sun 28 T m1.0 spur b15.5 x −0.146; big step 40 T m1.0 spur b14 x −0.097. Ring 63 T m1.5, small step 18 T m1.5, carriers, pins, bearings, housing, arch and ears are untouched. Ratio = 1 + 40·63/(28·18) = **6.000**; centre distance 33.75 on both stages. Built with `s_gear` (sun + 3 planets, one 90 s run from the STEP); the geometry is in `calc/hip_gear_geometry.py` (asserted) and the mesh check in `calc/hip_gear_mesh_check.py`.
- **Phasing note (changed).** Zs/3 = 9.33 is not an integer, so a planet is **not** a plain 120° rotated copy any more. The 3 planets are the same part, offset 0, but planets 2 and 3 are spun on their pins by **20°·6 and 20°·3** (multiples of the 20° small-step pitch, so the ring mesh is unchanged) before the 120° / 240° rotation. This is the only valid set: (j₂,j₃) ∈ {(6,3),(6,12),(15,3),(15,12)}; the same planet works at any of them. The assembly condition (Zs·Zp2 + Zr·Zp1)/(3·gcd) = 504 is an integer, and the sun is fitted last. In the print/assembly the planets are identical parts; only their install angle differs (mark the dot on the big step and index it to the sun with the 20° steps; a wrong install shows as a binding sun).
- **Clearances.** Big-step swept R 54.7 mm < skirt big-section inner R 58.5 (3.8 mm); tip gap between planets 16.7 mm. Lightening holes (outer edge r 17.0) stay inside the big-step root (R 18.65).
- **Mass.** Printed gears: sun 21.8 g + planets 3 × 28.3 → 84.8 g (was 18.0 + 102.0): **−13 g/side**. Gearbox per side about **484 g** without the Al plate (printed 390 g + bought 94 g), about **564 g** with it.
- **Strength (materials_gears.md):** sun-planet SF 1.78 static at 20 Nm / 50 °C (fatigue 1.40), ring mesh 2.26. Tests: print the sun first (m1.0 teeth on the 0.4 nozzle).
- The rev 0 text below (8:1, 18 T / 36 T, planets rotated copies, 413-435 g, Zs/N = 6) is **superseded** where it conflicts with this section: the tooth table above and the part list were updated, the assembly paragraph and the old mass table were not rewritten.
- `build_hip_gearbox.py`: sun/planet sections updated (profile from `hip_gear_geometry.py`, planet copies spun on their pins, lightening holes at r 13.5); it was not re-run end to end (kernel hang), the STEP/STL/.solidcraft are the reference. Exploded screenshot retaken.

## REV 1 (2026-11-05): structural fixes, arch, rotated ears (client: weight and size are soft, priority = finish)

**How it was built.** Rebuilding the full history in one run hangs this kernel (run --in on the old .solidcraft re-evaluates every loft; > 10 min). The saved design was therefore re-made from the STEP of the 23:24 design (10 s import) with small scripts, each < 100 s: Ring, Cover, Skirt, CarrierOut rebuilt (solid.remove + new bodies), then arch + second bearing. `cad/parts/hip_gearbox.solidcraft` now holds the imported base plus the last script. `build_hip_gearbox.py` has all changes (full-history rebuild not re-verified).

| Change | Result |
|---|---|
| **Second output bearing** | 6806 #2 (B_6806_2) at local z 65-72 on a Ø30 journal of CarrierOut (z 65-73). Bearing centres y 87.5 and 108.5 = **21 mm apart**; thigh plane (hex 26 A/F, z 53-65) at **y 94-103, between the bearings**. Bearing 2 is axially free (bearing 1 locates). Needs a retainer (snap ring or the clamp washer lip) at assembly |
| **Arch (HG_Arch, 24.9 g/side with 1.29 g/cm³ default; 23 g at 1.2)** | Bar 16 x 12 (z 64-76, u 10-72) with a Ø47 ring and a 16 x 15.5 post (z 42.5-64) on the cover ear at local 255 (world 105 deg), M3 x 60 stack bolt through post + cover/ring/skirt ears. Seat Ø42 with a 4 mm lip (z 72-76) |
| **Thigh clamp (changed)** | The 3 x M4 inserts on the hex face are gone (the journal covers them). The thigh sits between the z 53 shoulder and a 2 mm spacer (z 63-65) pushed by the bearing-2 inner race; one M4 + washer in a steel insert (Ø5.6 x 10) in the journal end clamps the stack. Torque goes through the hex. **Insert pull-out test coupon is still an open item** (see below) |
| **Skirt stiffened** | Windows narrowed from 20 x 14 (saved CAD) to 10 x 10 (frames ~4.4 mm thick, 2 mm proud), plus 6 external ribs 5 x 4.9 mm between the windows. Estimate (section modulus +22 %, lower Kt): SF 1.41 -> about 1.7 (>= 1.5). Structural to re-confirm |
| **Cover lip** | Lip 2 mm thick x 2 mm bite (z 51-53, r 19-23.5), was 1 mm. Shear area x2: SF 1.1 -> about 1.5 at 1.7 kN axial (estimate). The arch lip (4 mm) takes the load in the other direction too if bearing 2 is axially closed |
| **M3 washers** | Mandatory on all 5 stack bolts (cover side Ø7 washer) and on the arch bolt: SF 0.75 -> 1.51 (structural.md 2d). Added to the bought list (6 x M3 washers) |
| **Ears rotated (body posts)** | Local angles 345, 285, **255**, 195, 165 = world angles **15, 75, 105, 165, 195 deg** (X toward +Z), same on the right side. Body hip posts at world 45/135/225/315: >= 30 deg from every ear. Housing reaches r 66.8 (x max 94.8 < 99.6 bulge limit, Ø140). Ring, cover, skirt and stack bolts all rotated together |
| **Skirt lip over the planets: dropped** | The 2 mm closing lip (r 52-58) would not join in this kernel (3 attempts, "faces that touch"). The old CAD had it as 5 loose bodies anyway. Limitation: the r 52.1-57.5 gap over the big planets stays open (dust only, no load) |
| Weight-saving steps | Skipped (client). Cover top back to 2.5 mm, no ribs, no post bores, no carrier pockets |

**Final mass per side (CAD volumes x 1.2 g/cm³, 100 % solid):** printed 403 g (sun 18, planets 102, carrier-in 34, carrier-out 66, ring 51, cover 42, skirt 68, arch 23) + bought about 94 g (rev-0 69 g + 6806 #2 19 g + extra washers/bolt/insert 6 g) = **about 500 g/side without the Al plate**; Al plate 79.9 g -> about 580 g/side. Two sides: about 1.16 kg. **O10 closed:** accepted by the client (soft target); the final numbers are reported to the Manager.

**Final envelope (left side; world = (28 + x, 40 + z, 280 - y); right side mirrored in Y).**
- Thigh plane: **world y 94-103**; bearing 1 centre y 87.5; bearing 2 y 105-112 (centre 108.5); stub end y 113.
- Housing: Ø133.6 max (ears, r 66.8) at y 53-80; x -38.8 to 94.8, z 213 to 347; main body Ø122 (Ø104 ring section).
- **Arch, world coordinates:** bar and bearing ring at **y 104-116**, covering X 1.6-51.5, Z 256.5-351.6 (ring Ø47 around the axis, bar 16 wide running toward world angle 105 deg (up, slightly rearward) to r 72); post at y 82.5-104 near X 2-17, Z 335-352 (r 56-71.5 at 105 deg).
- **Clear zone the leg and body must keep free:** around the hip axis, everything outboard of y 103.5 inside r 24 except the Ø30 stub; the 16 mm-wide strip y 104-116 along 105 deg out to r 72; the thigh may not rise above y 103.5 inside the arch footprint. The thigh sweeps world angles 1.5 to -74.7 deg (far from the arch). The body bracket (if any) takes the arch bar end at X 1.6-17, Z 335-352, y 104-116; the arch is otherwise bolted to the housing, not to the body.
- Body side wall y 63 and the keep-out y > 99 in body.md must be changed to y > 82.5 around the post at 105 deg (post sits y 82.5-104).

**Closed:** OQ-2 (single 6806 -> two 6806 + arch). O10 (mass overrun accepted by client, final numbers above).

**Open items (new):**
1. **M4 insert pull-out test coupon** in PAHT-CF (1 steel insert at the journal end carries the thigh clamp; limit torque to about 0.4 Nm until tested).
2. Bearing 2 retainer (snap ring or printed lip) and fit of the Ø42 seat (calibration coupon).
3. Arch post/bar stress (about 1.1 kN radial at the bearing, lever about 21 mm + 56 mm) has not been analysed by Structural; the post is 16 x 15.5 mm PAHT-CF on one ear. Recommend an FEA/hand check before printing; if it fails, widen the post or add a second ear.
4. Skirt SF and cover-lip SF values above are estimates.
5. Open skirt lip gap over the planets (limitation).
6. build_hip_gearbox.py was not re-run end to end after rev 1 (kernel hangs); the STEP and .solidcraft are the reference.

## 1. Gear design and checks (all values from `hip_gear_geometry.py`)

| Item | Value |
|---|---|
| Stage 1 | Sun **28 T** → planet big step **40 T**. m **1.0**, 20°, **spur**, profile shifts x_sun **−0.146**, x_planet **−0.097** (sum −0.243 gives centre distance 33.75 exactly), b 14 (sun 15.5 wide). Sun tip R 14.85 / root R 12.60; planet tip R 20.90 (swept R **54.7**, was 57.5), root Ø37.3 |
| Stage 2 | Planet small step 18 T → fixed ring 63 T. m 1.5, 20°, **herringbone ψ = ±20°**, b 20 (2 × 10) |
| Ratio | 1 + (63·36)/(18·18) = **8.000** (ring fixed, carrier output) |
| Centre distances | 1.25·(18+36)/2 = **33.75** = 1.5·(63−18)/2 = **33.75** → no profile shift |
| Contact ratio | stage 1 **1.75**, stage 2 **1.79** (ring addendum shortened to 0.9 m) |
| Big-step tip gap between planets | 10.96 mm |
| Big-planet swept radius | **57.5 mm (Ø115)**: drives the housing size (see §6) |
| Backlash | Each gear is thinned by 0.06 mm (ring spaces widened by 0.06 mm), so 0.12 mm per mesh. Output lost motion (sun held) = **0.20°** (target ≤ 0.5°) |
| Mesh check of the CAD polylines | 2D raster over one planet small-step pitch with the 6:1 kinematics and **all 3 planets** against the sun: **0 interference points**. Minimum flank gap **0.056 mm** (stage 1) and 0.033 mm (stage 2). Output: `calc/hip_gear_mesh_check_output.txt` |
| Tooth profile | Involute polyline, **10 points per flank**, plus a 2-point root transition (≈ 0.38 m root fillet). Tip and root are polylines |
| Planet bearing wall | 685ZZ bore Ø11 to small-step root Ø23.25: 6.1 mm |

### Assembly condition and tooth phasing (compound planets)
- General condition: (Zs·Zp2 + Zr·Zp1)/(N·gcd(Zp1, Zp2)) = (324 + 2268)/(3·18) = **48 → integer, OK.**
- Here the condition is stronger: **Zs/N = 6 and Zr/N = 21 are both integers**. So planet k is planet 0 rotated by 120°·k about the main axis, and **all three planets are the same printed part with the same step offset.** Any single offset between the two steps assembles, because the sun is free to turn when it is inserted last. This is checked in the script.
- **Chosen offset: 0.** One big-step tooth and one small-step tooth sit on the same radial line, and every small tooth lines up with a big tooth (pitch 20° vs 10°). Mark that line with a dot on the big-step face, for inspection only.
- CAD phases (gear-local angle 0 = +X):
  - sun: gap on 0° (teeth at 10° + 20°k)
  - planet 0 at (33.75, 0): small-step gap facing the ring (teeth at 10° + 20°k), big-step tooth facing the sun (teeth at 0° + 10°k)
  - ring: tooth centred on 0° (k·360/63)
- Herringbone: the ring mid-section (z 29.5) is turned by tanψ·10/47.25 = 4.41°, and the planet small step by tanψ·10/13.5 = 15.4°. Same hand, as an internal mesh needs. Both apexes sit at z 29.5.
- Assembly order:
  1. Fit pins and planets in the carrier-in.
  2. Drop that into the ring (all 3 planets mesh: 63/3 integer).
  3. Fit the carrier-out.
  4. Lower the housing onto the motor, so that the sun on the rotor enters last and finds its phase by turning.

### Why stage 1 is spur and stage 2 herringbone
**Herringbone on stage 1: tried, not used.** SolidCraft makes herringbone reliably (a ruled loft through 3 sections; that is how stage 2 is built). Stage 1 stays spur for an axial-constraint reason:
- If both meshes were herringbone, the planet would be located axially twice: by the ring apex and by the sun apex. The sun is fixed axially by the motor bearings.
- Print and motor tolerances (±0.1–0.3 mm) would then preload the teeth axially.
- With stage 1 spur: the planets float ±0.2 mm on their pins (0.3 mm shims, 0.5 mm gaps) and centre on the ring herringbone. The sun can slide along the spur mesh.

This costs no strength: the O3 Lewis check gave no helix credit (A8), so stage 1 SF 2.09 holds.

## 2. Part list

| # | Part | Qty/side | Material / process | Measured volume (CAD) | Mass |
|---|---|---|---|---|---|
| P1 | HG_Sun: 28 T m1.0 spur (x −0.146, face 15.5) on a Ø50 × 5 flange; 4 × M3 counterbored on Ø40 (8308 rotor); Ø14 × 2 relief for the rotor hub | 1 | PAHT-CF, 100 % | 18.19 cm³ | 21.8 g |
| P2 | HG_Planet: 40 T m1.0 spur (x −0.097) (z 5.5–19.5) + 18 T herringbone (z 19.5–39.5); 2 × Ø11 685 pockets, Ø6 pin bore; 6 × Ø7 lightening holes on r 13.5 (inside the root Ø37.3) | 3 | PAHT-CF, 100 % | 3 × 23.54 cm³ | 84.8 g |
| P3 | HG_CarrierIn: ring Ø81.5/Ø52 × 4 with 3 integral Ø14 posts (z 5–40); 3 × Ø5 press holes for the pins; M3 heat-set inserts in the post tops | 1 | PAHT-CF, 100 % (or 6 walls + 60 %) | 28.04 cm³ | 33.6 g |
| P4 | HG_CarrierOut: plate Ø81.5 × 9, blind Ø5 pin holes, 6806 seat (Ø30 stub with inner-race shoulder, groove for the cover boss), **output hex 26 A/F × 6** with 3 × M4 steel inserts on Ø15, homing tab | 1 | PAHT-CF, 100 % | 44.96 cm³ | 54.0 g |
| P5 | HG_Ring: 63 T m1.5 herringbone internal, OD Ø104.2 with 5 bolt ears (r 64) | 1 (mirror R) | PAHT-CF, 100 % | 42.88 cm³ | 51.5 g |
| P6 | HG_Cover: flange + wall Ø104.2, top plate, 6806 boss Ø42 bore with outboard lip, 2 internal stop blocks, 5 ears | 1 (mirror R) | PAHT-CF, 5–6 walls 60 % | 34.16 cm³ | 41.0 g (100 %) |
| P7 | HG_Skirt (housing): flange on the Al plate (6 × M3 through, Ø108 BC), Ø100.8 skirt around the 8308 (2 mm air gap, 6 × 10 × 10 vent/wire windows), 45° cone, **Ø121.8 big-planet section**, lip that closes over the planets, 5 ears with M3 nut seats | 1 (mirror R) | PAHT-CF, 5–6 walls 60 % (thermal: PAHT-CF next to the can) | 54.25 cm³ | 65.1 g (100 %) |
| M1 | HG_AlPlate: 104 × 104 × 3, R8 corners. Ø12 centre hole (magnet). 4 × Ø4.5 on Ø40 (stator M4). 6 × Ø3.4 on Ø108 (skirt). 4 × Ø4.5 at ±44 (to the body side plate). 4 × Ø14 vents. 2 × M2 tapped at ±10.5 (encoder breakout) | 1 | 6061-T6, 3 mm, laser/waterjet | 29.59 cm³ | 79.9 g |

### Bought parts per side

| Item | Qty | Spec | Mass |
|---|---|---|---|
| Planet bearings | 6 | 685ZZ 5 × 11 × 5 | 11.4 g |
| Output bearing | 1 | **6806-2RS** 30 × 42 × 7 (6808 does not fit; see §5) | 19 g |
| Planet pins | 3 | Hardened dowel Ø5 × 45 (DIN 6325 / ISO 8734 m6) | 20.8 g |
| Shim washers | 6 | DIN 988 5 × 10 × 0.3 (one each end of each planet) | 0.6 g |
| Sun screws | 4 | M3 × 6 DIN 912 (check rotor thread depth, O14) | |
| Carrier screws | 3 | M3 × 12 DIN 7984 low head + 3 × M3 heat-set inserts (Ø4 × 7) in the post tops | |
| Output interface | 3 | M4 **steel** threaded inserts (Ensat-type, hole Ø5.6 × 10) in the hex; thigh bolts M4 × 16 + steel washers; torque by the 26 A/F hex | |
| Housing stack bolts | 5 | M3 × 35 DIN 912 through cover + ring + skirt ear, nyloc nut under the ear | |
| Skirt-to-plate | 6 | M3 × 10 + nut (through-bolt, nut on the flange top) | |
| Stator screws | 4 | M4 × 6–8 (8308 stator, through the Al plate) | |
| Plate-to-body | 4 | M4 + nut/insert in the body side plate | |
| Encoder | 1 | AS5047P/AS5048A breakout + Ø6 × 2.5 diametric magnet, 2 × M2 brass/A2 screws, shims for the 1.5 mm gap | (in layout, 8 g) |
| Fasteners total | | screws, nuts, washers, inserts | ≈ 17.5 g |

## 3. Print settings and orientation (Bambu A1, 0.4 mm hardened nozzle, PAHT-CF dried 80 °C/8 h, bed 100 °C, textured PEI + glue)

| Part | Orientation | Notes |
|---|---|---|
| Sun | Flange down (z 0 on the bed) | Ø14 relief bridges 14 mm. Counterbores open upward. 0.12 mm layers |
| Planet ×3 | **Big step down** | Small step and herringbone (20° from vertical) on top, no supports. Bottom 685 pocket → Ø6 ledge, 2.5 mm overhang. Lightening holes bridge ≤ 3.5 mm under the small-step root. 0.12 mm layers, 100 % |
| CarrierIn | Ring face (z 1) down, posts up | No overhangs |
| CarrierOut | **Inboard face (z 40) down** | Pin holes on the bed side. Groove, stub, hex and tab grow upward. No supports |
| Ring | Either face down | Herringbone teeth self-supporting. Brim recommended (Ø138 incl. ears) |
| Cover | Top face (z 52) down | Wall, boss and stop blocks grow upward. 6806 boss bore printed in XY |
| Skirt | **Flange (z −28.5) down** | The 45° cone is self-supporting. The **5 ears (z 13.5–19.5) overhang ≈ 8 mm**: small tree supports under each ear, or add a 45° gusset in rev 1. Windows bridge 10 mm |

- Every part fits the A1 bed: the largest is Ø138 × 50 mm (skirt with ears).
- Fits: 685 pockets Ø11.0 and pin holes Ø4.95 are press fits. 6806 seats Ø30.0 / Ø42.0 are nominal, tuned by a **calibration coupon** (materials rule: press 0 to −0.05 mm, sliding 0.2 mm).
- Gear backlash is in the tooth thickness (0.12 mm per mesh).
- The minimum running gap between parts at different speeds is 0.5 mm axial and ≥ 0.5 mm radial.

## 4. Mass (measured volume × ρ; PAHT-CF 1.2 g/cm³, 6061 2.70 g/cm³)

| Group | Mass |
|---|---|
| Printed gears (sun + 3 planets + ring), 100 % | 171.5 g |
| Carriers (in + out, 100 %) | 87.6 g (73.00 cm³ total) |
| Housing (skirt + cover), 100 % / at ~80 % effective fill (6 walls + 60 %) | 106.1 / 84.9 g |
| **Printed total** | **365 g at 100 %; 344 g with housing at ~80 %** |
| Bought (bearings 30.4, pins 20.8, shims 0.6, fasteners/inserts ≈ 17.5) | 69.3 g |
| **Gearbox per side (without Al plate)** | **≈ 413–435 g** |
| Al motor plate 104 × 104 × 3 | 79.9 g (layout: 32 g) |

**O10 result: the CAD is much heavier than both estimates.**
- BOM: 271 g. Materials: 150–200 g. CAD: **≈ 413–435 g**, so +142 to +164 g per side and **≈ +0.3 kg per robot**, plus +96 g for the two Al plates.
- Cause: the frozen gear set. The 36 T big step is Ø47.5 and 100 % solid, so the three planets alone weigh 102 g. The big planets sweep Ø115, so the housing needs a Ø122 section. The materials estimate assumed a Ø96–106 housing.

Recovery options, not applied (they need Materials/Manager approval):
1. Print gears with 6 walls + 40 % gyroid core (allowed by materials §4: "or 5–6 walls so teeth are all perimeters"): ≈ −35 g.
2. Pocket the carrier-out plate between the pins, and hollow the posts above the inserts: ≈ −12 g.
3. Rib the cover top plate (2.5 → 1.6 mm + ribs): ≈ −8 g.
4. Open the Al plate between the 4 body bolts (keep ≥ 80 × 80 cm² of exposed area for thermal): ≈ −25 g.
5. Larger skirt windows (also cooler): ≈ −6 g.

All of these together reach ≈ 330 g per side.

## 5. Bearing and interface choices
- **6806, not 6808.** The pins sit on r 33.75 (Ø5 hole edge at r 31.25), so the output bearing must stay inside r ≈ 28.
  - With a 6808 (OD 52), the cover boss and groove reach r 29 and leave < 2.4 mm to the pin holes.
  - With a 6806, the groove ends at r 25, leaving 6.25 mm of wall.
- **Steel output interface.** The output is a **26 A/F hex × 6 mm** that engages a hex socket in the thigh:
  - torque goes through the hex flanks by form fit (≈ 5.5 MPa bearing at 20 Nm)
  - clamping is by 3 × M4 into **steel** inserts on Ø15
  - this replaces a pure bolt-friction joint, which would give only ≈ 15 Nm with M4s on that small radius
- **Ring torque path.** Ring → 5 × M3 through-bolts, friction ≈ 76 Nm, to the skirt → 6 × M3 through-bolts to the Al plate → 8308 stator (4 × M4) and body side plate (4 × M4). Every primary joint is bolted through (materials rule). Inserts are used only at the carrier posts and the output.
- **Spring anchor: none on the gearbox output** (design rule). The thigh crank and spring anchors belong to the thigh and body (theory P3 spring re-fit: 5.5 J, anchor 49 mm outward, no effect here).

## 6. Envelope vs layout (`hip_gearbox_envelope.py`)

| Item | Layout (P2) | CAD | Status |
|---|---|---|---|
| Axial: rotor face → output face | 40 mm (world y 40–80, thigh from 81) | **53 mm** (output shoulder at world y 93; hex to 99) | **+12 mm**: the thigh plane must move to y 93–103 |
| Housing Ø, big-planet section (world y 34.5–61.5) | Ø100 | **Ø121.8** (ears to Ø138 at 5 angles) | Inside the body (side wall y ±63) but **exceeds the body box**: x 88.9 vs front 85, z 340.9 vs top 340. Skirt flange x 86 |
| Housing Ø, ring section (world y 59.5–79.5, the shank's Y range) | Ø100 | Ø104.2 + ears placed outside the shank sweep | **Shank ↔ ring 6.7 mm** (was 8.8; ≥ 5 OK) |
| Knee / C joint vs housing | — | 56.9 / 35.4 mm | OK |
| Al plate | Ø100 × 3 | 104 × 104 × 3 | Inside the body box (x 80, z 332) |
| Motor-side encoder | Ø30 × 8 at y 0.5–8.5 | Envelope body reserved at the same place. Magnet Ø6 × 2.5 in the plate's Ø12 hole, 1.5 mm gap | OK |

## 7. Homing hard stop
- **Tab:** on the carrier-out rim, 8 mm wide, r 39.5–47.5, z 40–48.5.
- **Stop blocks:** two blocks on the cover inner wall (r 42.25–49.5).
- **Engagement points:**
  - crouch stop at thigh_ang **+1.5°** (1° past full crouch, hip 101)
  - extension stop at **−74.7°** (2° past full extension)
  - free travel −72.7° … +0.5° is untouched
- **Load path:** the stop load goes carrier → cover → housing → body. **It never passes through the teeth.**
- The TPU end stop (thigh ↔ body, from hip 130) stays the landing stop. It is not on the gearbox output.
- **Contact pressure** at a 20 Nm homing/stall torque: ≈ 455 N on 6 × 8 mm ≈ 9.5 MPa (PAHT-CF OK). The stop is **not** sized for the 92–120 Nm landing stop torque; the TPU stop carries that.

## Assumptions
1. 8308 rotor face is flat at z = 0 with a hub ≤ Ø14 × 2. The stator base is at z = −28.5. Rotor M3 thread depth ≥ 4 mm. The shaft end is reachable through the stator centre for the encoder magnet. **To measure on arrival (O14).**
2. 685ZZ / 6806 seats are nominal sizes, tuned by the coupon. PAHT-CF density 1.2 g/cm³ at 100 %.
3. CAD pose is nominal stance: the thigh lies along local +29.99°.
4. Planets float axially ±0.2 mm on the shims. The carrier floats only within the 6806 clearance.
5. (Rev 1) Two 6806 (21 mm apart, thigh between them) carry the leg radial load and moment; the arch carries bearing 2 to the housing.
6. Bought-part masses are catalogue values (685ZZ 1.9 g, 6806-2RS 19 g); fastener mass is estimated.

## Open questions
- **OQ-1 (Mech Design / Manager): envelope.** The frozen gear set does not fit the P2 envelope.
  - The thigh plane moves +12 mm outboard (y 93–103); the knee pin and C-pin span grow.
  - The body front and top must clear a Ø122 hip housing at y 34.5–61.5: either local bulges of ≈ 4 mm front and ≈ 1–4 mm top (shell inner wall), or move the hip 6 mm down and back.
  - Width at hip height stays < 150, so the 300 mm width is unaffected.
- **OQ-2 (Structural): single 6806 — CLOSED in rev 1 (second 6806 on an arch, see REV 1).** It carries thigh loads with an ≈ 10 mm overhang (bearing centre y 87.5 to thigh mid-plane y 98).
  - The moment (≈ 3 Nm per 300 N) tilts the carrier against the planet meshes.
  - Recommend a second support: a thigh outboard bearing on a body-fixed stub, or a 6806 pair (+7 mm axial). Decide before printing.
- **OQ-3 (Materials / Manager): O10 mass overrun — CLOSED (client: weight is not a problem; about 500 g/side).** ≈ +150 g per side. Pick from the recovery list in §4, or accept the mass.
- **OQ-4 (Electrical / Control):** confirm the motor-axis encoder only (as in the layout). The output hex has no room for a second magnet. An output-side encoder would sit in the thigh at y ≈ 100.
- **OQ-5:** the 8308 lead exit angle. One of the six 10 × 10 skirt windows takes the leads; it may need widening once the motor is measured.

## Changes to design assumptions
1. **Hip gearbox envelope.** Ø100 × 40 → **Ø121.8 (Ø138 at the ears) × 53 mm** (plus a Ø100.8 skirt over the motor). The materials "housing OD ≈ 106" missed the Ø115 big-planet sweep. Log in DECISIONS.md.
2. **Output bearing 6806** (the 6808 option is ruled out by the pin-hole wall).
3. **Stage 1 spur, stage 2 herringbone ψ 20°**, instead of herringbone on both. The planets float axially.
4. **Ring addendum 0.9 m** (internal-gear tip relief). Stage-2 contact ratio is 1.79.
5. **Output interface:** a hex drive plus 3 × M4 steel inserts, instead of a bolt-only circle.
6. **Hip gearbox mass ≈ 413–435 g/side** (BOM 271), and **Al plate 80 g/side** (layout 32 g). Mass budget +≈ 0.39 kg per robot if no recovery is applied.
7. The carrier posts belong to the inboard carrier (printability). The homing stop is on the output, inside the cover.
