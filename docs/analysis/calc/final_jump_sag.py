"""Jump with the final spring (3.5 N/mm, F0 15 N, Fmax 169 N) at 6.4 / 6.9 kg incl. battery sag.
Run (from this folder): python3 final_jump_sag.py > final_jump_sag_output.txt
Same push-off model as theory_calc.jump (hip 6:1, 40 A, CAD 4-bar rev 2 tables from leg_refit_jump), but the bus voltage
sags: V = Voc - R_int * I_bat, I_bat = P_elec / V, P_elec = 2 * (Ke*w*I + I^2*R_ll)  (two hips). Real = sim x 0.80 (O13/P3 convention)."""
import math, numpy as np
import leg_refit_jump as L
import theory_calc as tc
G = tc.g

def jump_sag(ph, y, J, T, mb, mu_tot, Voc, Rint, N=6, Ilim=40.0, dt=2e-5):
    yy, v, t = tc.Y_CROUCH, 0.0, 0.0
    Ipk = Ibat_pk = Vmin = Voc
    Ibat_pk = 0.0
    while yy < tc.Y_EXT:
        Jy = np.interp(yy, y, J); phi = np.interp(yy, y, ph)
        wm = N * v / Jy
        def cur(Vb):
            I = min(Ilim, max(0.0, (tc.K_MOD * Vb - tc.KE * abs(wm)) / tc.R_LL))
            return I, (2 * (tc.KE * abs(wm) * I + I * I * tc.R_LL)) / Vb
        lo, hi = 0.4 * Voc, Voc                               # bisection on Vb + Rint*Ib(Vb) = Voc (Ib falls as Vb rises)
        for _ in range(30):
            Vb = (lo + hi) / 2
            lo, hi = (Vb, hi) if Vb + Rint * cur(Vb)[1] < Voc else (lo, Vb)
        I, Ib = cur(Vb)
        Tm = tc.KT * I
        F = (Tm * N * tc.ETA_H + T(phi)) / Jy
        v += (2 * F / mb - G) * dt; yy += v * dt; t += dt
        Ibat_pk = max(Ibat_pk, Ib); Vmin = min(Vmin, Vb); Ipk = max(Ipk, I)
        if t > 1: return None
    M = mb + mu_tot; vto = mb * v / M
    return dict(h=vto * vto / (2 * G), Ib=Ibat_pk, Vmin=Vmin, t=t)

if __name__ == '__main__':
    B, A, k, F0 = (39, 31), (97.4, 70.9), 3500, 15.0
    print("Final spring 3.5 N/mm, F0 15 N; hip 6:1; unsprung 0.84 kg/side; min hip height 140 mm; real = sim x 0.80")
    print("| mass kg | Voc (pack open-circuit) | R_int mOhm | V min under load | peak battery A | push-off ms | jump sim cm | jump real cm |")
    print("|---|---|---|---|---|---|---|---|")
    for mass in (6.4, 6.9):
        r0 = L.jump(B, A, mass, k=k, F0=F0)        # fixes tc state (motor KV130, mass, Y_CROUCH) and returns fixed-V result
        ph, y, Jt = L.leg_tables(B)
        tc.set_motor(130); tc.M_TOT = mass; tc.Y_CROUCH = 0.140
        import p3_spring as sp
        sp.A = np.array(A) * 1e-3
        L_ext = float(sp.spring_len(float(np.interp(tc.Y_EXT, y, ph))))
        def T(phi):
            l = float(sp.spring_len(np.array(phi))); dl = (float(sp.spring_len(np.array(phi) + 1e-5)) - float(sp.spring_len(np.array(phi) - 1e-5))) / 2e-5
            return max(0.0, F0 + k * (l - L_ext)) * abs(dl)
        mb = mass - 1.68
        for Voc, Rint, lab in ((25.2, 0.0, "fixed 25.2"), (22.2, 0.0, "fixed 22.2 (no sag)"), (19.8, 0.0, "fixed 19.8 (old test value)"),
                               (25.2, 0.040, ""), (22.2, 0.040, ""), (22.2, 0.080, "aged/cold pack"), (20.5, 0.040, "near empty, 3.4 V/cell"), (20.5, 0.080, "near empty, aged")):
            r = jump_sag(ph, y, Jt, T, mb, 1.68, Voc, Rint)
            print(f"| {mass} | {Voc} {lab} | {Rint*1e3:.0f} | {r['Vmin']:.1f} V | {r['Ib']:.0f} | {r['t']*1e3:.0f} | {r['h']*100:.1f} | **{r['h']*80:.1f}** |")
    print("\nCheck: 'fixed 19.8' row equals leg_refit_jump (20.2 cm at 6.4 kg, 19.7 at 6.9 kg).")
