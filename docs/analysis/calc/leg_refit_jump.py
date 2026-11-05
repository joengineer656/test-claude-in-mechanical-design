"""Rev 2 leg refit check (hip 10.6 mm ahead of the axle at h195): jump with the CAD 4-bar kinematics.
Run: python3 leg_refit_jump.py   (reuses theory_calc + p3_spring.make; hip 6:1; CAD mass 6.0/6.4/6.9 kg; unsprung 0.84 kg/side)
Rev 1 = B (46,30) anchor (94.1,71.2); rev 2 = B (39,31) anchor (97.4,70.9). Spring 2.7 N/mm, F0 8 N, crank 40."""
import sys, math, numpy as np
sys.path.insert(0, '../../../cad/parts/src')
import build_leg as L
import theory_calc as tc
import p3_spring as sp

U = L.U


def leg_tables(B):
    L.B = np.array(B)
    rows = []
    for t in np.linspace(10, -85, 381):
        p = L.pose_th(t)
        if p: rows.append((p['h'], math.radians(t), p['W'][0]))
    rows = sorted(rows)
    h = np.array([r[0] for r in rows]); ph = np.array([r[1] for r in rows])
    keep = np.r_[True, np.diff(h) > 1e-6]
    h, ph = h[keep], ph[keep]
    # keep the branch used by the leg (monotonic th(h)): drop everything outside 100..300 mm
    m = (h > 100) & (h < 300)
    h, ph = h[m] * 1e-3, ph[m]
    J = np.abs(np.gradient(h, ph))
    return ph, h, J


def jump(B, A, mass, N=6, V=19.8, ymin=0.140, k=2700, F0=8.0):
    ph, y, J = leg_tables(B)
    tc.set_motor(130); tc.M_TOT = mass; tc.Y_CROUCH = ymin
    sp.A = np.array(A) * 1e-3
    L_ext = float(sp.spring_len(float(np.interp(tc.Y_EXT, y, ph))))
    def T(phi):
        l = float(sp.spring_len(np.array(phi)))
        dl = (float(sp.spring_len(np.array(phi) + 1e-5)) - float(sp.spring_len(np.array(phi) - 1e-5))) / 2e-5
        return max(0.0, F0 + k * (l - L_ext)) * abs(dl)
    mb = mass - 2 * 0.84
    r = tc.jump(N, V, mb, 2 * 0.84, T, (ph, y, J))
    r2 = tc.jump(N, 22.2, mb, 2 * 0.84, T, (ph, y, J))
    Lc = float(sp.spring_len(float(np.interp(ymin, y, ph))))
    s = Lc - L_ext
    yn = 0.195; phn = float(np.interp(yn, y, ph)); Jn = float(np.interp(yn, y, J))
    hold = T(phn) - mb * 9.81 / 2 * Jn      # motor torque per leg to hold nominal height (+ = spring wins)
    return dict(hold=hold, jump198=r['h'] * 80, jump222=r2['h'] * 80, Imax=r['Imax'], Tpk=tc.KT * r['Imax'] * N * tc.ETA_H, L_ext=L_ext * 1e3,
                L_cr=Lc * 1e3, stroke=s * 1e3, Fmax=F0 + k * s, E_leg=F0 * s + 0.5 * k * s * s, hmin=float(y.min()) * 1e3, hmax=float(y.max()) * 1e3)


if __name__ == "__main__":
    for lab, B, A, k, F0 in (("rev1 B(46,30) A(94.1,71.2) spring 2.7/8", (46, 30), (94.1, 71.2), 2700, 8.0),
                             ("rev2 B(39,31) A(97.4,70.9) spring 2.7/8", (39, 31), (97.4, 70.9), 2700, 8.0),
                             ("rev2 B(39,31) A(97.4,70.9) spring 3.5/15", (39, 31), (97.4, 70.9), 3500, 15.0)):
        for mass in (6.0, 6.4, 6.9):
            r = jump(B, A, mass, k=k, F0=F0)
            print(f"{lab} M={mass}: jump real(x0.8) {r['jump198']:.1f} cm @19.8 V, {r['jump222']:.1f} @22.2 V; hip peak {r['Tpk']:.1f} Nm; "
                  f"spring ext/crouch {r['L_ext']:.1f}/{r['L_cr']:.1f} mm, stroke {r['stroke']:.1f}, Fmax {r['Fmax']:.0f} N, E/leg {r['E_leg']:.2f} J; "
                  f"hold@195 {r['hold']:+.2f} Nm/leg; hip range {r['hmin']:.0f}..{r['hmax']:.0f}")
