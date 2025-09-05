"""
Unit tests for core/finite_differences.py
"""

import pytest
import numpy as np
from core.finite_differences import FiniteDifferences


class TestFiniteDifferences:
    """Test cases for FiniteDifferences class"""

    def test_forward_difference(self):
        """Test forward difference for f(x) = x^2"""
        def f(x):
            return x**2

        x = 2.0
        h = 1e-8
        result = FiniteDifferences.forward_difference(f, x, h)

        # Analytical derivative: f'(x) = 2x, so f'(2) = 4
        expected = 4.0
        assert abs(result - expected) < 1e-6

    def test_backward_difference(self):
        """Test backward difference for f(x) = x^2"""
        def f(x):
            return x**2

        x = 2.0
        h = 1e-8
        result = FiniteDifferences.backward_difference(f, x, h)

        # Analytical derivative: f'(x) = 2x, so f'(2) = 4
        expected = 4.0
        assert abs(result - expected) < 1e-6

    def test_central_difference(self):
        """Test central difference for f(x) = x^2"""
        def f(x):
            return x**2

        x = 2.0
        h = 1e-8
        result = FiniteDifferences.central_difference(f, x, h)

        # Analytical derivative: f'(x) = 2x, so f'(2) = 4
        expected = 4.0
        assert abs(result - expected) < 1e-6  # Central should be more accurate

    def test_second_derivative_central(self):
        """Test second derivative using central difference for f(x) = x^2"""
        def f(x):
            return x**2

        x = 2.0
        h = 1e-6
        result = FiniteDifferences.second_derivative_central(f, x, h)

        # Analytical second derivative: f''(x) = 2
        expected = 2.0
        assert abs(result - expected) < 1e-2
