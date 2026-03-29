#!/usr/bin/env python3
"""Test script to demonstrate the package functionality."""

import sys
import os

# Add parent directory to path to find the package
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mypackage import (
    add_numbers,
    multiply_numbers,
    is_even,
    reverse_string,
    calculate_average,
    factorial,
    fibonacci,
)

def main() -> None:
    """Test all utility functions."""
    print("Testing MyPackage utility functions:")
    print("=" * 40)
    
    # Test add_numbers
    result = add_numbers(5, 7)
    print(f"add_numbers(5, 7) = {result}")
    
    # Test multiply_numbers
    result = multiply_numbers(4, 6)
    print(f"multiply_numbers(4, 6) = {result}")
    
    # Test is_even
    result = is_even(10)
    print(f"is_even(10) = {result}")
    result = is_even(7)
    print(f"is_even(7) = {result}")
    
    # Test reverse_string
    result = reverse_string("Hello World")
    print(f'reverse_string("Hello World") = "{result}"')
    
    # Test calculate_average
    numbers = [1, 2, 3, 4, 5]
    result = calculate_average(numbers)
    print(f"calculate_average({numbers}) = {result}")
    
    # Test factorial
    result = factorial(5)
    print(f"factorial(5) = {result}")
    
    # Test fibonacci
    result = fibonacci(8)
    print(f"fibonacci(8) = {result}")
    
    print("=" * 40)
    print("All tests completed successfully!")

if __name__ == "__main__":
    main()