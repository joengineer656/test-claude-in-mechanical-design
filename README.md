# Test Claude in Mechanical Design — 2-wheel wheel-legged balance robot

A graduate-project mechanical design of an Ascento-style wheel-legged balance robot (4-bar legs, extension springs for the jump, 3D-printed planetary gearboxes), produced by Claude acting as an engineering manager with sub-agent engineers, modelled in SolidCraft.

**Status: PAUSED by the client (decision A16).** This is a design in progress, not a release. Nothing has been printed or tested on hardware.

## Requirements (Requariment.txt, BOM File.txt)
~500 × 300 mm, 3–4 kg (client later accepted growth), ≥10 km/h, jump up to 20 cm, single-leg climbing, lidar mapping, everything 3D printed. 4× Eaglepower 8308 motors, 4× MKS XDrive Mini drivers, ESP32 + Raspberry Pi 4, LiPo, lidar, Pi camera.

## Where things are
| Path | Content |
|---|---|
| `PLAN.md` | master plan and phases |
| `DECISIONS.md` | every client decision and manager decision (A1–A16), the log all engineers read |
| `DISCUSSION.md` | summary of the client ↔ manager ↔ agents conversation |
| `docs/design_targets.md` | frozen P1 numbers (rev 2, later edits are in DECISIONS.md) |
| `docs/analysis/` | theory, electrical, control (incl. staged test plan §3.7), materials/gears, thermal, structural, mass; `calc/` has the Python scripts |
| `docs/parts/` | spec per part: body, wheel, leg, hip gearbox, interfaces |
| `docs/assembly.md` | assembly interference/CoM report (rev 0 and rev 1) |
| `docs/layout.md`, `docs/screenshots/` | layout and renders |
| `bom/` | bill of materials and mass |
| `cad/parts/`, `cad/assembly/` | SolidCraft designs and the Python builders in `src/` |
| `exports/stl`, `exports/step` | printable STL and STEP (assembly STEP is gzipped: `robot_assembly.step.gz`) |
| `cad/vendor/SOURCES.md` | where bought-part 3D models come from |

## Key numbers (see docs for sources)
Hips: Eaglepower 8308 KV130, 6:1 printed planetary (PAHT-CF). Wheels: T-Motor MN5008 KV170, 3.5:1, Ø170 PETG hub + TPU tyre. Leg 4-bar with spring 3.5 N/mm, 15 N preload. 6S LiPo, 50 A fuse. Mass ≈ 6.3–6.9 kg. Simulated (not tested): balance and 12 km/h pass; jump ≈ 21 cm from 22.2 V at rest, ≈ 19.5–20 cm from 20.5 V.

## Known open issues
- Assembly rev 1: M3 (hex sleeve rotation), M13 (Pi vs hip plates), extension stop travel, front cover lip, M16 undecided (docs/assembly.md).
- Structural rev 2 changes (C1–C11, docs/analysis/structural.md): the leg parts are updated (rev 2b); the body/gearbox/tie updates were **interrupted** and those files may be half-applied. The assembly does not yet include rev 2b leg masses (+~0.3 kg per leg).
- Hand calculations only, no FEA. Thermal re-review skipped by the client (A11).
- Spring is thin on margin (SF 1.19 wire, hooks weaker): bench-test before use.
- All masses/thermal numbers are estimates; PAHT-CF print quality and M4 insert pull-out are untested.
- Large third-party vendor STEP files and the 128 MB assembly STEP are not committed (`.gitignore`); build scripts regenerate them.

## Tools
CAD: SolidCraft (`solidcraft-cli`, scripts in `cad/*/src/`). Python 3 for calculations.
