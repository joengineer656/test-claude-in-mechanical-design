# Wheel module (one side; the other is the mirror) - CAD rev 1

Owner: Wheel CAD Engineer · 2026-11-05 · Built headless: `python3 cad/parts/src/build_wheel.py WORKDIR` then `cad/parts/src/run_wheel.sh WORKDIR <part>` (SolidCraft CLI, own process; the app/MCP was not used).
Files: `cad/parts/wheel.solidcraft` (assembly, 26 bodies), `exports/step/wheel.step` (assembly), `exports/step/wheel_<part>.step`, `exports/stl/wheel/<part>.stl`, `docs/screenshots/wheel_iso.png`, `wheel_gears_z56.png` (gear section at u 56), `wheel_section.png` (true section y=0 through the axle, viewed from the back; iso has the tyre at 35 % opacity), gear check `docs/analysis/calc/wheel_gear_geometry.py` (+ `_output.txt`).
Frame: Z = axle, u = Z, outboard +; world (left) = (0, 80+u, 85). STL are in this frame (re-centre in the slicer). Every part is symmetric, so the right side uses the same files (or mirror).
Client rule applied (DECISIONS last row): the spec's mass cuts were **skipped** (stronger version kept: 4 mm flange, fins 8 high, no windows, N=32 cells kept only because the tyre is the lightest-risk item) and the track is **not** reduced: overall width is now soft (~301 mm per the O-W1 outer face Y 151).

## Part list
| Part | File | Material | Notes |
|---|---|---|---|
| WH_Axle (hollow fixed axle) | axle | Al 6061-T6, CNC (STEP is the drawing) | flange Ø56x4 (u -16..-12), neck Ø38 (wall 3.4 over the Ø31.2 seat; shank foot hole becomes Ø38.2), shoulder Ø40, journal Ø30 (u 0.5..14.5), Ø14 bore, Ø31.2 seat u -24..-1, 12 fins 1.2x10.7x8 + ring, 4x Ø3.4 motor screw holes on Ø25, 4x Ø4.2 M4 holes on Ø46 |
| WH_RingSleeve | ringsleeve | PAHT-CF | flange Ø60x3, tube OD63/ID59, web (u 48.5..49.5), 60T ring zone OD84 u 49.5..62.5 |
| WH_Sun | sun | PAHT-CF | 24T b12, collar Ø26, recess Ø21 for the motor cap, Ø6.2 bore, 4x M3 screws on Ø18 with 15 mm deep Ø5.8 head pockets from the gear side |
| WH_Planet_1..3 | planets | PAHT-CF | 18T b12, 2x Ø11.1 pockets for 685ZZ, Ø5.05 pin hole. One STL with 3 bodies (print 3, identical) |
| WH_CarrierA | carrierA | PAHT-CF | plate Ø58x4.5 + 3 posts Ø10 on r24 at 60/180/300 deg, pin holes 3.5 deep |
| WH_CarrierB | carrierB | PAHT-CF | plate Ø58x4.5, Ø24 access hole for the sun screws, 4x Ø4 insert holes on Ø40, 3 post screws |
| WH_Hub | hub | PETG | bearing boss, web, drum, 12 spokes, stop flange Ø150, rim ring Ø132/138, 12 castellated tabs, 8 insert bosses |
| WH_Cover (centre disc) | cover | PETG | Ø145 step disc, 12 x Ø16 holes on Ø100 PCD, boss, 8 x M3 on Ø125 |
| WH_Tyre | tyre | TPU 95A | Ø170x25, 12 inner ribs, 32 through-cells, 24 tread grooves, outboard lip |
| WH_MagHolder | bought.stl (body) | Al/PETG small turned/printed part | holds the Ø6x2.5 magnet on the motor shaft |
Reference/bought bodies in `bought.stl`/assembly: MN5008 envelope block Ø55.6x27 + Ø20 cap + Ø6 shaft (T-Motor sizes), 2x 6806-2Z, 6x 685ZZ, 3x Ø5x20 dowel, Ø30x8 encoder board, Ø6x2.5 magnet. No STEP exists for these (SOURCES.md), so envelopes are used.

## Gear stage
24/18/60, m1.25, 20 deg, b 12, ratio 3.500, 3 planets at 120 deg, a = 26.25 (ring fixed, sun input, carrier output). **Spur, not herringbone** (herringbone lofts hang this kernel for the ring; spur is reliable, wheel torque is low). 0.06 mm/flank backlash as the hip. Assembly rule: (zs+zr)/3 = 28, zs/3 and zr/3 integers, so all planets are identical. Phasing: planets tooth at 0 deg, sun gap at 0 deg (tooth at 7.5), ring space at 0 deg. Mesh check: see `wheel_gear_geometry_output.txt` (raster overlap sweep over one planet pitch; result: max overlap planet-sun 0 mm2 and planet-ring 0 mm2 at 0.15 mm raster over 13 carrier angles, so the planets mesh without interference).

## Masses (volumes measured in SolidCraft; density x volume)
| Part | Volume cm3 | Density | Solid g | Est. printed g |
|---|---|---|---|---|
| Axle | 22.13 | 2.70 | 59.8 | 59.8 |
| RingSleeve | 34.62 | 1.30 | 45.0 | 45.0 (100 %) |
| Sun / 3 planets | 8.24 / 10.86 | 1.30 | 10.7 / 14.1 | same |
| CarrierA / B | 11.85 / 9.18 | 1.30 | 15.4 / 11.9 | same |
| Hub (PETG) | 118.5 | 1.27 | 150.6 | ~111 (30 % gyroid, thin walls solid) |
| Cover (PETG) | 35.6 | 1.27 | 45.2 | ~38 |
| Tyre (TPU) | 73.7 | 1.21 | 89.2 | 89 (3 walls, 0 % infill matches the thin CAD walls) |
| Bought (motor 128, 2x6806 38, 685 8, pins 9, screws/inserts ~19, encoder+magnet 8) | | | 210 | 210 |
| **Module total** | | | **~652** | **~606** |
Not included: half shank + cables (39 g). Unsprung target 536 g: over by ~65 g (est.) to ~110 g (solid). Expected, because the cuts were skipped by decision. The printed-mass column uses my own fill assumption: weigh the first print.

## Print orientation and settings (A1, hardened 0.4 nozzle)
- PAHT-CF parts (sun, planets, carriers, ring sleeve): dried 80 C/8 h, gear axis Z, flat on the bed (ring sleeve flange down), 100 % infill / 5 walls, 0.16-0.2 layer, no supports. Print a coupon first (O15).
- Hub: PETG, rim ring up (cover side up), boss down, tree supports under the spokes only; 4 walls, 30 % gyroid, 0.2 layer, 240 C/80 C bed. Cover: PETG flat, 4 walls.
- Tyre: TPU 95A HF, one face down, 3 walls, 0 % infill, 0.2 layer, slow outer wall (25 mm/s). Fits A1 easily.

## Bought parts / hardware
MN5008 KV170, 2x 6806-2Z, 6x 685ZZ, 3x Ø5x20 h6 dowel, Ø6x2.5 NdFeB, AS5047P breakout Ø30, 4x M3x25 DIN 7984 A2 (motor, see below), 4x M4 on the shank, 3x M3 (carrier A-B), 4x M3 (carrier B to cover), 8x M3x10 (cover to hub), 4x M3 sun screws M3x8, M3 heat-set inserts Ø4x5.7 (8 hub, 4 carrier B), 3x pilot screws. Non-magnetic (A2) fasteners within 10 mm of the magnet.

## Tyre tabs: fit and tolerance
12 tabs 4 mm radial (r 68.5..72.9, i.e. Ø145.8 as printed), 12 slots 8.6 wide parallel-sided at 15+30k deg. Tyre: ID Ø145.4 (0.2 radial interference on the tab tops, TPU stretches), 12 inner ribs 8.0 wide x 4.5 radial in the slots (0.3 per side loose, drives the tyre rotationally), rib length 22.5 (tab length), outboard inward lip r 69.6..72.7 captured by the stepped cover (disc Ø145 then Ø139). Inboard side: stop flange Ø150. No glue. Needs a print test (TPU shrinkage; O-W7). Tread: 24 straight grooves 2 wide (chevron not made), cell zone r 74.9..82.8.

## Assumptions and changes to design assumptions
1. Spur gears instead of herringbone (above).
2. **Encoder seat moved**: the spec's Ø31.2 board seat up to u 5 is impossible (journal is OD 30, bore Ø31.2 cuts it away). Now: Ø31.2 seat to u -1 only (neck, wall 1.4 mm), board u -11.5..-3.5 (chip face -3.5), magnet face u -2.0 (gap 1.5), magnet holder u -2..14.5 (Ø12.6 in the Ø14 bore), motor screw heads sit in the Ø31.2 seat on the step (u -1..+2) and the screws run through the journal and the sleeve flange: **M3 x 25** (not x14), engagement ~6.5 mm into the motor base (O14: verify thread depth).
3. Carrier posts Ø10 on r24 (spec Ø12 on r26.25 did not fit the Ø58 plate). Sleeve gets a web u 48.5..49.5 (spec had no link tube-to-ring). Hub rim ring ID Ø132 with insert bosses Ø8 at r62.5 (spec put inserts on the ring itself). Rim and tabs end at u 68.5 and the cover disc fills u 68.5..71 (tyre/cover 25 wide, outer face u 71 as the spec).
4. Neck grown Ø34 to Ø38 (wall 1.4 to 3.4 mm, rev 2 fix); shank foot hole Ø38.2.
5. Spec tab "tangential 18, gap 8.6" does not add up (12 tabs on Ø138 are 27.5 wide with 8.6 gaps): used 8.6 slots.
6. Cable slots in the axle flange and the hub labyrinth lip were not modelled (the bore carries the cables).
7. Mass cuts skipped, track not reduced (client decision). Width is ~301 mm.

## Open questions
- O-WH1 (closed, rev 2): outboard race retained by a DIN 472 Ø42x1.2 circlip in a groove at u 14.5..15.7 in the hub boss (boss now to u 15.8); the ring sleeve flange has a Ø37/Ø53 x 1.9 recess on its inboard face for clearance. Check the hub groove prints cleanly or cut it after printing.
- O-WH2 (closed, rev 2): neck wall now 3.4 mm; Structural to re-check.
- O-WH3: fin area now larger than the spec (8 high), still below Thermal's 200 cm2; re-check allowable current.
- O-WH4: sun screws M3x8 engage 5.5 mm in the rotor (O14); the sun cbore pockets are 15 mm deep (tool access through the Ø24 hole in carrier B).
- O-WH5: hub bearing-seat stiffness in PETG under creep: consider Al insert sleeves; bearing pair is still a touching pair (O-W2).
- Hub/cover masses are estimates until a slicer run.
