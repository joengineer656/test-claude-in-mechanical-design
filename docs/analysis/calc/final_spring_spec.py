"""Hip snapper spring check + purchasable spec: 3.5 N/mm, F0 15 N, Fmax 169 N, 2.0 mm music wire, OD 13 (Wahl / Shigley ch.10).
Run (from this folder): python3 final_spring_spec.py > final_spring_spec_output.txt"""
import math, numpy as np
import leg_refit_jump as L
import p3_spring as sp

d, OD, k, F0, Fmax = 2.0, 13.0, 3.5, 15.0, 169.0          # mm, mm, N/mm, N, N
G = 79.3e3      # MPa, ASTM A228 (Shigley 11.5 Mpsi); G=81.5 used in earlier scripts changes Na by 3 %
Sut = 2211 / d ** 0.145                                    # MPa, A228 (Shigley A=2211 MPa mm^m, m=0.145)
D = OD - d; C = D / d
Kw = (4 * C - 1) / (4 * C - 4) + 0.615 / C
tau = lambda F: 8 * F * D * Kw / (math.pi * d ** 3)
Na = G * d ** 4 / (8 * D ** 3 * k)
print(f"Wire {d} mm A228: Sut {Sut:.0f} MPa; D {D:.1f}, ID {OD-2*d:.1f}, C {C:.2f}, Wahl Kw {Kw:.3f}")
print(f"Active coils for {k} N/mm: Na = {Na:.1f} (G {G/1e3:.1f} GPa); body coils Nb = Na - G/E(0.4) = {Na-0.4:.1f}; body length (Nb+1)d = {(Na-0.4+1)*d:.1f} mm")
print(f"Initial tension {F0} N -> tau_i = {8*F0*D/(math.pi*d**3):.0f} MPa (typical winding range C=5.5: ~28-85 MPa) -> achievable")
print("\nBody shear (Wahl), allowable 0.45 Sut = %.0f MPa (static, stress-relieved)" % (0.45 * Sut))
for lab, F in (("F0 15 N", F0), ("nominal 195 mm", None), ("Fmax 169 N", Fmax)):
    if F: print(f"  {lab}: {tau(F):.0f} MPa, SF {0.45*Sut/tau(F):.2f}")
# hook: Shigley full-loop eq. with C1 = 2 r1/d; bending allowable 0.75 Sut, torsion at the bend (C2) 0.40 Sut
def hook(Deff, r1, r2, F):
    C1 = 2 * r1 / d; C2 = 2 * r2 / d
    Kb = (4 * C1 ** 2 - C1 - 1) / (4 * C1 * (C1 - 1)); Kt = (4 * C2 - 1) / (4 * C2 - 4)
    sb = F * (Kb * 16 * Deff / (math.pi * d ** 3) + 4 / (math.pi * d ** 2))
    tt = Kt * 8 * F * Deff / (math.pi * d ** 3)
    return sb, tt
print("\nHook stresses at 169 N (bend A bending, bend B torsion); allow bending 0.75 Sut = %.0f, torsion 0.40 Sut = %.0f MPa" % (0.75 * Sut, 0.4 * Sut))
for lab, Deff, r1, r2 in (("full loop, hook D = coil D (11 mm), r1 = D/2, r2 = 2d", D, D / 2, 2 * d),
                          ("full loop, r2 = 3d", D, D / 2, 3 * d),
                          ("reduced hook: hook mean D 8.5 (ID 6.5), arm = mean(D, Dh) = 9.75, r1 4.25, r2 = 3d (ESTIMATE)", (D + 8.5) / 2, 4.25, 3 * d)):
    sb, tt = hook(Deff, r1, r2, Fmax)
    print(f"  {lab}: bending {sb:.0f} MPa (SF {0.75*Sut/sb:.2f}), torsion {tt:.0f} MPa (SF {0.4*Sut/tt:.2f})")
# lengths and forces from the rev 2 CAD kinematics
B, A = (39, 31), (97.4, 70.9)
ph, y, J = L.leg_tables(B)
sp.A = np.array(A) * 1e-3
sl = lambda h: float(sp.spring_len(float(np.interp(h * 1e-3, y, ph)))) * 1e3
Lext = sl(289)
print(f"\nPin-centre distance (CAD rev 2): h289 {Lext:.1f}, h195 {sl(195):.1f}, h140 {sl(140):.1f} mm; ext. at 140 = {sl(140)-Lext:.1f} mm")
pin = 5.0
print(f"Anchor/crank pins are 5 mm, so inside-hook length at F0 (= free length) Li = {Lext+pin:.1f} mm; at crouch {sl(140)+pin:.1f} mm")
print("force vs hip height (incl. over-travel into the TPU stop; mechanical reach 116 mm):")
for h in (289, 250, 195, 160, 140, 130, 120, 116):
    ext = sl(h) - Lext; F = F0 + k * ext
    print(f"  h {h}: spring {sl(h):.1f} mm, ext {ext:.1f}, F {F:.0f} N, body tau {tau(F):.0f} MPa ({tau(F)/(0.45*Sut)*100:.0f} % of allow)")
Fy = 0.45 * Sut / tau(1.0)
print(f"Force at the 0.45 Sut body limit: {Fy:.0f} N = extension {(Fy-F0)/k:.1f} mm (beyond free) -> hip height ~{ [h for h in range(289,115,-1) if F0+k*(sl(h)-Lext) > Fy][:1] }")
# fatigue (Zimmerli, unpeened): Ssa 398, Ssm 534 MPa @1e7 cycles; Gerber/Goodman with Ssu = 0.67 Sut
Ssu = 0.67 * Sut; Sse = 398 / (1 - 534 / Ssu)
def goodman(Fmin, Fmax_):
    ta, tm = (tau(Fmax_) - tau(Fmin)) / 2, (tau(Fmax_) + tau(Fmin)) / 2
    r = ta / tm; Ssa = r * Sse * Ssu / (r * Ssu + Sse)
    return ta, tm, Ssa / ta
Fnom = F0 + k * (sl(195) - Lext)
print(f"\nFatigue (Zimmerli unpeened, Sse {Sse:.0f} MPa @1e7, Goodman): jump cycle 15->169 N: ta {goodman(F0,Fmax)[0]:.0f}, tm {goodman(F0,Fmax)[1]:.0f}, SF(1e7) {goodman(F0,Fmax)[2]:.2f}; "
      f"stance cycle 15->{Fnom:.0f} N: SF {goodman(F0,Fnom)[2]:.2f}")
print("  Jump count in the test plan: ~500 jumps (structural S10) -> finite life, far below 1e7; hook fatigue is the limiter, not the body.")
# mass
Lw = math.pi * D * (Na + 3) + 2 * 25
print(f"\nWire length ~{Lw:.0f} mm -> mass {Lw*math.pi/4*d*d*7.85e-6*1e3:.0f} g/spring (BOM placeholder 35 g)")
