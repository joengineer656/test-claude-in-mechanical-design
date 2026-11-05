# Body + electronics bay: build spec, rev 0 (spec only, nothing modelled)

Owner: Chassis Design Engineer (Mechanical Design) · 2026-11-04
Inputs: DECISIONS.md, design_targets.md rev 2 (frozen), layout.md rev 0, parts/hip_gearbox.md, analysis/electrical.md, analysis/thermal.md, cad/vendor/SOURCES.md.
Frame as layout.md: X fwd, Y left, Z up, origin on the ground under the robot centre. Body box x −125…85, y ±63, z 150…340. Hip (left) at (28, +, 280). Right side mirrored. Units mm.
**Rule: SolidCraft is not run in this task.** §14 is the build-step plan.

## 0. Conflicts found in the inputs (resolved here, see §13)
- Layout says the spring anchor is at world (75.2, ±79, 336.6), but the later DECISIONS row says (94.1, 71.2) **from the hip**, i.e. world (122.1, ±79, 351.2). That is **37 mm ahead of the front wall and 11 mm above the top**. So the anchor sits on an outrigger, not on the box. I use (94.1, 71.2) as (dx, dz) from the hip.
- Fuse: design_targets says 50 A, electrical.md says MAXI 60 A slow. The hatch is sized for a MAXI blade holder, so it takes either.
- Layout puts the hip Al plate at y 8.5–11.5, inboard of the motor. The 4 × Ø4.5 at ±44 therefore need **posts** from the plate to the side plate (§3).

## 1. Parts, material, wall

| ID | Part | Material | Wall | Why |
|---|---|---|---|---|
| B1 | Side plate L / R (hip carrier, driver wall) | **PAHT-CF** | 2.4 (hip pad 4) | Carries the hip reaction and the 180 N anchor load. Warm (drivers, hip Al plate). Stiff. Same material as the housing it bolts to |
| B2 | Bottom tray + battery bay + rail | PETG | 1.6 floor, 1.2 walls | Light, ductile |
| B3 | Top lid (mast, e-stop, switch, fuse hatch) | PETG | 1.6 | Snap hooks need ductility. PAHT-CF hooks snap off |
| B4 | Front cover (inlet grille, fan duct, camera) | PETG | 1.2 | |
| B5 | Rear cover (outlet grille, charge port) | PETG | 1.2 | |
| B6 | Lidar mast Ø20 | PETG | 2.0 | |
| B7 | Mounts: Pi deck, ESP/IMU spine, resistor bracket | PETG (bracket: 1 mm Al) | 2.0 | |

- **PETG for the shell, PAHT-CF only for B1.** Body air is 41 °C ventilated, 56 °C sealed (thermal §2c). PETG HDT is ≈ 69 °C and it stays clear of all hot parts by the stand-off rules in §8 and §9. The drivers' FET plates reach 80 °C locally, so they sit on ≥ 5 mm stand-offs and never touch plastic.
- All walls are 3 perimeters (1.2 = 3 × 0.4) at 0.2 mm layers. Bosses and posts are 100 % solid.
- Every part is smaller than 256 mm on the A1, so **no part needs a size split**. Largest: B1 210 × 190 × 14, flat on the bed. The 6 parts exist for access (layout §5, with the side plates and rear cover counted separately).

## 2. Body parameters (for the CAD script)

| Name | Value | Meaning |
|---|---|---|
| body_x0 / body_x1 | −125 / 85 | rear / front outer face |
| body_w | 126 | outer width. Side plate outer y = ±63 |
| body_z0 / body_z1 | 150 / 340 | bottom / top |
| wall_t | 1.2 | general wall |
| wall_side | 2.4 | side plate |
| floor_t / lid_t | 1.6 | tray floor, top lid |
| hip_x, hip_z | 28, 280 | hip axis (CAD: left side) |
| hip_plate_hole | 44 | ± offset of the 4 × Ø4.5 holes |
| hip_post_d / hip_post_hole | 9 / 4.5 | posts |
| bulge_d | 129 | Ø122 housing + 3.5 clearance |
| bulge_wall | 1.6 | |
| bulge_y0, bulge_y1 | 33, 63 | housing section 34.5–61.5 + clearance |
| bat_l, bat_w, bat_h | 107, 45, 35 | pack along Z, Y, X (upright). Pack: 107 tall, 45 wide, 35 thick |
| bat_x, bat_trim | −104.5, 0…+20 | rail position (see §5, OQ-2) |
| pi_hole_x, pi_hole_y | 58, 49 | Pi 4 holes, M2.5 |
| plate_d | 70 | driver Al plate 70 × 70 × 1.5 |
| drv_stand | 6 | driver-plate stand-off height |
| vent_in_w/h, vent_out_w/h | 60 × 55, 70 × 50 | gross vents |
| fan_d, fan_hole | 40, 32 | fan, Ø3.3 holes on 32 × 32 |
| lidar_x, mast_h, mast_d | −40, 25, 20 | |
| anch_dx, anch_dz, anch_y | 94.1, 71.2, 79 | spring anchor from the hip |
| stop_dx, stop_dz | 72.3, 12.5 | TPU end stop from the hip (100.3, 292.5 world) |
| snap_w, snap_t, snap_h | 8, 1.0, 1.2 | cantilever snap hook |
| insert_m3_d, insert_m25_d, insert_m2_d | 4.2, 3.6, 3.2 | heat-set holes |

## 3. Side plates B1 (hips)

- Outline: x −125…85, z 150…340 (210 × 190), y 60.6…63 per side (wall_side 2.4). Fits the bed flat, outside face down.
- Panels are open by default: the plate is a **frame** (rim 8 wide, ribs 6 wide, 2.4 thick) with the skin kept only where something mounts (driver pads, hip pad). Target open area 50 %.
- **Hip opening:** Ø130 through hole, centre (28, 280). The ring-section ears are at r 64 (hip_gearbox §6), so the hole is Ø130, not Ø108.
  - The ring section Ø104.2 passes through, and the Ø121.8 big-planet section stays inboard (y ≤ 61.5).
  - Inboard face recess: Ø125 × 1.0 deep around the opening, so the housing lip clears (inner face 60.6 → 61.6).
  - Outboard pad: **Ø140 × 2 (y 63–65)**, restoring the web. Shank sweeps at y 68–80, so there is 3 mm to the shank.
- **4 hip posts** (carry the Al plate): at hip ± 44 in X and Z, i.e. world (−16 / 72, 236 / 324). Post Ø9 × length from the Al plate outer face (y 11.5) to the side plate inner face (y 60.6), **49.1 mm**, bore Ø4.5, 100 % PAHT-CF, printed upright with the side plate, M4 × 55 with nut in a hex pocket on the outer pad.
  - The skirt flange (Ø108 BC, ears) must be notched at the 4 corners: **OQ-1**.
  - Post centre radius 62.2 sits inside the Ø125 recess edge (62.5). So the recess is **interrupted by 4 flat lands** (Ø14) at the posts.
- **Hip bulges** (front and top shell only; they are the inner-wall regions around the housing):
  - A cylindrical shell coaxial with the hip, Ø129 × bulge_wall 1.6, y 33…63 on each side.
  - Front: reaches x 28 + 64.5 + 1.6 = **94.1 vs the 85 front plane** (+9 mm beyond; the housing alone needs 88.9 → +4 mm as in hip_gearbox §6, plus 3.5 clearance and wall).
  - Top: z 280 + 64.5 + 1.6 = **346.1 vs 340** (+6 mm).
  - Open towards the shell interior, so it adds only the 1.6 mm shell. These are cut/added in the side plate frame, front cover edge and top lid edge. Seams are at y = ±33, which is clear of the e-stop, switch and fuse.
  - Width at the hip stays < 150 (hip_gearbox OQ-1).
- **Spring anchor outrigger** (§10) and **end stop seat** (§11) are printed in the side plate.
- Driver pads: §7. Cable slot: §12.

## 4. Tray B2

- 210 × 126 footprint, floor 1.6, walls 1.2 × 12 high on all four sides, floor opened 50 % (lightening 18 × 18 hex holes) except under the battery and the ESP spine.
- Joins to B1 with a **tongue and groove** (tongue 2.4 × 8 on the tray, groove in B1) plus 4 × M3 × 8 per side into **M3 heat-set inserts in the tray**. These are the structural joints and are not snaps.
- Cable channel: two 8 × 6 ribs along x on the floor at y = ±22.
- Bottom z 150 means a 150 mm ground gap at nominal and 56 mm at crouch. Add 4 small PETG skid ribs (no feet needed).

## 5. Battery bay (upright 6S 2200 mAh)

- Pack 107 × 45 × 35 stands on the tray, 107 along Z, 35 along X, 45 along Y. Centre x −104.5 (rear face x −122), z 153…260 (206.5 centre).
- **Cradle:** open frame, internal 38 × 48 (pack + 3 mm per axis, since packs vary 105–116 × 34–49), cheeks 2.0 × 80 tall, 2 slots for a **25 mm Velcro strap** around the pack, 3 mm closed-cell foam pad on the floor and cheeks.
- **Rail:** the cradle base plate is 2 mm and has 2 slotted holes **M4, 4.5 × 24** at y ±15 along x, bolted into 2 **M4 heat-set inserts** (tray rib, 100 % solid). Travel = 20 mm (marked scale each 2 mm).
- Leads: XT60 + 7-pin JST-XH balance lead exit at the **top** of the pack. Loop of 40 mm slack. A strain relief clip (zip-tie post) on the cradle top.
- A fixed 6 mm gap between the rear face and the rear cover is kept for the charge pigtail (§9).
- **OQ-2:** the layout leaves 0…+20 mm (the pack is at the rear wall), but the request is ±20. The CoM sensitivity is only 365 g × 20 / 4370 = **1.7 mm per 20 mm** of rail travel. A 3 mm rear gap is not enough for rearward trim. Proposal: nominal at bat_trim = +20 mm, giving −20 … 0 mm rearward in practice (+1.7 mm CoM fwd budget stays on the controller side). Needs the Pi deck and the drivers to move 20 mm: not possible, so **the rail stays 0 … +20 mm** unless the client accepts moving the Pi.

## 6. Electronics: Pi, ESP32, IMU

**Pi 4 (85 × 56, heatsink, 28 high, centre (−42.5, 0, 214)).**
- Pi deck B7a: 2 mm PETG plate 92 × 62, held by **4 corner posts** (Ø8, from the tray) at x −85…0.
- Holes 58 × 49, 3.5 mm from the board edge: **4 × M2.5 heat-set inserts (Ø3.6 × 4)** in posts 5 mm high. USB-C power from the 5 V buck via GPIO 5 V pins. Board z ≈ 200.
- Keep 8 mm free around the heatsink for the air path. Camera cable (CSI) and UART lead to the ESP32 are tied to the deck.

**ESP32 PCB (70 × 50, centre (25, 0, 190)).**
- 4 × M2 posts in a 64 × 44 rectangle (the real pattern depends on the PCB: **OQ-5**), 5 mm high, inserts M2 (Ø3.2 × 3).
- Posts rise from a **spine**: a 3 mm × 40 central web on the tray floor along x 0…60, tied to both tray ribs.

**IMU (0, 0, 187), mid-plane y = 0.**
- On the ESP PCB, so the PCB has to be stiff: spine height 37 mm, 2 cross-braces to the tray ribs, **no rubber**, no cable pull on the board (cables clamped 20 mm away).
- Nearest heat/magnetic sources ≥ 47.9 mm (layout §3, rule ≥ 40). Keep the IMU away from the fan magnet (fan x 77, 77 mm away).
- Board must stay level: the spine top is a machined-flat feature (print the posts' top face down on the bed? no: print upright, 0.1 mm layers), check with a level.

## 7. Driver plates and mounts

- 4 × XDrive Mini (63 × 58 × 1.6, M3 holes 56.6 × 51.5) on **70 × 70 × 1.5 Al plates with a 1 mm thermal pad**. Keep-out above the board 20 mm until the real part is measured (O7).
- Position: x −85 centre (−120…−50), y ±46.75 centre, z 275 (hip driver) and 195 (wheel driver). Left and right mirrored.
- Plate carried by **4 × M3 stand-offs, 6 mm high** (rule ≥ 5), on 4 printed pads in the side plate skin. Each pad Ø9 with an **M3 heat-set insert** (4.2 × 5.7).
  - Plate hole pattern 60 × 60 (Ø3.4), with the board 56.6 × 51.5 stand-offs M3 × 6 on top of the plate (4 more nylon stand-offs).
  - Plate inner face at y ≈ 54.6 (6 mm off the wall inner face 60.6). The 20 mm component keep-out reaches y ≈ 33, which is clear of the battery (y ±22.5), Pi (±28) and resistors (±15 + 25).
- The two driver stacks per side are 80 mm apart (z 275 and 195) with 10 mm between plates, which is the fan airflow path from front to rear.
- Phase / power connectors face down and rearward (x −120 side) to keep wires away from the hip motor (x −18…74).

## 8. Fan, vents, brake resistors

- **Fan:** 40 × 40 × 10 (Noctua NF-A4x10 5 V or equivalent, ≥ 3.3 CFM) in the front cover at (77, 0, 185), blowing **in**, 4 × Ø3.3 holes on 32 × 32 with M3 × 16 screws and nuts, or 4 heat-set inserts in a Ø46 duct ring. A 2 mm foam ring seals the duct to the inlet grille.
- **Inlet** (front, low): 60 × 55 window in B4 at (85, 0, 185) = 33 cm² gross. Fine mesh (printed grille: 1.6 wide slats at 3.2 pitch = 50 % open, 17 cm² net, over the 16 cm² rule).
- **Outlet** (rear, top): 70 × 50 window in B5 at (−125, 0, 310), 35 cm² gross, same grille. Slats angled down 30 deg so the grille hides the inner view.
- Lid and side frame gaps count as extra leakage only; they are not designed as vents.
- **Brake resistors** 2 × HS25 2R0 (51 × 28 × 15): at (−72.5, ±15, 257.5).
  - On a **1 mm Al bracket** (60 × 40) on 2 × **M3 × 12 stand-offs (Al or steel, 10 mm tall)**, mounted to the tray spine / rear rib, so there is ≥ 10 mm of air to any plastic. The bracket itself is clamped on metal posts only; the plastic posts are 20 mm lower.
  - Sits at the outlet side in the exhaust path, z 257.5 below the outlet at 310.
  - **Check:** the battery top is at z 260, x −122…−87, and the resistor reaches x −98: a **3.5 mm resistor-to-pack overlap in x** exists (layout geometry, y ±15 vs pack y ±22.5). Move the resistors to x ≥ −82 or raise them to z ≥ 275 (OQ-4).
  - Fault case: 200 °C. The cable (silicone, 18 AWG) leaves away from the body, not touching it.

## 9. Switches, fuse, e-stop, charge port, cables

All on the top lid B3 and rear cover B5. Lid boss thickness around each opening is 3 mm.
- **E-stop** Ø22 latching NC, head Ø40, at (−100, 0, 335): Ø22.3 hole + anti-rotation flat, locknut from below, 3 mm boss. Head clears the lidar plane (top ≈ z 360 < lidar 385).
- **Anti-spark switch** at (−100, +38, 332): Ø19.2 hole (confirm the real part, **OQ-5**).
- **Fuse hatch** at (−97.5, −40, 328): 28 × 20 opening in B3 with a **snap-on hatch** (2 hooks, thumb notch). The MAXI holder sits below the hatch on 2 × M3 posts, so a fuse can be changed without opening the lid.
- **Charge/balance port** at the rear cover, (−125, 0, 175), below the outlet: panel with 1 × XT60-F (charge, parallel to the pack via a 12 AWG pigtail) and 1 × JST-XH 7-pin socket for the balance lead. Cut-out 24 × 32, 4 × M2.5 inserts. The pigtail goes through the 6 mm gap behind the pack. **The charge XT60 bypasses fuse and switch: confirm with Electrical (OQ-4).**
- **Cable routing:** one trunk on each tray rib channel (y ±22), tied every 40 mm with 2.5 × 1.2 zip-tie slots printed into the ribs; PDB at (52, 0/−35, 160). Power runs ≤ 25 cm. Phase and signal wires are not parallel within 15 mm; encoder SPI is shielded and 45 cm.
- **Strain reliefs:** 3 per cable group: at the connector (zip post 3 mm from it), at the shell wall exit (clamp block 12 × 12), and at the pack. Wheel-motor and encoder leads leave through a **side plate slot 16 × 8 at (x 20, z 190), with a TPU grommet** (position is a parameter: it must clear the thigh sweep, **OQ-6**).
- Lidar cable: Ø5 channel up the mast to the top lid, one zip post inside.

## 10. Lidar mast and camera

- **LD19: 38.6 × 38.6 × 33.5** (SOURCES: not measured; re-measure at import). Mast **Ø20 × 25, hollow (2 mm wall)**, base flange Ø32 × 3 with 3 × M3 on Ø26 into 3 inserts in the lid boss (3 mm lid + ring rib). Top plate Ø30 × 3 with the LD19 holes (unmeasured: **OQ-5**, assume 4 × M2.5 on a 30 mm square).
- Mast centre x −40, base z 365 → the mast bottom is the lid top at z 340, so the mast is really 25 and the lid top is **z 340**; lidar base z 365, optics plane ≈ z 385–395. Nothing above z 360.
- 360° view: the mast Ø20 sits below the scan plane. The LD19 body is above it. Hip bulge tops are z 346 and lower than 385 plane. **PASS.**
- **Camera** Pi Cam 3 (25 × 24 × 11.5), front cover at (91, 0, 300): 2 × M2 inserts, window 12 × 12, 3 mm lens-window lip, 4 mm recess so the lens sits flush with x 85. Ribbon through a 17 × 2 slot to the Pi deck.

## 11. Spring anchors and end-stop seats

- **Anchor pin:** hardened steel dowel **Ø6 × 36**, centre at (hip_x + 94.1, ±anch_y, hip_z + 71.2) = **(122.1, ±79, 351.2)**.
  - Carried by an **outrigger arm** from the side plate (y 63…79): a 12-wide PAHT-CF beam in the plate's own XZ plane, running from the front-top corner (x 85, z 340) to the anchor. Printed with the side plate (layers in the plate plane, so the tension load is in-plane).
  - **Boss:** Ø16 × 16 deep (y 63…79), Ø5.9 press hole through the boss (press fit 0 to −0.05 per materials rule), 6 mm hole tolerance by coupon. The pin projects y 79…99 (hook plane y 81–95), with a **retaining E-clip groove** at the tip.
  - Loads at 180 N: pin shear 6.4 MPa; pin bending at 9 mm lever 1.6 Nm gives about 76 MPa (steel, OK); boss bearing 180/(6 × 16) = 1.9 MPa. Beam: 12 × 12 at 180 N × 40 mm lever = 7.2 Nm gives 25 MPa in-plane, **SF ≈ 3 on PAHT-CF layers**; check by a pull test.
  - Direction of the 180 N pull: along the spring axis, toward the thigh crank, down and rear. Beam ribs go from the anchor back to **3 side plate rim joints**.
- **TPU end stop seat** at (100.3, ±86, 292.5): pocket 18 × 18 × 12 deep on a 15 × 20 PAHT-CF bracket from the side plate rim (y 80…92 plane, x 85…105), 2 retention lips + 1 × M3 cross screw into an insert. Pad: TPU 95A about Ø16 × 20, ≈ 10 kN/m, engaged at hip 130, ≥ 30 mm travel. The bracket takes the landing stop load into the side plate, **not the gearbox**. **OQ-7:** the bracket's lever arm lengthens the load path; Structural to check 92–120 Nm landing.

## 12. Heat-set insert list (M3 × 5.7, Ø4.2 hole unless marked; hot-pressed at 220 °C, into PETG/PAHT-CF 100 % bosses 2.4 wall min)

| Where | Qty | Size |
|---|---|---|
| Tray to side plate (per side 4) | 8 | M3 |
| Top lid screws (2 rear corners) | 2 | M3 |
| Battery rail | 2 | M4 (Ø5.6) |
| Driver pads (4 per plate, 4 plates) | 16 | M3 |
| Pi posts | 4 | M2.5 |
| ESP posts | 4 | M2 |
| Fan duct (optional) | 4 | M3 |
| Resistor bracket posts | 4 | M3 |
| Mast flange | 3 | M3 |
| Lidar top | 4 | M2.5 |
| Camera | 2 | M2 |
| Charge panel | 4 | M2.5 |
| End-stop brackets | 2 | M3 |
| Total | **59** (≈ 0.25 g each, 15 g: counted in the 160 g fasteners) | |

## 13. Snap-fit covers

- Front cover B4, rear cover B5, top lid B3, fuse hatch: **cantilever hooks** snap_w 8 × snap_t 1.0 × free length 10, hook 1.2 deep, 45° lead, 90° retain (service) or 45° (permanent). PETG strain at 1.2 mm deflection on 10 mm: ε = 1.5 t y/L² = 1.8 % (< 3 % limit).
- B4 and B5: 4 hooks each (2 top, 2 bottom). B3: 6 hooks + 2 M3 screws at the rear corners (the e-stop push load and the mast need a retained lid). Fuse hatch: 2 hooks.
- A 0.3 mm clearance gap all around; print the hooks along the layer plane (cover flat on the bed, hooks printed on their sides in the plane of the layers).
- Weight saving vs screws: ≈ 12 screws and 12 inserts avoided ≈ 6 g plus 20 min of assembly.

## 14. Mass estimate (layout: shell 282 g, target ≤ 300 g)

| Part | Volume basis | Mass g |
|---|---|---|
| B1 side plate × 2 (frame, 50 % open, PAHT-CF 1.2) incl. pads, outrigger, bracket | ≈ 36 cm³ each | 2 × 43 = 86 |
| 4 hip posts (Ø9 × 49, bore) × 2 sides | 2.6 cm³ each, 8 posts | 25 |
| B2 tray + battery bay + rail + ribs | | 52 |
| B3 top lid + mast + bosses | | 34 |
| B4 front cover + fan duct | | 28 |
| B5 rear cover + charge panel seat | | 26 |
| B7 Pi deck + ESP spine + resistor bracket | | 22 |
| Hip bulges (included in the side plate, front and top edges) | | 8 |
| **Total** | | **281** |

- **Ties to the layout (282 g) and is ≤ 300 g.** Margin 19 g. Uncertainty is ±15 % (O16), so up to about 323 g is possible; the recovery lever is making the side plate 50 → 60 % open (−8 g) and lightening the top lid.
- Not counted (in the 160 g body fasteners): inserts 15 g, steel pins 2 × 4 g, screws, stand-offs, grommets.
- The 2 hip bulges and the 4 posts per side (25 g) were not explicit in the layout: they are the cause of the tight margin.

## 15. Open questions

- **OQ-1** Skirt flange (Ø108 BC) meets the 4 hip posts at r 62: notch it, or Gearbox Engineer limits the flange to r ≤ 56. Also confirm Ø130 opening vs the ear positions.
- **OQ-2** Battery rail: layout gives 0…+20 mm (rear wall), request says ±20. CoM authority is 1.7 mm per 20 mm. Decide whether to move the Pi/drivers for rearward room or use a ballast pocket.
- **OQ-3** Spring anchor coordinate: confirm (94.1, 71.2) is (dx, dz) from the hip in world axes; layout still shows the old point.
- **OQ-4** Electrical: charge-port path around fuse and switch; resistor x/z vs the pack (3.5 mm overlap); fuse 50 vs 60 A; driver orientation.
- **OQ-5** Measure on arrival: LD19 and driver hole patterns, ESP32 PCB pattern, switch hole, XDrive height (O7).
- **OQ-6** Wheel cable slot position vs the thigh/shank sweep (needs the leg clearance model).
- **OQ-7** End-stop and anchor outriggers are 37 mm and 20 mm ahead of the front plane: they increase depth at nominal 299.8 mm? (They are inboard of the wheel-front extent, so the check should be re-run: depth is set by the coupler pin C, not the body.)
- **OQ-8** PETG creep near warm parts (56 °C sealed case): ventilation must work; consider ASA for the tray.

## 16. SolidCraft build-step plan (do not run now)

1. New design; set the user parameters of §2.
2. Sketch XZ and extrude B1 outline (y 60.6–63), cut the frame windows, the Ø130 hip hole, the Ø125 recess, the Ø140 pad, the 4 post lands.
3. Add the 4 hip posts (Ø9 × 49.1, Ø4.5 bore) and the hex nut pockets. Add driver pads and insert holes (rectangular pattern), the cable slot, the anchor outrigger + boss + pin hole, and the end-stop bracket + pocket.
4. Mirror B1 about the XZ plane (y → −y); keep it as a separate body.
5. Build the tray: floor, walls, ribs, battery bay, slotted rail holes, grooves for B1, insert holes.
6. Build the front and rear covers: grille slat patterns, fan seat, camera window, charge panel cut-out, snap hooks.
7. Build the top lid: openings for the e-stop, switch, fuse hatch, the mast flange, hooks; then the mast and its top plate.
8. Build the mounts (Pi deck, ESP spine, resistor bracket).
9. Import vendor STEPs (Pi, LD19, camera, XT60, fan placeholder) and placeholders (battery, XDrive, resistor), check interference with `measure`.
10. Export STL per part (flat orientations) and STEP of the assembly; record the volumes and update §14.
