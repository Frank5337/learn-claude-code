# MyPackage

A sample Python package with utility functions for common operations.

## Installation

```bash
pip install .
```

For development installation with testing dependencies:

```bash
pip install -e ".[dev]"
```

## Usage

```python
from mypackage import add_numbers, multiply_numbers, is_even, reverse_string

# Basic math operations
result = add_numbers(2, 3)  # Returns 5
product = multiply_numbers(4, 5)  # Returns 20

# Number utilities
even_check = is_even(10)  # Returns True

# String utilities
reversed_text = reverse_string("hello")  # Returns "olleh"

# More functions available
from mypackage.utils import calculate_average, factorial, fibonacci

average = calculate_average([1, 2, 3, 4, 5])  # Returns 3.0
fact = factorial(5)  # Returns 120
fib_seq = fibonacci(7)  # Returns [0, 1, 1, 2, 3, 5, 8]
```

## Available Functions

### Math Functions
- `add_numbers(a, b)`: Add two numbers
- `multiply_numbers(a, b)`: Multiply two numbers
- `is_even(number)`: Check if a number is even
- `calculate_average(numbers)`: Calculate average of a list
- `factorial(n)`: Calculate factorial
- `fibonacci(n)`: Generate Fibonacci sequence

### String Functions
- `reverse_string(text)`: Reverse a string

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=mypackage

# Run specific test file
pytest mypackage/tests/test_utils.py -v
```

### Code Quality

```bash
# Format code with black
black .

# Check code style with flake8
flake8 mypackage

# Type checking with mypy
mypy mypackage
```

## License

MIT License