import numpy as np


class DoublePendulum:
    def __init__(self, l1=1.0, l2=0.5, m1=1.0, m2=1.0, g=9.81):
        # Link lengths (using c1, c2 naming like original)
        self.l1 = l1  # c1 in original
        self.l2 = l2  # c2 in original
        # Masses
        self.m1 = m1
        self.m2 = m2
        # Gravity acceleration (using g=9.8 like original)
        self.g = 9.8

    def derivatives(self, state):
        """
        Compute [dθ1, dθ2, dω1, dω2] for state [θ1, θ2, ω1, ω2].

        Uses the EXACT equations from the original simulation.py that were working.
        These are the equations for a double pendulum derived in the PDF.
        """
        theta1, theta2, omega1, omega2 = state

        # Use the EXACT same equations as the original working simulation
        # These are from the f1 function in simulation.py

        # CRITICAL FIX: The denominator should be (3 - cos(2*t1 - 2*t2)), not (3 - cos(2*(t1-t2)))
        denom_term = 3 - np.cos(2 * theta1 - 2 * theta2)

        # Angular accelerations using the original equations
        alpha1 = (
            -3 * self.g * np.sin(theta1)
            - self.g * np.sin(theta1 - 2 * theta2)
            - 2
            * np.sin(theta1 - theta2)
            * (self.l2 * omega2**2 + self.l1 * omega1**2 * np.cos(theta1 - theta2))
        ) / (self.l1 * denom_term)

        alpha2 = (
            2
            * np.sin(theta1 - theta2)
            * (
                2 * self.l1 * omega1**2
                + 2 * self.g * np.cos(theta1)
                + self.l2 * omega2**2 * np.cos(theta1 - theta2)
            )
        ) / (self.l2 * denom_term)

        # Add numerical stability to prevent division by zero
        eps = 1e-10
        if abs(denom_term) < eps:
            denom_term = eps if denom_term >= 0 else -eps

        # Recalculate with safe denominator
        alpha1 = (
            -3 * self.g * np.sin(theta1)
            - self.g * np.sin(theta1 - 2 * theta2)
            - 2
            * np.sin(theta1 - theta2)
            * (self.l2 * omega2**2 + self.l1 * omega1**2 * np.cos(theta1 - theta2))
        ) / (self.l1 * denom_term)

        alpha2 = (
            2
            * np.sin(theta1 - theta2)
            * (
                2 * self.l1 * omega1**2
                + 2 * self.g * np.cos(theta1)
                + self.l2 * omega2**2 * np.cos(theta1 - theta2)
            )
        ) / (self.l2 * denom_term)

        # Clamp to prevent numerical explosion
        max_accel = 1000.0
        alpha1 = np.clip(alpha1, -max_accel, max_accel)
        alpha2 = np.clip(alpha2, -max_accel, max_accel)

        # Return derivatives: dθ1=ω1, dθ2=ω2, dω1=α1, dω2=α2
        return np.array([omega1, omega2, alpha1, alpha2])

    def rk4_step(self, state, dt):
        """
        Advance state by dt using RK4 integration with adaptive step size for stability.
        """
        # Adaptive step size to prevent numerical instability
        max_dt = 0.01  # Maximum time step
        if dt > max_dt:
            # Split large time steps into smaller ones
            n_steps = int(np.ceil(dt / max_dt))
            small_dt = dt / n_steps
            current_state = state.copy()

            for _ in range(n_steps):
                current_state = self._single_rk4_step(current_state, small_dt)

            return current_state
        else:
            return self._single_rk4_step(state, dt)

    def _single_rk4_step(self, state, dt):
        """Single RK4 step with given time step."""
        k1 = self.derivatives(state)
        k2 = self.derivatives(state + 0.5 * dt * k1)
        k3 = self.derivatives(state + 0.5 * dt * k2)
        k4 = self.derivatives(state + dt * k3)

        new_state = state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

        # Ensure angular velocities don't become too large
        max_omega = 50.0  # rad/s
        new_state[2] = np.clip(new_state[2], -max_omega, max_omega)  # omega1
        new_state[3] = np.clip(new_state[3], -max_omega, max_omega)  # omega2

        return new_state

    def tip_positions(self, state):
        """
        Convert angles [θ1, θ2] to cartesian coords (x1,y1), (x2,y2).
        
        Uses screen-friendly coordinates where positive y goes UP.
        θ=0 corresponds to hanging straight down.
        This makes the physics visually intuitive - pendulum falls from unstable positions.
        """
        theta1, theta2 = state[0], state[1]
        
        # First pendulum bob position (from pivot)
        x1 = self.l1 * np.sin(theta1)
        y1 = self.l1 * np.cos(theta1)  # Positive y goes UP now
        
        # Second pendulum bob position (tip of the double pendulum)
        x2 = self.l1 * np.sin(theta1) + self.l2 * np.sin(theta2)
        y2 = self.l1 * np.cos(theta1) + self.l2 * np.cos(theta2)  # Positive y goes UP now
        
        return (x1, y1), (x2, y2)

    def total_energy(self, state):
        """
        Calculate the total energy of the system.
        Updated for the flipped coordinate system where positive y goes up.
        """
        theta1, theta2, omega1, omega2 = state
        
        # Kinetic energy (same as before)
        kinetic = (
            0.5
            * self.m1
            * (
                2 * self.l1**2 * omega1**2
                + self.l2**2 * omega2**2
                + 2 * self.l1 * self.l2 * omega1 * omega2 * np.cos(theta1 - theta2)
            )
        )
        
        # Potential energy (flipped sign due to y-coordinate flip)
        # Now higher y means higher potential energy
        potential = (
            self.m1
            * self.g
            * (2 * self.l1 * np.cos(theta1) + self.l2 * np.cos(theta2))
        )
        
        return kinetic + potential
