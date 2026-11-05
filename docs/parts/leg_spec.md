# Leg Build Spec — rev 0 (spec only, no CAD yet)

Owner: Leg Design Engineer (Mechanical Design) · 2026-11-04 · ONE leg, built ×2 (right = mirror about world XZ).
Inputs: DECISIONS.md, docs/design_targets.md (frozen), docs/layout.md, docs/parts/hip_gearbox.md (thigh plane +12 mm, hex 26 A/F, shank ↔ ring 6.7 mm), theory.md (§3.3, landing LC, P3 spring re-fit), materials_gears.md, thermal.md.
Calc: `docs/analysis/calc/leg_spec_calc.py` (4-bar solve, clearances, sections, SF). SolidCraft NOT used.

Frame: hip-relative (x fwd, z up) for the leg plane; Y is the lateral (left side shown, world y). World hip = (28, ±y, 280) at nominal.

## 0. Summary and the three things that need a decision

| Item | Result |
|---|---|
| Links | thigh 121 · knee→wheel 189 · coupler 113 · knee→C 42 (C is 175° from K→W) · B = (46, 34) · hip 101–289 mm above axle. Re-solved, matches layout to < 1 mm |
| Material | PAHT-CF (conditioned UTS 65, static allowable 0.70 → 45.5 MPa, one-way fatigue 19.5, reversed 14.3, E ≈ 5 GPa assumed) |
| Metal needed | **Shank: 2 mm 6061-T6 structural cover plate** (printed-only SF 1.12, fails the side-fall case). Pins: hardened steel Ø8. Bushings: sintered bronze. Wheel axle: Al hollow axle (hub carrier, already in layout §6). Hip: steel inserts already in the gearbox hex |
| Mass | ≈ 164 g printed+plate per leg (**328 g for 2**) vs 254 g budget → **+74 g**, plus ≈ 45 g/leg hardware (layout lumps 97 g/leg of joint hardware) |

Open decisions (details §11):
1. **Spring ↔ B-pin clearance is negative at crouch (−1.3 mm).** The layout's 3.3 mm treated B as a point. The B pin must cross the spring plane (y 93–107) to reach the coupler plane. Needs B 3 mm lower, or the anchor moved (Theory).
2. **Offset single-shear knee** (thigh plane y 93–103, shank y 68–78/80): LC-D adds a 24 mm-offset couple (≈ 48 Nm) that the links take in torsion. In-plane SFs below are OK. Needs a 3-D check (Structural/FEA) or a double-shear shank yoke.
3. **Depth.** The C-pin eye is the front-most point. With a R12 eye the nominal depth is **301.8 mm** and crouch **323 mm** (layout 299.8 / 321). An R ≤ 10 eye does not carry the load in PAHT-CF. Accept "around 300" or use a 6061 eye.

## 1. Y stack (outboard +, left side; layout §1 shifted per hip_gearbox.md)

| Item | Y range (mm) | Note |
|---|---|---|
| Hip housing ring | 59.5–79.5 | Ø104.2, cover to 93 |
| **Shank** printed channel + Al plate | 68–78 + 78–80 | inboard of the thigh; plate is the outboard face (keeps 80 for the carrier flange and the hub stack, so width stays 300) |
| Cable gap (knee loop) | 80–93 | phase wires ride here |
| **Thigh** | 93–103 | hex output shoulder at 93 |
| Crank arm + clevis | 94–106 | ears 94–98 and 102–106, hook slot 98–102 |
| Spring (axis y = 100) | 93.5–106.5 | OD 13 |
| **Coupler** | 108–122 (eyes 14 wide) | outboard; clears the spring by 1.5 |
| Wheel hub, tyre | 80–127… per layout | unchanged |

Pins: K spans 68–106 (Ø8 × 44), C spans 68–122 (Ø8 × 58), B spans from the hip-housing lug to 122 (Ø8 × ≈ 70, see OQ-1).

## 2. Kinematic check (4-bar solve, `leg_spec_calc.py`)

| Hip h | thigh ang | shank ang (K→W) | K (hip-rel) | C | C world x | Spring length |
|---|---|---|---|---|---|---|
| 101 crouch | +0.48° | −147.3° | (121.0, 1.0) | (158.2, 20.5) | 186.2 | 152.0 |
| 130 end-stop | −7.66° | −143.0° | (119.9, −16.1) | (155.5, 6.2) | 183.5 | 149.1 |
| 195 nominal | −29.99° | −134.6° | (104.8, −60.5) | (136.8, −33.3) | 164.8 | 138.6 |
| 289 extended | −72.68° | −113.4° | (36.0, −115.5) | (56.0, −78.6) | 84.0 | 111.0 |

- **C pin swing:** x 158.3 → 55.1, z +21.4 → −78.6 over the full range (a 34° rotation about K, radius 42). Spring span 152 → 111 = 41 mm (theory 41).
- **Depth at crouch** = C world x 186.2 + eye R 12 + 125 (rear) = **323 mm** (layout 321 used R ≈ 10). Nominal: 164.8 + 12 + 125 = **301.8**. Hip travel 130 → 101 is 29 mm (≥ 30 target read as hip travel, per layout §7.5).
- **Spring ↔ B pin** (centre line to B, then − 6.5 spring − 4 pin): crouch 10.2 → **−0.3 mm** (Ø8 pin; −1.3 with a Ø10 boss), 130: +1.6, nominal +6.3, extended +10.7. Moving B 3 mm down (34 → 31) gives ≈ +2.7 at crouch. Theory re-verifies hip range 101–289.
- Shank ↔ ring 6.7 mm at crouch (hip_gearbox.md); shank and thigh never share a Y range, so thigh ↔ shank cannot collide even when folded to 31°.

## 3. Load cases used (theory.md, 4.31 kg, fixed TPU stop)

| LC | Knee pin N | Coupler N | Axle N | Use |
|---|---|---|---|---|
| A controlled | 345 | 263 | 156 | fatigue |
| B symmetric, motors off | 1125 | 1094 (scaled) | 220 | ultimate |
| C one wheel, controlled | 597 | 454 | 192 | fatigue |
| D one wheel, motors off | **2011** | 1955 (scaled from 2720/2798) | 337 | ultimate, design SF ≥ 1.5 on allowable 45.5 |
| LC3 side fall | assumed 300 N lateral at the tyre (theory gives no number) | | | shank weak axis |
| Sliding landing | axle horizontal = 0.8 × 337 N | | | shank |

Stop torque 92–120 Nm at the hip (materials §7). Bending in the thigh peaks at the stop contact: M = 2011 × (121 − 73) = 97 Nm.

## 4. Thigh (H → K, 121)

- **Hip boss:** Ø38 × 10, hex socket **26 A/F + 0.15 clearance per flat, 6 deep** (floor 4 mm), flat wall 6 mm. 3 × M4 × 16 button head + Ø9 steel washers through the floor into the gearbox steel inserts on Ø15 (120° pitch, set by the hex orientation, homing tab slot). Hex flank bearing ≈ 5.5 MPa at 20 Nm → SF ≈ 8.
- **Section:** closed box, Y 10 × in-plane depth 56 at the stop station (r = 73), wall 3, taper to depth 30 at K (R14 boss) and to the Ø38 boss at H. Printed as a channel (open outboard) with a 2 mm PAHT-CF cover, 6 × M2.5 and CA glue. The depth is asymmetric: 22 mm above the H–K line, 34 below (the top edge face at r = 73 is the **striker** for the stop).
- **SF:** I = 93.4 × 10³ mm⁴, Z = 3739 mm³. LC-D: σ = 97 000 / 3739 = **25.8 MPa → SF 1.76** (≥ 1.5). LC-C: 7.7 MPa vs one-way fatigue 19.5 → **SF 2.5**.
- **Knee eye:** R14, flanged sintered-bronze bushing **ID 8 × OD 12 × L 10**, ligament 8 mm.
- **Crank:** 40 mm opposite the thigh (hip-rel (−40 cos θ, −40 sin θ)), arm 10 × 16 in-plane, slot 4 mm, ears 4 mm, Ø4 steel pin (h6, L 14) with e-clips. 180 N: ear bearing 90 / (4 × 4) = 5.6 MPa (< 10 materials rule), pin shear 7 MPa, arm σ = 7.2 Nm / 327 mm³ = 22 MPa → SF 2.1. Pin in double shear, not on the gearbox output.
- Printed 44 g.

## 5. Coupler (B → C, 113)

- Hollow bar Y 14 × 16, wall 2.4. Eyes Ø34 → R17 would break depth, so **R12 eyes**, one flanged bronze bushing **ID 8 × OD 12 × L 12** each, Y 14 wide.
- Tension LC-D 1955 N: A = 121 mm² → 16.2 MPa → SF 2.8. Lug (ligament 6 mm, Kt 2.5): 29 MPa → **SF 1.56**.
- Buckling (pin-pin, E = 5 GPa): in-plane Pcr 14.3 kN (SF 7.3), out-of-plane Pcr 11.3 kN (**SF 5.8**).
- Bushing pressure LC-D 20 MPa (sintered bronze static ≥ 35), LC-C 4.7 MPa.
- Printed 32 g. Print on its side? No: flat (see §10).

## 6. Shank (K–C–W lever)

- **Printed channel (PAHT-CF) + 2 mm 6061-T6 plate.** Printed part Y 10 (68–78): inboard web 3, side walls 2.4, ribs at 45° every 14 mm. Depth in plane: 44 at K, tapering to 30 at W (cavity 24 at the foot so the cables clear), K→C arm 42 long, depth 30. The Al plate (waterjet, same outline, 2 mm, 5 × M2.5 A2 + epoxy) is the outboard face, so the printed part never bridges.
- **Loads** at hip 130 (LC-D): M at K = 337 × 151 = 50.8 Nm vertical only, **81.5 Nm with 0.8 friction**.

| Check | Result |
|---|---|
| Printed only, vertical, σ | 27 MPa, SF 1.7 |
| Printed only, with friction | 40.5 MPa, **SF 1.12 (fail)** |
| With Al plate (it takes 74 % by stiffness, E 69 vs 5 GPa) | Al σ 127 MPa, **SF 1.9 on yield 240**; printed 10.6 MPa SF 4.3 |
| LC3 lateral 300 N, arm 189 mm, weak axis, printed only | 106 MPa, **fails** |
| LC3 with Al plate | Al 192 MPa, **SF 1.25** (thin; 300 N is an assumption, check with Structural) |

- **Eyes:** knee eye R14 with bronze **ID 8 × OD 12 × L 12** (shank Y is 12 with the plate). C eye R12 with the same bushing (pin passes through to the coupler at y 108–122).
- **Wheel foot** (see §9). Printed 43 g + Al plate 46 g (1.5 mm plate saves 11 g, check SF).

## 7. Pins, bushings, joints

| Joint | Pin | Bearing | Load LC-D | Check |
|---|---|---|---|---|
| H | hex + 3 × M4 × 16 (steel inserts) | gearbox 6806 | torque ≤ 16 Nm | hex SF ≈ 8 |
| K | Ø8 h6 hardened steel (≥ 12.9 class or 42CrMo4 ground), L 44, e-clip grooves | thigh L10 + shank L12 flanged sintered bronze ID 8 / OD 12 | 2011 N | bushing 25 / 21 MPa static; pin bending (couple, M = F × 24 / 2) **480 MPa, SF 2.3 on 1100**; shear 40 MPa |
| C | Ø8, L 58 | shank L12 + coupler L12 | 1955 N | pin bending ≈ 455 MPa (offset 22) → same SF ≈ 2.4 |
| B | Ø8, L ≈ 70 | coupler L12 | 1955 N | lug on the hip housing / side plate (layout §8.6) |
| Crank, anchor | Ø4 steel h6 | none (hook on pin) | 180 N | §4, §8 |

- **685ZZ not used** (static capacity ≈ 0.5 kN, below the 2 kN case). 608ZZ pairs would also work (static 1.4 kN each, SF 1.4) but are 3× heavier and 14 mm wide. This **replaces BOM items 21–23** (4 × 608-2RS, 12 × 688-2RS, Ø8 × 30 pins): new list per leg = 3 × Ø8 pins, 6 bushings, 2 × Ø4 pins. BOM Engineer to update.
- Fits: bushing press into printed eye with −0.05 mm, ream, retain with the flange + e-clip; pin h6 in bronze, 0.02 clearance. Grease with PTFE grease.
- **Couple:** the offset knee and C pins load the pin and bushings as a single shear with a 22–24 mm arm. Equilibrium is closed by link torsion/bushing edge loads. See OQ-2.

## 8. Spring crank, anchors, end stop, rest bumpers

- **Spring:** 2.7 N/mm, d 2.0, OD 13, free ≈ 110, 8 N preload, 122 N at 152 mm (design 180 N), spring axis plane y = 100, 3 mm Y at the thigh crank pin.
- **Crank pin P** = H − 40 u(θ). Spring length 111 → 152 (values in §2 reproduce theory).
- **Body anchor:** hip-rel **(94.1, 71.2)** → world (122.1, ±100, 351.2). This is 37 mm in front of the body front face (x 85) and 11 mm above the top (z 340), so it needs an **Al bracket "spring tower"**: 3 mm 6061 bent U (ears 3 mm, gap 6 → slot for the hook, Ø4 steel pin in double shear), 3 × M4 through the body side plate / top with nut and washer, **3-hole slot ±5 mm** for the spring length tolerance. 180 N × 40 mm cantilever = 7.2 Nm. Al bearing 90 / (3 × 4) = 7.5 MPa. **Not on the gearbox output.** Height 351 + 10 = 361 < lidar base 365 (x −40, no overlap in x).
- **TPU end stop:** pad **95A TPU 10 × 10 × 25 tall, 15 % gyroid, 2 walls**, k ≈ 10 N/mm (±50 %, tune on the bench: print 3 densities), on a body bracket at hip-rel **(72.3, 12.5)** (r = 73, world (100.3, 292.5)). Striker = thigh top edge face at r = 73. Engages at **hip 130** (θ = −7.66°), pad compresses 10 mm at hip 101 → 99 N → 6.9 Nm; the pad is 25 tall (40 % strain), so hip travel 130 → 101 = 29 mm ≈ 30. Pad ↔ B-pin: 11 mm (layout).
- **Hard stop:** gearbox crouch stop at θ = +1.5° (hip_gearbox.md) is the last resort, not the landing stop.
- **Rest bumpers:** 2 × TPU 95A pads Ø10 × 6 on the thigh striker face and on the shank (K→W arm, at the crouch fold) so a folded robot rests thigh-on-body, never on the gearbox output. Third: shank ↔ coupler rest at extended (hip 289): 6 mm TPU dot on the C arm.

## 9. Wheel axle mount (shank foot)

- Foot pad Ø60 around W, Y 68–80, printed + the Al plate (covering the foot too).
- **Central through hole Ø16** from the inboard pocket to the plate face: the Al hollow fixed axle (hub carrier, Ø14 bore through its length) bolts to the outboard face. Encoder pocket **Ø30.4 × 8 on the inboard face** (y 68–76 pocket, 1.5 mm gap set by shims), AS5047P breakout with a 6 mm Ø magnet on the motor axis. Non-magnetic M2 screws within 10 mm.
- **Carrier flange: 4 × M4 on Ø44**, bolted through with captive hex pockets on the inboard face (bolt through, not inserts: primary load path). Axle moment: 337 N × 22 mm offset (bearing centre y 102 to the foot face y 80) = 7.4 Nm → bolt tension 170 N each, edge distance 10 mm (2.5 d) OK.
- Cable slot radial in the foot for the SPI cable; phase wires pass in a 6 × 10 mm slot at the carrier side.

## 10. Cable route, print orientation and splits

**Cables (per leg):** 3 phase wires (silicone AWG 16) + shielded SPI cable ≈ 45 cm.
1. Body side plate grommet at hip-rel (≈ +30, −55) → follows the outside of the housing → thigh channel entry slot at r ≈ 60 (inboard face y 93).
2. Thigh cavity (cover plate access): phase wires on the upper side, SPI on the lower, separated ≥ 15 mm by a rib.
3. **Knee:** phase wires make a half-turn **service loop (radius ≥ 20, slack ≈ 40 mm) in the 13 mm cable gap (y 80–93)** and enter the shank cavity through the Al plate slot at the knee boss. The SPI cable leaves the thigh on the inboard face, wraps the knee boss inboard of the shank, and runs in a **2 mm groove on the inboard face of the shank** (y 66.5–68, proud 1.5 mm; body wall clearance ≥ 1.5 mm).
4. Foot: phase wires into the carrier slot; SPI to the encoder pocket (inboard). **Separation: SPI at y ≈ 66.5, phase at y ≈ 76–83 → ≥ 15 mm** along the shank; in the thigh by the rib; at the knee by the shank thickness. Bend radius ≥ 6 × OD; P-clips every 40 mm; strain relief tie at the knee and at the foot.

**Print (Bambu A1, 256³, hardened nozzle, dried PAHT-CF; hardened insert temps from materials §6):**

| Part | Orientation | Split |
|---|---|---|
| Thigh channel | **flat, outboard (open) face up**, Y = print Z, layers in the XZ bending plane, 0.5 mm chamfer on bed edges | none (≈ 150 × 60) |
| Thigh cover | flat | none |
| Shank channel | flat, open face up, **diagonal on the bed** (span C…W ≈ 231 + bosses ≈ 275; bed diagonal 362) | none; if it exceeds, bolted lap at mid-length (2 × M4, dowel) |
| Shank Al plate | waterjet 2 mm | — |
| Coupler | flat on its side face (Y 14 vertical), eyes bored −0.05 | none |
| Stop pad, bumpers | TPU, flat | — |
| Spring tower, ears | 6061 3 mm bent | — |

Eye bores printed Ø11.9 and reamed to 12.0 (calibrate on the test coupon). Wall ≥ 2.4 load paths, internal fillets ≥ 2 mm, section changes R ≥ 5.

## 11. Mass per leg vs layout

| Part | This spec | Layout (per leg) |
|---|---|---|
| Thigh | 44 g | 33 |
| Shank (printed + Al plate) | 43 + 46 = 89 g | 63 |
| Coupler | 32 g | 31 |
| **Subtotal** | **165 g (330 for 2)** | **127 (254 for 2) → +76 g robot** |
| Hardware (pins, bushings, hex bolts, clips, fasteners, pad) | ≈ 45 g | 97 (knee 40, C 25, B 16, hip joint 16) → −52 g |

Net robot effect ≈ +24 g. Cuts if needed: Al plate 1.5 mm (−11 g/leg, re-check LC3), taper thigh walls to 2.4 (−5 g), lattice the coupler infill (−4 g).

## 12. CAD script parameter names (SolidCraft user parameters)

`leg_thigh=121`, `leg_shank_KW=189`, `leg_coupler=113`, `leg_knee_C=42`, `leg_shank_bend=175`, `leg_B_x=46`, `leg_B_z=34`, `leg_hip_hmin=101`, `leg_hip_hmax=289`,
`thigh_y0=93`, `thigh_t=10`, `thigh_depth_stop=56`, `thigh_depth_K=30`, `thigh_wall=3`, `thigh_stop_r=73`, `thigh_stop_up=22`,
`hex_af=26`, `hex_clear=0.15`, `hex_depth=6`, `hex_boss_d=38`, `insert_pcd=15`, `hip_bolt=M4x16`,
`crank_r=40`, `crank_slot=4`, `crank_pin_d=4`, `spring_y=100`, `anchor_x=94.1`, `anchor_z=71.2`, `anchor_slot=5`,
`shank_y0=68`, `shank_t_print=10`, `shank_plate_t=2`, `shank_depth_K=44`, `shank_depth_W=30`, `shank_depth_C=30`, `shank_wall=2.4`, `shank_web=3`, `foot_d=60`, `foot_hole_d=16`, `enc_pocket_d=30.4`, `enc_pocket_depth=8`, `carrier_bolt_pcd=44`,
`coup_y0=108`, `coup_t=14`, `coup_depth=16`, `coup_wall=2.4`, `eye_R=12`, `knee_eye_R=14`,
`pin_d=8`, `bush_id=8`, `bush_od=12`, `bush_L_thigh=10`, `bush_L_shank=12`, `bush_L_coupler=12`,
`stop_pad=10x10x25`, `stop_x=72.3`, `stop_z=12.5`, `bumper_d=10`, `cable_loop_r=20`, `spi_groove_w=5`.
Pose parameters follow layout §1 (`hip_h`, `thigh_ang`, `shank_ang`, `coupler_ang`, `spring_ang`, `spring_len`); the pose table in §2 gives the new values.

## 13. SolidCraft build-step plan (NOT run)

1. New design `cad/parts/leg.solidcraft`; set the §12 parameters (batch `parameters.change`).
2. Sketch the leg plane (XZ) at nominal pose: pins H, K, C, B, W, crank P, stop point, anchor; dimension with the parameters. Verify K, C, W against §2.
3. Thigh: extrude the outline at Y 93–103 → pocket the channel (3 mm wall) → hex socket 26 A/F ×6 → 3 × Ø4.5 bolt holes on Ø15 → boss R14 + bushing bore Ø12 → crank arm + 4 mm slot (Y 94–106) → striker flat. Cover plate as a second body.
4. Shank: extrude outline at Y 68–78 → pocket the channel with 45° ribs → bores for the knee and C bushings → foot Ø60, Ø16 hole, Ø30.4 × 8 pocket, 4 × M4 hex pockets on Ø44 → SPI groove, cable slots. Al plate: same outline, Y 78–80.
5. Coupler: bar + two R12 eyes, bores Ø12.
6. Pins, bushings, hex bolts, TPU pad, tower bracket as bought/sheet parts.
7. Assemble at three poses using §2 values; measure ≥ 1.5 mm spring ↔ B, ≥ 5 mm shank ↔ ring, depth ≤ 302 (nominal).
8. Mirror for the right leg (STL mirrored in the slicer for the channel and cover); export STEP + STL under `exports/`.

## 14. Open questions

- **OQ-1 (Theory/Mechanical):** spring ↔ B pin −0.3 mm (Ø8) at crouch. Shift B 3 mm down (re-verify the 101–289 range, transmission angle 35°) or the spring anchor, or cantilever the B pin from the outboard side.
- **OQ-2 (Structural):** knee/C 24 mm offset couple (≈ 48 Nm in LC-D). Run a 3-D FEA, or replace with a shank yoke straddling the thigh at the knee (double shear, pin Ø8 bending SF 4.5).
- **OQ-3 (Manager):** depth 301.8 / 323 mm with R12 eyes; leg mass +76 g/robot vs 254 g (net +24 g after the lighter hardware).
- **OQ-4 (Structural):** LC3 side-fall lateral load is assumed 300 N (SF 1.25 on the Al plate). Provide a real value.
- **OQ-5 (Materials):** PAHT-CF modulus E ≈ 5 GPa assumed; confirm on a coupon with the bushing press-fit and insert tests (O16).
- **OQ-6 (BOM):** replace the 608/688 bearings and Ø8 × 30 pins with bushings and Ø8 × 44/58/70 pins; add Al plate, tower bracket and TPU pads.
- **OQ-7 (Electrical):** 3 phase AWG 16 + SPI routing; SPI shield grounding at the body end.
- **OQ-8:** spring tower is 37 mm outside the body front (x 122); layout/body must carry it.

---

# Rev 1 addendum (supersedes conflicting rev 0 values) — Manager update + client "weight and size are not a problem"

**Rules now:** no mass cuts (ignore the §11 cuts and the mass target; just report the final mass); width 300 and depth 300 are soft. Load cases are **structural.md §3 S1–S13** (S4 = LC-B, S5 = LC-D, S3 = LC-C, S6 = slide add-on 0.8 × axle, S7 = side fall, S9 = stall, S10 = push-off, S1 = spring creep 24 h at 50 °C). Open question OQ-4 (side-fall load) is now S7; use the structural.md value when derived.

## R1. Thigh = hub between two hip bearings
- Hip output now has two bearings: 6806 inboard (y ≈ 87.5) and a second on the **outboard arch stub at y ≈ 108** (spacing ≥ 21 mm). The thigh hub (Ø42 × 10, y 93–103) sits **between** them; the hex drive passes through the thigh plane, and the stub shaft (Ø30 seat) runs on through the hub bore on a clearance of 0.5 mm (the thigh must not touch the stub).
- **Hex socket: steel-lined.** 1.5 mm 304/ 4140 hex sleeve (26 A/F inner, 29 A/F outer, 10 long) pressed and epoxied into a PAHT-CF hub (hub OD 44, wall 7.5). PETG is banned (SF 0.78). Bearing on the flats ≈ 5.5 MPa at 20 Nm in steel, 3 × M4 × 16 washers unchanged. Fits S9/S10 (17.3 Nm) with SF > 5.
- **Arch clearance (new, check in CAD):** the stub arch must cross y 93–108 outside the swept thigh/crank envelope. The crank (r 40) sweeps only 74°; place the arch legs on the unswept sector (hip-rel below-front of the housing, r ≥ 46) and keep ≥ 3 mm from the spring (y 93.5–106.5) and the B pin. Coupler (y 108–122) is 57 mm from H, so the stub end (y 108) is clear of it.

## R2. Stronger sections (SF vs structural.md S1–S13, allowable 45.5 static, 19.5 fatigue)
| Part | Rev 1 section | Result |
|---|---|---|
| Thigh | Y 10, depth 60 at stop station, wall 4, taper to 34 at K, hub OD 44 | Z 5219 mm³, S5 σ 18.5 MPa, **SF 2.46**; S3 fatigue SF ≈ 3.5 |
| Shank | printed web 3 / wall 3, depth 44 → 32 at W, **Al plate 3 mm** (6061-T6; stiffness share 78 %) | S5 + S6: Al σ 88 MPa, **SF 2.7** on yield; printed SF 6.1; S7 at 300 N (placeholder) Al SF **1.47** |
| Coupler | Y 14 × 16, wall 3.2, **eye R14** (depth grows 2 mm: nominal ≈ 304 mm, crouch ≈ 325 mm, soft) | lug (ligament 8, Kt 2.5) **SF 2.1**; buckling SF > 5 |
| Pins | Ø8 → **Ø10 h6 steel**, bushings ID 10 × OD 14 × L 12 | pin bending (offset couple) ≈ 246 MPa, **SF 4.5** on 1100; bushing p 17–20 MPa |
| Spring clevis and tower | ears 5 mm, tower Al 4 mm, Ø5 pin | bearing 90 / (5 × 5) = 3.6 MPa; S1 creep: steel pin in Al, no plastic in the anchor path |

Ø10 pin/R14 eyes make OQ-1 worse (spring ↔ B clearance ≈ −1.3 mm at crouch): fix by moving B 3 mm down or the anchor (OQ-1), now a required step. Offset-couple OQ-2: because mass is free, **choose the shank yoke straddling the thigh at the knee** (inboard ear y 68–80, outboard ear at y 116–124 on a 3 mm Al bridge strap along the C arm), so the knee pin is in double shear. Structural confirms.

## R3. Mass (reported, not capped)
Printed per leg ≈ thigh 58 + shank 46 + Al plate 69 + coupler 40 ≈ 213 g; hardware ≈ 55 g. Both legs ≈ 0.54 kg vs 254 g budget (+0.29 kg, estimate ±15 %).
