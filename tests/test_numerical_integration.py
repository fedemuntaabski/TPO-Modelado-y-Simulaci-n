"""
Unit tests for core/numerical_integration.py
"""

import pytest
import numpy as np
from core.numerical_integration import NumericalIntegration


class TestNumericalIntegration:
    """Test cases for NumericalIntegration class"""

    def test_trapezoid_simple_function(self):
        """Test trapezoid rule with f(x) = x^2 from 0 to 1"""
        def f(x):
            return x**2

        a, b = 0, 1
        result = NumericalIntegration.trapezoid(f, a, b, n=100)

        # Analytical result: ∫x^2 dx from 0 to 1 = 1/3 ≈ 0.3333
        expected = 1/3
        assert abs(result - expected) < 0.01  # Should be reasonably accurate

    def test_simpson_13_simple_function(self):
        """Test Simpson 1/3 rule with f(x) = x^2 from 0 to 1"""
        def f(x):
            return x**2

        a, b = 0, 1
        result = NumericalIntegration.simpson_13(f, a, b, n=100)

        # Analytical result: ∫x^2 dx from 0 to 1 = 1/3 ≈ 0.3333
        expected = 1/3
        assert abs(result - expected) < 0.001  # Simpson should be more accurate

    def test_simpson_38_simple_function(self):
        """Test Simpson 3/8 rule with f(x) = x^2 from 0 to 1"""
        def f(x):
            return x**2

        a, b = 0, 1
        result = NumericalIntegration.simpson_38(f, a, b, n=99)  # Will be adjusted to multiple of 3

        # Analytical result: ∫x^2 dx from 0 to 1 = 1/3 ≈ 0.3333
        expected = 1/3
        assert abs(result - expected) < 0.01

    def test_gauss_quadrature_simple_function(self):
        """Test Gauss quadrature with f(x) = x^2 from 0 to 1"""
        def f(x):
            return x**2

        a, b = 0, 1
        result = NumericalIntegration.gauss_quadrature(f, a, b, n=5)

        # Analytical result: ∫x^2 dx from 0 to 1 = 1/3 ≈ 0.3333
        expected = 1/3
        assert abs(result - expected) < 1e-10  # Gauss quadrature should be very accurate

    def test_adaptive_simpson_simple_function(self):
        """Test adaptive Simpson with f(x) = x^2 from 0 to 1"""
        def f(x):
            return x**2

        a, b = 0, 1
        result = NumericalIntegration.adaptive_simpson(f, a, b)

        # Analytical result: ∫x^2 dx from 0 to 1 = 1/3 ≈ 0.3333
        expected = 1/3
        assert abs(result - expected) < 1e-6  # Adaptive should be very accurate
