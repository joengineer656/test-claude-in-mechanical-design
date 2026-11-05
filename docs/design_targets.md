# Design Targets — rev 2 — FROZEN (Gate B approved by client 2026-11-04)

Sources: docs/analysis/{theory, electrical, control, materials_gears, thermal, mass_budget}.md, bom/bom.md. Every value traces to one of these (see their Sources sections). Calc scripts: docs/analysis/calc/.
Any change to a number here must be logged in DECISIONS.md first.

## 1. Headline
1. **Mass: client accepts 4.31 kg** (requirement changed from 3–4 kg). Low-cost cuts (A) are still encouraged but not required.
2. **Motors:** hips 8308 KV130 + 8:1; wheels T-Motor MN5008 KV170 + 3.5:1. 12 km/h at low battery with balance headroom.
3. **Jump:** 8 J springs kept. Sim 35 cm (with springs) → real ≈ 28 cm (sim done at 3.6 kg — re-run at 4.31 kg, O13).
4. **6S** safe for MKS XDrive Mini; 2 brake resistors.
5. **Heat:** aluminium finned stator carrier in each wheel hub; 40 mm fan + vents; hubs in **PETG**.
6. **All gears PAHT-CF**; metal pins, bearings, axles.

## 2. Target numbers
| Item | Target | Source |
|---|---|---|
| Envelope | 500 H × 300 W × ≤300 D mm | requirement |
| Mass | ≤4.31 kg (client accepted) | client |
| Hip motor | Eaglepower 8308 **KV130** ×2, Ø92×28.5, stator 4×M4 on Ø40, rotor 4×M3 on Ø40; Kt 0.0636 Nm/A | client, theory |
| Wheel motor | **T-Motor MN5008 KV170** ×2, 128 g, Ø55.6×32, 6 mm shaft, 14 pole pairs, **R 270 mΩ** (official T-Motor drawing; "720" was max power 720 W). Rotor 8×M3 on Ø12/Ø18, stator 4×M3 on Ø25 | client, theory |
| Wheel | Ø170 mm, hub **PETG**, TPU tyre with plug-and-play slots (hub tabs) + lattice holes | client, thermal |
| Wheel gearbox | **3.5:1**, sun 24 / planet 18 / ring 60, m1.25 herringbone 20°, b = 12 mm, ring OD ≈ 86, PAHT-CF, Ø5×20 hardened pins, 2×685ZZ per planet, axle bearings carry all radial load | materials |
| Hip gearbox | **6:1 compound stepped planet (rev 2.2)**: sun 28 T m1.0 → planet 40 T m1.0 (b14); planet 18 T m1.5 → fixed ring 63 T m1.5 b20; 3 planets; PAHT-CF; 6806 ×2; steel inserts; hip peak 13 Nm @40 A | materials 6:1 option, theory |
| Hip torque | standing 2.3, climb 5.3, cont 5.7 Nm (6.5 with 3 mm Al plate), peak 17.3 Nm | theory, thermal |
| Current limits | hip 20 A (**40 A push-off mandatory for 20 cm jump**, only in push-off, ≤1 jump/10 s); wheel 15 A ≤3–5 s, ~5 A cont (≈7 A with finned carrier) | materials, thermal |
| Leg 4-bar | thigh 121, knee→wheel 189, coupler 113, knee→coupler pin 42 mm; hip 100–290 mm above axle | theory |
| Springs | 1 extension spring/leg, 2.7 N/mm, 2 mm music wire, OD 13, ~45 coils, free ≈110 mm, 8 N preload, 122 N max @42 mm, **5.5 J total** (client chose 8 J — flagged), body anchor (94.1, 71.2) mm from hip, 40 mm crank, anchor pins 180 N | theory P3 re-fit |
| Landing rules | **TPU end stop ≈10 kN/m engaging at hip height 130 mm above axle, ≥30 mm travel (O13)** → hip gearbox ≤16 Nm, knee pin ≤2.0 kN; spring never anchored on gearbox output; driver fault = phases floating; landing stroke ≥100 mm; rest bumpers | materials, control |
| CoM | over axle ±5 mm fore-aft, ≤5 mm lateral | theory |
| Backlash | wheel ≤1°, hip ≤0.5° | control |
| IMU | ICM-42688-P, ±30 mm of CoM, mid-plane, ≥40 mm from motors/drivers | control |
| Encoders | hips: driver AS5047P + leg-side encoder + crouch hard stop. Wheels: AS5047P/AS5048A breakout at hub, Ø6×2.5 diametric magnet, 1.5 mm gap, Ø30×8 envelope, shielded SPI ≈45 cm, ≥15 mm from phase wires | control, electrical |
| Electronics | 4 drivers in body on 70×70×1.5 Al plate; Pi 4 + heatsink; ESP32 PCB; 40 mm fan ≥3.3 CFM; ≥16 cm² vents in + out; LD19 on top with 360° clear view; Pi cam front | electrical, thermal |
| Battery | 1 × 6S 2200 mAh 50C (~67 min); jump peak ≈72 A / 70 ms | client, electrical |
| Protection | 50 A fuse, anti-spark switch + e-stop, 2 × 2 Ω 25 W brake resistors away from plastic, 10k NTC per motor | electrical, thermal |
| Control | ESP32 1 kHz est / 500 Hz control; CAN 1 Mbit (set manually); Pi 4 SLAM over UART | control |
| Firmware | Makerbase ODrive 0.5.1 fork — never run odrivetool upgrade | electrical |
| Printing | Bambu A1 (256³), hardened nozzle + dryer for PAHT-CF; split parts >250 mm | client |
| Vendor CAD | bought parts from cad/vendor/ (SOURCES.md) | client |

## 3. Mass
| Scenario | Mass |
|---|---|
| All decisions (accepted) | 4.31 kg |
| With optional cuts A | 3.85 kg |
Unsprung 0.536 kg/side.

## 4. Open engineering items (not blocking P2)
- O10 Hip gearbox mass 271 g (BOM) vs 150–200 g (materials) — settle from CAD volume.
- ~~O11~~ CLOSED: Al stator carrier = hollow fixed axle Ø14 bore, magnet + encoder on axis (docs/layout.md).
- ~~O12~~ CLOSED: 270 mΩ (T-Motor drawing).
- ~~O13~~ CLOSED: at 4.31 kg jump 25.5 cm real @19.8 V with springs (19.1 without → springs mandatory); 12 km/h OK; balance recovers 5°/10°, max tilt 43–45°. Fault landing fixed by the softer end stop; wheel gear ultimate raised to 9 Nm (SF ≈1.66, OK).
- O14 Measure on arrival: KV, R, L (≥50 µH), poles, masses, inertia; MN5008 bolt pattern.
- O15 Bench only: current loop rate, encoder CS pin, brake ramp, NTC pin, PAHT-CF print quality.
- O16 Unverified estimates: fatigue derates, insert pull-out, thermal resistances ±30–50 %, printed masses ±15 %.
