import numpy as np
import matplotlib.pyplot as plt


##This code simulates the dynamics of a double inverse pendulum.

# Constants
c1 = 1.0
c2 = 0.5
m = 1
g = 9.8

# Eval function
def f1(t1, t2, w1, w2):
    return np.array([
        w1,
        w2,
        (-3 * g * np.sin(t1) - g * np.sin(t1 - 2 * t2) - 2 * np.sin(t1 - t2) * (c2 * w2**2 + c1 * w1**2 * np.cos(t1 - t2))) / (c1 * (3 - np.cos(2 * t1 - 2 * t2))),
        (2 * np.sin(t1 - t2) * (2 * c1 * w1**2 + 2 * g * np.cos(t1) + c2 * w2**2 * np.cos(t1 - t2))) / (c2 * (3 - np.cos(2 * t1 - 2 * t2)))
    ])

# Initial conditions
t1 = np.zeros(10001)
t2 = np.zeros(10001)
w1 = np.zeros(10001)
w2 = np.zeros(10001)

t1[0] = -np.pi/3
t2[0] = -5*np.pi/6
w1[0] = 0.00
w2[0] = 0

h = 0.001
t = np.arange(0, 10, h)

# Initialize arrays
mx1 = np.zeros(len(t))
my1 = np.zeros(len(t))
mx2 = np.zeros(len(t))
my2 = np.zeros(len(t))
E = np.zeros(len(t))

# Runge-Kutta loop
for i in range(len(t)-1):
    # Update variables
    k1 = f1(t1[i], t2[i], w1[i], w2[i])
    k2 = f1(t1[i] + k1[0] * h/2, t2[i] + k1[1] * h/2, w1[i] + k1[2] * h/2, w2[i] + k1[3] * h/2)
    k3 = f1(t1[i] + k2[0] * h/2, t2[i] + k2[1] * h/2, w1[i] + k2[2] * h/2, w2[i] + k2[3] * h/2)
    k4 = f1(t1[i] + k3[0] * h, t2[i] + k3[1] * h, w1[i] + k3[2] * h, w2[i] + k3[3] * h)

    # Update variables
    t1[i+1] = t1[i] + h/6 * (k1[0] + 2*k2[0] + 2*k3[0] + k4[0])
    t2[i+1] = t2[i] + h/6 * (k1[1] + 2*k2[1] + 2*k3[1] + k4[1])
    w1[i+1] = w1[i] + h/6 * (k1[2] + 2*k2[2] + 2*k3[2] + k4[2])
    w2[i+1] = w2[i] + h/6 * (k1[3] + 2*k2[3] + 2*k3[3] + k4[3])

    # Calculate positions and energy
    mx1[i] = c1 * np.sin(t1[i]) + c2 * np.sin(t2[i])
    my1[i] = -c1 * np.cos(t1[i]) - c2 * np.cos(t2[i])
    mx2[i] = c1 * np.sin(t1[i]) + c2 * np.sin(t2[i])
    my2[i] = -c1 * np.cos(t1[i]) - c2 * np.cos(t2[i])
    E[i] = 0.5 * m * (2 * c1**2 * w1[i]**2 + c2**2 * w2[i]**2 + 2 * c1 * c2 * w1[i] * w2[i] * np.cos(t1[i] - t2[i])) - m * g * (2 * c1 * np.cos(t1[i]) + c2 * np.cos(t2[i]))

# Plotting
fig, axs = plt.subplots(2, 2)

axs[0, 0].plot(t, mx1)
axs[0, 0].set_title('X-Position 1')
axs[0, 0].set_xlabel('Time')
axs[0, 0].set_ylabel('Position')

axs[0, 1].plot(t, my1)
axs[0, 1].set_title('Y-Position 1')
axs[0, 1].set_xlabel('Time')
axs[0, 1].set_ylabel('Position')

axs[1, 0].plot(t, mx2)
axs[1, 0].set_title('X-Position 2')
axs[1, 0].set_xlabel('Time')
axs[1, 0].set_ylabel('Position')

axs[1, 1].plot(t, my2)
axs[1, 1].set_title('Y-Position 2')
axs[1, 1].set_xlabel('Time')
axs[1, 1].set_ylabel('Position')

plt.tight_layout()
plt.show()

plt.plot(t, E)
plt.title('Energy')
plt.xlabel('Time')
plt.ylabel('Energy')
plt.show()
