"""Utility functions for common operations.

This module provides a collection of utility functions for mathematical
operations, string manipulation, and data processing.
"""

from typing import List, Union, Optional


def add_numbers(
    a: Union[int, float], b: Union[int, float]
) -> Union[int, float]:
    """Add two numbers.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of a and b
        
    Examples:
        >>> add_numbers(2, 3)
        5
        >>> add_numbers(2.5, 3.5)
        6.0
    """
    return a + b


def multiply_numbers(
    a: Union[int, float], b: Union[int, float]
) -> Union[int, float]:
    """Multiply two numbers.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Product of a and b
        
    Examples:
        >>> multiply_numbers(2, 3)
        6
        >>> multiply_numbers(2.5, 4)
        10.0
    """
    return a * b


def is_even(number: int) -> bool:
    """Check if a number is even.
    
    Args:
        number: Integer to check
        
    Returns:
        True if number is even, False otherwise
        
    Examples:
        >>> is_even(4)
        True
        >>> is_even(7)
        False
    """
    return number % 2 == 0


def reverse_string(text: str) -> str:
    """Reverse a string.
    
    Args:
        text: String to reverse
        
    Returns:
        Reversed string
        
    Examples:
        >>> reverse_string("hello")
        'olleh'
        >>> reverse_string("Python")
        'nohtyP'
    """
    return text[::-1]


def calculate_average(
    numbers: List[Union[int, float]]
) -> Optional[float]:
    """Calculate the average of a list of numbers.
    
    Args:
        numbers: List of numbers
        
    Returns:
        Average of the numbers, or None if the list is empty
        
    Examples:
        >>> calculate_average([1, 2, 3, 4, 5])
        3.0
        >>> calculate_average([]) is None
        True
    """
    if not numbers:
        return None
    return sum(numbers) / len(numbers)


def factorial(n: int) -> int:
    """Calculate factorial of a non-negative integer.
    
    Args:
        n: Non-negative integer
        
    Returns:
        Factorial of n
        
    Raises:
        ValueError: If n is negative
        
    Examples:
        >>> factorial(5)
        120
        >>> factorial(0)
        1
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def fibonacci(n: int) -> List[int]:
    """Generate Fibonacci sequence up to n terms.
    
    Args:
        n: Number of terms to generate
        
    Returns:
        List containing the first n Fibonacci numbers
        
    Raises:
        ValueError: If n is negative
        
    Examples:
        >>> fibonacci(5)
        [0, 1, 1, 2, 3]
        >>> fibonacci(1)
        [0]
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return []
    if n == 1:
        return [0]
    
    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[i-1] + sequence[i-2])
    return sequence[:n]
