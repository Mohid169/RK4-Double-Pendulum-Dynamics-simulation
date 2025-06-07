import numpy as np

class DoublePendulum:
    def __init__(self, l1=1.0, l2=0.5, m1=1.0, m2=1.0, g=9.81):
        # Link lengths
        self.l1 = l1
        self.l2 = l2
        # Masses (currently unused in simplified EOM)
        self.m1 = m1
        self.m2 = m2
        # Gravity acceleration
        self.g = g

    def derivatives(self, state):
        """
        Compute [dθ1, dθ2, dω1, dω2] for state [θ1, θ2, ω1, ω2].
        """
        theta1, theta2, omega1, omega2 = state
        
        # Trigonometric shorthands
        sin_t1 = np.sin(theta1)
        sin_t2 = np.sin(theta2)
        sin_diff = np.sin(theta1 - theta2)
        cos_diff = np.cos(theta1 - theta2)

        # Denominator (for equal masses simplification)
        denom = self.l1 * (3 - np.cos(2 * (theta1 - theta2)))

        # Angular accelerations (α1, α2)
        alpha1 = (
            -3 * self.g * sin_t1
            - self.g * np.sin(theta1 - 2 * theta2)
            - 2 * sin_diff * (self.l2 * omega2**2 + self.l1 * omega1**2 * cos_diff)
        ) / denom

        alpha2 = (
            2 * sin_diff * (
                2 * self.l1 * omega1**2
                + 2 * self.g * np.cos(theta1)
                + self.l2 * omega2**2 * cos_diff
            )
        ) / (self.l2 * (3 - np.cos(2 * (theta1 - theta2))))

        # Return derivatives: dθ1=ω1, dθ2=ω2, dω1=α1, dω2=α2
        return np.array([omega1, omega2, alpha1, alpha2])

    def rk4_step(self, state, dt):
        """
        Advance state by dt using RK4 integration.
        """
        k1 = self.derivatives(state)
        k2 = self.derivatives(state + 0.5 * dt * k1)
        k3 = self.derivatives(state + 0.5 * dt * k2)
        k4 = self.derivatives(state + dt * k3)
        return state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

    def tip_positions(self, state):
        """
        Convert angles [θ1, θ2] to cartesian coords (x1,y1), (x2,y2).
        Pivot at (0,0), y positive up.
        """
        theta1, theta2 = state[0], state[1]
        x1 = self.l1 * np.sin(theta1)
        y1 = -self.l1 * np.cos(theta1)
        x2 = x1 + self.l2 * np.sin(theta2)
        y2 = y1 - self.l2 * np.cos(theta2)
        return (x1, y1), (x2, y2)
