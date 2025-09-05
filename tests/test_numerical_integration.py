"""
Unit tests for core/numerical_integration.py
"""

import pytest
import numpy as np
from core.numerical_integration import NumericalIntegration


class TestNumericalIntegration:
    """Test cases for NumericalIntegration class"""

    def test_rectangle_rule_simple_function(self):
        """Test rectangle rule with f(x) = x^2 from 0 to 1"""
        def f(x):
            return x**2

        a, b = 0, 1
        result = NumericalIntegration.rectangle_rule(f, a, b, n=100)

        # Analytical result: ∫x^2 dx from 0 to 1 = 1/3 ≈ 0.3333
        expected = 1/3
        assert abs(result - expected) < 0.1  # Rectangle rule is less accurate

    def test_midpoint_rule_simple_function(self):
        """Test midpoint rule with f(x) = x^2 from 0 to 1"""
        def f(x):
            return x**2

        a, b = 0, 1
        result = NumericalIntegration.midpoint_rule(f, a, b, n=100)

        # Analytical result: ∫x^2 dx from 0 to 1 = 1/3 ≈ 0.3333
        expected = 1/3
        assert abs(result - expected) < 0.01  # Midpoint rule should be more accurate

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

    def test_adaptive_simpson_simple_function(self):
        """Test adaptive Simpson with f(x) = x^2 from 0 to 1"""
        def f(x):
            return x**2

        a, b = 0, 1
        result = NumericalIntegration.adaptive_simpson(f, a, b)

        # Analytical result: ∫x^2 dx from 0 to 1 = 1/3 ≈ 0.3333
        expected = 1/3
        assert abs(result - expected) < 1e-6  # Adaptive should be very accurate

    def test_newton_cotes_integration_rectangle(self):
        """Test newton_cotes_integration with rectangle method"""
        def f(x):
            return x**2

        a, b = 0, 1
        result = NumericalIntegration.newton_cotes_integration(f, a, b, n=100, method="rectangle")

        expected = 1/3
        assert abs(result - expected) < 0.1

    def test_newton_cotes_integration_simpson_13(self):
        """Test newton_cotes_integration with Simpson 1/3 method"""
        def f(x):
            return x**2

        a, b = 0, 1
        result = NumericalIntegration.newton_cotes_integration(f, a, b, n=100, method="simpson_13")

        expected = 1/3
        assert abs(result - expected) < 0.001

    def test_newton_cotes_integration_invalid_method(self):
        """Test newton_cotes_integration with invalid method"""
        def f(x):
            return x**2

        a, b = 0, 1
        with pytest.raises(ValueError):
            NumericalIntegration.newton_cotes_integration(f, a, b, n=100, method="invalid")
