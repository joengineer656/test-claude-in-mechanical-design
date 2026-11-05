# Bill of Materials — Wheel-Legged Balance Robot (P1, rev 2)

Owner: BOM / Requirements Engineer · Date: 2026-11-04 · Phase P1 (no CAD).
Companion: `docs/analysis/mass_budget.md`.

Inputs:
- DECISIONS.md
- design_targets.md
- theory.md "P1 follow-up (O9)"
- **electrical.md "P1 follow-up (O9)" (final)**
- **materials_gears.md "P1 follow-up (O9 wheel gear)" (final)**
- **thermal.md (final)**

Rows marked **MAY CHANGE** are estimates or depend on the open items in §5.

**Headline:** the rev-2 bottom-up total is **4.31 kg**. That is **712 g over the 3.6 kg target and 312 g over the 4.0 kg hard limit**.
- The lighter wheel motors save 416 g against rev 1.
- Most of that is used up again by three things:
  - the larger compound hip gearbox: +96 g printed per hip vs rev 1
  - the 6S 2200 pack: +110 g vs 2 × 1300
  - added parts: hip end stops, hub encoder kits and leg cables, hip encoders, PDB
- Thermal adds **+158 g**: Al hip plates, Al wheel stator carriers with fins, driver Al plates, fan, NTCs, PETG hub.
- Cheap cuts bring it to **~3.85 kg**, and lightening the hip gearbox and legs to ~3.72 kg.
- **≤ 3.6 kg needs a 6S 1500 mAh pack on top of every cut (3.60 kg, no further margin)** (mass_budget §5).

## 1. Full BOM (rev 2)

| # | Subsystem | Item / spec | Qty | Unit (g) | Mass source | Total (g) | Supplier | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | Hip actuators | Eaglepower 8308 **KV130** (hip) | 2 | 336 | [S1] 336 g (KV90 listing; 325–350 g) | 672 | [link](https://www.technobotix.in/products/eagle-powor-la-8308-kv90-motor/1781252000000073016) | Client: KV130. KV130 mass not separately published; same frame assumed. MAY CHANGE ±14 g |
| 2 | Hip actuators | Printed hip gearbox, compound stepped-planet 8:1, **all PAHT-CF** (housing touches the can — Thermal) | 2 | 185 | calc §3 mass_budget | 370 | print in-house | Materials O3 geometry; Materials range 150–200 g incl. bearings. MAY CHANGE |
| 3 | Hip actuators | Al 6061 hip motor mount plate 3 mm (Ø100, 50 % lightened), doubles as the hip-driver heat plate | 2 | 32 | calc 2.7 g/cm³ | 64 | local CNC / laser | Thermal §4 item 4 |
| 4 | Hip actuators | Bearing **6906-2RS 30×47×9** (hip output bearing 1; was 6808 in rev 0 and 6806 until A13/C7; C0 about 5 kN) | 2 | 45 | catalogue ~45 g (6806 was 19 g) | 90 | any | A13 C7; +26 g per side vs 6806. Leg outer bearing stays 6806 (leg.md) |
| 5 | Hip actuators | Bearing 6803-2RS 17×26×5 (carrier inner) | 2 | 8 | estimate | 16 | any |  |
| 6 | Hip actuators | Bearing 685ZZ 5×11×5 (2 per stepped planet) | 12 | 2 | estimate | 24 | any | Materials O3 |
| 7 | Hip actuators | Planet pin hardened dowel Ø5×30 (ISO 8734) | 6 | 4.6 | calc steel 7.85 g/cm³ | 28 | Misumi/McMaster |  |
| 8 | Hip actuators | Steel sun pinion option (MOD1.25, 18T) | 2 | 8 | estimate | 16 | Misumi/KHK | only if bench test shows wear. MAY CHANGE |
| 9 | Hip actuators | Hip leg-side absolute encoder (magnetic breakout, e.g. AS5600/AS5047 class) + magnet + holder + cable | 2 | 8 | estimate | 16 | TBD (Electrical/Control) | Client decision; part not chosen. MAY CHANGE |
| 10 | Hip actuators | TPU hip end stop, ≥20 mm travel, ≤25 kN/m (O4a) | 2 | 10 | estimate | 20 | print in-house |  |
| 11 | Wheel modules | T-Motor **MN5008 KV170** (hub) | 2 | 128 | [S9] 128 g incl. cable | 256 | [link](https://store.tmotor.com/goods.php?id=999) | Ø55.6×32, 6 mm shaft, 270 mΩ, 15 A peak |
| 12 | Wheel modules | Wheel gear core 3.5:1 **24/18/60** m1.25 b12 PAHT-CF (sun, 3 planets, ring insert) + 6× 685ZZ + 3× Ø5×20 hardened pins + fasteners; carrier integrated in hub | 2 | 72 | Materials O9: 65–80 g integrated | 144 | print in-house + Misumi/any | standalone carrier/housing would be ≈110 g (+38). MAY CHANGE |
| 13 | Wheel modules | Stator mount sleeve PETG (ring around motor axis, holds ring insert; axis kept free for encoder) | 2 | 16 | calc 15 cm³ × 0.85 × 1.27 | 32 | print in-house | Electrical O9-b: no solid axle through the axis |
| 14 | Wheel modules | Wheel bearings 6806-2RS 30×42×7, 2 per wheel, span ≥20 mm | 4 | 19 | estimate (catalogue-typical) | 76 | any | carry all radial load ≤312 N (Theory) |
| 15 | Wheel modules | Wheel hub **PETG** (ASA preferred), castellated rim (= planet carrier) | 2 | 87 | calc rev 1 × PETG density | 174 | print in-house | Thermal: PLA rejected. ASA would be 73 g (−14) |
| 16 | Wheel modules | Al 6061 stator carrier 3 mm + finned cap ≥200 cm² (leg side) | 2 | 30 | Thermal est. 25–35 g | 60 | local CNC | unsprung; CONFLICT: Thermal keys it to a steel axle, Electrical needs a free motor axis |
| 17 | Wheel modules | TPU tyre Ø170/Ø146×25, 40 % voids | 2 | 110 | Materials §7 | 220 | print in-house |  |
| 18 | Wheel modules | Wheel fasteners (motor mount, hub) | 2 | 10 | estimate | 20 | any |  |
| 19 | Wheel modules | Hub encoder kit: AS5047P/AS5048A breakout + Ø6×2.5 diametric magnet + holder, non-magnetic M2 | 2 | 6 | Electrical O9-d est. | 12 | any | unsprung |
| 20 | Legs L+R | Printed leg set PETG (thigh 121, shank 189, coupler 113, rocker, spring mounts) | 2 | 127 | calc rev 1 × PETG density | 254 | print in-house | ½ shank counted unsprung by Theory (25 g) |
| 21 | Legs L+R | Bearing 608-2RS (knee) | 4 | 12 | estimate | 48 | any | knee pin 1572 N worst case |
| 22 | Legs L+R | Bearing 688-2RS / F688 (other 4-bar joints) | 12 | 3.5 | estimate | 42 | any |  |
| 23 | Legs L+R | Joint pin steel Ø8×30 / shoulder bolt | 8 | 12 | calc | 96 | Misumi |  |
| 24 | Legs L+R | Extension spring, 2.7 N/mm, 8 N preload, 146 N max, 52 mm stroke (4 J/leg) | 2 | 35 | estimate from energy | 70 | Lee Spring / custom | Theory recommends trying a 4 J-total spring first (~20 g). MAY CHANGE |
| 25 | Legs L+R | Retaining rings / shims | 16 | 0.5 | estimate | 8 | any |  |
| 26 | Legs L+R | TPU rest bumpers | 2 | 3 | estimate | 6 | print in-house |  |
| 27 | Body | Printed body set (side plates, tray, covers, brackets, lidar mast) | 1 | 282 | calc rev 1 | 282 | print in-house |  |
| 28 | Body | Battery strap + padded cradle foam | 1 | 15 | estimate | 15 | any |  |
| 29 | Electronics | Raspberry Pi 4 + heatsink | 1 | 56 | [S6] 46 g + 10 g est. | 56 | [link](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) |  |
| 30 | Electronics | microSD | 1 | 0.5 | estimate | 0 | any |  |
| 31 | Electronics | ESP32 custom PCB (Pi-HAT size) with **ICM-42688-P** IMU, CAN transceiver | 1 | 25 | Electrical est. | 25 | JLCPCB/PCBWay | IMU ±30 mm from CoM, ≥40 mm from motors |
| 32 | Electronics | Pi Camera (v2/v3) + ribbon | 1 | 7 | Electrical 3–4 g + ribbon | 7 | [link](https://www.raspberrypi.com/products/camera-module-3/) |  |
| 33 | Electronics | Diametric magnet Ø6×2.5 (hip motors) | 2 | 1 | estimate | 2 | any |  |
| 34 | Power | Electronic anti-spark switch 6S ≥100 A | 1 | 18 | Electrical est. | 18 | any |  |
| 35 | Power | E-stop latching mushroom 22 mm | 1 | 30 | Electrical est. | 30 | any |  |
| 36 | Power | Power distribution board (bus bars, TVS SMDJ26A, 470 µF, sense, 3 A fuse) | 1 | 25 | Electrical est. | 25 | custom |  |
| 37 | Power | 5 V buck Pololu D36V50F5 | 1 | 7 | Electrical est. | 7 | [link](https://www.pololu.com/product/4091) |  |
| 38 | Electronics | MKS XDrive Mini — **all 4 in the body** (hips coaxial on 8308; wheels on body plate) | 4 | 40 | estimate (no published mass) | 160 | [link](https://makerbase3d.com/product/makerbase-xdrive-mini-high-precision-brushless-servo-motor-controller-based-on-odrive3-6-with-as5047p-on-board/) | Electrical O9-b |
| 39 | Electronics | Al heat plate 70×70×1.5 mm + 1 mm thermal pad (wheel drivers) | 2 | 21 | calc 7.35 cm³ × 2.7 + pad | 42 | Al sheet | Thermal: needed for the wheels if the body is sealed; mandatory for the hips (covered by the hip mount plate) |
| 40 | Electronics | 40 mm 5 V fan ≥3.3 CFM + 2 mesh vent grilles | 1 | 15 | estimate | 15 | any | Thermal §4 item 5 |
| 41 | Electronics | 10 k NTC B3950 in stator end-turns (×4 motors) + NTC on the brake resistors (×2), with leads | 6 | 1.5 | estimate | 9 | any | wheel NTC leads add a pair to each leg cable |
| 42 | Electronics | LD19 lidar + cable | 1 | 52 | [S5] 47 g + 5 g | 52 | [link](https://www.robotshop.com/products/dfrobot-dtof-ld19-laser-lidar-sensor-kit-12m) |  |
| 43 | Power | **LiPo 6S 2200 mAh 50C**, XT60 (single pack) | 1 | 350 | Electrical O9-d est. 330–360; sourced range 261–370 g [S10] | 350 | e.g. SLS XTRON / Overlander / Dualsky | Client decision. MAY CHANGE ±30 g by brand |
| 44 | Power | Brake resistor 2 Ω 25 W Al-clad (Arcol HS25 2R0), **hip boards only** | 2 | 10 | Electrical est. | 20 | [link](https://www.arcolresistors.com/) | Electrical O9-c: 4 → 2 |
| 45 | Power | Main fuse MAXI **50 A** slow + inline holder | 1 | 15 | Electrical est. | 15 | Littelfuse 299 | was 60 A |
| 46 | Wiring | Shielded encoder cable 4-pair 28 AWG, 0.45 m (per leg) | 2 | 13.5 | Electrical O9-d | 27 | any | ½ counted unsprung |
| 47 | Wiring | Phase extension 3× 18 AWG high-flex, 0.45 m (per leg) | 2 | 15 | Electrical O9-d | 30 | any | ½ counted unsprung |
| 48 | Wiring | Remaining harness: 12/14/18/20 AWG, CAN, XT60/XT30, heat-shrink | 1 | 110 | Electrical O9-d est. | 110 | any |  |
| 49 | Fasteners | M4×10 (8308 stator, 4/motor) | 8 | 1.9 | estimate | 15 | any |  |
| 50 | Fasteners | M3×8 (8308 rotor, 4/motor) | 8 | 0.9 | estimate | 7 | any |  |
| 51 | Fasteners | M3×25 (hip gearbox housings, 8/gearbox) | 16 | 1.7 | estimate | 27 | any |  |
| 52 | Fasteners | M3×10 (body, legs, drivers, brackets) | 90 | 1 | estimate | 90 | any |  |
| 53 | Fasteners | M2.5×6 + nylon standoffs | 12 | 0.6 | estimate | 7 | any |  |
| 54 | Fasteners | M3 nyloc nuts | 36 | 0.35 | estimate | 13 | any |  |
| 55 | Fasteners | M3 washers | 50 | 0.15 | estimate | 8 | any |  |
| 56 | Fasteners | Heat-set insert M3×5.7 | 120 | 0.35 | estimate | 42 | Ruthex-type |  |
| 57 | Wiring | Thermal pads, labels, zip ties | 1 | 10 | estimate | 10 | any |  |
| | | **TOTAL rev 2** | | | | **4312** | | |

Subsystem totals (g): Hip actuators 1278 · Wheel modules 994 · Legs L+R 524 · Body 297 · Electronics 368 · Power 465 · Wiring 177 · Fasteners 209 · **Total 4312 g**.

**Unsprung mass per side: 0.536 kg.** This is the wheel module plus ½ of the shank plus ½ of the leg cables. All drivers are in the body.

| Part | g |
|---|---|
| MN5008 | 128 |
| Gear core | 72 |
| PETG stator sleeve | 16 |
| Al stator carrier + finned cap | 30 |
| 2 × 6806 | 38 |
| PETG hub | 87 |
| Tyre | 110 |
| Fasteners | 10 |
| Encoder kit | 6 |
| ½ cables | 14 |
| ½ shank | 25 |
| **Total** | **536** |

Theory's jump and landing figures used 0.465 kg, so the bottom-up value is **+71 g per side**. With the cheap cuts (tyre, rim, ASA hub, sleeve merged into the Al carrier) it falls to **≈ 0.44 kg**.

Not on the robot: 6S balance charger, 8 g cell-checker buzzer (tests only), LiPo bag, bench PSU (with brake resistor fitted), USB-UART, spare magnets/bearings, and filament: PAHT-CF (needs a dry box and hardened nozzle), PETG, PLA, TPU 95A.

## 2. BOM inconsistencies and gaps

| # | Issue | Status rev 2 |
|---|---|---|
| I1 | "Lipo battery 12v x2" was ambiguous | **Resolved by client:** one 6S 2200 mAh 50C pack (25.2 V full). No published mass for a 50C pack; sourced 6S 2200 packs weigh 261–370 g. 350 g is used (Electrical). |
| I2 | No IMU | **Resolved:** ICM-42688-P on the ESP32 PCB. |
| I3 | No brake resistors | **Resolved, but changed:** the client asked for 4 × 2 Ω 25 W. Electrical O9-c **fits 2, on the hip boards only**, because the voltage-based ramp protects the shared bus. The client should acknowledge the change. Must be verified by the P6a disconnect test. |
| I4 | No fuse/switch/e-stop/5 V | **Resolved:** 50 A MAXI slow fuse (was 60 A), anti-spark switch, e-stop, PDB, Pololu D36V50F5. |
| I5 | "PCB (ESP32 + Pi 4)" | The ESP32 PCB is Pi-HAT size and stacks on the Pi standoffs. |
| I6 | AS5047P is on the XDrive Mini | **Resolved (Electrical O9-b):** all 4 drivers are in the body. Each wheel hub gets an AS5047P/AS5048A breakout + Ø6×2.5 magnet (6 g), and each leg gets a 0.45 m shielded SPI cable plus a 3 × 18 AWG phase cable. **Open:** the magnet needs access to the MN5008 inboard shaft end. |
| I7 | KV not specified | **Resolved:** hips KV130 (mass taken from the KV90 listing, same frame). Wheels: MN5008 KV170, 128 g. |
| I8 | Hip angle ambiguous through 8:1 | **Resolved:** a leg-side encoder per hip (part TBD, 8 g est.). |
| I9 | Hip gearbox mass | **Open, largest uncertainty.** Materials gives 150–200 g each *including* bearings and pins. The BOM calc from the O3 geometry gives 193 g printed + 86 g metal = **279 g**. The gap is up to ~100 g per hip. |
| I10 | Wheel hub PLA vs PETG/ASA | **Thermal: PLA rejected** (cavity air 66 °C). Hub is PETG minimum, ASA preferred (ASA is 14 g lighter per hub but needs a draft shield on the open A1). **Client approval needed** (DECISIONS said PLA/ABS). |
| I11 | Unsprung mass: Theory 0.465 kg vs BOM 0.536 kg | Control sim and landing loads should use 0.536 kg (0.44 kg if the cuts are taken). |
| I12 | Theory's example teeth 20/15/50 cannot be assembled with 3 planets | Use Materials' **24/18/60** (i = 3.500). |
| I13 | The motor axis must stay free for the encoder, so there is no solid axle through it | Use a PETG stator sleeve + 2 × 6806 around the axis. **Structural must confirm** for 312 N and the side-fall moment. |
| I14 | **Thermal vs Electrical at the hub:** Thermal's Al stator carrier is "keyed to the steel axle", with the finned cap on the leg side. Electrical needs the inboard motor axis free for the encoder magnet and breakout. | Open for Mech (P2). The likely answer is a hollow Al carrier/cap with the encoder inside it; this could also replace the PETG sleeve (−16 g per side). |
| I15 | **MN5008 KV170 resistance:** 270 mΩ (T-Motor/RobotShop) vs 720 mΩ (Robozar listing) | Open. Thermal rejects 720 mΩ (R ∝ 1/KV² from KV340 gives ≈ 0.22 Ω). At 0.72 Ω the sealed-hub limit drops to 2.2 A. **Measure R_ll on arrival (P6a).** |
| I16 | Thermal parts were missing from the BOM | Added: 40 mm fan + vents, Al hip mount plates ×2, Al driver plates, Al wheel stator carriers with fins ×2, 10 k NTC ×4 motors + ×2 brake resistors. The Pi heatsink was already in. |

## 3. Requirement traceability

| ID | Requirement | Satisfied by | Verification | Status rev 2 |
|---|---|---|---|---|
| R1 | ~50 cm × 30 cm | Leg 121/189/113 mm, Ø170 wheels, body ~160 mm wide | Calc, CAD envelope (Gate C) | Open |
| R2 | Mass 3–4 kg, target ≤ 3.6, hard 4.0 | Whole BOM | `mass_budget.md`; weigh parts on arrival; weigh robot (P7) | **FAIL: 4.31 kg.** ~3.85 kg with cheap cuts; 3.60 kg only with every cut + 6S 1500 |
| R3 | ≥ 10 km/h (design 12) | MN5008 KV170 + 3.5:1 + Ø170 | Theory O9: 19.3 km/h loaded; P6c timed run | Pass on paper |
| R4 | Jump 20 cm | 8308 KV130 + 8:1 compound + springs | Theory O9 (25 cm without springs, ideal, at 3.6 kg); sim P5; P6e→f | Must re-run at the real mass and 0.536 kg unsprung (0.44 kg after cuts) |
| R5 | Single-leg climb | Independent hips, 5.3 Nm needed | Sim; P6d | Open |
| R6 | Lidar map to team | LD19, Pi 4, Wi-Fi | Bench SLAM + field test | Open |
| R7 | All printed, room for parts | Printed parts ≤ 250 mm; PAHT-CF gears | CAD fit check | Open. 4 drivers now in the body bay |
| R8 | CoM in the middle | 6S pack on the trim rail; IMU at CoM | CAD mass properties; hang test | Open |
| D1 | Ascento legs + springs | Legs, extension springs 2.7 N/mm | Theory, Structural | In BOM |
| D2 | Printed; TPU plug-in tyre | Hub + tyre | Print / push-fit / slip test | In BOM |
| D3 | Printed gearboxes; metal where needed | Hip 8:1 compound, wheel 24/18/60, both PAHT-CF; steel pins | Materials Lewis (wheel SF 3.3/1.8/fatigue 2.0; hip SF 2.1); P6a coupon + bench | In BOM |
| D5 | 6S + XDrive Mini | 12–56 V in, 60 V FETs; MN5008 compatible (O9-a) | Electrical | Pass |
| D6 | Hub motors + planetary | MN5008 + 3.5:1 in wheel | Theory/Materials O9 | In BOM |
| D7 | Bambu A1 ≤ 250 mm | Largest part Ø170 tyre | CAD bounding box | OK |
| D8 | LD19/LD06 | LD19 47 g | Sourced | OK |
| D9 | No CAD before Gate B | — | Gate | Complied |
| D10 | Verify KV | 8308 KV130, MN5008 KV170 | Measure KV/R/L/mass on arrival (O7) | Open |
| D11 | Hip torque, springs, landing | Hip actuator, springs, TPU end stops | Theory / Materials O3/O4 | In BOM |
| D12 | ≥ 10 % margin | — | `mass_budget.md` | **Not met** (−712 g vs 3.6 kg) |
| T1 | Thermal: ventilated bay, motor NTCs, Al heat paths, no PLA near motors | Fan, vents, Al plates/carriers, NTC ×6, PETG/ASA hub, PAHT-CF hip housing | thermal.md calc; P6a heat run (30 min at 3.5 A, sealed hub) | In BOM |
| D13 | 25.2 V, regen, staged tests | 2 brake R, 50 A fuse, anti-spark switch, e-stop, TVS | Electrical; P6 | In BOM |
| D14 | Documentation | This file + mass_budget.md | Review | Done |
| New | Hip 8308 **KV130** | Hip actuators | Measure on arrival | In BOM |
| New | Wheel **MN5008 KV170** + 3.5:1 | Wheel modules | Theory/Materials O9 | In BOM |
| New | **One 6S 2200 mAh 50C** | Power | Electrical: 72 A jump peak (33 C), ~67 min mixed use | In BOM (350 g est.) |
| New | **PAHT-CF** hip gears, compound 8:1 | Hip gearbox | Materials O3; gear coupon (O6) | In BOM |
| New | 4 × 2 Ω 25 W brake resistors | Power | Electrical O9-c | **2 fitted** (see I3) |
| New | **ICM-42688-P** | ESP32 PCB | Control | In BOM |
| New | Leg-side hip encoder | Hip actuators | Control/Electrical | In BOM (part TBD) |

## 4. Assumptions
- **8308 KV130:** 336 g. Only KV90 has a published mass; the same frame is assumed. **MN5008 KV170:** 128 g including cable (T-Motor store).
- **Hip gearbox:** Materials O3 geometry (ring 63T m1.5, Ø94.5, b20; stepped planets 36/18). PAHT-CF at 1.06 g/cm³ for the gears, PETG at 1.27 g/cm³ for the housing.
- **Wheel gearbox:** Materials O9 integrated design, 65–80 g including 6 × 685ZZ and 3 × Ø5×20 pins. 72 g (mid-range) is used. The carrier is part of the hub.
- **Electrical:** masses from electrical.md O9-d, ≈ 936 g. The BOM also counts the lidar cable, camera ribbon, hip magnets, microSD and wheel-driver body plates, giving 967 g in the same scope.
- **Tyre:** Materials §7 (110 g).
- **Legs:** rev-1 geometry × PETG density.
- **Spring:** 35 g per leg estimated from energy.
- **Thermal parts:** Al at 2.7 g/cm³. Hip plate Ø100 × 3 mm, 50 % lightened (32 g), which also serves as the hip-driver heat plate (Thermal §4 item 4). Wheel Al carrier + fins 30 g (Thermal: 25–35 g). Hip gearbox housing changed to PAHT-CF (Thermal), so the printed hip set is 185 g.
- **Uncertainty:** printed parts ±15 %; estimates not weighed.

## 5. Open questions
1. **Hip gearbox mass (I9):** 150–200 g (Materials) or 279 g (BOM)? This is worth up to ~200 g on the total.
2. **Battery:** if all other cuts are taken, the client must accept 6S 1500 mAh (~250 g, ≈ 45 min mixed) to reach ≤ 3.6 kg. 6S 1800 mAh lands at ~3.61 kg.
3. **MN5008 shaft:** is the inboard shaft end reachable for the magnet? Can the stator sleeve take the wheel loads without an axle? (Mech/Structural, P2.)
4. **Hip leg-side encoder:** part number (Electrical/Control).
5. **Spring energy:** 8 J or 4 J total. Theory recommends designing the anchors for 8 J and fitting a 4 J spring first.
6. **Brake resistors:** the client's 4 vs Electrical's 2. Client to acknowledge.
7. **Weigh on arrival:** 8308 KV130, XDrive Mini, the 6S pack.
8. **MN5008 R_ll:** 270 vs 720 mΩ (I15). Measure on arrival; it sets the hub thermal limit.
9. **Hub heat path vs encoder (I14):** Mech must solve this in P2.
10. **Client approval:** hub in PETG/ASA instead of PLA/ABS.

## 6. Sources
- [S1] Eaglepower LA 8308 KV90, 336 g: https://www.technobotix.in/products/eagle-powor-la-8308-kv90-motor/1781252000000073016 · ~325 g: https://www.technobotix.in/blogs/post/eagle-power-la-8308-kv90-brushless-motor-%E2%80%93-unmatched-power-for-heavy-lift-drones · KV90–205 variants: https://www.amazon.com/Eaglepower-Brushless-Motor-Loading-Agricultural/dp/B0FLWVRBY8
- [S4] MKS XDrive Mini 12–56 V: https://manuals.plus/ae/1005006480243178 · https://github.com/makerbase-motor/MKS-ODrive
- [S5] LD19 47 g: https://www.robotshop.com/products/dfrobot-dtof-ld19-laser-lidar-sensor-kit-12m
- [S6] Pi 4 46 g (reseller): https://littlebirdelectronics.com.au/products/raspberry-pi-4-model-b
- [S9] T-Motor MN5008 KV170: 128 g, 270 mΩ, 15 A, Ø55.6×32, 6 mm shaft: https://store.tmotor.com/goods.php?id=999 · https://robotshop.com/products/tmotor-uav-brushless-motor-antigravity-mn5008-kv170
- [S10] 6S 2200 mAh pack masses:
  - Turnigy 30C Shorty, 261 g: https://hobbyking.com/pt_pt/turnigy-2200mah-6s-22-2v-30c-shorty.html
  - SLS XTRON 30C, 324 g: https://www.stefansliposhop.de/akkus/sls-xtron/sls-xtron-30c/sls-xtron-2200mah-6s1p-22-2v-30c-60c::2117.html
  - LemonRC 70C, 350 g: https://lindinger.at/en/RC-Electronics/Drive-Set/Batteries/Pichler-LiPo-Akku-LEMONRC-2200-22-2V-6S-70C/9791507
  - Overlander 80C, 370 g: https://nexusmodels.co.uk/products/2200mah-6s-22-2v-80c-lipo-battery-overlander-extreme-pro
- Pololu D36V50F5: https://www.pololu.com/product/4091
- MN5008 KV170 720 mΩ listing (conflict): https://www.robozar.com/product/t-motor-antigravity-mn5008-kv170/
- Internal: electrical.md O9-a…d, materials_gears.md §4/§7/O3/O9, theory.md O9, thermal.md.

## 7. Changes to design assumptions

| Was (rev 1) | Now (rev 2) | Reason |
|---|---|---|
| 4 × 8308 (KV unconfirmed) | 2 × 8308 KV130 (hips) + 2 × T-Motor MN5008 KV170 (wheels, 128 g) | Client |
| Hip 2-stage ~9:1, 145 g printed | Compound stepped-planet 8:1, PAHT-CF gears: **193 g printed + 86 g metal** | Materials O3 / client |
| Wheel 1-stage 5:1 on 8308 | **3.5:1, 24/18/60 m1.25 b12 PAHT-CF, carrier in hub, 72 g incl. pins + 6 × 685ZZ**. PETG stator sleeve + 2 × 6806 around a free motor axis (no axle) | Materials O9, Electrical O9-b |
| 2 × 3S 1300 mAh (240 g) | **1 × 6S 2200 mAh 50C (350 g est.)** | Client / Electrical |
| 4 × 2 Ω 50 W brake resistors (80 g) | **2 × 2 Ω 25 W (20 g)**, hip boards only | Electrical O9-c |
| Main fuse 40–60 A | **50 A** MAXI slow | Electrical O9-c |
| Drivers at the motors (wheel drivers on legs) | **All 4 drivers in the body**. Hub encoder breakout + magnet (6 g); 0.45 m shielded SPI + 3 × 18 AWG phases per leg | Electrical O9-b |
| Generic IMU | ICM-42688-P on the ESP32 PCB | Client |
| Hip angle from the motor encoder | + leg-side hip encoder ×2 (16 g) | Client / Control |
| No hip end stops | TPU hip end stops ×2 (O4a) | Materials O4 |
| Tyre 35 mm, 106 g | Ø170/Ø146×25, 110 g | Materials §7 |
| Springs 50 g/leg placeholder | Extension spring 2.7 N/mm, 35 g/leg | Theory |
| Wiring 141 g | 110 g harness + 57 g leg cables + 10 g misc; PDB 25 g | Electrical O9-d |
| Wheel hub PLA/ABS | **PETG (ASA preferred)**; PLA rejected | Thermal |
| Hip gearbox housing PETG | **PAHT-CF** + 3 mm Al mount plate (also the driver heat plate) | Thermal |
| Closed passive body | 40 mm fan + vents; Al heat plates under the drivers | Thermal |
| No wheel heat path | Al stator carrier + finned cap ×2 (30 g each, unsprung) | Thermal |
| No motor temperature sensing | 10 k NTC in all 4 motors + on both brake resistors | Thermal |
| Total 4.36 kg | **4.31 kg**; ~3.85 kg with cheap cuts; 3.60 kg with everything + 6S 1500 | — |
| Unsprung 0.70 kg/side | **0.536 kg/side** (≈ 0.44 kg after cuts) | — |

## 8. Final CAD masses (rev 3, 2026-11-05)

Full table and CoM inputs: `docs/analysis/mass_actual.md`. The rev-2 masses above are **superseded** for printed parts, hip gearbox, wheel module and legs.

| Case | Mass |
|---|---|
| Solid CAD mass | **6.86 kg** |
| Realistic sliced mass | **6.41 kg** |
| Realistic range | **6.0–6.9 kg** (central ≈ 6.4 kg) |
| BOM rev 2 (for comparison) | 4.31 kg |

- **Unsprung mass per side** (wheel + shank + ½ cables): **0.84 kg sliced, 0.93 kg solid** (rev 2: 0.536 kg).
- Largest changes against rev 2:
  - Legs: 0.58 kg → 1.78–1.96 kg (arch plates, steel posts, outrigger beams, Al shank plates, straps, Ø10 pins and bushings)
  - Hip gearbox: 185 g → 413–434 g per side, and the Al plate 32 g → 80 g
  - Wheel module: 497 g → 606–652 g (Al axle, ring sleeve, two-plate carrier, PETG hub)
  - Body: 282 g → 475–611 g
- Purchased parts are unchanged. Hardware still to be counted: the hip-gearbox ear relief, a box beam for the B-pin path, and cable clips (≈ +50–150 g).
- The mass limits are soft by client decision (DECISIONS 2026-11-04). The jump and speed must be re-verified at this mass.
