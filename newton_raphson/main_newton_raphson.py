"""
Main file to run the Newton-Raphson application.
"""
import tkinter as tk
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from newton_raphson.newton_raphson_app import NewtonRaphsonApp


def main():
    """Run the Newton-Raphson application."""
    root = tk.Tk()
    app = NewtonRaphsonApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()