# Mass Budget — rev 2 (P1, after client decisions and the O9 follow-ups)

Owner: BOM / Requirements Engineer · Date: 2026-11-04 · Line items: `bom/bom.md` (rev 2).

Inputs (all final):
- DECISIONS.md
- theory.md O9
- electrical.md O9
- materials_gears.md O9
- thermal.md

## 0. Result

| Configuration | Mass | Margin to 3.6 kg | Margin to 4.0 kg |
|---|---|---|---|
| Rev 1 baseline (4 × 8308, 2 × 3S 1300) | 4.36 kg | −763 g | −363 g |
| **Rev 2 bottom-up (client decisions + Electrical/Materials/Thermal parts)** | **4.31 kg** | **−712 g (−19.8 %)** | **−312 g (−7.8 %) — FAILS** |
| Rev 2 − cheap cuts A | 3.85 kg | −245 g | +155 g (3.9 %) |
| A + B (hip gearbox to Materials' figure, PAHT-CF legs) | 3.72 kg | −122 g | +278 g (7.0 %) |
| A + B + C (6S 1500 mAh ≥ 65C + light wheel-gear options) | **3.60 kg** | **+2 g** | +402 g (10.0 %) |
| A + B + 6S 1300 mAh | 3.57 kg | +32 g | +432 g (10.8 %) |

**Conclusion:** the client's rev-2 configuration is **0.31 kg over the hard limit as specified**.
- The lighter wheel motors saved 416 g.
- That saving was cancelled by four additions:
  - the compound PAHT-CF hip gearbox and its Al plates (+~190 g vs rev 1)
  - the 6S 2200 pack (+110 g vs 2 × 1300)
  - Thermal's heat-path parts (+158 g)
  - encoder/NTC/leg cabling
- The cheap cuts recover 467 g. **≤ 3.6 kg is reachable only with every cut plus a smaller battery (6S 1500 or 1300).** Even then the margin over the target is ~0, though 10 % to the 4.0 kg limit holds.
- Recommendation for Gate B: take cuts A + B now. Have Materials confirm the hip gearbox mass (the biggest uncertainty, up to ±200 g). Ask the client to choose between a 6S 1500 pack (~46 min) and accepting ~3.72 kg (7 % margin to 4.0 kg).

## 1. Bottom-up by subsystem (rev 2)

| Subsystem | Main contents | Mass (g) | % |
|---|---|---|---|
| Hip actuators ×2 | 8308 KV130 (672), PAHT-CF compound 8:1 printed (370), 6808 + 6803 + 12 × 685ZZ + Ø5 pins + steel sun option (136), Al mount plates (64) | 1278 | 30 |
| Hip actuators ×2 (cont.) | Leg-side encoders (16) and TPU end stops (20) are included in the 1278 g | | |
| Wheel modules ×2 | MN5008 KV170 (256), gear core 24/18/60 incl. pins + 685ZZ (144), PETG hub (174), TPU tyre (220), 4 × 6806 (76), Al stator carrier + fins (60), PETG sleeve (32), encoder kits (12), fasteners (20) | 994 | 23 |
| Legs L + R | PETG links (254), 608/688 bearings (90), Ø8 pins (96), springs (70), clips/bumpers (14) | 524 | 12 |
| Body | Printed shell/plates/brackets/mast (282), battery cradle/strap (15) | 297 | 7 |
| Electronics | 4 × XDrive Mini (160), Pi 4 + heatsink (56), LD19 (52), ESP32 PCB + ICM-42688-P (25), wheel-driver Al plates (42), fan + vents (15), NTC ×6 (9), camera, magnets, microSD | 368 | 9 |
| Power | 6S 2200 50C (350), 2 brake resistors (20), 50 A fuse, anti-spark switch, e-stop, PDB, buck (95) | 465 | 11 |
| Wiring | Leg cables, shielded SPI + phases (57), harness (110), misc (10) | 177 | 4 |
| Fasteners | M3/M4/M2.5, nuts, washers, 120 inserts | 209 | 5 |
| **Total** | | **4312** | 100 |

The Electrical-scope parts total 967 g in the BOM, against Electrical's own ≈ 936 g. The BOM adds the lidar cable, camera ribbon, hip magnets, microSD and wheel-driver plates.

### Top 10 items (qty × unit)

| # | Item | Mass (g) |
|---|---|---|
| 1 | 2 × Eaglepower 8308 KV130 (hips) | 672 |
| 2 | 2 × printed hip gearbox 8:1, PAHT-CF | 370 |
| 3 | 6S 2200 mAh 50C pack | 350 |
| 4 | Printed body set | 282 |
| 5 | 2 × T-Motor MN5008 KV170 | 256 |
| 6 | 2 × printed leg set (PETG) | 254 |
| 7 | 2 × TPU tyre | 220 |
| 8 | 2 × PETG wheel hub | 174 |
| 9 | 4 × MKS XDrive Mini | 160 |
| 10 | 2 × wheel gear core (incl. pins + 685ZZ) | 144 |

The top 10 make up 2882 g, 67 % of the total.

### Unsprung mass per wheel side

| Part | g |
|---|---|
| MN5008 KV170 | 128 |
| Gear core 24/18/60 (pins, 6 × 685ZZ, fasteners) | 72 |
| PETG stator sleeve | 16 |
| Al stator carrier + finned cap | 30 |
| 2 × 6806-2RS | 38 |
| PETG hub (= carrier) | 87 |
| TPU tyre | 110 |
| Wheel fasteners | 10 |
| Encoder kit | 6 |
| ½ leg cables | 14 |
| ½ shank (Theory convention) | 25 |
| **Total** | **536** |

After cuts A (tyre −45, rim −20, ASA hub −14, sleeve merged into the Al carrier −16) the total is **≈ 441 g**.

Theory and Control used 0.465 kg. Both should re-run with 0.536 kg, or 0.44 kg if cuts A are approved.

## 2. Assumptions
- **Printed-part model:** mass = effective solid volume × fill × density.
  - Densities (g/cm³): PAHT-CF 1.06 (Materials), PETG 1.27, PLA 1.24, ASA 1.07, TPU 1.21.
  - Gears are 100 % solid.
  - Uncertainty ±15 % (≈ ±190 g on the printed total of ~1.27 kg).
- **Hip gearbox (Materials O3):**
  - Compound stepped planet, 8:1.
  - Sun 18T m1.25; planets 36T (m1.25, b14) / 18T (m1.5, b20); fixed ring 63T m1.5 (pitch Ø94.5).
  - All PAHT-CF, because Thermal requires PAHT-CF where the housing touches the can.
  - Calc §3: 185 g printed + 86 g metal = 271 g per hip.
  - **Materials quotes 150–200 g including metal.** This is unresolved. The BOM keeps the conservative calc.
- **Wheel gear (Materials O9):** integrated design, 65–80 g → 72 g.
- **Wheel bearing arrangement:** 2 × 6806 around a free motor axis (Electrical O9-b). The ring is held by a PETG sleeve.
- **Thermal Al parts at 2.7 g/cm³:**
  - Hip plate Ø100 × 3 mm, 50 % lightened → 32 g. It also serves as the hip-driver heat plate (Thermal §4 item 4).
  - Wheel-driver plates 70 × 70 × 1.5 mm → 20 g + pad.
  - Wheel stator carrier + fins 30 g (Thermal: 25–35 g).
- **Electrical masses** from electrical.md O9-d (estimates; Electrical says weigh on arrival).
- **Springs:** 35 g per leg (8 J total). The 4 J option is in cuts A.

## 3. Printed-part calculation detail (rev 2 changes only; rev-1 body/leg/hub geometry is unchanged)

| Part | Geometry | Mass (g) |
|---|---|---|
| Hip ring insert | OD106 / ID94.5 × 20, PAHT-CF | 38 |
| Hip housing | tube Ø110 × 25 × t2.4 + Ø110 × 4 cap (40 % lightened), fill 0.85, **PAHT-CF** | 39 |
| Hip stepped planets ×3 | Ø45 × 14 (50 % webbed) + Ø27 × 20 − Ø11 bore | 66 |
| Hip sun | Ø22.5 × 14 | 6 |
| Hip carrier | 2 × Ø80 × 5, 40 % lightened, fill 0.85 | 27 |
| Hip output flange | 10 cm³ × 0.85 | 9 |
| **Hip printed, each** | | **185** |
| Wheel gear core | Materials O9 table: sun 10, planets 12, ring 15, pins 9, 685ZZ 12, fasteners 5 = 63; integrated range 65–80 | 72 |
| Wheel PETG stator sleeve | 15 cm³ × 0.85 × 1.27 | 16 |
| Wheel hub | rev-1 geometry × PETG | 87 (ASA 73) |
| Tyre | Materials: Ø170/Ø146 × 25, 40 % voids | 110 |
| Leg set | rev-1 geometry × PETG | 127 |

## 4. Battery options (single 6S pack)

| Pack | Mass | Δ vs 2200 | Energy (80 % usable) | Mixed runtime at 35 W (Electrical) | Jump peak 72 A |
|---|---|---|---|---|---|
| **6S 2200 mAh 50C (client)** | 350 g (Electrical est.; sourced 261–370 g [B9]) | 0 | 39 Wh | ≈ 67 min | 33 C ✓ |
| 6S 1800 mAh | ≈ 295 g (est.) | −55 | 32 Wh | ≈ 55 min | needs ≥ 50C ✓ |
| 6S 1500 mAh | ≈ 250 g (est.) | −100 | 27 Wh | ≈ 46 min | needs **≥ 65C** (50C = 75 A, too tight) |
| 6S 1300 mAh | ≈ 220 g (est.) | −130 | 23 Wh | ≈ 40 min | needs **≥ 75C** |

The masses below 2200 mAh are scaled from the rev-1 3S data (2 × 3S 1300 = 240 g). **They are not sourced; MAY CHANGE.**

## 5. Cheapest cuts (ranked by g saved per cost/risk)

| Set | Cut | Saves (g) | Cost | Risk | Owner |
|---|---|---|---|---|---|
| A | Tyre Ø170/Ø154 × 25, 50 % voids (62 g vs 110) | 90 | 0 | low–med (grip, wear) | Wheel / Materials |
| A | Body covers 0.8 mm / LW-PLA, more pocketed side plates (PETG near the drivers per Thermal) | 65 | ~€20 | low | Materials |
| A | Snap-fit covers (−40 M3 + inserts), Al M3 on non-structural joints | 60 | ~€10 | low | Mech |
| A | Drop the wheel-driver Al plates: fan-vented body (Thermal says they are needed only if sealed) | 42 | 0 | low (Thermal to confirm) | Thermal |
| A | Hub rim 2.0 mm + more lightening | 40 | 0 | low | Wheel |
| A | Hollow Ø8 × 1 pins except the knee | 40 | ~€10 | low | Structural |
| A | Merge the PETG stator sleeve into the Al stator carrier | 32 | 0 | low (also solves I14) | Mech / Thermal |
| A | 4 J-total springs (Theory recommends trying first) | 30 | 0 | low | Theory |
| A | ASA hub instead of PETG (Thermal's preferred material) | 28 | 0 | low–med (warps on the open A1; needs a draft shield) | Materials |
| A | Infill 40 → 20 % on thick non-gear parts | 20 | 0 | low | Materials |
| A | 12 mm latching e-stop instead of a 22 mm mushroom | 20 | 0 | low | Electrical |
| | **Subtotal A** | **467 → 3.85 kg** | | | |
| B | Hip gearbox to Materials' 150–200 g incl. metal (verify from tooth geometry; webbed planets) | 80 (up to 200) | 0 | med (gear strength) | Materials |
| B | Legs in PAHT-CF (1.06 vs 1.27 g/cm³) | 43 | ~€30 | low–med | Materials / Structural |
| | **Subtotal A + B → 3.72 kg** | | | | |
| C | 6S 1500 mAh ≥ 65C pack | 100 | ~€50 | med (46 min runtime) | **Client** |
| C | Wheel gear: b10 + 1 bearing per planet (Materials light options) | 24 | 0 | low–med | Materials |
| | **A + B + C → 3.60 kg** | | | | |
| alt | 6S 1300 mAh ≥ 75C instead of 1500 | +30 more | — | runtime 40 min | Client |

Not recommended:
- Smaller hip motors (needed for the jump).
- Fewer brake resistors (already reduced to 2).
- Dropping the Thermal Al parts on the hips (mandatory for the hip drivers).
- Printing gears below 100 %.

## 6. Open questions
1. **Hip gearbox mass:** BOM 271 g per hip vs Materials 150–200 g. Materials/Mech should estimate from the actual tooth geometry. This is the largest single uncertainty.
2. **Battery:** will the client accept a 6S 1500 mAh ≥ 65C pack (~46 min), or a total of ~3.72 kg (7 % margin to 4.0 kg) with the 2200?
3. **MN5008 KV170 R_ll:** 270 mΩ (T-Motor/RobotShop) vs 720 mΩ (Robozar). Thermal rejects 720 by KV² scaling. Measure on arrival; at 0.72 Ω the sealed-hub limit is 2.2 A.
4. **Hub heat path vs encoder (I14):** Thermal keys the Al carrier to an axle; Electrical needs the motor axis free. Mech must decide in P2. Merging the carrier with the sleeve is cut A.
5. **Client approval:** hub in PETG/ASA instead of PLA/ABS (Thermal); 2 brake resistors instead of 4 (Electrical).
6. **Weigh on arrival:** 8308 KV130 (only the KV90 mass is published), XDrive Mini (40 g est.), the 6S pack.

## 7. Sources
- 8308 KV90 336 g (KV130 assumed the same frame): https://www.technobotix.in/products/eagle-powor-la-8308-kv90-motor/1781252000000073016
- T-Motor MN5008 KV170, 128 g incl. cable, 270 mΩ: https://store.tmotor.com/goods.php?id=999 , https://robotshop.com/products/tmotor-uav-brushless-motor-antigravity-mn5008-kv170 ; conflicting 720 mΩ listing: https://www.robozar.com/product/t-motor-antigravity-mn5008-kv170/
- LD19 47 g: https://www.robotshop.com/products/dfrobot-dtof-ld19-laser-lidar-sensor-kit-12m · Pi 4 46 g: https://littlebirdelectronics.com.au/products/raspberry-pi-4-model-b
- [B9] 6S 2200 packs, 261–370 g:
  - https://hobbyking.com/pt_pt/turnigy-2200mah-6s-22-2v-30c-shorty.html
  - https://www.stefansliposhop.de/akkus/sls-xtron/sls-xtron-30c/sls-xtron-2200mah-6s1p-22-2v-30c-60c::2117.html
  - https://lindinger.at/en/RC-Electronics/Drive-Set/Batteries/Pichler-LiPo-Akku-LEMONRC-2200-22-2V-6S-70C/9791507
  - https://nexusmodels.co.uk/products/2200mah-6s-22-2v-80c-lipo-battery-overlander-extreme-pro
- 3S data used to scale the smaller 6S packs:
  - https://hobbywireless.com/batteries-c-120_15/tattu-1300mah-111v-3s-75c-lipo-battery-p-2139.html
  - https://besomi.com/ae_en/zop-power-111v-1300mah-75c-li-po-battery.html
- Internal: theory.md O9, electrical.md O9-a…d, materials_gears.md O3/O9/§7, thermal.md §1–§6.

## 8. Changes to design assumptions

| Was (rev 1) | Now (rev 2) | Effect (g) |
|---|---|---|
| 4 × 8308 336 g | 2 × 8308 KV130 + 2 × MN5008 KV170 128 g | −416 |
| Hip 2-stage 9:1, 145 g printed, PETG/PA | Compound 8:1, all PAHT-CF, 185 g printed + 86 g metal; + 3 mm Al mount plate 32 g | +~190 for the pair |
| Wheel gearbox 5:1 + 61808/61806 | 24/18/60 integrated (72 g) + 2 × 6806 + PETG sleeve; no axle through the motor axis | −~100 for the pair |
| 2 × 3S 1300 (240 g) | 6S 2200 50C (350 g) | +110 |
| 4 brake resistors 50 W (80 g) | 2 × 25 W (20 g) | −60 |
| Drivers at the motors | All 4 in the body; hub encoder kit + shielded SPI + phase cables through the legs | +~70 |
| No thermal parts | Fan + vents, Al hip plates, Al wheel-driver plates, Al wheel carriers with fins, NTC ×6 | +158 |
| Wheel hub PLA | PETG (ASA preferred) | +4 |
| Body 3.95 → 4.36 kg | **4.31 kg bottom-up**; 3.85 / 3.72 / 3.60 kg with cuts A / A+B / A+B+C | — |
| Unsprung 0.70 kg/side | **0.536 kg/side** (0.44 kg with cuts A) | — |
| Target 3.6 kg reachable with S3 | **Reachable only with A + B + C (incl. a smaller battery); zero margin to 3.6 kg** | — |

## 9. Final CAD masses (rev 3, 2026-11-05)

This section **supersedes** §0–§5 for the total. Those sections remain as the rev-2 budget history. The full component table, with the CoM-script inputs, is in `docs/analysis/mass_actual.md`.

| Case | Mass | vs rev 2 (4.31 kg) |
|---|---|---|
| Solid CAD | **6.86 kg** | +2.55 kg |
| Realistic sliced | **6.41 kg** | +2.10 kg |
| Realistic range | **6.0–6.9 kg** | — |

| Subsystem (g) | Solid | Sliced | Low | Rev 2 |
|---|---|---|---|---|
| Legs (2) | 1963 | 1777 | 1689 | ≈ 580 |
| Hip actuators (2) | 1765 | 1723 | 1527 | 1278 |
| Wheel modules (2) | 1304 | 1212 | 1140 | 994 |
| Body | 831 | 695 | 650 | ≈ 457 |
| Power + electronics + wiring | 1000 | 1000 | 954 | 1010 |
| **Total** | **6863** | **6407** | **5960** | **4312** |

- **Unsprung mass per side:** 0.84 kg (sliced) to 0.93 kg (solid), i.e. wheel 606–652 g + shank, Al plate and strap 217–267 g + ½ cables 14 g. Rev 2 was 0.536 kg and Theory used 0.465 kg.
- **CoM:** the nominal CoM moves from +2 mm to about +11 mm ahead of the axle, because the legs, gearboxes and plates sit forward. The battery rail cannot trim it rearwards.
- The 3.6 kg target and the 4.0 kg hard limit are now soft by client decision, so the §5 cut lists are no longer needed to meet a mass limit. The low case (5.96 kg) needs only cuts already approved by the manager: hip gearbox recovery options 1–5, a pocketed arch plate and shank, a thinner hub.
- **Action:** Theory and Control re-verify the 20 cm jump, the 12 km/h speed headroom, and balance at 6.4 kg with 0.84–0.93 kg unsprung per side.

### Changes to design assumptions (rev 3)
1. Robot mass: 4.31 kg → **6.4 kg realistic (6.0–6.9 kg)**.
2. Unsprung mass per side: 0.536 kg → **0.84–0.93 kg**.
3. CoM at nominal: +2 mm → **≈ +11 mm** forward of the axle (approximate; positions of the leg sub-parts are estimates).
4. Hip gearbox mass: 185 g printed → 413–434 g per side. Al hip plate: 32 g → 80 g.
5. Leg mass: ≈ 290 g per pair in the layout → 1.7–1.9 kg per pair.

### Open questions (rev 3)
1. Does the design still meet 20 cm and 12 km/h at 6.4 kg? (Theory/Control)
2. Re-measure the hip gearbox after the rework (options 1–5 not applied here).
3. Weigh the first prints; the hub and cover masses are estimates.
4. CoM script needs real centroids from the `.solidcraft` files.

### Sources (rev 3)
`docs/parts/wheel.md`, `body.md`, `leg.md`, `hip_gearbox.md`, `docs/layout.md`, `DECISIONS.md`, `docs/analysis/electrical.md`.
