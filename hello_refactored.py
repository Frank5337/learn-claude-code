#!/usr/bin/env python3
"""A simple hello world program with type hints and documentation.

This module demonstrates proper Python coding practices including:
- Type hints for function signatures
- Comprehensive docstrings
- Main guard pattern
- Clear module-level documentation
"""

import sys
from typing import Optional


def greet(name: Optional[str] = None) -> str:
    """Generate a greeting message.
    
    Args:
        name: The name to greet. If None, defaults to "World".
        
    Returns:
        A greeting string in the format "Hello, {name}!".
        
    Examples:
        >>> greet()
        'Hello, World!'
        >>> greet("Alice")
        'Hello, Alice!'
    """
    if name is None:
        name = "World"
    return f"Hello, {name}!"


def main() -> None:
    """Main entry point for the program.
    
    This function demonstrates the usage of the greet function
    and handles command-line arguments if provided.
    """
    # Get name from command line arguments if provided
    name = None
    if len(sys.argv) > 1:
        name = sys.argv[1]
    
    # Generate and print the greeting
    message = greet(name)
    print(message)


if __name__ == "__main__":
    main()
