#!/usr/bin/env python3
"""
Test script for ODE integration
"""

from src.core.function_parser import create_function_evaluator_2d
from src.core.ode_runge_kutta import RungeKuttaSolver
import numpy as np

def test_ode_integration():
    print("Testing ODE integration...")

    # Create scalar function
    f_scalar = create_function_evaluator_2d('y - t**2 + 1')

    # Create array wrapper
    def f_array(t, y):
        return np.array([f_scalar(t, y[0])])

    # Test solver
    solver = RungeKuttaSolver(method='rk4', step=0.1)
    result = solver.solve(f_array, 0, 2, [0.5], step=0.1)

    print(f"Test successful: {len(result.t)} points")
    print(f"Final value: {result.y[-1]}")
    print(f"Method: {result.method}")
    print(f"Steps taken: {result.steps_taken}")

if __name__ == "__main__":
    test_ode_integration()
