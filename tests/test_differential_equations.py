"""
Unit tests for core/differential_equations.py
"""

import pytest
import numpy as np
from core.differential_equations import DifferentialEquations


class TestDifferentialEquations:
    """Test cases for DifferentialEquations class"""

    def test_euler_simple_ode(self):
        """Test Euler method with simple ODE: dy/dt = -y, y(0) = 1"""
        def f(t, y):
            return -y

        t_span = (0, 1)
        y0 = 1.0
        n_points = 11

        t, y = DifferentialEquations.euler(f, t_span, y0, n_points)

        # Analytical solution: y = exp(-t)
        y_exact = np.exp(-t)

        # Check initial condition
        assert abs(y[0] - 1.0) < 1e-10

        # Check final value (should be close to exp(-1))
        assert abs(y[-1] - np.exp(-1)) < 0.1  # Euler is not very accurate

    def test_rk4_simple_ode(self):
        """Test RK4 method with simple ODE: dy/dt = -y, y(0) = 1"""
        def f(t, y):
            return -y

        t_span = (0, 1)
        y0 = 1.0
        n_points = 11

        t, y = DifferentialEquations.rk4(f, t_span, y0, n_points)

        # Analytical solution: y = exp(-t)
        y_exact = np.exp(-t)

        # Check initial condition
        assert abs(y[0] - 1.0) < 1e-10

        # Check final value (RK4 should be more accurate than Euler)
        assert abs(y[-1] - np.exp(-1)) < 0.01

    def test_rk2_simple_ode(self):
        """Test RK2 method with simple ODE: dy/dt = -y, y(0) = 1"""
        def f(t, y):
            return -y

        t_span = (0, 1)
        y0 = 1.0
        n_points = 11

        t, y = DifferentialEquations.rk2(f, t_span, y0, n_points)

        # Check initial condition
        assert abs(y[0] - 1.0) < 1e-10

        # Check that solution decreases
        assert y[-1] < y[0]

    def test_rk45_simple_ode(self):
        """Test RK45 method with simple ODE: dy/dt = -y, y(0) = 1"""
        def f(t, y):
            return -y

        t_span = (0, 1)
        y0 = 1.0

        t, y = DifferentialEquations.rk45(f, t_span, y0)

        # Check initial condition
        assert abs(y[0] - 1.0) < 1e-10

        # Check final value (RK45 should be very accurate)
        assert abs(y[-1] - np.exp(-1)) < 1e-6
