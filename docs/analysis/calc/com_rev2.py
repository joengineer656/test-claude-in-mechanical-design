"""CoM after the rev 2 leg refit: swap the leg bodies (new CAD, world coords) and shift wheel-side bodies +dx with the axle.
Run: python3 com_rev2.py bodies_nominal.json leg_measure.json  (leg_measure.json = solidcraft-cli eval cad/parts/leg.solidcraft)"""
import json, sys, copy
import com_assembly as c
bodies = json.load(open(sys.argv[1])); leg = json.load(open(sys.argv[2]))['bodies']
DX = (28 - 10.57) - c.AXLE_X                       # axle moves forward relative to the body
new = []
for b in bodies:
    n = b['name']
    if n.startswith('Leg') and n[3] in 'LR' and n[4] == '_': continue      # legs replaced below
    b = copy.deepcopy(b)
    if n.startswith('WH') and n[2] in 'LR': b['com'][0] += DX
    new.append(b)
for side, sg in (('L', 1), ('R', -1)):
    for b in leg:
        if b['name'].startswith('REF_'): continue
        com = list(b['center_of_mass']); com[1] *= sg
        new.append(dict(name=f"Leg{side}_{b['name']}", com=com, vol=b['volume_mm3'], bbox=None))
c.AXLE_X += DX
c.LUMPS = [(n, g, (x + DX if n.startswith('WheelFasteners') else x), y, z) for n, g, x, y, z in c.LUMPS]
for lab, sl in (('solid', False), ('sliced', True)):
    M, com, rows = c.run(new, sl)
    print(f"{lab}: mass {M:.0f} g  CoM x {com[0]:.1f} (axle {c.AXLE_X:.2f}: {com[0]-c.AXLE_X:+.1f} mm), y {com[1]:+.2f}, z {com[2]:.1f}")
M, com, rows = c.run(new)
lg = [(r[2], r[3]) for r in rows if r[0].startswith('LegL_')]
m = sum(a for a, _ in lg); print(f"leg (one side) mass {m:.0f} g, CoM x {sum(a*b[0] for a,b in lg)/m:.1f}")
