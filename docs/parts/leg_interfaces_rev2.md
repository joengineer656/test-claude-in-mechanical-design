# Leg rev 2 interfaces (for Body and Hip-gearbox owners) — FINAL numbers, 2026-11-05

Refit for CoM (A4/M9): 4-bar B pin moved (46,30) -> **(39,31)** (leg frame, hip-relative, X fwd / Y up). Hip is now **10.6 mm ahead of the axle at h195** (was 37.1). Hip fixed at world (x 28, z 280); **axle world x = 17.43** (was -9.09), axle z = 85 at h195. Range 140..289 kept (mechanical reach 116..303).

## Thigh angle (gearbox homing tab / stop)  — angles measured as in build_leg (deg, CCW from +X fwd, hip-relative)
| hip height h | thigh angle | axle x rel. hip | axle x world |
|---|---|---|---|
| 140 (end stop) | **-0.29** | -6.6 | 21.4 |
| **195 nominal** | **-24.26** | -10.6 | 17.4 |
| 289 | -77.09 | -53.3 | -25.3 |
**Homing tab / hex index: -24.26 deg** (hex repeats each 60 deg: -24.26 = +35.74 mod 60). The thigh hex pocket has a vertex pointing along the thigh axis (hexpts(.,0) rotated by the thigh angle), sleeve inner 26.3 A/F, output hex 26 A/F. Thigh swing 140->289 = 76.8 deg (was 67). End-stop contact angle = -0.29 deg (pad now seated for 140).

## Thigh plane / Y stack (world y, mm)
Shank 71-79 (hub starts 80.5) · K pad to 93.5 · **thigh plate 94-104 (+1)** · hex sleeve **94-98 (4 mm, inboard end only; pocket 29.2 A/F, relieved to y 100)** · ONE central Ø9 hole for the M4 clamp screw (3 pcd-15 holes removed) · crank 105-117, spring band 104.5-117.5 (axis 111) · arch plate/outer 6806 **119.5-126.5** · coupler 127.5-141.5 · strap 142.5-148.5 · stub Ø30/24 to 126.5.
Gearbox: cover lip must stay <= y 93.5 inboard of the thigh (thigh face at y 94; keep 0.5 mm min). Gearbox deletes its bearing 2 / Ø30 journal ext / HG_Arch (M1): the leg's outer 6806 (Ø42 seat, y 119.5-126.5) is the only outer support.

## Arch posts (for Body M5) — unchanged
Ø16x3 steel tubes at r 82, angles **142 deg and 162 deg** (hip-relative, X fwd/Y up), y 40-119.5 (now 2 mm longer at the outboard end; bolted to the hip Al plate at y 40).

## Spring / anchor
Anchor pin (leg frame) **(97.4, 70.9)** = world (125.4, z 350.9), on the leg arch plate y 105..119.5 pin, carried by the arch plate + posts + box beam. **Body spring dowel/boss deleted (M7)**. Spring: **3.5 N/mm, F0 15 N, Fmax 169 N** (anchor design load 180 N holds) — needed to keep the 20 cm jump after the refit; see leg.md.

## Body asks
Beam foot plate sits on the body top at leg X 57-104 (world x 85-132), y 38-52, z 359-365: 2 x M5 seats in the top rib. Lug/beam top = world z 367.5 (<= 368 lidar rule). Arch posts: see above. Body axle notch must follow the axle path above.
Exports are now in WORLD coordinates (left leg); right = mirror about XZ.
Wheel axle path in the body frame (hip-relative, for the body notch): h140 (-6.6,-140) · h195 (-10.6,-195) · h289 (-53.3,-289).

## Rev 2b changes (A13) — what moved for Body / Gearbox
- **Shank Al plate now y 65-71** (inboard face y 65, was 68). Body: keep >= 1 mm to the pad ring. Gearbox: no change (thigh plane y 94-104, sleeve y 94-98, stub y to 126.5, cover lip <= 93.5 all unchanged). Sleeve is now a **round O38 x 4 steel insert** (hex 26.3 A/F inside) in a round O38 pocket in the thigh; output hex 26 A/F, homing angle -24.26 unchanged.
- **Arch posts O18 x 3** (r 82, 142 / 162 deg, y 40-119.5 unchanged). Body holes D20, collar D32 (C8). Body base seat at y 40 + collar D16.4 per C10 is still Body's.
- **Beam foot 47 x 32: world x 85-132, y 38-70, z 359-365**, 4 x M5 through-bolts at world (94.5, 42), (94.5, 66), (122.5, 42), (122.5, 66) (vertical, z), 3 mm Al backing plate 41 x 28 at world x 88-129, y 40-68, z 350-353. Body B1T_Tie shelf (y 38-66, x 66-132, z 353-359) must grow to y 70 and give 4 x O5.5 holes + clearance for the backing plate below; Body sees M5 not M4. Beam top stays z 367.5; beam runs z 355.5-367.5 at y >= 70, so nothing of Body may sit at z 355.5-359, y 70-119.5, x 105-145 (check mast/lidar side).
- C stand-off: nothing new for Body/Gearbox; its inboard nuts sit on the shank plate face (y 65), so the plate pocket depth matters only for the pad-ring clearance above.
