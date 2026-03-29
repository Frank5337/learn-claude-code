"""MyPackage - A sample Python package with utility functions.

This package provides various utility functions for common tasks.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Import key functions to make them available at package level
from .utils import (
    add_numbers,
    multiply_numbers,
    is_even,
    reverse_string,
    calculate_average,
    factorial,
    fibonacci,
)

__all__ = [
    "add_numbers",
    "multiply_numbers",
    "is_even",
    "reverse_string",
    "calculate_average",
    "factorial",
    "fibonacci",
]
