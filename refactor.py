import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple


# Define constants and initial conditions
def initialize() -> Tuple[
    float,
    float,
    float,
    float,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    float,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
]:
    """
    Initializes constants, initial conditions, and arrays for the simulation.

    Returns:
        Tuple containing constants, initial conditions, and arrays.
    """
    c1 = 1.0
    c2 = 0.5
    m = 1
    g = 9.8


# Define the differential equation function
def f1(
    t1: float, t2: float, w1: float, w2: float, c1: float, c2: float, g: float
) -> np.ndarray:
    """
    Calculates the derivatives for the differential equations.

    Args:
        t1: Angle of the first pendulum.
        t2: Angle of the second pendulum.
        w1: Angular velocity of the first pendulum.
        w2: Angular velocity of the second pendulum.
        c1: Length of the first pendulum.
        c2: Length of the second pendulum.
        g: Acceleration due to gravity.

    Returns:
        Array of derivatives.
    """
    return np.array(
        [
            w1,
            w2,
            (
                -3 * g * np.sin(t1)
                - g * np.sin(t1 - 2 * t2)
                - 2 * np.sin(t1 - t2) * (c2 * w2**2 + c1 * w1**2 * np.cos(t1 - t2))
            )
            / (c1 * (3 - np.cos(2 * t1 - 2 * t2))),
            (
                2
                * np.sin(t1 - t2)
                * (2 * c1 * w1**2 + 2 * g * np.cos(t1) + c2 * w2**2 * np.cos(t1 - t2))
            )
            / (c2 * (3 - np.cos(2 * t1 - 2 * t2))),
        ]
    )


# Runge-Kutta integration
def runge_kutta(
    c1: float,
    c2: float,
    g: float,
    t1: np.ndarray,
    t2: np.ndarray,
    w1: np.ndarray,
    w2: np.ndarray,
    h: float,
    t: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Performs Runge-Kutta integration to solve the differential equations.

    Args:
        c1: Length of the first pendulum relative to verticle.
        c2: Length of the second pendulum relative to verticle.
        g: Acceleration due to gravity.
        t1: Array of angles for the first pendulum.
        t2: Array of angles for the second pendulum.
        w1: Array of angular velocities for the first pendulum.
        w2: Array of angular velocities for the second pendulum.
        h: Time step.
        t: Array of time points.

    Returns:
        Updated arrays for angles and angular velocities.
    """
    for i in range(len(t) - 1):
        # Update variables
        k1 = f1(t1[i], t2[i], w1[i], w2[i])
        k2 = f1(
            t1[i] + k1[0] * h / 2,
            t2[i] + k1[1] * h / 2,
            w1[i] + k1[2] * h / 2,
            w2[i] + k1[3] * h / 2,
        )
        k3 = f1(
            t1[i] + k2[0] * h / 2,
            t2[i] + k2[1] * h / 2,
            w1[i] + k2[2] * h / 2,
            w2[i] + k2[3] * h / 2,
        )
        k4 = f1(
            t1[i] + k3[0] * h, t2[i] + k3[1] * h, w1[i] + k3[2] * h, w2[i] + k3[3] * h
        )

        # Update variables
        t1[i + 1] = t1[i] + h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        t2[i + 1] = t2[i] + h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        w1[i + 1] = w1[i] + h / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])
        w2[i + 1] = w2[i] + h / 6 * (k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3])
    return t1, t2, w1, w2


# Calculate positions and energy
def calculate_positions_energy(
    c1: float,
    c2: float,
    m: float,
    g: float,
    t1: np.ndarray,
    t2: np.ndarray,
    w1: np.ndarray,
    w2: np.ndarray,
    mx1: np.ndarray,
    my1: np.ndarray,
    mx2: np.ndarray,
    my2: np.ndarray,
    E: np.ndarray,
    t: np.ndarray,
) -> None:
    """
    Calculates the positions and energy of the system.

    Args:
        c1: Length of the first pendulum.
        c2: Length of the second pendulum.
        m: Mass of the pendulums.
        g: Acceleration due to gravity.
        t1: Array of angles for the first pendulum.
        t2: Array of angles for the second pendulum.
        w1: Array of angular velocities for the first pendulum.
        w2: Array of angular velocities for the second pendulum.
        mx1: Array of x-positions for the first pendulum.
        my1: Array of y-positions for the first pendulum.
        mx2: Array of x-positions for the second pendulum.
        my2: Array of y-positions for the second pendulum.
        E: Array of energy values.
        t: Array of time points.
    """
    for i in range(len(t) - 1):
        mx1[i] = c1 * np.sin(t1[i]) + c2 * np.sin(t2[i])
        my1[i] = -c1 * np.cos(t1[i]) - c2 * np.cos(t2[i])
        mx2[i] = c1 * np.sin(t1[i]) + c2 * np.sin(t2[i])
        my2[i] = -c1 * np.cos(t1[i]) - c2 * np.cos(t2[i])
        E[i] = 0.5 * m * (
            2 * c1**2 * w1[i] ** 2
            + c2**2 * w2[i] ** 2
            + 2 * c1 * c2 * w1[i] * w2[i] * np.cos(t1[i] - t2[i])
        ) - m * g * (2 * c1 * np.cos(t1[i]) + c2 * np.cos(t2[i]))

    return mx1, my1, mx2, my2


# Plot results
def plot_results(
    t: np.ndarray,
    mx1: np.ndarray,
    my1: np.ndarray,
    mx2: np.ndarray,
    my2: np.ndarray,
    E: np.ndarray,
) -> None:
    """
    Plots the simulation results.

    Args:
        t: Array of time points.
        mx1: Array of x-positions for the first pendulum.
        my1: Array of y-positions for the first pendulum.
        mx2: Array of x-positions for the second pendulum.
        my2: Array of y-positions for the second pendulum.
        E: Array of energy values.
    """
    # Plotting
    fig, axs = plt.subplots(2, 2)

    axs[0, 0].plot(t, mx1)
    axs[0, 0].set_title("X-Position 1")
    axs[0, 0].set_xlabel("Time")
    axs[0, 0].set_ylabel("Position")

    axs[0, 1].plot(t, my1)
    axs[0, 1].set_title("Y-Position 1")
    axs[0, 1].set_xlabel("Time")
    axs[0, 1].set_ylabel("Position")

    axs[1, 0].plot(t, mx2)
    axs[1, 0].set_title("X-Position 2")
    axs[1, 0].set_xlabel("Time")
    axs[1, 0].set_ylabel("Position")

    axs[1, 1].plot(t, my2)
    axs[1, 1].set_title("Y-Position 2")
    axs[1, 1].set_xlabel("Time")
    axs[1, 1].set_ylabel("Position")

    plt.tight_layout()
    plt.show()

    plt.plot(t, E)
    plt.title("Energy")
    plt.xlabel("Time")
    plt.ylabel("Energy")
    plt.show()


# Main function
def main() -> None:
    """
    Main function to run the simulation.
    """
    pass


if __name__ == "__main__":
    main()
