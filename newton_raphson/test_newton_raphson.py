"""
Test file for Newton-Raphson method.
"""
import numpy as np
from newton_raphson import NewtonRaphson


def test_quadratic_function():
    """Test Newton-Raphson with a quadratic function."""
    # f(x) = x^2 - 4, root at x = 2
    f = lambda x: x**2 - 4
    df = lambda x: 2*x
    
    # Create solver
    nr = NewtonRaphson(f, df, tolerance=0.001)
    
    # Solve starting from x0 = 3
    root, iterations, converged = nr.solve(3.0)
    
    # Print results
    print("\nTest function: f(x) = x^2 - 4")
    print(f"Root found: {root:.8f}")
    print(f"Converged: {converged}")
    print(f"Number of iterations: {len(iterations)}")
    
    # Print iteration table
    print("\nIteration Table:")
    print(f"{'n':^5} | {'xn':^15} | {'f(xn)':^15} | {'f\'(xn)':^15} | {'xn+1':^15} | {'Error |xn+1-xn|':^15}")
    print("-" * 85)
    
    for data in iterations:
        i = data['iteration']
        x_n = data['x_current']
        fx = data['fx']
        dfx = data['dfx']
        x_next = data['x_next']
        error = data['error']
        
        print(f"{i:^5} | {x_n:^15.8f} | {fx:^15.8f} | {dfx:^15.8f} | {x_next:^15.8f} | {error:^15.8f}")


def test_trigonometric_function():
    """Test Newton-Raphson with a trigonometric function."""
    # f(x) = sin(x), root at x = 0
    f = lambda x: np.sin(x)
    df = lambda x: np.cos(x)
    
    # Create solver
    nr = NewtonRaphson(f, df, tolerance=0.001)
    
    # Solve starting from x0 = 0.5
    root, iterations, converged = nr.solve(0.5)
    
    # Print results
    print("\nTest function: f(x) = sin(x)")
    print(f"Root found: {root:.8f}")
    print(f"Converged: {converged}")
    print(f"Number of iterations: {len(iterations)}")
    
    # Print iteration table
    print("\nIteration Table:")
    print(f"{'n':^5} | {'xn':^15} | {'f(xn)':^15} | {'f\'(xn)':^15} | {'xn+1':^15} | {'Error |xn+1-xn|':^15}")
    print("-" * 85)
    
    for data in iterations:
        i = data['iteration']
        x_n = data['x_current']
        fx = data['fx']
        dfx = data['dfx']
        x_next = data['x_next']
        error = data['error']
        
        print(f"{i:^5} | {x_n:^15.8f} | {fx:^15.8f} | {dfx:^15.8f} | {x_next:^15.8f} | {error:^15.8f}")


if __name__ == "__main__":
    test_quadratic_function()
    test_trigonometric_function()