"""Rev 2 (A1/M1): one gearbox 6806 at y 87.5 + the leg's outer 6806 at y 121 (33.5 mm). Hand calc, same ball/seat model as structural_hip_gearbox.py.
Thigh = rigid beam on the hex (carrier, bearing 1) and the stub bearing at y121. Loads at y99 (knee/thigh plane), spring 180 N at the crank y110."""
import math
pi=math.pi
AL=65*0.9*0.7; E=2000.
C,C0=4450.,2900.; dm=36.; Z=15; B=7.; d_in=30.; Q0=5*C0/Z; al=math.radians(20)
cases={'LC-A':345,'LC-C':597,'LC-B':1125,'LC-D':2011}; Fs=180.
y1,y2,yF,yS=87.5,121.0,99.0,110.0
def ball(F,arm):
    M=F*arm/1000.; Qr=5*F/(Z*math.cos(al)); Qn=4*M*1000/(Z*dm)/math.sin(al)
    p0=M*1000/(pi*d_in*B**2/12); Kth=(E/5.)*pi*d_in*B**3/24/2/1000
    return M,Q0/(Qr+Qn),AL/p0 if p0 else 99,math.degrees(M/Kth)
print('bearing 1 (gearbox) with the thigh load path; spring 180 N (was 122); SF ball / seat / tilt deg')
for tag,yh in (('A ideal beam, support at brg1 y87.5',87.5),('B hex edge contact y94 (inboard end of hub)',94.0),('C hex contact at hub centre y99 (rigid thigh)',99.0)):
    for n,Fk in cases.items():
        # R1 at yh, R2 at y2; moments about y2
        R1=(Fk*(y2-yF)+Fs*(y2-yS))/(y2-yh); R2=Fk+Fs-R1
        arm=yh-y1
        M,sfb,sfs,th=ball(R1,max(arm,0.001)) if arm>0 else (0,Q0/(5*R1/(Z*math.cos(al))),99,0)
        print(f'{tag[:44]:44s} {n}: R1={R1:5.0f} N M1={M:5.1f} Nm SFball={sfb:4.2f} SFseat={sfs:5.2f} tilt={th:4.2f}deg | brg2 R2={R2:5.0f} N C0/R2={C0/max(R2,1):4.1f}')
# lateral slide axial 0.97-1.7 kN on the cover lip (OD42 shear, t axial): printed lip, z-layer factor 0.4
print('cover lip after trim to y92:')
for t in (2.0,1.0):
    for F in (970,1700):
        tau=F/(pi*42*t); print(f' t={t} mm axial {F} N: tau={tau:.1f} MPa SF={0.577*AL*0.4/tau:.2f}')
# hex: radial now carried via hex in the worst case C
Fr=2011+Fs
for T in (20,):
    pt=T*1000/(3*13*0.5*(26/math.sqrt(3))*6); pr=Fr/(26*6); print(f'hex worst radial {Fr:.0f} N: p={pt+pr:.1f} MPa SF PAHT={AL/(pt+pr):.2f} (sleeve steel 26.3 A/F: contact stays in the hub/steel)')
# skirt bending: bearing 1 radial R1 (case C) x 77.5 (plate to bearing) + moment M1
for n in ('LC-A','LC-D'):
    R1=cases[n]+Fs; Mb=R1*77.5/1000; sig=Mb*1000/(pi*48.6**2*2.4*0.8)
    print(f'skirt bending case C {n}: Mb={Mb:.0f} Nm SF={AL/(2.5*sig):.2f} (2.4 mm wall; CAD wall 3.4 -> x1.65: {AL/(2.5*sig)*1.65:.2f})')
