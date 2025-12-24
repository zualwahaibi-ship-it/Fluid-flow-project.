import math

# =======================
# CONSTANTS
# =======================
rho = 1000
mu = 1e-3
g = 9.81
eta = 0.75
eps = 1.5e-6

# Velocity limits (fixed input)
Vmin = 4 * 0.3048     # m/s
Vmax = 6.5 * 0.3048   # m/s

K_VALUES = {
    "globe_valve": 6.3,
    "angle_valve": 3.0,
    "gate_valve": 0.13,
    "check_valve": 2.0,
    "elbow_90": 0.74,
    "elbow_45": 0.30,
    "long_radius_elbow": 0.46,
    "tee_run": 0.40,
    "tee_branch": 1.30,
    "coupling": 0.04,
    "union": 0.04
}

def friction_factor(Re, D):
    if Re < 2000:
        return 64 / Re
    return 0.001375 * (1 + (20000*(eps/D) + (1e6/Re))**(1/3))

def major_loss(f, L, D, V):
    return f * (L/D) * (V**2/(2*g))

def minor_loss(fittings, V):
    hm = 0
    for name, count in fittings.items():
        hm += count * K_VALUES.get(name, 0) * (V**2/(2*g))
    return hm


# =======================
# USER INPUT
# =======================
Q = float(input("Flow rate Q (m^3/s): "))
L = float(input("Pipe length L (m): "))
Z = float(input("Elevation head Z (m): "))
hours = float(input("Operating hours per year: "))
cost_kWh = float(input("Electricity cost per kWh: "))

print("\nAvailable fittings:")
for x in K_VALUES:
    print("-", x)

print("\nEnter fittings (name count), type 'done' when finished.")
fittings = {}

while True:
    entry = input("Fitting: ")
    if entry.lower() == "done":
        break
    name, count = entry.split()
    fittings[name] = int(count)

# =======================
# DIAMETERS
# =======================
D_min = math.sqrt((4*Q)/(math.pi * Vmax))   # smaller
D_max = math.sqrt((4*Q)/(math.pi * Vmin))   # larger


# =======================
# CASE 1 — USING Vmax & Dmin
# =======================
Re1 = rho * Vmax * D_min / mu
f1 = friction_factor(Re1, D_min)
hf1 = major_loss(f1, L, D_min, Vmax)
hm1 = minor_loss(fittings, Vmax)
H1 = hf1 + hm1 + Z
P1 = (rho*g*Q*H1)/(eta*1000)
C1 = P1 * hours * cost_kWh


# =======================
# CASE 2 — USING Vmin & Dmax
# =======================
Re2 = rho * Vmin * D_max / mu
f2 = friction_factor(Re2, D_max)
hf2 = major_loss(f2, L, D_max, Vmin)
hm2 = minor_loss(fittings, Vmin)
H2 = hf2 + hm2 + Z
P2 = (rho*g*Q*H2)/(eta*1000)
C2 = P2 * hours * cost_kWh


# =======================
# OUTPUT
# =======================
print("\n=========== RESULTS ===========")

print(f"Dmin at Vmax: {D_min:.4f} m ({D_min*1000:.1f} mm)")
print(f"Dmax at Vmin: {D_max:.4f} m ({D_max*1000:.1f} mm)")
print("--------------------------------")

print("CASE 1 — Using Vmax & Dmin")
print(f"Total Head: {H1:.3f} m")
print(f"Pump Power: {P1:.3f} kW")
print(f"Annual Cost: {C1:.2f}")
print("--------------------------------")

print("CASE 2 — Using Vmin & Dmax")
print(f"Total Head: {H2:.3f} m")
print(f"Pump Power: {P2:.3f} kW")
print(f"Annual Cost: {C2:.2f}")
print("================================")
