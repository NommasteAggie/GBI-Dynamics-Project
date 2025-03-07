import matplotlib.pyplot as plt

# Variables based on Lockheed Martin THAAD
ceiling = 150000 # meters
force_thrust = 33434  # Estimated thrust in Newtons
mass_int = 900  # kg
mass_of_fuel = 825  # kg
max_velocity = 2800  # m/s
time = int(round(ceiling/max_velocity,0)) # Total time (s) Ceiling/velocity
mass_dot = mass_of_fuel/time  # kg/s
d = 1  # Time step (s)


# Initial weight (at t=0)
weight = mass_int * 9.81  # Newtons

# Function to compute delta-V
def delta_v(dt, W, F, dm, m, v):
    return dt * (F - W - dm * v) / m if m > 0 else 0  # Prevent division by zero

# Main Execution
if __name__ == "__main__":
    v = [0]
    t = [0]
    y = [0]
    # Change in mass calculations
    for i in range(0, time, d):
        m = mass_int - mass_dot * i  # Mass decreases as fuel burns
        if m <= mass_int - mass_of_fuel:  # Stop simulation when fuel runs out
            break

        W = m * 9.81  # Update weight
        dv = delta_v(d, W, force_thrust, mass_dot, m, v[i])
        dy = (v[i] +dv) * d
        v_new = v[i] + dv
        y_new = y[i] + dy
        v.append(v_new)
        y.append(y_new)
        t.append(i+1)


    # Constant Mass calculations
    v_1 = [0]
    y_1 = [0]
    for i in range(0, time, d):
        m_1 = mass_int
        W_1 = m_1 * 9.81
        dv_1 = ((force_thrust - W_1) / m_1) * d
        dy_1 = (v_1[i] + dv_1) * d
        v_new_1 = v_1[i] + dv_1
        y_new_1 = y_1[i] + dy_1
        v_1.append(v_new_1)
        y_1.append(y_new_1)

    # Plot results

    plt.figure(1, figsize=(10, 7))

    plt.plot(t, y, label="Height (Varying Mass)")
    plt.plot(t, y_1, label="Height (Constant Mass)")
    plt.hlines(y=15000, xmin=0, xmax=75, color='g', linestyle=':', linewidth=1, label='Interception')
    plt.vlines(x=18, ymin=0, ymax=15000, color='b', linestyle=':', linewidth=1, label='Interception Time')
    plt.ylabel("Height (m)")
    plt.xlabel("Time (s)")
    plt.title("GBI Position")
    plt.legend()
    plt.grid()
    plt.minorticks_on()
    plt.savefig("GBI_position")

    plt.figure(2, figsize=(10, 7))
    plt.title("GBI Velocity")
    plt.plot(t, v, label="Velocity (Varying Mass)", color='g')
    plt.plot(t, v_1, label="Velocity (Constant Mass)", color="red")
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.legend()
    plt.grid()
    plt.savefig("GBI_velocity")
