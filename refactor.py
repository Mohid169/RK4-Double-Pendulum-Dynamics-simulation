import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rcParams

# Set larger figure size for better visualization
rcParams["figure.figsize"] = (10, 8)


class DoublePendulum:
    def __init__(self, l1=1.0, l2=0.5, m1=1.0, m2=1.0, g=9.8):
        """
        Initialize double pendulum system

        Parameters:
        l1, l2: lengths of the rods
        m1, m2: masses of the pendulums
        g: gravity constant
        """
        self.l1 = l1
        self.l2 = l2
        self.m1 = m1
        self.m2 = m2
        self.g = g

    def derivatives(self, state):
        """Calculate derivatives for the pendulum state variables"""
        theta1, theta2, omega1, omega2 = state

        # Common terms to avoid repetition
        sin_t1 = np.sin(theta1)
        sin_t2 = np.sin(theta2)
        sin_diff = np.sin(theta1 - theta2)
        cos_diff = np.cos(theta1 - theta2)
        denominator = self.l1 * (3 - np.cos(2 * (theta1 - theta2)))

        # Angular accelerations
        alpha1 = (
            -3 * self.g * sin_t1
            - self.g * np.sin(theta1 - 2 * theta2)
            - 2 * sin_diff * (self.l2 * omega2**2 + self.l1 * omega1**2 * cos_diff)
        ) / denominator

        alpha2 = (
            2
            * sin_diff
            * (
                2 * self.l1 * omega1**2
                + 2 * self.g * np.cos(theta1)
                + self.l2 * omega2**2 * cos_diff
            )
        ) / (self.l2 * (3 - np.cos(2 * (theta1 - theta2))))

        return np.array([omega1, omega2, alpha1, alpha2])

    def rk4_step(self, state, dt):
        """
        Perform one Runge-Kutta 4th order step

        Parameters:
        state: current state [theta1, theta2, omega1, omega2]
        dt: time step
        """
        k1 = self.derivatives(state)
        k2 = self.derivatives(state + 0.5 * dt * k1)
        k3 = self.derivatives(state + 0.5 * dt * k2)
        k4 = self.derivatives(state + dt * k3)

        return state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

    def simulate(self, initial_state, t_max=10.0, dt=0.01):
        """Run simulation for t_max seconds with time step dt"""
        n_steps = int(t_max / dt)
        t = np.linspace(0, t_max, n_steps)

        # Initialize arrays
        states = np.zeros((n_steps, 4))
        states[0] = initial_state

        # Positions of the pendulum bobs
        x1 = np.zeros(n_steps)
        y1 = np.zeros(n_steps)
        x2 = np.zeros(n_steps)
        y2 = np.zeros(n_steps)

        # Energy over time
        energy = np.zeros(n_steps)

        # Run simulation
        for i in range(n_steps - 1):
            states[i + 1] = self.rk4_step(states[i], dt)

            # Calculate positions
            theta1, theta2 = states[i][:2]
            x1[i] = self.l1 * np.sin(theta1)
            y1[i] = -self.l1 * np.cos(theta1)
            x2[i] = x1[i] + self.l2 * np.sin(theta2)
            y2[i] = y1[i] - self.l2 * np.cos(theta2)

            # Calculate energy
            theta1, theta2, omega1, omega2 = states[i]

            # Kinetic energy
            v1_squared = self.l1**2 * omega1**2
            v2_squared = (
                self.l2**2 * omega2**2
                + self.l1**2 * omega1**2
                + 2 * self.l1 * self.l2 * omega1 * omega2 * np.cos(theta1 - theta2)
            )
            kinetic = 0.5 * self.m1 * v1_squared + 0.5 * self.m2 * v2_squared

            # Potential energy - zero at the pivot
            potential = -self.m1 * self.g * self.l1 * np.cos(
                theta1
            ) - self.m2 * self.g * (self.l1 * np.cos(theta1) + self.l2 * np.cos(theta2))

            energy[i] = kinetic + potential

        # Calculate final positions and energy
        theta1, theta2 = states[-1][:2]
        x1[-1] = self.l1 * np.sin(theta1)
        y1[-1] = -self.l1 * np.cos(theta1)
        x2[-1] = x1[-1] + self.l2 * np.sin(theta2)
        y2[-1] = y1[-1] - self.l2 * np.cos(theta2)

        # Calculate final energy
        theta1, theta2, omega1, omega2 = states[-1]
        v1_squared = self.l1**2 * omega1**2
        v2_squared = (
            self.l2**2 * omega2**2
            + self.l1**2 * omega1**2
            + 2 * self.l1 * self.l2 * omega1 * omega2 * np.cos(theta1 - theta2)
        )
        kinetic = 0.5 * self.m1 * v1_squared + 0.5 * self.m2 * v2_squared
        potential = -self.m1 * self.g * self.l1 * np.cos(theta1) - self.m2 * self.g * (
            self.l1 * np.cos(theta1) + self.l2 * np.cos(theta2)
        )
        energy[-1] = kinetic + potential

        return {
            "time": t,
            "states": states,
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
            "energy": energy,
        }

    def create_animation(self, results, show_trace=True, save_file=None):
        """Create animation of pendulum motion"""
        fig, ax = plt.subplots()
        ax.set_xlim(-2.5, 2.5)
        ax.set_ylim(-2.5, 2.5)
        ax.set_aspect("equal")
        ax.grid()
        ax.set_title("Double Pendulum Animation")

        # Plot components
        (line,) = ax.plot([], [], "o-", lw=2, color="blue")
        (trace,) = ax.plot([], [], "-", lw=1, color="red", alpha=0.5)
        time_text = ax.text(0.02, 0.95, "", transform=ax.transAxes)
        energy_text = ax.text(0.02, 0.90, "", transform=ax.transAxes)

        # Trace history (limited to last 100 positions)
        trace_length = 100
        trace_x = np.zeros(trace_length)
        trace_y = np.zeros(trace_length)

        def init():
            """Initialize animation"""
            line.set_data([], [])
            trace.set_data([], [])
            time_text.set_text("")
            energy_text.set_text("")
            return line, trace, time_text, energy_text

        def animate(i):
            """Update animation for frame i"""
            # Get pendulum positions
            x0, y0 = 0, 0  # Origin
            x1, y1 = results["x1"][i], results["y1"][i]
            x2, y2 = results["x2"][i], results["y2"][i]

            # Update pendulum line
            line.set_data([x0, x1, x2], [y0, y1, y2])

            # Update trace
            if show_trace:
                trace_x[:-1] = trace_x[1:]
                trace_y[:-1] = trace_y[1:]
                trace_x[-1] = x2
                trace_y[-1] = y2
                valid_idx = ~np.isnan(trace_x)
                trace.set_data(trace_x[valid_idx], trace_y[valid_idx])

            # Update time and energy text
            time_text.set_text(f'Time: {results["time"][i]:.2f}s')
            energy_text.set_text(f'Energy: {results["energy"][i]:.4f}J')

            return line, trace, time_text, energy_text

        # Create animation
        n_frames = len(results["time"])
        sample_rate = max(
            1, n_frames // 300
        )  # Limit to ~300 frames for smoother playback

        anim = FuncAnimation(
            fig,
            animate,
            frames=range(0, n_frames, sample_rate),
            init_func=init,
            blit=True,
            interval=30,
        )

        if save_file:
            anim.save(save_file, writer="pillow", fps=30)

        plt.close()
        return anim

    def plot_results(self, results):
        """Plot positions and energy from simulation results"""
        fig, axs = plt.subplots(3, 1, figsize=(10, 12))

        # Plot x positions
        axs[0].plot(results["time"], results["x1"], label="Rod 1")
        axs[0].plot(results["time"], results["x2"], label="Rod 2")
        axs[0].set_title("X Positions")
        axs[0].set_xlabel("Time (s)")
        axs[0].set_ylabel("Position (m)")
        axs[0].legend()
        axs[0].grid(True)

        # Plot y positions
        axs[1].plot(results["time"], results["y1"], label="Rod 1")
        axs[1].plot(results["time"], results["y2"], label="Rod 2")
        axs[1].set_title("Y Positions")
        axs[1].set_xlabel("Time (s)")
        axs[1].set_ylabel("Position (m)")
        axs[1].legend()
        axs[1].grid(True)

        # Plot energy
        axs[2].plot(results["time"], results["energy"])
        axs[2].set_title("Total Energy")
        axs[2].set_xlabel("Time (s)")
        axs[2].set_ylabel("Energy (J)")
        axs[2].grid(True)

        plt.tight_layout()
        return fig


# Run a simulation
if __name__ == "__main__":
    # Create pendulum with the parameters from the original code
    pendulum = DoublePendulum(l1=1.0, l2=0.5)

    # Initial conditions (from original: t1[0] = -np.pi/3, t2[0] = -5*np.pi/6)
    initial_state = np.array([-np.pi / 3, -5 * np.pi / 6, 0.0, 0.0])

    # Run simulation
    results = pendulum.simulate(initial_state, t_max=10.0, dt=0.001)

    # Plot trajectories and energy
    pendulum.plot_results(results)
    plt.show()

    # Create and display animation
    animation = pendulum.create_animation(results, show_trace=True)
    try:
        # For Jupyter notebooks
        from IPython.display import HTML

        HTML(animation.to_jshtml())
    except ImportError:
        plt.show()  # Fallback to matplotlib's built-in animation viewer
