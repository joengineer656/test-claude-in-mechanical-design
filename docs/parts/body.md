# Body + electronics bay: detailed CAD (rev 2)

Owner: Chassis CAD Engineer · 2026-11-04 · replaces the spec-only rev 0 (`body_spec.md` stays as the design intent).
Client decision applied: weight and size are soft, so no lightening cuts beyond the vents, thick walls, PAHT-CF where loaded.

## Files
| What | Path |
|---|---|
| Generator (stages 1-4, `python3 build_body.py N out.json`, then `solidcraft-cli run out.json [--in ../body.solidcraft] --save ../body.solidcraft`) | `cad/parts/src/build_body.py` |
| Design (multi-body, both sides, built headless) | `cad/parts/body.solidcraft` |
| STL per printed part | `exports/stl/body/B*.stl` |
| STEP (all bodies incl. bought envelopes) | `exports/step/body.step` |
| Screenshots | `docs/screenshots/body_iso.png` (left/top views render slowly on this machine; regenerate with `solidcraft-cli snapshot --in cad/parts/body.solidcraft --view left`) |
Frame: X forward, Y left, Z up, mm, world coordinates (hip at 28, 280). Left side +Y, right side mirrored by the generator loop.

## Rev 2 (2026-11-05): assembly mismatches M5-M8, M13, M14 (DECISIONS A3, A6, A7; leg numbers from `leg_interfaces_rev2.md`)
Generator: stages 1-4 as before, then `python3 build_body.py 5 s5.json` (tie patch, also re-exports the STEP). Run all from the repo root (export paths are relative). Hand/AABB-level checks only; the boolean interference run against the new leg/gearbox STEPs belongs to the Assembly engineer.
| # | Change |
|---|---|
| M8 | Wheel axle path notched at hip 140: axle world (x 21.4, z 140) per the leg note, R31 cylinder cut through both side plates (y 59-64.5) and the tray walls + floor edge (y 54-62). Tray/plate bolts moved to x -100, -60, -20, 70 (x 0 was in the notch). Parameters `AXX, AXR` at the top of the script; if the Leg owner moves the 140 pose, change `AXX`. |
| M5 | Leg arch posts D16 at r 82, 142 deg = (x -36.6, z 330.5) and 162 deg = (x -50.0, z 305.3), y 40-119.5. Side plate: D18 hole at 162 deg with a D30 collar (y 60-65); at 142 deg the hole is a slot open to the plate top (post top z 338.5 vs plate top 340). Lid: D19 notch at the 142 deg post (y 36-62). Lid/plate middle hook moved x -30 -> -18 (was inside the post). Hip driver plate and the XDrive keep-out lose a 9 x 14 mm corner (x -60..-49, z 296-311) so the 162 deg post clears; **the driver pad at (-55, 305) is deleted: the hip driver plate has 3 screws (Electrical to confirm or add a tab)**. |
| M6 | Ear relief in the TPU seat arm (x 88-96.5, y 78.5-83.5, z 289-304 for the 15 deg ear at x <= 94.8, y 79.5-82.5); the TPU pocket now starts at y 83.5 (8.6 deep instead of 12; the Leg stop pad is seated on the leg arch plate, check pad length). |
| M7 | Anchor outrigger beams, boss and the Ø6 steel dowel (REF_AnchorPin) are deleted. Tie: plate tab (x 58-85, up to z 351) + separate **B1T_Tie** (web y 63-66 x 66-85 z 340-359, shelf y 38-66 x 66-132 z 353-359) under the leg box beam foot plate (world x 85-132, y 38-52, z 359-365), 2 x M4 web-to-tab, 4 x Ø4.5 shelf-to-foot (2 x 2, pitch 27 x 7). Split from the plate because plate + shelf was 257 mm (bed 256). The load path is only a concept: PAHT-CF cantilever shelf (47 mm), Structural to size it for the 180 N anchor load (an Al shelf or a steel L-bracket may be needed). |
| M13 | Resistors + bracket 35 mm aft (REF_Res x -86..-35; bracket 54 x 62 mm, x -86..-32; posts at x -81 / -39, now at y +-28 so they clear the XDrive boards at y >= 32.6). Pi deck 20 mm aft and ~2.5 mm lower (deck x -83..-8, z 195.5-197.5; the 3 mm lower target would touch the ESP PCB; Pi ref x -85..0, z 202.5-230.5, 4 deck posts at y +-28). Battery cradle: cheeks shortened to x -86, front wall lowered to z 193 (under the deck), one strap slot (z 170). Camera moved outside the front cover (REF_Camera3 x 85-96.8); the cover pocket is deleted, the inside pad and 2 x D3.2 screw holes (through the cover) stay. XDrive keep-out refs added (REF_XDrive_*: 63 x 58 x 18, x -116.5..-53.5, y 32.6-50.6, assumed). Rail trim: the pack can no longer move forward (cradle wall is 2 mm from the Pi); the rail trim is lost (forward-only anyway). |
| M14 | LD19 = D54 x 35 (REF_Lidar z 368-403, centre x -40). Mast top plate D60 x 3 (z 365-368); the 4 x D2.7 holes at +-15 are still **unmeasured** (the vendor STEP is an assembly, no hole pattern; check on the real unit; Requirements/Electrical). |
| IMU | REF_IMU 14 x 14 x 3 at x 8 on the ESP32 PCB, which is raised 4 mm (posts +4; ESP z 197.6-199.2, IMU z 199.2-202.2, centre z 200.7). Estimated CoM with the leg rev 2 (axle +26.5 mm forward, CoM about 20 mm world x, z about 226): IMU distance about 28 mm (<= 30, was 32.2). Motor distance about 40 mm (rule >= 40, marginal). **To be re-computed by the Assembly engineer with the rev 2 STEPs; `IMUX` in the script moves it.** |

## Parts, material, mass (CAD volume, 100 % solid)
| Part | Material | Volume cm3 | Solid mass g | Print orientation / settings |
|---|---|---|---|---|
| B1_Side_L / R (rev 2: axle-path notch R31, D18 holes for leg arch posts, collar, tie tab; plate 2.4, hip hole D130, pad ring, D140 bulge shell, 4 hip posts D9 x 49 + lands, 8 driver pads, anchor outrigger + boss, TPU seat arm, hook slots, cable slot) | PAHT-CF (1.2) | 109.0 each | 131 each | Outer face down, posts and bulge grow up; 0.2 mm, 5 walls, 100 % in posts/boss, hardened nozzle, dried |
| B1T_Tie_L / R (rev 2: web + shelf under the leg beam foot plate, 2 x M4 to the plate tab, 4 x Ø4.5 to the beam) | PAHT-CF | 11.4 each | 14 each | Shelf face down |
| B2_Tray (floor 1.6, walls 1.2, rail ribs, channel ribs, bosses, Pi/ESP/resistor posts, spine, skids) | PETG (1.27) | 110.0 | 140 | Floor down, posts upright; 0.2 mm, 3 walls |
| B2b_Cradle (base 2, cheeks 2, slotted M4, strap slots) | PETG | 18.4 | 23 | Base down |
| B7a_PiDeck + 4 M2.5 posts | PETG | 9.4 | 12 | Flat |
| B3_Lid (e-stop, switch, fuse opening, charge opening, mast boss, 6 side hooks, windows for cover hooks) | PETG | 33.7 | 43 | Flat, outside up; hooks lie in the layer plane |
| B4_Front (17-slot inlet grille, fan duct + 4 insert holes, camera pocket + window, hip notches, 4 hooks) | PETG | 38.5 | 49 | Flat, outer face down |
| B5_Rear (15-slot outlet grille, 4 hooks) | PETG | 25.8 | 33 | Flat |
| B6_Mast (D20, flange, LD19 plate now Ø60) | PETG | 12.0 | 15 | Flange down |
| B1S_HipSeat_L / R (Al 6061, 3 mm ring OD140/ID108, 8 x M3) | Al | 24 each (calc) | ~ 2 x 22 (bought/cut) | laser cut |
**Printed total (CAD solid, rev 2) = 604 g** (PAHT-CF 289 g, PETG 315 g; rev 1 was 611 g). Mass values are from the exported STL volumes. With slicer infill (walls + 40-100 %) the real print mass is ~ 450-500 g (estimate, not measured). Layout shell budget was 282 g (target 300 g): **+170 g to +330 g over, accepted by the client (soft target)**. Biggest items: solid 2.4 mm side plates with no frame windows beyond 3 small ones, the tray floor, and the 96 mm resistor posts.
All parts are < 256 mm (B1 238 x 190 x 99 tall incl. the bulge and arms: fits the A1 bed; the printed height 99 mm is below the 256 limit). No part needs splitting.

## Bought parts and inserts
Steel dowel removed (rev 2, M7), M4 x 12 for the tie (6 per side incl. beam foot), TPU 95A end-stop pads (2), M3/M4/M2.5/M2 heat-set inserts (driver pads 14 x M3, tray 8 x M3 in bosses, rail 2 x M4, resistor posts 4 x M3, mast 3 x M3 in lid, Pi 4 x M2.5, ESP 4 x M2, fan 4 x M3, camera 2 x M2), 1 mm Al resistor bracket (REF_ResBracket_Al1mm), Al hip seat rings, **M3 washers under every bolt head and nut that bears on a printed ear/boss (structural rule)**, M4 x 55 + nut + washer for the 4 hip posts. Fuse holder MAXI **50 A** slow-blow in the lid hatch (28 x 20 opening). Vendor STEPs (Pi, LD19, camera) were not imported; bought parts are envelope boxes (positions in the script).

## Structural updates (coordinator messages)
- **Hip seat (S12, Q3):** the side plate is PAHT-CF with a 4 mm pad ring (Ø140) around the hip hole and a **3 mm Al seat ring** (B1S_HipSeat, bolted by 8 x M3 on the pad) that carries the housing radial load; the 4 hip posts only carry torque. The seat bore is Ø108 (ring section Ø104.2); the housing ear relief in the seat is **not yet cut: open question OQ-A** (ears at r 64).
- **Outboard hip stub (arch at y ~ 108):** keep-out reserved outboard of **y 99**. All body features outboard of the plate (anchor beams y 63-73, boss to 79, pin to 99, end-stop arm to 92) stay inside y 99. The arch bracket is not modelled (envelope from the gearbox engineer pending). Bulge/plate dims are parameters at the top of the script.
- Load cases S1 (anchor 180 N: PAHT-CF beams, steel pin, boss 16 x 16), S8, S12 (battery 15 g: Velcro strap + cheeks, retention check by test), S13 (resistors on Al standoffs, PETG >= 5 mm from hot parts) are addressed in the design; none has been analysed numerically here.

## Changes to design assumptions
1. **Hip bulge**: tube Ø140 inner (not Ø129) because the skirt ears reach r 69: front reach x 99.6 (+14.6 beyond the 85 plane), top z 351.6. The front and top covers have notches around it. Check the depth requirement (OQ-B).
2. Battery raised 9.4 mm (pack z 162.6-269.6, was 153-260) to fit the rail, cradle and foam. Pi moved 20 mm forward (centre x -22.5) so the rail trim of 20 mm does not hit it. Resistors moved to x -51..0, z 259-274 (clear of the pack and of the hip driver). Charge port moved from the rear cover to the lid (x -77..-57, 20 x 32 opening): the pack stands against the rear wall, so the rear position was blocked. **The charge XT60 still bypasses fuse and switch (Electrical to confirm).**
3. Driver pad bosses are 4 mm tall, so the Al plate inner face is at y ~ 50.6 (spec 54.6).
4. Mast lidar base z 368 (spec 365): 3 mm top plate added.
5. Hip Al plate recess Ø125 dropped: the Ø130 hole already clears the lip.

## Clearances checked (hand/AABB level, not a boolean interference run)
Driver plates vs battery, Pi, resistors: >= 20 mm in y. Pack vs Pi deck at trim 20: 1 mm. Fan (x 64-74) vs ESP (x -10..60): 4 mm. Resistor posts vs hip driver board: outside its footprint. Hip housing Ø122 (y 34.5-61.5) vs bulge Ø140: 9 mm. Anchor/stop features vs the 99 mm arch keep-out: OK.
**Collision found (OQ-1, unresolved):** the 4 hip posts (r 62.2 at 45 deg, y 11.5-60.6) coincide with the skirt ears at r 64-69 (y 53.5-59.5) at about 45 and 130-135 deg world. The gearbox engineer must rotate the ears about 20 deg or the posts need notched ears.

## Assumptions / open questions
- OQ-A hip seat ear relief; OQ-B depth with the Ø140 bulge and end-stop arm (x 113); OQ-C end-stop arm attaches only through the pad ring (thin joint), analyse for 92-120 Nm; OQ-D 96 mm resistor posts are slender: add a bridge to the side plate or shorten; OQ-E tray joint is bolted bosses only (no tongue and groove); OQ-F LD19 / driver / ESP / switch hole patterns unmeasured; OQ-G cover hooks (1 mm PETG, 10 mm) not tested; OQ-H snap hook strain 1.8 % calculated only; OQ-I wheel lead slot at (x 20, z 190) vs the thigh sweep; OQ-J fuse hatch lid is an opening only (no snap hatch part modelled); the sunk nut pockets are round (hex in the slicer); the E-stop anti-rotation flat, the foam, and the 4 mast-side snaps are not modelled.
- Mass values use 1.27 (PETG) and 1.2 (PAHT-CF) on CAD volumes; SolidCraft default 1.29 was not used.
