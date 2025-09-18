"""
Newton-Raphson method implementation for finding roots of equations.
"""
import numpy as np
from typing import Callable, List, Tuple, Dict, Any


class NewtonRaphson:
    """
    Implementation of Newton-Raphson method for finding roots of equations.
    """
    
    def __init__(self, function: Callable, derivative: Callable, 
                 tolerance: float = 1e-6, max_iterations: int = 100):
        """
        Initialize the Newton-Raphson solver.
        
        Args:
            function: The function f(x) for which we want to find the root
            derivative: The derivative f'(x) of the function
            tolerance: The error tolerance for convergence
            max_iterations: Maximum number of iterations
        """
        self.function = function
        self.derivative = derivative
        self.tolerance = tolerance
        self.max_iterations = max_iterations
        self.iterations = []
        
    def solve(self, x0: float) -> Tuple[float, List[Dict[str, Any]], bool]:
        """
        Apply Newton-Raphson method to find the root starting from x0.
        
        Args:
            x0: Initial guess
            
        Returns:
            Tuple containing:
                - The approximated root
                - List of iteration data
                - Boolean indicating whether the method converged
        """
        self.iterations = []
        x_current = x0
        
        for i in range(self.max_iterations):
            fx = self.function(x_current)
            dfx = self.derivative(x_current)
            
            # Check if derivative is too close to zero to avoid division by zero
            if abs(dfx) < 1e-10:
                return x_current, self.iterations, False
            
            # Calculate next approximation
            x_next = x_current - fx / dfx
            
            # Calculate absolute error (non-percentage)
            error = abs(x_next - x_current)
            
            # Store iteration data
            iteration_data = {
                'iteration': i + 1,
                'x_current': x_current,
                'fx': fx,
                'dfx': dfx,
                'x_next': x_next,
                'error': error
            }
            self.iterations.append(iteration_data)
            
            # Check for convergence
            if error < self.tolerance:
                return x_next, self.iterations, True
            
            # Update current value
            x_current = x_next
        
        # If we reached max iterations without converging
        return x_current, self.iterations, False
    
    def get_iterations_data(self) -> List[Dict[str, Any]]:
        """
        Get the iteration data.
        
        Returns:
            List of dictionaries containing iteration data
        """
        return self.iterations