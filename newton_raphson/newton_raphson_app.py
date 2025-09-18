"""
UI implementation for Newton-Raphson method.
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
from typing import Callable
import sys
import os

# Add parent directory to path to import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import function parser from src
from src.core.function_parser import parse_function

from newton_raphson.newton_raphson import NewtonRaphson


class NewtonRaphsonApp:
    """
    UI Application for Newton-Raphson method.
    """
    
    def __init__(self, root):
        """
        Initialize the UI application.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Newton-Raphson Method")
        self.root.geometry("900x600")
        
        # Create the main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create the input frame
        self.create_input_frame()
        
        # Create the results frame
        self.create_results_frame()
    
    def create_input_frame(self):
        """Create the input frame with all input fields."""
        input_frame = ttk.LabelFrame(self.main_frame, text="Input Parameters", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        # Function input
        ttk.Label(input_frame, text="Function f(x):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.function_var = tk.StringVar(value="x**2 - 4")
        ttk.Entry(input_frame, textvariable=self.function_var, width=40).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Derivative input
        ttk.Label(input_frame, text="Derivative f'(x):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.derivative_var = tk.StringVar(value="2*x")
        ttk.Entry(input_frame, textvariable=self.derivative_var, width=40).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Initial point input
        ttk.Label(input_frame, text="Initial Point (x₀):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.initial_point_var = tk.StringVar(value="3.0")
        ttk.Entry(input_frame, textvariable=self.initial_point_var, width=40).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Tolerance input
        ttk.Label(input_frame, text="Tolerance (|xₙ₊₁ - xₙ|):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.tolerance_var = tk.StringVar(value="0.001")
        ttk.Entry(input_frame, textvariable=self.tolerance_var, width=40).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Max iterations input
        ttk.Label(input_frame, text="Max Iterations:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.max_iterations_var = tk.StringVar(value="100")
        ttk.Entry(input_frame, textvariable=self.max_iterations_var, width=40).grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Calculate button
        ttk.Button(input_frame, text="Calculate", command=self.calculate).grid(row=5, column=0, columnspan=2, pady=10)
    
    def create_results_frame(self):
        """Create the results frame with the output table."""
        results_frame = ttk.LabelFrame(self.main_frame, text="Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create table for iterations
        columns = ("iteration", "x_n", "f(x_n)", "f'(x_n)", "x_n+1", "error")
        self.tree = ttk.Treeview(results_frame, columns=columns, show="headings")
        
        # Define column headings
        self.tree.heading("iteration", text="Iteration")
        self.tree.heading("x_n", text="xₙ")
        self.tree.heading("f(x_n)", text="f(xₙ)")
        self.tree.heading("f'(x_n)", text="f'(xₙ)")
        self.tree.heading("x_n+1", text="xₙ₊₁")
        self.tree.heading("error", text="Error |xₙ₊₁ - xₙ|")
        
        # Define column widths
        self.tree.column("iteration", width=80)
        self.tree.column("x_n", width=150)
        self.tree.column("f(x_n)", width=150)
        self.tree.column("f'(x_n)", width=150)
        self.tree.column("x_n+1", width=150)
        self.tree.column("error", width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        # Place table and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create a frame for the result message
        self.result_frame = ttk.Frame(self.main_frame, padding="10")
        self.result_frame.pack(fill=tk.X, pady=5)
        
        # Result message
        self.result_var = tk.StringVar()
        ttk.Label(self.result_frame, textvariable=self.result_var, font=("TkDefaultFont", 10, "bold")).pack(anchor=tk.W)
    
    def calculate(self):
        """Perform the Newton-Raphson calculation and display results."""
        try:
            # Clear previous results
            self.tree.delete(*self.tree.get_children())
            self.result_var.set("")
            
            # Parse input values
            function_str = self.function_var.get()
            derivative_str = self.derivative_var.get()
            initial_point = float(self.initial_point_var.get())
            tolerance = float(self.tolerance_var.get())
            max_iterations = int(self.max_iterations_var.get())
            
            # Parse functions with 'x' as the variable
            function = parse_function(function_str, ["x"])
            derivative = parse_function(derivative_str, ["x"])
            
            # Create Newton-Raphson solver and find root
            nr_solver = NewtonRaphson(function, derivative, tolerance, max_iterations)
            root, iterations, converged = nr_solver.solve(initial_point)
            
            # Display iterations in the table
            for i, data in enumerate(iterations):
                values = (
                    data['iteration'],
                    f"{data['x_current']:.8f}",
                    f"{data['fx']:.8f}",
                    f"{data['dfx']:.8f}",
                    f"{data['x_next']:.8f}",
                    f"{data['error']:.8f}"
                )
                self.tree.insert("", tk.END, values=values)
            
            # Display result message
            if converged:
                self.result_var.set(f"Root found: {root:.8f} (Converged in {len(iterations)} iterations)")
            else:
                self.result_var.set(f"Method did not converge. Last approximation: {root:.8f}")
            
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")