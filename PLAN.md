# Wheel-Legged Balance Robot — Master Plan (rev 0)

Manager: Claude (Engineering Manager). Status: **rev 2 — Gate B approved; P2 master layout in progress; client asked to continue to the end.**

## 1. Requirements (from Requariment.txt)
| # | Requirement | Design target we will use |
|---|---|---|
| R1 | Size ~50 cm tall × 30 cm | Envelope 500 (H, legs extended) × 300 (W) × ≤300 (D) mm |
| R2 | Mass 3–4 kg | Target 3.6 kg, hard limit 4.0 kg |
| R3 | Speed ≥ 10 km/h | Design for 12 km/h (20 % margin) |
| R4 | Jump up to 20 cm | Wheel clearance 20 cm, legs + springs ("snappers") |
| R5 | Climb with a single leg on uneven ground | Independent L/R legs, roll compensation ±10 cm |
| R6 | Lidar mapping, map sent to team | Lidar on top, 360° clear view; Pi 4 does SLAM, Wi-Fi out |
| R7 | All 3D printed, room for every part | PLA/ABS/PETG structure, TPU tyre, closed electronics bay |
| R8 | CoM in the middle | CoM on the mid-plane (L/R) and over the wheel axle at nominal stance; batteries on an adjustable rail to trim it |

## 2. Fixed interface data (from datasheets in this folder)
- **Motor Eaglepower 8308** (×4): Ø92 × 28.5 mm. Stator side 4×M4 on Ø40. Rotor side 4×M3 on Ø40. Shaft adapter Ø31 with 4×Ø3.
- **Driver MKS XDrive Mini** (×4): 63 × 58 mm, 6×Ø3.3 holes, pattern 56.6 × 51.5 mm (mid holes 24 / 27.5 mm).
- Raspberry Pi 4 (85 × 56, holes 58 × 49, M2.5), ESP32 on custom PCB, Pi Camera, Lidar LD19/LD06, 2× 3S LiPo in series = 6S 22.2 V. Printer Bambu A1 (256³ mm).

## 3. Architecture (Ascento / reference-image style)
- **4 motors = 2 hip + 2 wheel.** Hip motor drives the leg through a 4-bar linkage (thigh + coupler + shank), wheel at the end of the shank.
- **Snappers:** spring pack between body and thigh, preloaded when the leg folds → released for the jump.
- **Gearboxes (3D printed):**
  - Hip: 2-stage or compound planetary, first estimate ~9:1 (high torque for jump/holding).
  - Wheel: single-stage planetary, first estimate ~4:1, inside the wheel hub.
- **Wheel:** PLA/ABS hub with castellated rim tabs (like Image #1) → TPU tyre with matching inner slots = plug-and-play, no glue. Tyre has through-holes (airless cells) for grip/compliance. Wheel Ø ≈ 160–180 mm (fits Ø92 motor + gearbox).
- **Body:** closed shell, side plates carry hips. Inside: batteries low and central (on rail for CoM trim), 4 drivers near their motors (short phase wires), Pi 4 + ESP32 PCB in middle, Lidar on top mast, camera on front.

## 4. First-pass numbers — SUPERSEDED, NOT CONFIRMED (rev 0 only; P1 replaces them)
- 12 km/h with Ø170 wheel → 375 wheel rpm. KV≈90 was an **assumption, not a confirmed value** — P1 must verify from a source.
- Jump 20 cm, 4 kg → 7.9 J potential energy, ~16 J at 50 % efficiency.
- Mass estimate 3.95 kg — **rejected by client as too close to 4 kg**; P1 must rework it with margin.

## 4b. P1 scope (client conditions, 2026-11-04)
| # | Item | Owner |
|---|---|---|
| 1 | Verify Eaglepower 8308 specs (KV variants, Kt, R, mass, max current/power) with sources | Robot Theory |
| 2 | Wheel gearbox: compare 4:1, 5:1, 6:1 on real motor data (top speed, wheel torque, balance-recovery torque) | Robot Theory |
| 3 | Hip torque, spring rate, preload, max compression, landing loads | Robot Theory (+ Structural for loads) |
| 4 | Hub-motor drawbacks: unsprung mass, wheel inertia, effect on jump/balance; compare vs body+belt | Robot Theory |
| 5 | Mass budget rework with ≥10 % margin below 4 kg | BOM / Requirements |
| 6 | 3D-printed planetary gear strength/durability; where metal gears, pins, shafts are needed | Materials + Structural |
| 7 | MKS XDrive Mini: voltage range vs 6S full charge 25.2 V, regen braking/over-voltage, motor compatibility | Electrical |
| 8 | Battery safety, power distribution, fusing, e-stop, BEC for Pi/ESP32 | Electrical |
| 9 | Control architecture, IMU, encoders, state estimation, jump coordination, balance sim plan | Robotics & Control |

Output of P1: `docs/design_targets.md` (frozen numbers) + one report per engineer. Every report has sections **Assumptions / Calculations / Sources / Open questions / Changes to design assumptions.**

## 5. Team (sub-agents) and what each delivers
| Engineer | Delivers (file) | Can spawn sub-engineers |
|---|---|---|
| Robot Theory Eng. | gear ratios, wheel Ø, spring rate, jump/speed calc, CoM target → `docs/analysis/theory.md` | — |
| BOM / Requirements Eng. | full BOM incl. bearings/screws/springs, mass budget, requirement trace → `bom/bom.md` | — |
| Materials Eng. | material + print settings per part, inserts, TPU shore → `docs/analysis/materials.md` | — |
| Mechanical Design Eng. | SolidCraft master layout, then parts → `cad/` | Gearbox, Wheel+Tyre, Leg+Spring, Chassis designers |
| Structural Eng. | load cases (landing 3–5 g, jump, fall), stress/safety factor per part → `docs/analysis/structural.md` | — |
| Thermal Eng. | motor/driver heat, PLA softening (~55 °C), vents, driver placement → `docs/analysis/thermal.md` | — |
| Robotics & Control Eng. | balance control (LQR/PID), IMU, encoders, state estimation, motor control loops, jump coordination, simulation → `docs/analysis/control.md` | Simulation engineer |
| Electrical Eng. | battery safety, driver compatibility, power distribution, protection (fuse, e-stop, regen clamp) → `docs/analysis/electrical.md` | — |

**Communication rule:** every instruction from the client goes to `DECISIONS.md` first; every engineer must read it before starting and re-check it before finishing.

**CAD rule:** SolidCraft is one shared session → CAD work runs **one designer at a time** (analysis engineers can run in parallel).

**Vendor models rule (client):** bought parts use downloaded 3D models (GrabCAD, manufacturer, McMaster…) from `cad/vendor/`, listed in `cad/vendor/SOURCES.md`, with dimensions checked against the datasheet.

## 6. Phases & gates
1. **P0 Plan** (this file) + client answers → **Gate A: client approves plan.**
2. **P1 Engineering calculations** (scope 4b) — Theory, Electrical, BOM, Materials+Structural, Control in parallel → `docs/design_targets.md`. **Gate B: client reviews and approves. NO detailed CAD before Gate B.**
3. **P2 Master layout** in SolidCraft (parameters: envelope, hip position, wheel Ø, leg lengths, battery position) + CoM check. **Gate C: client sees screenshot.**
4. **P3 Detail parts** (sequential): gearboxes → wheel + TPU tyre → legs + springs → body/electronics bay → lid/lidar mast.
5. **P4 Analysis** — Structural + Thermal review the CAD, fixes loop back to P3.
6. **P5 Balancing simulation** — model with real masses/inertias from CAD, tune controller, test disturbances; then legs-fixed hop sim.
7. **P6 Prototype testing (staged, jumps last):** 6a gearbox bench test → 6b wheels-only balancing on a tether → 6c driving + speed test → 6d leg height change / single-leg climb → 6e small hops (5 cm) → 6f full 20 cm jump. Each stage has a pass criterion before the next.
8. **P7 Release** — final BOM, mass/CoM report, STL + STEP exports, assembly screenshots, test report.

## 7. Project structure
```
Balance Robot with AI/
├── PLAN.md                ← this file
├── DECISIONS.md           ← client instructions log (read by all engineers)
├── Requariment.txt, BOM File.txt, datasheet images (inputs, untouched)
├── docs/design_targets.md ← P1 frozen numbers (Gate B)
├── docs/analysis/         ← theory, electrical, control, materials_gears, structural, thermal (.md)
├── bom/                   ← bom.md (+ mass budget)
├── cad/parts/             ← one SolidCraft design per part
├── cad/assembly/          ← master layout / full assembly
└── exports/stl, exports/step
```

## 8. Top risks
1. Mass ≈ 4 kg limit (4 big 8308 motors). Mitigation: infill/topology, lighter lidar, battery size.
2. 3D-printed gears under jump/landing shock. Mitigation: herringbone gears, PETG/PA, wide face, steel pins.
3. Speed needs the higher battery voltage (see question 1).
4. Unsprung mass at the wheel (hub motor) hurts jumping.
