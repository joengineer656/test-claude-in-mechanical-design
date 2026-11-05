"""Leg spec checks (no CAD). Hip-relative frame, x fwd, z up, mm. Run: python3 leg_spec_calc.py"""
import numpy as np
def brentq(f,a,b):
    fa=f(a)
    for _ in range(80):
        m=(a+b)/2; fm=f(m)
        if fa*fm<=0: b=m
        else: a,fa=m,fm
    return (a+b)/2
T,S,CP,KC,BEND=121.,189.,113.,42.,175.
B=np.array([46.,34.]); HIPX=28.
def u(a): return np.array([np.cos(np.radians(a)),np.sin(np.radians(a))])
def pose(th):
    K=T*u(th)
    f=lambda s:np.linalg.norm(K+KC*u(s+BEND)-B)-CP
    ss=np.linspace(-180,-60,800); v=[f(s) for s in ss]
    for i in range(799):
        if v[i]*v[i+1]<0: s=brentq(f,ss[i],ss[i+1]); break
    C=K+KC*u(s+BEND); W=K+S*u(s)
    return dict(th=th,sh=s,K=K,C=C,W=W,h=-W[1])
def at_h(h): return pose(brentq(lambda t:pose(t)['h']-h,-74,1))
P={h:at_h(h) for h in (101,130,195,289)}
for h,p in P.items(): print(h,"th %.2f sh %.2f K %s C %s W %s"%(p['th'],p['sh'],p['K'].round(1),p['C'].round(1),p['W'].round(1)),"C world x %.1f"%(p['C'][0]+HIPX))
cs=[pose(t)['C'] for t in np.linspace(-73,1,200)]
print("C pin x range (hip-rel) %.1f..%.1f z %.1f..%.1f"%(min(c[0] for c in cs),max(c[0] for c in cs),min(c[1] for c in cs),max(c[1] for c in cs)))
# spring: crank 40 opposite thigh, body anchor
A=np.array([94.1,71.2])
def seg_d(p,a,b):
    t=np.clip(np.dot(p-a,b-a)/np.dot(b-a,b-a),0,1); return np.linalg.norm(p-(a+t*(b-a)))
for h,p in P.items():
    cr=-40*u(p['th']); L=np.linalg.norm(A-cr)
    print("h%d spring len %.1f  to B %.1f (centre line; minus r6.5 minus pin r5 = %.1f)"%(h,L,seg_d(B,cr,A),seg_d(B,cr,A)-6.5-5))
# 4-bar force transfer at hip 130, LC-D: shank moment about K
for h in (101,130):
    p=P[h]; arm_h=abs(p['W'][0]-p['K'][0]); arm_v=abs(p['W'][1]-p['K'][1])
    print("h",h,"arms to K: horiz %.0f vert %.0f -> M(337N vert) %.1f Nm; +mu 0.8 horiz %.1f Nm"%(arm_h,arm_v,337*arm_h/1e3,(337*arm_h+0.8*337*arm_v)/1e3))
# sections (mm, N, MPa). PAHT-CF conditioned UTS 65: static allow 45.5, one-way fatigue 19.5, reversed 14.3, E 5 GPa assumed
ST,FO,FR,E=45.5,19.5,14.3,5000.
def box(b,h,t): return (b*h**3-(b-2*t)*(h-2*t)**3)/12.
# thigh: stop station, Y10, depth 56, wall 3 (channel + 2mm cover => closed box)
Ith=box(10,56,3); Zth=Ith/28; Mld=2011*(121-73); Mc=597*(121-73)
print("thigh Z %.0f  M_D %.0f Nm sigma %.1f SF %.2f | LC-C sigma %.1f SF_oneway %.2f"%(Zth,Mld/1e3,Mld/Zth,ST/(Mld/Zth),Mc/Zth,FO/(Mc/Zth)))
# shank at K: depth 44, Y12, wall: web 3 + walls 2.4 channel + 2mm Al cover (E 69000), modular ratio
n=69000/E; Ish_p=box(10,44,2.4); Ial=2*38**3/12
# treat as: printed channel I (approx closed-box wall 2.4) + Al plate
M=337*154+0.8*337*114  # N.mm hip 130 pose, sliding
Mv=337*154
Ieq=Ish_p+n*Ial; kAl=n*Ial/Ieq
sAl=kAl*M/(2*38**2/6); sP=(1-kAl)*M/(Ish_p/22)
print("shank K: Al share %.2f, Al sigma %.0f MPa (SF yield240 %.2f); printed sigma %.1f SF %.2f (vertical only: %.1f SF %.2f)"%(kAl,sAl,240/sAl,sP,ST/sP,(1-kAl)*Mv/(Ish_p/22),ST/((1-kAl)*Mv/(Ish_p/22))))
# printed only (no plate)
print("shank printed-only sigma %.1f SF %.2f"%(M/(Ish_p/22),ST/(M/(Ish_p/22))))
# side fall LC3: 300 N lateral at tyre, arm 189 to K, weak axis
Iw=(44*10**3-38*5.2**3)/12; Iw2=Iw+n*(38*2**3/12+ 76*4**2)  # plate on outer face, 5mm from centroid
print("weak-axis printed-only sigma %.0f MPa; with Al plate share"%(300*189/(Iw/6)), "Ieq %.0f vs %.0f"%(Iw2,Iw))
# coupler 14 x 16 hollow wall 2.4 (eyes 34 OD), Pcr
Ic=box(16,14,2.4); Io=box(14,16,2.4)  # out-of-plane (weak): width in Y=14
Ao=14*16-(14-4.8)*(16-4.8)
for nm,I in (("in-plane",(14*16**3-9.2*11.2**3)/12),("out-of-plane",(16*14**3-11.2*9.2**3)/12)):
    Pcr=np.pi**2*E*I/CP**2; print("coupler",nm,"I %.0f Pcr %.0f N SF %.1f (1955 N)"%(I,Pcr,Pcr/1955))
print("coupler area %.0f sigma %.1f SF %.2f; eye OD34 lug Kt2.5: %.1f SF %.2f"%(Ao,1955/Ao,ST/(1955/Ao),2.5*1955/(2*6*14),ST/(2.5*1955/(2*6*14))))
# pin d10 12.9 steel single-shear offset
for d in (8,10):
    M=2011*24/2; print("pin d%d bending %.0f MPa shear %.0f MPa"%(d,32*M/(np.pi*d**3),2011/(np.pi*d*d/4)))
print("bushing p knee Ø10x12 shank %.1f MPa, Ø10x10 thigh %.1f MPa"%(2011/(10*12),2011/(10*10)))
# mass
rho=1.2
vth=(0.5*(Ith and (56*10-50*4)*0+ (10*56-4*50))*0+0)
def area_box(b,h,t): return b*h-(b-2*t)*(h-2*t)
th=np.mean([area_box(10,d,3) for d in (56,56,30,26)])*121/1e3*rho+ 2*(np.pi*(18**2-0)/4*10)/1e3*rho*0.6
sh_ch=(np.mean([ (44*3+2*2.4*9),(32*3+2*2.4*9)])*189 + 140*42)/1e3*rho +10/1e3*rho*1000*0
sh_al=(189*38+42*30)*2*2.7/1e3
cp=(area_box(14,16,2.4)*113+2*np.pi*17**2*14*0.5)/1e3*rho
print("mass g: thigh %.0f, shank PAHT %.0f + Al plate %.0f, coupler %.0f; sum %.0f vs budget 127"%(th,sh_ch,sh_al,cp,th+sh_ch+sh_al+cp))
