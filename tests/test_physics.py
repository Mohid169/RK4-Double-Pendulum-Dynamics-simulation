#!/usr/bin/env python3
"""
Basic tests for the double pendulum physics engine.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import unittest
from pendulum_art.physics import DoublePendulum


class TestDoublePendulum(unittest.TestCase):
    
    def setUp(self):
        """Set up test pendulum"""
        self.pendulum = DoublePendulum(l1=1.0, l2=0.5, m1=1.0, m2=1.0, g=9.81)
    
    def test_initialization(self):
        """Test pendulum initialization"""
        self.assertEqual(self.pendulum.l1, 1.0)
        self.assertEqual(self.pendulum.l2, 0.5)
        self.assertEqual(self.pendulum.m1, 1.0)
        self.assertEqual(self.pendulum.m2, 1.0)
        self.assertEqual(self.pendulum.g, 9.81)
    
    def test_derivatives_shape(self):
        """Test that derivatives return correct shape"""
        state = np.array([0.0, 0.0, 0.0, 0.0])
        derivatives = self.pendulum.derivatives(state)
        self.assertEqual(derivatives.shape, (4,))
    
    def test_derivatives_equilibrium(self):
        """Test derivatives at equilibrium (hanging down)"""
        # At equilibrium: theta1=0, theta2=0, omega1=0, omega2=0
        state = np.array([0.0, 0.0, 0.0, 0.0])
        derivatives = self.pendulum.derivatives(state)
        
        # At equilibrium, angular velocities should be zero
        self.assertAlmostEqual(derivatives[0], 0.0, places=10)  # dtheta1/dt = omega1
        self.assertAlmostEqual(derivatives[1], 0.0, places=10)  # dtheta2/dt = omega2
        
        # Angular accelerations should also be zero at equilibrium
        self.assertAlmostEqual(derivatives[2], 0.0, places=6)   # domega1/dt
        self.assertAlmostEqual(derivatives[3], 0.0, places=6)   # domega2/dt
    
    def test_rk4_step_stability(self):
        """Test that RK4 step doesn't explode with reasonable inputs"""
        state = np.array([np.pi/4, np.pi/6, 0.0, 0.0])
        dt = 0.01
        
        new_state = self.pendulum.rk4_step(state, dt)
        
        # Check that the new state is reasonable (no NaN or inf)
        self.assertTrue(np.all(np.isfinite(new_state)))
        
        # Check that angles haven't changed drastically in one small step
        angle_change = np.abs(new_state[:2] - state[:2])
        self.assertTrue(np.all(angle_change < 0.1))  # Less than 0.1 radians change
    
    def test_tip_positions(self):
        """Test tip position calculations"""
        # Test case: both pendulums hanging straight down
        state = np.array([0.0, 0.0, 0.0, 0.0])
        (x1, y1), (x2, y2) = self.pendulum.tip_positions(state)
        
        # First pendulum should be at (0, -l1)
        self.assertAlmostEqual(x1, 0.0, places=10)
        self.assertAlmostEqual(y1, -self.pendulum.l1, places=10)
        
        # Second pendulum should be at (0, -l1-l2)
        self.assertAlmostEqual(x2, 0.0, places=10)
        self.assertAlmostEqual(y2, -self.pendulum.l1 - self.pendulum.l2, places=10)
    
    def test_tip_positions_right_angle(self):
        """Test tip positions when first pendulum is horizontal"""
        # First pendulum horizontal (90 degrees), second hanging down
        state = np.array([np.pi/2, np.pi/2, 0.0, 0.0])
        (x1, y1), (x2, y2) = self.pendulum.tip_positions(state)
        
        # First pendulum should be at (l1, 0)
        self.assertAlmostEqual(x1, self.pendulum.l1, places=10)
        self.assertAlmostEqual(y1, 0.0, places=10)
        
        # Second pendulum should be at (l1+l2, 0)
        self.assertAlmostEqual(x2, self.pendulum.l1 + self.pendulum.l2, places=10)
        self.assertAlmostEqual(y2, 0.0, places=10)
    
    def test_energy_conservation_approximation(self):
        """Test that energy is approximately conserved over short periods"""
        state = np.array([np.pi/4, np.pi/6, 0.1, 0.05])
        dt = 0.001
        
        def calculate_energy(s):
            """Calculate total energy"""
            theta1, theta2, omega1, omega2 = s
            
            # Kinetic energy (simplified for equal masses)
            ke = 0.5 * (self.pendulum.l1**2 * omega1**2 + 
                       self.pendulum.l2**2 * omega2**2 + 
                       2 * self.pendulum.l1 * self.pendulum.l2 * omega1 * omega2 * np.cos(theta1 - theta2))
            
            # Potential energy
            pe = -self.pendulum.g * (self.pendulum.l1 * np.cos(theta1) + self.pendulum.l2 * np.cos(theta2))
            
            return ke + pe
        
        initial_energy = calculate_energy(state)
        
        # Simulate for a short time
        for _ in range(100):
            state = self.pendulum.rk4_step(state, dt)
        
        final_energy = calculate_energy(state)
        energy_change = abs(final_energy - initial_energy)
        energy_relative_change = energy_change / abs(initial_energy)
        
        # Energy should be conserved to within 1% over this short simulation
        self.assertLess(energy_relative_change, 0.01)


class TestPendulumUtilities(unittest.TestCase):
    
    def test_angle_wrapping(self):
        """Test that angles wrap correctly around the circle"""
        # This test would be useful if we implemented angle wrapping
        # For now, just test that large angles don't break the simulation
        pendulum = DoublePendulum()
        
        # Large initial angles
        state = np.array([10*np.pi, -5*np.pi, 0.0, 0.0])
        derivatives = pendulum.derivatives(state)
        
        # Should still produce finite derivatives
        self.assertTrue(np.all(np.isfinite(derivatives)))


def run_tests():
    """Run all tests"""
    unittest.main(verbosity=2)


if __name__ == "__main__":
    run_tests() 