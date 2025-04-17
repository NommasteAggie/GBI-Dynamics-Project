import matplotlib.pyplot as plt
import numpy as np

# Constants based on Lockheed Martin THAAD
ceiling = 150000  # meters
impulse_specific = 304  # seconds
force_thrust = 33434  # N
mass_int = 900  # kg
mass_of_fuel = 825  # kg
max_velocity = 2800  # m/s
time = int(round(ceiling / max_velocity, 0))  # Estimated powered flight duration (s)
mass_dot = mass_of_fuel / time  # kg/s
time_interception = 30000 / 1416.3334  # Time until interception
d = 1  # Time step (s)
simulation_time = 500

# Drag-related constants
rho_0 = 1.225  # kg/m³ at sea level
H = 8500  # scale height (m)
Cd = 0.3  # drag coefficient
A = 0.3  # cross-sectional area in m²

### === ORIGINAL MODELS (No Drag) ===

# Varying mass without drag
v = [0]; t = [0]; y = [0]; a = []; burnout_time = 0
for i in range(0, simulation_time):
    if i < time:
        m = mass_int - mass_dot * i
        W = m * 9.81
        net_force = force_thrust - W - mass_dot * v[-1]
    else:
        if burnout_time == 0:
            burnout_time = i
        m = mass_int - mass_of_fuel
        net_force = -m * 9.81
    dv = (net_force / m) * d
    v_new = v[-1] + dv
    y_new = y[-1] + v_new * d
    if y_new < 0: break
    v.append(v_new)
    y.append(y_new)
    t.append(i + 1)
    a.append(dv / d)

# Constant mass without drag
v_1 = [0]; y_1 = [0]; a_1 = []
for i in range(0, simulation_time):
    if i < time:
        m_1 = mass_int
        net_force = force_thrust - m_1 * 9.81
    else:
        m_1 = mass_int - mass_of_fuel
        net_force = -m_1 * 9.81
    dv_1 = (net_force / m_1) * d
    v_new_1 = v_1[-1] + dv_1
    y_new_1 = y_1[-1] + v_new_1 * d
    if y_new_1 < 0: break
    v_1.append(v_new_1)
    y_1.append(y_new_1)
    a_1.append(dv_1 / d)

### === NEW MODELS WITH DRAG ===

# Varying mass with drag
v_drag = [0]; y_drag = [0]; a_drag = []; t_drag = [0]
for i in range(0, simulation_time):
    if i < time:
        m = mass_int - mass_dot * i
        W = m * 9.81
        rho = rho_0 * np.exp(-y_drag[-1] / H)
        Fd = 0.5 * rho * Cd * A * v_drag[-1]**2
        drag_dir = -1   if v_drag[-1] > 0 else 1
        net_force = force_thrust - W + drag_dir * (Fd) - mass_dot * v_drag[-1]
    else:
        m = mass_int - mass_of_fuel
        W = m * 9.81
        rho = rho_0 * np.exp(-y_drag[-1] / H)
        Fd = 0.5 * rho * Cd * A * v_drag[-1]**2
        drag_dir = -1  if v_drag[-1] > 0 else 1
        net_force = -W + drag_dir * (Fd)
    dv = (net_force / m) * d
    v_new = v_drag[-1] + dv
    y_new = y_drag[-1] + v_new * d
    if y_new < 0: break
    v_drag.append(v_new)
    y_drag.append(y_new)
    t_drag.append(i + 1)
    a_drag.append(dv / d)

# Constant mass with drag
v_drag_1 = [0]; y_drag_1 = [0]; a_drag_1 = []
for i in range(0, simulation_time):
    if i < time:
        m = mass_int
        W = m * 9.81
        #rho = 1.293
        rho = rho_0 * np.exp(-y_drag_1[-1] / H)
        Fd = 0.5 * rho * Cd * A * v_drag_1[-1]**2
        drag_dir = -1 if v_drag_1[-1] > 0 else 1
        net_force = force_thrust - W + drag_dir * (Fd)
    else:
        m = mass_int - mass_of_fuel
        W = m * 9.81
        rho = rho_0 * np.exp(-y_drag_1[-1] / H)
        #rho = 1.293
        Fd = 0.5 * rho * Cd * A * v_drag_1[-1]**2
        drag_dir = -1 if v_drag_1[-1] > 0 else 1
        net_force = -W + drag_dir * (Fd)
    dv = (net_force / m) * d
    v_new = v_drag_1[-1] + dv
    y_new = y_drag_1[-1] + v_new * d
    if y_new < 0: break
    v_drag_1.append(v_new)
    y_drag_1.append(y_new)
    a_drag_1.append(dv / d)

# Burnout point for markers
burnout_idx = time if time < len(t_drag) else -1

### === PLOTS ===

# Position Plot
plt.figure(figsize=(10, 7))
plt.plot(t, y, label="Varying Mass (No Drag)", linestyle='-', color='blue')
plt.plot(t[:len(y_1)], y_1, label="Constant Mass (No Drag)", linestyle='-', color='green')
plt.plot(t_drag, y_drag, label="Varying Mass + Drag", linestyle='--', color='blue')
plt.plot(t_drag[:len(y_drag_1)], y_drag_1, label="Constant Mass + Drag", linestyle='--', color='green')

if burnout_idx != -1:
    plt.scatter(t_drag[burnout_idx], y_drag[burnout_idx], marker='X', zorder=1, label="Burnout", color='red')
    plt.scatter(t_drag[burnout_idx], y_drag_1[burnout_idx], marker='X', zorder=1, color='red', s = 50)
    plt.scatter(t[burnout_idx], y[burnout_idx], marker='X', zorder=1, color='red', s = 50)
    plt.scatter(t_drag[burnout_idx], y_1[burnout_idx], marker='X', zorder=1, color='red', s = 50)

plt.hlines(y=15000, xmin=0, xmax=time_interception, color='r', linestyle='--', linewidth=1, label='Interception')
plt.vlines(x=time_interception, ymin=0, ymax=15000, color='r', linestyle=':', linewidth=1, label='Interception Time')
plt.ylabel("Height (m)")
plt.xlabel("Time (s)")
plt.title("GBI Position")
plt.legend()
plt.grid()
plt.minorticks_on()
plt.savefig("GBI_position_all")

# Velocity Plot
plt.figure(figsize=(10, 7))
plt.title("GBI Velocity")
plt.plot(t, v, label="Varying Mass (No Drag)")
plt.plot(t[:len(v_1)], v_1, label="Constant Mass (No Drag)")
plt.plot(t_drag, v_drag, label="Varying Mass + Drag", color='purple')
plt.plot(t_drag[:len(v_drag_1)], v_drag_1, label="Constant Mass + Drag", color='orange')
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.legend()
plt.grid()
plt.savefig("GBI_velocity_all")

# Acceleration Plot
plt.figure(figsize=(10, 7))
plt.title("GBI Acceleration")
plt.plot(t[:len(a)], a, label="Varying Mass (No Drag)")
plt.plot(t[:len(a_1)], a_1, label="Constant Mass (No Drag)")
plt.plot(t_drag[:len(a_drag)], a_drag, label="Varying Mass + Drag", color='purple')
plt.plot(t_drag[:len(a_drag_1)], a_drag_1, label="Constant Mass + Drag", color='orange')
plt.xlabel("Time (s)")
plt.ylabel("Acceleration (m/s²)")
plt.axhline(y=0, color='gray', linestyle='--', linewidth=1)
plt.legend()
plt.grid()
plt.savefig("GBI_acceleration_all")
