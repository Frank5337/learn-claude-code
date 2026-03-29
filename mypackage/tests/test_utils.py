"""Unit tests for the utils module."""

import pytest
from mypackage.utils import (
    add_numbers,
    multiply_numbers,
    is_even,
    reverse_string,
    calculate_average,
    factorial,
    fibonacci,
)


class TestAddNumbers:
    """Test cases for add_numbers function."""
    
    def test_add_integers(self):
        """Test adding two integers."""
        assert add_numbers(2, 3) == 5
        assert add_numbers(-5, 10) == 5
        assert add_numbers(0, 0) == 0
    
    def test_add_floats(self):
        """Test adding two floats."""
        assert add_numbers(2.5, 3.5) == 6.0
        assert add_numbers(-1.5, 2.5) == 1.0
    
    def test_add_mixed(self):
        """Test adding integer and float."""
        assert add_numbers(2, 3.5) == 5.5
        assert add_numbers(2.5, 3) == 5.5


class TestMultiplyNumbers:
    """Test cases for multiply_numbers function."""
    
    def test_multiply_integers(self):
        """Test multiplying two integers."""
        assert multiply_numbers(2, 3) == 6
        assert multiply_numbers(-5, 4) == -20
        assert multiply_numbers(0, 100) == 0
    
    def test_multiply_floats(self):
        """Test multiplying two floats."""
        assert multiply_numbers(2.5, 4.0) == 10.0
        assert multiply_numbers(-1.5, 2.0) == -3.0


class TestIsEven:
    """Test cases for is_even function."""
    
    def test_even_numbers(self):
        """Test that even numbers return True."""
        assert is_even(2) is True
        assert is_even(0) is True
        assert is_even(-4) is True
    
    def test_odd_numbers(self):
        """Test that odd numbers return False."""
        assert is_even(3) is False
        assert is_even(1) is False
        assert is_even(-5) is False


class TestReverseString:
    """Test cases for reverse_string function."""
    
    def test_reverse_basic(self):
        """Test basic string reversal."""
        assert reverse_string("hello") == "olleh"
        assert reverse_string("Python") == "nohtyP"
    
    def test_reverse_empty(self):
        """Test reversing empty string."""
        assert reverse_string("") == ""
    
    def test_reverse_with_spaces(self):
        """Test reversing string with spaces."""
        assert reverse_string("hello world") == "dlrow olleh"


class TestCalculateAverage:
    """Test cases for calculate_average function."""
    
    def test_average_integers(self):
        """Test average of integers."""
        assert calculate_average([1, 2, 3, 4, 5]) == 3.0
        assert calculate_average([10, 20, 30]) == 20.0
    
    def test_average_floats(self):
        """Test average of floats."""
        assert calculate_average([1.5, 2.5, 3.5]) == 2.5
    
    def test_average_empty_list(self):
        """Test average of empty list returns None."""
        assert calculate_average([]) is None
    
    def test_average_single_element(self):
        """Test average of single element list."""
        assert calculate_average([42]) == 42.0


class TestFactorial:
    """Test cases for factorial function."""
    
    def test_factorial_positive(self):
        """Test factorial of positive numbers."""
        assert factorial(0) == 1
        assert factorial(1) == 1
        assert factorial(5) == 120
        assert factorial(7) == 5040
    
    def test_factorial_negative(self):
        """Test factorial of negative number raises ValueError."""
        with pytest.raises(ValueError, match="Factorial is not defined for negative numbers"):
            factorial(-5)


class TestFibonacci:
    """Test cases for fibonacci function."""
    
    def test_fibonacci_sequence(self):
        """Test Fibonacci sequence generation."""
        assert fibonacci(0) == []
        assert fibonacci(1) == [0]
        assert fibonacci(2) == [0, 1]
        assert fibonacci(5) == [0, 1, 1, 2, 3]
        assert fibonacci(7) == [0, 1, 1, 2, 3, 5, 8]
    
    def test_fibonacci_negative(self):
        """Test Fibonacci with negative n raises ValueError."""
        with pytest.raises(ValueError, match="n must be non-negative"):
            fibonacci(-3)


def test_import_from_package():
    """Test that functions can be imported from the package directly."""
    from mypackage import add_numbers, multiply_numbers, is_even
    assert add_numbers(2, 3) == 5
    assert multiply_numbers(2, 3) == 6
    assert is_even(4) is True


if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__, "-v"])