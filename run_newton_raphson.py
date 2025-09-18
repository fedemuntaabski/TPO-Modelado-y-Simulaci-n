"""
Script to run the Newton-Raphson application.
"""
import sys
import os
import tkinter as tk

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from newton_raphson.newton_raphson_app import NewtonRaphsonApp


def main():
    """Run the Newton-Raphson application."""
    root = tk.Tk()
    app = NewtonRaphsonApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()