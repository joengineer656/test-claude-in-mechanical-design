"""2D (sagittal) wheeled inverted pendulum: LQR sanity check + torque/speed requirement.
numpy only (scipy not installed): CARE solved by the Hamiltonian eigenvector method.
State s = [x, xdot, theta, thetadot] (theta = body pitch from vertical, +forward lean),
input u = total wheel output torque (both wheels), acting wheel <-> body (stator on leg).
Run: python3 sim_lqr_2d.py   (edit PARAMS below; all SI units)."""
import numpy as np

PARAMS = dict(
    m_total=3.6,      # kg, whole robot (design_targets.md; also run 4.0)
    m_wheel=0.72,     # kg, ONE wheel assembly incl. hub motor + gearbox (unsprung, theory.md A2)
    r=0.085,          # m, wheel radius (Ø170)
    l=0.25,           # m, body CoM height above axle (varies with leg length)
    k_g=0.12,         # m, body pitch radius of gyration about its CoM
    I_wheel=1.0e-3,   # kg m², ONE wheel+tyre+ring spinning at wheel speed
    J_rotor=2.0e-4,   # kg m², ONE 8308 rotor (ESTIMATE, verify)
    N=3.91,           # wheel gear ratio (23/22/67 planetary)
    KV=130.0,         # rpm/V; Kt = 8.27/KV
    i_max=15.0,       # A, wheel current limit
    eta=0.85,         # gearbox efficiency
    mu=0.8,           # tyre friction (no-slip model, so traction is applied as a torque clip)
    g=9.81,
)

def matrices(p, th=0.0):
    mb = p["m_total"] - 2 * p["m_wheel"]
    Ib = mb * p["k_g"] ** 2
    J, N, r, l = 2 * p["J_rotor"], p["N"], p["r"], p["l"]
    Iw = 2 * p["I_wheel"]
    # rotor abs. speed = N*xdot/r - (N-1)*thetadot (stator fixed to leg/body)
    M = np.array([[2 * p["m_wheel"] + mb + Iw / r**2 + J * N**2 / r**2, mb * l * np.cos(th) - J * N * (N - 1) / r],
                  [mb * l * np.cos(th) - J * N * (N - 1) / r,             mb * l**2 + Ib + J * (N - 1) ** 2]])
    return M, mb

def f(s, u, p):
    x, v, th, w = s
    M, mb = matrices(p, th)
    rhs = np.array([u / p["r"] + mb * p["l"] * np.sin(th) * w**2, -u + mb * p["g"] * p["l"] * np.sin(th)])
    a = np.linalg.solve(M, rhs)
    return np.array([v, a[0], w, a[1]])

def linear(p):
    M, mb = matrices(p)
    Mi = np.linalg.inv(M)
    G = Mi @ np.array([[0, 0], [0, mb * p["g"] * p["l"]]])  # d(acc)/d(x,theta)
    Bq = Mi @ np.array([1 / p["r"], -1.0])
    A = np.array([[0, 1, 0, 0], [G[0, 0], 0, G[0, 1], 0], [0, 0, 0, 1], [G[1, 0], 0, G[1, 1], 0]])
    B = np.array([[0], [Bq[0]], [0], [Bq[1]]])
    return A, B

def lqr(A, B, Q, R):
    n = A.shape[0]
    Ri = np.linalg.inv(R)
    H = np.block([[A, -B @ Ri @ B.T], [-Q, -A.T]])
    w, V = np.linalg.eig(H)
    U = V[:, w.real < 0]
    P = np.real(U[n:] @ np.linalg.inv(U[:n]))
    res = A.T @ P + P @ A - P @ B @ Ri @ B.T @ P + Q
    assert np.abs(res).max() < 1e-6 * max(1, np.abs(P).max()), "CARE residual too big"
    K = Ri @ B.T @ P
    assert np.all(np.linalg.eigvals(A - B @ K).real < 0), "closed loop not stable"
    return K

# Bryson weights: x 0.5 m, v 1 m/s, theta 0.1 rad, thetadot 1 rad/s, torque 5 N m
Q = np.diag([1 / 0.5**2, 1 / 1.0**2, 1 / 0.1**2, 1 / 1.0**2])
R = np.array([[1 / 5.0**2]])

def sim(p, K, th0, u_max=np.inf, T=3.0, dt=1e-3, ctrl_hz=500):
    """Nonlinear sim, controller at ctrl_hz with one-sample delay, torque clipped to ±u_max."""
    s = np.array([0, 0, np.radians(th0), 0.0])
    every = int(round(1 / (ctrl_hz * dt)))
    u_next = u = 0.0
    peak_u = peak_v = 0.0
    for k in range(int(T / dt)):
        if k % every == 0:
            u, u_next = u_next, float(np.clip(-(K @ s)[0], -u_max, u_max))
        k1 = f(s, u, p); k2 = f(s + dt / 2 * k1, u, p); k3 = f(s + dt / 2 * k2, u, p); k4 = f(s + dt * k3, u, p)
        s = s + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        peak_u, peak_v = max(peak_u, abs(u)), max(peak_v, abs(s[1]))
        if abs(s[2]) > np.radians(60):
            return False, peak_u, peak_v
    return abs(s[2]) < np.radians(1) and abs(s[3]) < 0.1, peak_u, peak_v

def min_torque(p, K, th0):
    lo, hi = 0.05, 50.0
    for _ in range(30):
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if sim(p, K, th0, mid)[0] else (mid, hi)
    return hi

def hold_torque(p, th0):
    """Torque that keeps the body at a constant tilt th0 (thetaddot = 0, from rest): physics floor."""
    th = np.radians(th0)
    M, mb = matrices(p, th)
    # unknowns xdd, u: M[0,0]xdd - u/r = 0 ; M[1,0]xdd + u = mb g l sin th
    a = np.linalg.solve(np.array([[M[0, 0], -1 / p["r"]], [M[1, 0], 1.0]]), [0, mb * p["g"] * p["l"] * np.sin(th)])
    return a[1], a[0]

def torque_limit(p):
    """Total usable wheel torque: min(motor current limit, traction)."""
    motor = 2 * (8.27 / p["KV"]) * p["i_max"] * p["N"] * p["eta"]
    traction = p["mu"] * p["m_total"] * p["g"] * p["r"]
    return min(motor, traction), motor, traction

def max_tilt(p, K, u_max):
    lo, hi = 0.0, 45.0
    for _ in range(14):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if sim(p, K, mid, u_max, T=5.0)[0] else (lo, mid)
    return lo

if __name__ == "__main__":
    print(f"{'m[kg]':>5} {'l[m]':>5} {'tilt':>5} {'floor[Nm]':>9} {'LQR pk':>7} {'pk@lim':>7} {'min sat':>7} {'dv pk':>6} {'max tilt':>8}")
    for m_total in (3.6, 4.0):
        for l in (0.15, 0.23, 0.35):
            p = dict(PARAMS, m_total=m_total, l=l)
            A, B = linear(p)
            K = lqr(A, B, Q, R)
            u_lim, motor, traction = torque_limit(p)
            mt = max_tilt(p, K, u_lim)
            for th0 in (5, 10):
                ok, pk, _ = sim(p, K, th0)
                assert ok, "unsaturated LQR must recover"
                okl, pkl, dv = sim(p, K, th0, u_lim)
                assert okl, "must recover at the torque limit"
                print(f"{m_total:5.1f} {l:5.2f} {th0:4d}° {hold_torque(p, th0)[0]:9.2f} {pk:7.2f} {pkl:7.2f} "
                      f"{min_torque(p, K, th0):7.2f} {dv:6.2f} {mt:7.1f}°")
        print(f"  m={m_total}: limit total {u_lim:.2f} N m = min(motor 15 A {motor:.2f}, traction {traction:.2f})")
    p = PARAMS
    w_m = 0.7 * p["KV"] * 19.8 * 2 * np.pi / 60  # ODrive v3.6 speed factor 0.7 (design_targets.md)
    v_cap = w_m / p["N"] * p["r"]
    print(f"\nRatio rule @19.8 V, factor 0.7: motor {w_m:.0f} rad/s -> wheel surface {v_cap:.2f} m/s (no load)")
    print(f"  N_max for 12 km/h + 1.0 m/s headroom = {w_m * p['r'] / (12 / 3.6 + 1.0):.2f} (N = {p['N']})")
    print("Torques are TOTAL for both wheels at the wheel shaft; per wheel = half.")
    print("K (m=3.6, l=0.23):", np.round(lqr(*linear(dict(PARAMS, l=0.23)), Q, R), 2))
