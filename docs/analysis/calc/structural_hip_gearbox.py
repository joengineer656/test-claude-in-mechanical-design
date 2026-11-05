"""Structural hand-calc for the hip gearbox (Structural Eng.). Run: python3 structural_hip_gearbox.py
All SF = allowable(50 C, static 0.7*UTS*T-retention) / stress at the UNFACTORED load. Pass >= 1.5."""
import math
pi=math.pi
# ---- material (materials_gears.md A9/A10): PAHT-CF 65 MPa conditioned, x0.9 at 50C, x0.7 static
ALLOW={'PAHT-CF':65*0.9*0.70,'PETG':34*0.75*0.70}   # MPa, 50 C
E_PRINT=2000.0  # MPa, conditioned PAHT-CF at 50 C (assumption, ~3 GPa dry/25 C)
# ---- loads (theory O13 re-run, fixed end stop) hip bearing = knee pin force; + spring on thigh crank
cases={'LC-A ctrl sym':345,'LC-C ctrl 1 wheel':597,'LC-B fault sym':1125,'LC-D fault 1 wheel':2011}
Fspring=122.0     # N sustained (180 N design); adds arithmetically (worst vector)
arm=10.5          # mm bearing centre y87.5 -> thigh mid-plane y98
# ---- 6806-2RS, real ratings (several makers 4.45-4.55 kN / 2.9-3.44 kN); use low end
C,C0=4450.,2900.; dm=36.; Z=15; B=7.; d_in=30.
Q0=5*C0/Z
print('== bearing, single 6806 @ overhang',arm,'mm; C=%g C0=%g Q0=%.0f N/ball'%(C,C0,Q0))
al=math.radians(20)
def ring(F,s_arm,label):
    M=F*s_arm/1000.        # Nm
    P0=0.6*F                # radial-only static equivalent (X0=0.6) - ignores moment
    Qr=5*F/(Z*math.cos(al))
    Qm=4*M*1000/(Z*dm)      # peak axial ball component from moment, N
    Qn=Qm/math.sin(al)
    Qmax=Qr+Qn
    p0=M*1000/(pi*d_in*B**2/12)   # MPa, peak seat pressure (cos phi * z linear) , one seat
    k=E_PRINT/5.0                 # MPa/mm Winkler, 5 mm layer
    Kth=k*pi*d_in*B**3/24/2/1000  # Nm/rad, two seats in series
    th=M/Kth
    print(f'{label:20s} Fr={F:6.0f} M={M:5.1f}Nm  C0/Fr={C0/F:4.2f} ball Qr={Qr:4.0f} Qm_ax={Qm:4.0f} Qn={Qn:4.0f} SFball={Q0/Qmax:4.2f} seat p0={p0:5.1f}MPa SFseat={ALLOW["PAHT-CF"]/p0:4.2f} tilt(seat)={math.degrees(th):4.2f}deg')
    return M,th
res={}
for n,F in cases.items(): res[n]=ring(F+Fspring,arm,n)
Pa=0.11; print('free tilt from bearing play: %.2f mrad = %.2f deg'%(Pa/dm*1000,math.degrees(Pa/dm)))
print('\n== option: pair of 6806 touching (centres 7 mm apart, load 10.5 mm outside nearer one)')
for n in ('LC-D fault 1 wheel',):
    F=cases[n]+Fspring; FB=F*(arm+7)/7; FA=F*arm/7
    print(f'{n}: outer bearing radial {FB:.0f} N ({FB/C0:.2f} C0), inner {FA:.0f} N reversed')
print('== option: 2nd bearing centred spacing s (load midway): radial each F/2')
for n,F in cases.items():
    F+=Fspring; print(f'{n:20s} each {F/2:5.0f} N  SF_static C0/(0.6*F/2)={C0/(0.6*F/2):.2f}  C0/(F/2)={C0/(F/2):.2f}')
print('   needs s=2*overhang=%.0f mm: 2nd bearing centre y=%.1f'%(2*arm,87.5+2*arm))
print('== option: 2nd bearing inboard at carrier-in (z~2, span 45.5 mm): outer bearing 1.23F')
for n,F in cases.items():
    F+=Fspring; print(f'{n:20s} outer {F*(1+arm/45.5):5.0f} N  inner reversed {F*arm/45.5:4.0f} N  C0/outer={C0/(F*(1+arm/45.5)):.2f}')
# ---- L10 for fatigue cases (oscillating, +-37 deg => count as revs)
for n in ('LC-A ctrl sym','LC-C ctrl 1 wheel'):
    F=cases[n]+Fspring; M=F*arm/1000; Pe=F+ 4*M*1000/dm*1/math.tan(al)*0  # radial only
    Qmax=5*F/(Z*math.cos(al))+4*M*1000/(Z*dm)/math.sin(al); Peq=Qmax*Z/5
    print(f'{n}: equivalent radial incl. moment {Peq:.0f} N, (C/P)^3 = {(C/Peq)**3:.0f} Mrev')
# ---- planet meshes taking the moment (lever 25 mm from bearing to planet mid-plane)
print('\n== carrier tilt -> planet meshes')
lev=25.0; Dr=94.5
T=16.0; Fp=T/(3*0.03375)*1.43           # pin load incl K_share*K_v at 16 Nm
Ft_ring=Fp*22.5/36                       # ring-mesh tangential per planet (with K)
print('torque-only ring-mesh tangential per planet at 16 Nm: %.0f N; pin load %.0f N'%(Ft_ring,Fp))
for n in ('LC-A ctrl sym','LC-C ctrl 1 wheel','LC-D fault 1 wheel'):
    M,th=res[n]; Kb=M/th  # Nm/rad of bearing seats
    kt=2500.  # N/mm tooth-pair radial-ish stiffness, plastic E~3GPa, b=20 (assumption)
    Kg=1.5*kt*lev**2/1000   # Nm/rad, 3 planets cos-weighted (1.5)
    share=Kg/(Kg+Kb)
    Fg=share*M/(lev/1000)   # N total radial on ring teeth
    Fn_each=1.46*(Fg/3)     # wedge on two flanks, 20deg PA, per planet (rough, 1 planet takes more)
    Fn_peak=1.46*(Fg*2/3)   # cosine distribution: worst planet ~2/3 of total
    print(f'{n:20s} gear share={share:4.2f} radial on teeth={Fg:5.0f} N  worst-planet wedge normal={Fn_peak:5.0f} N  x torque load {Fn_peak/Ft_ring:4.1f}')
print('misalignment over ring face b=20: tilt 0.17deg ->%.3f mm ; 1deg -> %.2f mm'%(20*math.radians(0.17),20*math.radians(1)))
# ---- hex drive
print('\n== hex 26 A/F x 6')
for T in (20,16):
    Fr=cases['LC-D fault 1 wheel']+Fspring
    pt=T*1000/(3*13*0.5*(26/math.sqrt(3))*6/1)   # 3 flats engaged, half flat length, apothem 13
    pr=Fr/(26*6)
    tau=16*T*1000/(pi*26**3)
    print(f'T={T}: p_torque={pt:.1f} MPa  p_radial(LC-D)={pr:.1f}  sum={pt+pr:.1f}  SF PAHT={ALLOW["PAHT-CF"]/(pt+pr):.2f} SF PETG={ALLOW["PETG"]/(pt+pr):.2f}; torsion shear {tau:.1f} MPa SF={0.577*ALLOW["PAHT-CF"]/tau:.1f}')
# M4 inserts + bolts: clamp only. lateral load -> axial
print('M4 8.8 bolt tension capacity 0.9*640*8.78=%.0f N; insert design pull 150 N rule is for heat-set; Ensat in PAHT-CF: see md'%(0.9*640*8.78))
# ---- planet pin
print('\n== planet pin d5 hardened (yield >=1000 MPa), span 40 mm')
for T in (20,16):
    Fp=T/(3*0.03375)*1.43; Fs=Fp*13.5/36; Fr=Fp*22.5/36
    zs,zr,L=12.5-2.5,29.5-2.5,40.0   # positions from left support (z=2.5)
    # simply supported beam, point loads Fs at zs, Fr at zr (same direction)
    Rb=(Fs*zs+Fr*zr)/L; Ra=Fs+Fr-Rb
    M=max(Ra*zs, Ra*zr-Fs*(zr-zs))   # moment under each load
    sig=M*32/(pi*5**3); tau=4*max(Ra,Rb)/(3*pi*5**2/4)
    print(f'T={T}: Fs={Fs:.0f} Fr={Fr:.0f} Ra={Ra:.0f} Rb={Rb:.0f} M={M:.0f} Nmm sigma={sig:.0f} MPa SF(1000)={1000/sig:.1f} cheek p={max(Ra,Rb)/(5*4):.1f} MPa SF={ALLOW["PAHT-CF"]/(max(Ra,Rb)/(5*4)):.1f}')
# ---- housing stack bolts & ring torque path
print('\n== stack bolts M3x35 x5 at r=64')
for T in (20,16):
    Ft=T*1000/64; per=Ft/5; per3=Ft/3
    pbear=per3/(3*6)
    pre=800.; muN=0.3*pre*5*64/1000*2   # two faces
    washer=pre/(pi/4*(7**2-3.4**2))
    print(f'T={T}: tangential at ears {Ft:.0f} N, per bolt {per:.0f} (3 sharing {per3:.0f}); ear bearing {pbear:.1f} MPa SF={ALLOW["PAHT-CF"]/pbear:.1f}; friction cap (800 N preload, 2 faces) {muN:.0f} Nm; with 50% creep {muN/2:.0f} Nm SF={muN/2/T:.1f}; washer p={washer:.0f} MPa SF={ALLOW["PAHT-CF"]/washer:.2f}')
print('M3 shear 3 sharing: tau=%.0f MPa vs 0.6*640'%(104/5.03))
# axial from lateral (see LC-L): 1.7 kN over 3-5 bolts
for F in (970,1700):
    print(f'axial {F} N on 5 bolts: {F/5:.0f} N each ({F/5/ (0.9*640*5.03):.2f} of M3 proof); cover lip shear area pi*42*1.5={pi*42*1.5:.0f} mm2 -> tau={F/(pi*42*1.5):.1f} MPa SF={0.577*ALLOW["PAHT-CF"]*0.4/(F/(pi*42*1.5)):.1f} (Z-layer 0.4)')
# ---- ear tear-out / skirt tube
print('\n== ear & skirt')
e=5-1.7; print('ear tear-out tau=%.1f MPa (e=%.1f mm, t=6) SF=%.1f; edge distance 5 mm = %.1f d (rule 2.5d)'%(104/(2*6*e),e,0.577*ALLOW['PAHT-CF']/(104/(2*6*e)),5/3))
T=20; tau=T*1000/(2*pi*48.6**2*2.4*0.8); print('skirt shear %.2f MPa'%tau)
for n in ('LC-A ctrl sym','LC-D fault 1 wheel'):
    F=cases[n]+Fspring; Mb=F*77.5/1000
    sig=Mb*1000/(pi*48.6**2*2.4*0.8); print(f'{n}: stack bending at plate Mb={Mb:.0f} Nm sigma={sig:.1f} MPa, with Kt 2.5 at windows {2.5*sig:.1f}; SF={ALLOW["PAHT-CF"]/(2.5*sig):.2f}')
# ---- Al plate bolts
print('\n== Al plate 4xM4 at +-44 (r=62.2)')
rb=44*math.sqrt(2)
for T,F in ((20,0),(16,cases['LC-D fault 1 wheel']+Fspring),(5,cases['LC-C ctrl 1 wheel']+Fspring)):
    V=T*1000/(4*rb); 
    for tag,Mb in (('all moment through plate',F*77.5/1000),('side plate carries radial',0)):
        shear=math.hypot(V,F/4 if Mb else 0); ten=Mb*1000/(2*88) if Mb else 0
        pb=shear/(4.5*3); pp=shear/(4*6)
        print(f'T={T} F={F:.0f} {tag:26s}: shear/bolt {shear:5.0f} N tension {ten:5.0f} N  Al bearing {pb:4.0f} MPa (6061 ~380) body-plate bearing {pp:4.1f} MPa SF PAHT={ALLOW["PAHT-CF"]/pp:4.2f} PETG={ALLOW["PETG"]/pp:4.2f}; M4 8.8 shear tau={shear/12.6:.0f}')
# ---- lateral landing slide (theory: add mu*F_axle) 
print('\n== LC-L lateral slide')
for n,Fax,h in (('LC-C',192,215),('LC-D',337,215)):
    Fy=0.8*Fax; Mx=Fy*h/1000; ax=Mx*1000/34
    print(f'{n}: Fy={Fy:.0f} N, roll moment {Mx:.0f} Nm, hip/B-pin axial couple (34 mm lever) {ax:.0f} N')
