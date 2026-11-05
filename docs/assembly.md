# Full robot assembly (both sides, nominal stance, hip 195 mm) - rev 1 (rev 0 report kept below as section R0)

# REV 1 (2026-11-05): rebuilt with the rev 2 parts (DECISIONS A1-A11)

Inputs: `body.step` (rev 2), `hip_gearbox.step` (rev 3.1), `wheel.step`, `leg_*.step` (rev 2, world coordinates, left), LD19 vendor STEP. All built, checked and photographed headless with `solidcraft-cli` (no shared-app clearance runs).

## R1.1 Files
| What | Path |
|---|---|
| Assembly design / STEP | `cad/assembly/robot_assembly.solidcraft`, `exports/step/robot_assembly.step` (191 bodies, both sides) |
| Builder | `cad/assembly/src/gen_assembly.py OUT.json IN_DIR` (IN_DIR = folder with copies of the part STEPs + `ld19.stp`), then `solidcraft-cli run OUT.json --save ... --out ...` |
| Pose / clearance runner (hip 140/195/289) | `gen_pose_checks.py H OUT.json all IN_DIR` (leg STEPs are now world coordinates: no handed-swap workaround; right leg = `solid.mirror` XZ) |
| Homing tab vs cover stops | `gen_tab_check.py THIGH_DEG OUT.json IN_DIR` (carrier rotated through the insert matrix of a 2nd gearbox copy; `solid.move` on a STEP component body rotates about the wrong frame, so the pose script's CarrierOut moves at 140/289 are NOT valid and were ignored) |
| Hex sleeve fit, electronics vs hip stack | `gen_hex_check.py`, `gen_elec_check.py` |
| Raw results | `cad/assembly/src/checks/rev1_*.json` (rev 0 results moved to `checks/rev0/`) |
| CoM | `com_assembly.py` (= `docs/analysis/calc/com_assembly.py`, output `com_assembly_output.txt`), per-body dump `bodies_nominal.json` |
| Screenshots | `docs/screenshots/assembly_iso/front/side/top/transparent.png` (side = along Y, robot front to the right; front = along X) |
Rule as in rev 0: PASS = gap >= 1.0 mm (moving) / >= 0.5 mm (static) or an intended mounting contact. Exact boolean interference on the real faces; gear bodies/bearings inside the housings, and the gearbox ring/planets, are left out of the pose runs. Not decidable by the kernel ("unchecked"): thigh vs carrier hub (pin in hole), spring cylinder vs thigh/crank pin (coaxial by construction), thigh vs shank at 289 (pin in hole) - see M16.

## R1.2 Overall size, CoM (nominal, hip 195)
| | rev 1 | rev 0 | note |
|---|---|---|---|
| Height | **403.0 mm** (LD19 top) | 403.0 | req. 500 PASS |
| Width | **302.0 mm** (tyre faces +-151) | 302.0 | soft limit 300, +2 |
| Depth | **308.9 mm** (x -125.0 rear cover to +183.9 shank/plate) | 303.4 | soft; +5.5 vs rev 0: the leg refit puts the foot 5.5 mm further forward |
| Mass | **6871 g solid / 6258 g sliced** (legs 1897, gearboxes 1720, wheels 1259, body+electronics 1463, lumps 532) | 6962 / 6325 | gearboxes -98 g (arch, bearing 2 gone) |
| CoM x vs axle (axle x 17.43) | **+1.6 mm solid / +0.4 mm sliced** (world x 19.0 / 17.8) | +22.2 / +21.1 | target +-5: **PASS** (leg doc says +2.0 / +0.9; lumps and real bodies differ by 0.4) |
| CoM y / height above axle | -0.01 / 143.0 mm | | lateral PASS |
| IMU (14x14x3 at x 8, z 199.2-202.2, centre z 200.7) | **29.4 mm from the CoM** (dx -11.0, dz -27.3): PASS (<= 30, 0.6 mm margin) | 32.2 | |
| IMU to 8308 motors | **33.2 mm** (surface) - rule >= 40: **FAIL** | 43.5 | see C2 |

## R1.3 Pass / fail per mismatch (left side; right = mirror)
Hip 140 / 195 / 289 unless stated. Numbers are minimum distances in mm.
| # | Result | Evidence |
|---|---|---|
| M1 outer hip support | **PASS** | bearing 2 / HG_Arch gone; thigh stub in the leg's 6806 = contact 0.0 (fit); thigh vs carrier hub could not be intersected (pin in hole) but the hex is checked in M3 |
| M2 crank / spring / arch band | **PASS** | spring (cyl. D13, axis y 111) vs arch plate 2.0, vs box beam 1.9-2.3, vs outer 6806 2.0 (140) / 5.2 (195) / >8, vs B pin 2.8 / 6.6 / >8; crank pin vs arch plate 2.5-2.6; no overlap at any height |
| M3 hex sleeve vs output hex | **FAIL** | sleeve vs HG_CarrierOut overlap **36.7 mm3** at nominal (rev 0: 52.9). Rotating the sleeve about the hip axis: overlap 0 only for -4.5 deg .. -7 deg (best -5.8: gap 0.12), +0.5 deg 41 mm3, -3 deg 9.7. The gearbox hex is at -29.99 deg (= the old homing angle), the leg's pocket vertex is at -24.26: **5.74 deg apart** (the tab was re-set, the hex was not) |
| M4 thigh vs cover | **PASS** | 1.0 (rule 1.0), all heights |
| M5 posts vs body | **PASS** | posts vs side plate 1.0, lid 1.5, hip driver plate 1.34, XDrive 1.98, hip seat ring 4.0, skirt/cover 5.4; no overlap |
| M6 cover/skirt ear vs TPU seat arm | **PASS (cover); skirt undecided** | side plate vs HG_Cover 1.0 at (91, 84, 301) = the ear/relief, no overlap; side plate vs skirt: the boolean fails (as in rev 0), the skirt has the same ear. Side plate vs hip Al plate contact 0.0 (bolted) |
| M7 spring anchor / tie | **PASS (geometry)** | dowel gone; B1T_Tie shelf vs box-beam foot: contact 0.0, no overlap (4 x Ø4.5 pattern not checked here); load path still Structural's |
| M8 axle vs body notch | **PASS** | at 140: axle vs tray 2.0, vs side plate 3.1 (rev 0: overlap 119/136 mm3); hub vs shank/body clear |
| M9 axle position | **PASS** | axle 10.6 mm behind the hip at 195 (rev 0 37.1); CoM +1.6 |
| M10 hub vs shank | **PASS** | 1.5 (>= 1.0) |
| M11 coupler vs arch plate / strap | **PASS** | 1.0 / 1.0 (rule 1.0, no margin) |
| M12 spring vs arch plate / beam / bearing | **PASS** | 2.0 / 1.9-2.3 / 2.0 (rev 0: 1.0 / 1.6 / 1.8) |
| M13 electronics vs hip stack | **FAIL (2 small)** | resistors vs skirt 5.3, bracket 5.6, XDrive boards, Pi deck, battery, ESP, fan, hip driver plates: clear (no overlap, no pair < 6 except below). **Pi 4 top (x -21.8..0, y +-(8.5..11.5), z 228-230.5) overlaps the hip Al plates: 150 mm3 each side, and the skirt 5.9 mm3 each side.** Camera box vs skirt ear: 1.0 / 0.3 mm3 at x 85.0-85.4 |
| M14 LD19 | **PASS (open: hole pattern)** | D54 x 35, z 368-403, nothing else above z 368 (box-beam top 367.5); mast plate hole pattern still unmeasured |
| M15 leg frame | **PASS** | the 10 leg STEPs import in world coordinates; right leg is a true mirror; CoM y = -0.01 |
| M16 thigh vs C pad at 289 | **MARGINAL, undecided** | thigh vs shank could not be intersected at 289 (pin in hole). Thigh striker lug (y 112) to the C pin: 5.86 mm = 0.2 mm to the pad R10.5 if the pad reaches y 112; leg doc says 4.2 mm. Leg to confirm with `build_leg.py --check` including the lug |
| M17 stop pad | **PASS** | thigh touches the TPU pad at 140 (0.2 mm3 contact, 7.0 from the spring), no contact at 195/289 |

## R1.4 Gearbox homing tab vs cover stop blocks (carrier rotated to the thigh angle)
| Thigh angle (deg) | Tab/carrier vs cover/ring |
|---|---|
| +15 / +20 | overlap 141 / 303 mm3 with HG_Cover (crouch stop) |
| +10 | contact (0.15 mm): **crouch stop at about +10 deg** |
| +5 .. -55 | clear except rotating gap 0.5 to cover/ring (nominal -24.26: 0.5 / 0.5) |
| -0.29 (h140) / -10 | 6.8 / 12.4 mm3 graze with the cover at (x -17, y 81.3, z 291) = cover ear at world 165 deg (about 1.3 mm of the ear above the 0.5 mm gap) |
| -60 / -65 / -70 / **-77.09 (h289)** | 5.9 / 18 / 143 / **322 mm3** (extension stop at about **-59.5 deg**) |
**Result: crouch end PASS (stop 10 deg beyond h140, so the TPU pad is the real stop). Extension end FAIL: the cover stop block blocks the carrier 17.6 deg before the thigh reaches -77.09 (h289), i.e. hip height about 263 mm max, not 289.** The tab was moved for the new nominal but the stop blocks stayed at the rev 1 world angles, and the free range is 69.6 deg, less than the 76.8 deg swing.

## R1.5 Remaining clashes (owner, exact fix)
| # | Clash | Owner | Fix |
|---|---|---|---|
| C1 | Extension stop block blocks the carrier at thigh -59.5 deg; need free to -77.09 | **Gearbox** | Move the extension stop block on the cover/ring by >= 20 deg toward extension (contact from -59.5 to <= -80 deg thigh, i.e. block edge rotated 20.5 deg about the hip axis in the direction the thigh turns for -h), keep crouch stop at about +10. Ear at 165 deg: trim the graze (6.8-12.4 mm3 at x -17, y 81.3, z 291) by 0.5 mm |
| C2 | Hex sleeve overlap 36.7 mm3: pocket/sleeve index is 5.74 deg off the gearbox hex | **Leg** (or Gearbox) | Rotate the thigh hex pocket + HexSleeve by -5.8 deg about the hip axis (vertex at -30.0 deg instead of -24.26, hex repeats 60). Alternative: rotate the output hex +5.8 deg in the carrier (and the tab with it) |
| C3 | IMU 33.2 mm from the motors (rule >= 40) and 29.4 from the CoM (rule <= 30) are **not both satisfiable**: a point <= 30 mm from the CoM (19.0, 228) is at most 36.8 mm from the motor surface | **Manager / Electrical** | Decide: the ICM-42688 has no magnetometer, so relax the motor distance to >= 30 mm (current 33.2). Otherwise add a magnetic screen |
| C4 | Pi 4 top corner hits the hip Al plates (150 mm3 each) and skirts (5.9) | **Body** | Notch the hip Al plate lower corner by 25 x 4 mm (x <= 0, z <= 231.5), or move the Pi deck 3 mm down (not possible: ESP) - notch preferred; or Pi/heatsink 3 mm aft |
| C5 | Camera box vs skirt ear (1.0 / 0.3 mm3) | **Body** | Camera x 86.5-98.3 (+1.5 mm) or ear relief 1 mm |
| C6 | Thigh striker lug vs C pad at 289 (about 0.2 mm, undecided) | **Leg** | Confirm; if confirmed trim the lug 2 mm or C pad R10.5 -> R9.5 |
| C8 | **Front cover B4_Front (lip x 73.8-85) overlaps the hip skirt 592 mm3 and the hip Al plate 198 mm3** (x 77.8-85, y 8.5-20, z 264-315; each side). Not seen in rev 0 (cover not in the list). Lid vs skirt 0.4 mm (below 0.5 static) | **Body** | Widen the hip notch of B4_Front: cut x 73.8-85, y 8-22 (and mirror), z 262-317 (left/right); lid notch +0.5 mm |
| C7 | Depth 308.9 mm (+8.9 over 300, soft) | Manager | Accept (client: size is soft) |
Open from earlier and not re-checkable here: tie shelf strength (Structural), bolt-hole alignment of the shelf and the box-beam foot, XDrive Mini/camera real heights.

# R0. Rev 0 report (historical; numbers below are rev 0 and superseded by REV 1 where they disagree)

Owner: Assembly Engineer · 2026-11-05 · inputs: the finished part STEPs (body, hip gearbox **6:1 rev 2**, wheel, 10 leg files), cad/vendor LD19 STEP, docs/parts/*.md, layout.md, DECISIONS.md.

## 1. Files
| What | Path |
|---|---|
| Assembly design (195 bodies, both sides) | `cad/assembly/robot_assembly.solidcraft` |
| STEP of the whole assembly (128 MB) | `exports/step/robot_assembly.step` |
| Builder (headless, rebuilds the design from the part STEPs) | `cad/assembly/src/gen_assembly.py` (`python3 gen_assembly.py out.json; solidcraft-cli run out.json --save ...`) |
| Pose + clearance runner (hip 140/195/289, left side) | `cad/assembly/src/gen_pose_checks.py` |
| Raw clearance / interference results (JSON) | `cad/assembly/src/checks/*.json` |
| CoM from the real bodies | `cad/assembly/src/com_assembly.py` = `docs/analysis/calc/com_assembly.py`, output `docs/analysis/calc/com_assembly_output.txt` |
| Per-body volume / centroid / bbox dump | `cad/assembly/src/bodies_nominal.json` |
| Screenshots | `docs/screenshots/assembly_iso.png`, `_front.png`, `_side.png`, `_top.png`, `_transparent.png` |

Screenshot note: the SolidCraft view names are used as the CLI renders them. `assembly_side.png` is the view along Y (robot front to the right), `assembly_front.png` is the view along X.
The design was built and the screenshots/checks were made with `solidcraft-cli` (own process), because a first `inspect.clearance` over all gear bodies in the shared app ran for more than 90 minutes and blocked it. **The app was still busy with that call when this report was written; open `robot_assembly.solidcraft` in the app when it is free.**

## 2. How the parts were placed (frame: X forward, Y left, Z up, ground z = 0)
| Part | Source frame | Placement |
|---|---|---|
| Body (both sides, bought envelopes inside) | world | as is. Its REF_HipHousing / REF_HipRing / REF_Lidar envelopes were removed (the real gearbox and the LD19 STEP replace them) |
| Hip gearbox (6:1 file) | Z = axis, world = (28 + x, 40 + z, 280 - y) | matrix, left; right = mirror about XZ. Arch matches hip_gearbox.md exactly (X 1.6-51.5, Z 256.5-351.6, y 82.5-116) |
| Wheel module | Z = axle, world = (x, 80 + u, 85 - y) | matrix, **axle at x = -9.09** (see M9), outer tyre face y 151; right = mirror |
| Leg (10 STEP files) | X = world x - 28, Y = world z - 280, Z = world y. **This is a handed swap (Y <-> Z), not a rotation** | reflected about the plane Y = Z, then moved by (28, 0, 280); right = mirror about XZ. Check: thigh knee boss at (129.3, 213.8), B pin (74, 310), thigh plane y 93-103: all agree with leg.md |
| LD19 lidar | official STEP, Y up, base plate at y = -10.2 | turned 90 deg, base at z 368 (mast top), centre x -40 |
| New envelopes | | IMU 14x14x3 on the ESP32 PCB (z 195.2-198.2); Pi camera 3 25x24x11.5 (x 73.5-85, assumed in the cover pocket); 4 XDrive boards 63x58x18 on the inner face of the 4 Al plates |
| Not modelled (masses are lumped in the CoM) | | PDB, 5 V buck, E-stop, anti-spark switch, fuse, harness, cables, fasteners |

## 3. Overall size at nominal stance
| | mm | note |
|---|---|---|
| Height | **403.0** | LD19 top (z 368 + 35). Layout had 398.5 with a 33.5 mm lidar. Requirement 500: PASS |
| Width | **302.0** | tyre outer faces y = +-151 (track as built). Requirement 300: **+2 mm, soft** |
| Depth | **303.4** | x -125.0 (rear cover) to +178.4 (leg shank/strap at the C pin). Requirement "around 300": **+3.4 mm, soft** |

## 4. Interference check
Method: `inspect.clearance` / `inspect.interference` (exact faces, boolean overlap volume) on the real bodies. Left side checked, the right side is the mirror image (the body is symmetric; the only body-shared items, the Pi, driver boards and resistors, are checked against both gearboxes). Poses: the body stays fixed; thigh, shank + wheel and coupler are moved as rigid links with the 4-bar kinematics of `build_leg.py` (hip 140 / 195 / 289; 101 mm is no longer allowed, minimum hip is 140). Gear bodies, bushings and bearings are left out of the pose runs (they take hours to measure and sit inside the housings); the Al plate, skirt, cover, arch, 8308 motor and output carrier are in. The housing ring (internal teeth) was not included: its outside equals the cover/skirt ear envelope.
Rule used: **PASS** = gap >= 1.0 mm (moving pair) or >= 0.5 mm (static pair) or an intended mounting contact; **MARGINAL** = 0.5-1.0 mm moving gap; **FAIL** = overlap or < 0.5 mm moving gap.
"min" is the smallest distance between the two bodies in mm; a negative sign is not given by the tool, an overlap is reported with its volume.

### 4.1 Wheel
| Pair | hip 140 | hip 195 | hip 289 | Result |
|---|---|---|---|---|
| Tyre vs housing cover (R 52, y to 93) | 34.7 | 70.2 | > 80 | **PASS** |
| Hub vs housing cover | 36.1 | > 80 | > 80 | PASS |
| Tyre vs gearbox arch (HG_Arch) / leg arch plate | 36.7 / 34.9 | > 80 | > 80 | PASS |
| Tyre vs bearing 2 / carrier out | 40.3 / 41.2 | > 80 | > 80 | PASS |
| Hub vs body side plate / tray | 17.5 / 19.9 | 32.7 / 34.0 | > 80 | PASS |
| **Wheel axle neck + flange vs body side plate / tray** | **overlap 119 / 136 mm3** | 37.0 / 37.2 | > 80 | **FAIL at 140** (see M8) |
| Wheel axle vs wheel driver plate | 22.0 | 57.9 | > 80 | PASS |
| Hub vs shank (rotating, y 80.5 vs 80.0) | 0.5 | 0.5 | 0.5 | **MARGINAL** (M10) |
| Axle vs shank foot / Al plate | contact (flange on the plate), no overlap | same | same | PASS: hole Ø38.2 and axle neck Ø38 are co-axial |
The leg.md concern "wheel hits the housing below 137 mm" does not occur in the real assembly: the hub is hollow and the housing is 35 mm from the tyre at 140. What stops the wheel at 140 is the **body**, not the housing.

### 4.2 Leg vs body, bulge and housing (left)
| Pair | 140 | 195 | 289 | Result |
|---|---|---|---|---|
| Thigh vs body side plate / Ø140 bulge | 1.0 | > 8 | > 8 | MARGINAL-PASS at 140 |
| Shank Al plate vs side plate / tray / front | 5.0 / 7.4 / 7.4 | 5.0 / 7.4 / 7.4 | 5.0 / 7.4 / - | PASS |
| Thigh TPU bumper vs side plate | 4.5 | 6.8 | > 8 | PASS |
| Hip seat ring vs arch posts | 4.0 | 4.0 | 4.0 | PASS |
| Arch posts vs housing skirt / cover | 5.4 | 5.4 | 5.4 | PASS |
| **Arch posts (Ø16, y 40-117.5) vs body side plate** | overlap 271 / 366 mm3 (posts 142 / 162 deg) | same | same | **FAIL** (M5) |
| **Post 142 deg vs lid / post 162 deg vs hip driver plate** | overlap 48 / 70 mm3 | same | same | **FAIL** (M5) |
| Beam vs side plate top (z 359.2 vs 359) | overlap 7.6 mm3 | same | same | PASS (0.2 mm touch; lap to arch plate 129 mm3 is a bolted joint) |
| Body anchor pin vs leg anchor pin / beam | 5.0 / 4.8 | 5.0 / 4.8 | - | see M7 |

### 4.3 Hip posts vs skirt ears, ring and seat
| Pair | Result |
|---|---|
| Body posts (r 62.2 at 45/135/225/315 deg) vs ears at 15/75/105/165/195 deg of skirt/cover | **No post-to-cover-ear contact within 12 mm** (skirt ears: boolean failed, see below). The rotated ear angles fix the old OQ-1 collision for the cover |
| **Cover ear at 15 deg vs body (end-stop / TPU seat arm), x 90-95, y 79.5-82.5, z 291-302** | **FAIL: overlap 39.7 mm3** (M6) |
| Skirt vs body side plate | not decided: the exact boolean fails ("no result"); the cover result above and the 5.5 mm hip-seat gap suggest the same 15 deg ear |
| Hip seat ring vs skirt / cover | 5.5 / 11.5 PASS |
| Body side plate vs hip Al plate | contact 0.0 (bolted, by design) |
| Body side plate vs 8308 motor | 11.7 PASS |

### 4.4 Spring, B pin, arch, thigh, coupler (hip 140 / 195 / 289)
| Pair | 140 | 195 | 289 | Result |
|---|---|---|---|---|
| Spring (Ø13 envelope) vs B pin Ø10 | 7.5 | > 8 (9.6 by leg.md) | > 8 | PASS |
| **Spring vs gearbox arch bar / ring (HG_Arch)** | not decided (boolean fails) | **overlap 2082 mm3 (cylinder) / 2510 mm3 (the leg's own 13x13 envelope, also confirmed in the shared app)** | **overlap 622 mm3** | **FAIL** (M1/M2) |
| **Spring vs bearing 2 (B_6806_2)** | **overlap 239 mm3** | 5.0 | > 8 | **FAIL at 140** (M2) |
| **Crank pin Ø5 vs HG_Arch** (same y band 104-116) | - | 4-6 | **overlap 236 mm3** | **FAIL at 289** (M2) |
| Spring vs anchor pin of the body | 4.5 | 4.5 | 4.5 | PASS |
| Spring vs leg arch plate / beam / outer bearing | 1.0 / 1.9 / 1.8 | 1.0 / 1.7 / 7.2 | 1.0 / 1.6 / - | MARGINAL (M12) |
| Leg arch plate vs HG_Arch (parallel faces y 124.5 vs 116 .. 117.5) | 1.5 | 1.5 | 1.5 | PASS |
| Thigh vs leg arch plate | 1.5 | 1.5 | 1.5 | PASS |
| **Thigh stub (Ø30/Ø24, y 103-124.5) vs bearing 2 and the carrier journal** | overlap 2346 mm3 | overlap 2346 mm3 | overlap 2346 mm3 | **FAIL** (M1) |
| **Thigh inboard face vs housing cover (rotating)** | 0.0 | 0.0 | 0.0 | **FAIL** (M4) |
| **Hex sleeve vs output hex (26 A/F)** | - | overlap 52.9 mm3 | - | **FAIL** (M3) |
| Coupler vs leg arch plate / knee strap (rotating) | 0.5 / 0.5 | 0.5 / 0.5 | 0.5 / 0.5 | **MARGINAL** (M11) |
| Coupler vs shank / K pin / B pin (bushings) | 2.0 | 2.0 | 2.0 | PASS |
| Thigh vs TPU stop pad | 3.1 | - | - | PASS (stop engages at 130 mm: the pad closes 3 mm earlier than designed) |
| **Thigh vs shank C-pad at full extension** | - | contact 0.0 | **overlap 1982 mm3** | **FAIL (to confirm by the leg owner; pose model, no bushings)** |
Hex-sleeve overlaps shown by the pose script at 140/289 are an artefact (the sleeve was not rotated with the thigh) and are not counted.

### 4.5 Electronics vs the hip stack and body
| Pair | Result |
|---|---|
| **Resistors HS25 (x -51..0, y 1-29, z 259-274) vs 8308 motor Ø92** | **overlap 4131 mm3 each**; vs hip Al plate 1076, skirt 1319, bracket vs motor 475 | **FAIL** (M13) |
| **Pi 4 (+ heatsink 28 mm) vs hip skirt / Al plate** | **overlap 1017 / 609 mm3**; vs the 225 deg hip post 115 mm3; Pi vs 8308 motor 1.7 mm | **FAIL** (M13) |
| **Pi camera envelope vs hip Al plate / skirt** | overlap 468 / 194 mm3 (cover pocket assumed at x 73.5-85) | **FAIL** (M13) |
| IMU (14x14x3) vs Pi deck / ESP32 PCB | 0.2 mm overlap / contact; IMU to 8308 motor 43.5 mm (cylinder), to the Pi 8.3 | IMU-motor PASS (>= 40), IMU vs deck marginal |
| XDrive boards (keep-out 18 mm, assumed) vs tray / Pi deck | overlap 160 / 35 mm3 | FAIL pending the real board height (M13) |
| Hip driver plate vs skirt / resistor vs other hip / mast vs plate | 11.3 / 12.5 / 10.7 | PASS |
| Battery vs tray / cradle / rear cover | 0.85 / 1.5 / 1.8 | PASS (foam) |
| Fan vs front cover | contact (duct) | PASS |

### 4.6 Cables and lidar
- **Cables (not modelled as bodies).** Wheel leads leave the body through the slot at (x 20, z 190) in the side plate and follow the shank (inboard Al plate face y 68-71, phase channel y 76-80), both at y < 93, i.e. inboard of the thigh plane (y 93-103) and the crank/spring/coupler (y 103-139): **no Y overlap**. The slot is 7 / 25 / 57 / 42 mm from the shank centre line at hip 101 / 140 / 195 / 289, so the cable needs a service loop of about 40 mm length on the body side. Closest approach to the thigh line is 24 mm at 289 but in another Y plane. **PASS (conditional on the loop; not measured on a bundle model).**
- **Lidar view.** LD19 z 368-403 (scan window inside this band). Highest other body: leg outrigger beam z 365.0, arch plate 361.2, side plates 359.2, mast 340-368. **Nothing is above z 368 except the lidar: the 360 deg view is free. PASS.** Mast flange is 32 mm wide against a Ø54 lidar base (M14).

## 5. Centre of mass (real bodies, nominal pose)
Method: SolidCraft volume centroid of each of the 195 bodies x density (PAHT-CF 1.2, PETG 1.27, TPU 1.21, Al 2.7, steel 7.85, bronze 8.8), bought envelopes at their real masses (battery 340 g, Pi 56, 8308 360.5, MN5008 128, bearings 19/1.9 g...), plus lumped items at layout positions (532 g). Script `com_assembly.py`.

| Basis | Mass | CoM x (world) | **vs axle (x = -9.09)** | y | Height above axle |
|---|---|---|---|---|---|
| Solid CAD | 6962 g | 13.2 | **+22.2 mm forward** | -0.01 | 141.0 |
| Sliced estimate (printed parts x 0.75) | 6325 g | 12.0 | **+21.1 mm forward** | -0.02 | 142.4 |
| Target | | | over the axle +-5 | <= 5 | |
**Fore-aft: FAIL (+22 mm). Lateral: PASS (0.0).** Moment of each group about the axle (kg.mm): both legs +139 (1880 g at x +64.8, i.e. 74 mm ahead of the axle), both hip gearboxes +66 (1818 g at x 27.4), body + electronics -46 (1473 g at x -40.6), lumps -4, wheels 0. Total +155 kg.mm.

Shift needed:
| Option | Size | Verdict |
|---|---|---|
| Battery rail | the rail only moves the pack forward (0 .. +20 mm = +1 mm of CoM, wrong way); an aft move of 456 mm would be needed | **cannot fix** |
| Move all body + electronics + lumps (2005 g) aft | 77 mm | not possible (body is 250 mm long) |
| Ballast at the rear wall (x -122) | 1.37 kg | rejected |
| **Move the hips (everything above the legs) 27 mm aft relative to the wheel axle, i.e. re-fit the 4-bar so that the hip is 10-15 mm (not 37 mm) ahead of the axle at nominal** | 27 mm of upper structure (5.7 kg) | **recommended: Leg + Theory (change B pin / thigh angle at nominal, the leg doc already moved the nominal thigh from -30 to -33.2 deg, which moved the axle 9 mm aft relative to the hip)** |
| Control trim | the controller holds the body pitched back by atan(22/141) = 8.9 deg so that the CoM is over the axle | works today, costs the lidar/camera attitude and the IMU offset; acceptable as an interim fix |
| Lighter / aft-placed legs | the legs carry 139 of the 155 kg.mm: ~ -1.3 kg of the front structure (outrigger beam, posts, arch plate 135 g each) moved or removed would give -10 mm | partial |
The old layout (+2.1 mm over the axle at 4.37 kg) no longer holds: legs 1.88 kg instead of 0.25 kg and a hip 37 mm ahead of the axle (layout assumed 28 with the axle under it).
At hip 140 / 289 the hip is 32.9 / 60.7 mm ahead of the axle (4.2 mm less / 23.6 mm more than nominal), so the CoM (upper structure about 80 % of the mass) moves about -3 / +19 mm relative to the axle (scaled estimate, not re-run with the legs posed).
IMU: at (0, 0, 196.7) it is 32.2 mm (dx 13.2, dz 29.3) from the CoM: **just outside the +-30 mm rule** (FAIL by 2 mm; it improves as the CoM moves aft).

Mass check: 6.96 kg solid / 6.33 kg sliced against 6.86 / 6.41 in mass_actual.md (agrees within 1.5 %). Groups: legs 1880 g, hip gearboxes 1818 g (484 g/side printed + motor + Al plate), wheels 1260 g, body + electronics 1473 g, lumps 532 g.

## 6. Mismatches between parts (each with fix and owner)
| # | Mismatch | Evidence | Proposed fix | Owner |
|---|---|---|---|---|
| M1 | **Two outboard hip supports on the same shaft.** Gearbox rev 1: carrier journal + 6806 #2 (y 105-112) + HG_Arch (y 104-116). Leg: hollow thigh stub Ø30/24 to y 124.5 + its own 6806 + 7 mm arch plate (y 117.5-124.5). The thigh stub goes through bearing 2 and the carrier journal; 3 bearing planes (87.5, 108.5, 121) | overlap thigh vs B_6806_2 2346 mm3 | **Pick one.** Preferred: keep the leg's outer bearing (33 mm spacing, better than 21): gearbox deletes B_6806_2, the Ø30 journal extension and the HG_Arch bar/ring and keeps only the hex + clamp insert; the leg arch plate stays on the posts. (Structural to re-check SF, both options need it.) | Manager decides; Gearbox + Leg |
| M2 | **Crank, spring and arch bar are in the same y band 104-116** (spring axis y 110, band 103.5-116.5). The spring crosses the arch bar/ring and bearing 2 at low hip heights; the crank pin hits the bar at 289 (the gearbox doc checked only the thigh sweep, not the crank at +180 deg) | spring vs HG_Arch 2082 mm3 (195), 622 (289); vs bearing 2 239 (140); crank pin vs arch 236 (289) | Resolved by M1 (no arch, no bearing 2). If the gearbox arch stays: move crank + spring outboard to y >= 118 (crank y 118-130, spring axis y 124, coupler to y 140-154, knee strap +14) | Leg (+ Gearbox) |
| M3 | **Hex socket vs output hex**: 26 A/F steel sleeve inner on a 26 A/F output (zero clearance), and the leg's hex is rotated by the nominal thigh angle -33.19 deg while the gearbox homing tab is set for -29.99 (3.19 deg). Corner overlap | HexSleeve vs HG_CarrierOut 52.9 mm3 at nominal | Sleeve inner 26.3 A/F (or output 25.8), and rotate the thigh hex pocket by +3.19 deg or move the homing tab/stop blocks to -33.19 deg (one of the two; hex repeats every 60 deg, so no other effect) | Leg + Gearbox |
| M4 | Thigh inboard face (y 93.0) touches the cover boss face (y 93.0): rotating parts at 0 gap | clearance 0.0 | Thigh plane y 94.0-104.0 (+1 mm, stub and crank follow), or trim the cover boss to y 92 | Leg (or Gearbox) |
| M5 | **Arch posts Ø16 (r 82, 142 and 162 deg, y 40-117.5) cut through the body**: side plate (271 / 366 mm3), lid (48), hip driver plate corner (70). body.md reserved nothing for them | overlaps | Body: 2 holes Ø18 (+ 2 mm) with reinforced seats in the side plate pad ring, notch the lid at 142 deg, chamfer the 70x70 hip driver plate corner by 12 mm (or move the posts to 120/165 deg after M1) | Body (+ Leg for post angles) |
| M6 | Cover/skirt ear at world 15 deg (x 94.8) hits the body end-stop/TPU seat arm (x 90-95, y 79.5-82.5, z 291-302) | 39.7 mm3 | Move the TPU seat arm 5 mm forward or notch it for the ear; or rotate the ear set 5 deg (gearbox) | Body (preferred) |
| M7 | **Spring anchor exists twice and does not connect.** Body Ø6 dowel at (122, 351) y 63-99 (keep-out y > 99) vs the leg's Ø5 anchor pin at the same x,z but y 104-117.5, carried by the leg arch plate; the beam is 5.3 mm below the pin. The 180 N spring load goes into the leg arch plate and posts, not the body | gaps 5.0 / 4.8 / 5.3 | Delete the body dowel and boss, or extend it to y 117.5 and let the beam end on it; Structural to decide which path takes the 180 N | Body + Leg |
| M8 | **Minimum hip height vs wheel axle.** The axle neck Ø38 (y 56-71) and flange Ø56 (y 64-68) enter the body bottom (z 148-150) below hip ~149 mm. At 140 they overlap the side plate and tray | overlaps 119 / 136 mm3 | (a) raise the minimum / end stop to 150 (the 140 mm choice was for the 20 cm jump), or (b) notch the side plates and tray edges (R30 around the axle path, Y 56-64), or (c) shorten the neck inboard of y 64 by 8 mm (needs the encoder seat moved) | Manager; Body for (b); Wheel for (c) |
| M9 | **Axle position relative to the hip.** The leg 4-bar (thigh nominal -33.19 deg, B moved) puts the axle 37.09 mm behind the hip at 195, not 28 mm as layout, wheel frame and CoM script assumed. In the assembly the wheel is at x = -9.09 | W_x from build_leg.py | CoM consequences in section 5. Re-fit the nominal pose (see section 5) | Leg + Theory |
| M10 | Rotating hub starts at y 80.5, 0.5 mm from the stationary shank (y 80.0) | 0.5 | Shank face to y 79 or hub to y 81.5; a thrust washer | Leg or Wheel |
| M11 | Coupler (y 125-139) is 0.5 mm from the arch plate (124.5) and the knee strap (139.5) while rotating | 0.5 / 0.5 | Spacer washers +0.5 per side, or re-space the Y stack by 1 mm | Leg |
| M12 | Spring envelope is 1.0 mm from the arch plate, 1.6 mm from the beam, 1.8 mm from the outer bearing | 1.0-1.8 | Spring axis y 110 -> 109.5 and arch plate 118.5, or a spring guide tube | Leg |
| M13 | **Body electronics vs the hip stack** (the body layout did not include the Ø92 motor, the Ø122 housing or the Al plates): resistors in the motor (4131 mm3 each), Pi vs skirt/plate/post (1017 / 609 / 115), camera vs plate/skirt (468 / 194), driver keep-outs vs tray/deck | overlaps | Resistors + bracket 35 mm aft (x -86..-35; battery stays 3 mm clear); Pi deck 20 mm aft (back to x -42.5, the rail trim only goes forward anyway) and 3 mm lower; camera on the layout position x 85-96.8 (outside the cover) or in a pocket with a notch in the front cover; PiDeck 3 mm up for the IMU; get the XDrive height | Body + Electrical |
| M14 | **LD19 is Ø54 x 35**, not 38.6 x 38.6 x 33.5. The STEP shows a Ø54 body, 35 mm tall; the mast plate is 32 x 32 | STEP bbox 54 x 46 x 35 | Mast plate Ø60 with the real hole pattern; overall height 403 | Body (+ Requirements) |
| M15 | Leg STEP files are in a handed-swapped frame (Y up, Z = world y) and the hex/stop chirality depends on it. Mirrored right legs therefore take the same convention | | Export the leg in world coordinates (left side) in the next rev | Leg |
| M16 | Thigh vs shank C-pad overlap at hip 289 (1982 mm3), pose model without bushings | | Leg owner to confirm with `build_leg.py --check` at 289 and trim the C pad | Leg |
| M17 | End-stop pad contact: the thigh reaches the TPU pad 3.1 mm before the design height (130 mm) at hip 140 | 3.1 | Re-set the pad seat 3 mm outward once M8 fixes the minimum height | Leg |
Not checked / not possible here: shank foot carrier bolt circle (pcd 46, 1.65 mm to the hole, open in leg.md), the interior fit of the planets (a pair already verified by the gearbox owner), bushing/press fits, cable bundles.

## 7. Assumptions
1. Left side = reference, right = exact mirror (body symmetric). Interference was measured on the left side with both-side Pi/driver/resistor checks.
2. Pose runs (140/289) move the thigh, shank (+ wheel) and coupler as rigid planar links with the build_leg.py kinematics; the gearbox output, hex sleeve and spring end are not re-posed (spring is rebuilt as a Ø13 cylinder between the crank pin and the anchor pin; at 195 the leg's own square 13 x 13 envelope is used for the overlap numbers because it is the part as delivered, the cylinder gives smaller overlaps).
3. XDrive board envelope 63 x 58 x 18 (keep-out), camera 25 x 24 x 11.5 at x 73.5-85, IMU 14 x 14 x 3: my placement, no datasheet.
4. Densities: PAHT-CF 1.2, PETG 1.27, TPU 1.21, Al 2.7, steel 7.85, bronze 8.8 g/cm3; solid volumes; sliced = printed parts x 0.75.
5. Resistor mass 10 g each is the BOM value (HS25 datasheet parts are heavier, ~20-30 g; this would move the CoM by < 0.5 mm).
6. Hip gearbox file = the new 6:1 STEP (28 T sun / 40 T planet); planets 2 and 3 are spun by 120 and 60 deg in that file.

## 8. Open questions
1. Which outboard hip support wins (M1)? Everything else on the spring side depends on it.
2. Is the nominal hip 37 mm ahead of the axle acceptable (control pitch 8.9 deg) or does the 4-bar get re-fitted (section 5)?
3. Minimum hip height 140 (jump) vs 149-150 (body clearance) - decision for the Manager (M8).
4. Is 303 x 302 x 403 mm accepted (soft limits, client rule)?
5. XDrive Mini and Pi camera 3 real heights; the Pi heatsink height.
6. The app request that was started on the heavy gear bodies is still running in the shared SolidCraft; it may need a restart of the app.

## 9. Changes to design assumptions (for DECISIONS.md)
1. Wheel axle is 37.09 mm behind the hip at nominal (layout said 28): the assembly frame origin x = 0 is not under the axle (axle at x -9.09).
2. CoM is 22 mm ahead of the axle at 6.96 kg (layout: +2.1 at 4.37 kg).
3. Overall size 303.4 x 302.0 x 403.0 mm (layout 299.8 x 300 x 398.5).
4. Minimum useful hip height is ~149 mm unless the body is notched (wheel neck vs body), not 140.
5. LD19 envelope is Ø54 x 35 (SOURCES.md and body.md used 38.6 x 38.6 x 33.5).
6. The real wheel does not hit the housing at 140 (hollow hub), so the "hip floor raised for the housing" reason in leg.md no longer applies; the reason is now the body bottom.
