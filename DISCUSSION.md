# Discussion summary (client ↔ Claude manager ↔ sub-agents)

This is a summary, not a raw transcript (raw logs contain tool output and local paths). The authoritative decision trail is `DECISIONS.md`.

1. **Kick-off.** Client asked for the full mechanical design of a 2-wheel wheel-legged balance robot (Ascento style) in SolidCraft, with Claude as engineering manager creating sub-engineers (mechanical design, structural, thermal, materials, BOM, robot theory) and a plan before building.
2. **Client choices.** Series 24 V battery, motors in the wheel hub, Bambu A1 printer, LD19/LD06 lidar.
3. **Gate A (conditional).** Client required: add Robotics & Control and Electrical engineers; verify motor specs; compare wheel ratios; hip torque/spring/landing loads; weight budget; printed planetary strength; driver 6S/regen check; balancing simulation and staged prototype tests before jumps; document assumptions and sources.
4. **P1 results and choices.** KV130 hip motors; lighter wheel motors (MN5008); 1× 6S 2200 mAh; PAHT-CF gears. Client accepted 4.31 kg, kept 8 J springs, chose PETG hubs, then approved Gate B ("start and continue to the end").
5. **Vendor models.** Client told the CAD engineers to use downloaded GrabCAD/manufacturer models for bought parts.
6. **Build phase.** Master layout, then four parts built in parallel using headless `solidcraft-cli` after the client asked why other parts were waiting. Client said weight and diameter increases are acceptable; priority is finishing.
7. **Findings.** Real mass ≈ 6.4–6.9 kg. A 20 cm jump failed at 8:1 hip ratio (≈16 cm) → 6:1 hip gearbox. Wrong early claim by the manager (that cutting leg mass raises the jump) was corrected.
8. **Assembly rev 0.** 17 mismatches, CoM +22 mm. Fixes: hip support, leg 4-bar re-fit (CoM +2 mm), spring 3.5 N/mm, body notches and tie.
9. **Structural rev 2.** Hand-calculation found weak C pad, shank, bush, tie; changes C1–C11 accepted (leg built; body/gearbox part interrupted).
10. **Client instructions at the end.** Skip the thermal test; pause after the running agents; then "stop everything"; then publish everything to GitHub.
