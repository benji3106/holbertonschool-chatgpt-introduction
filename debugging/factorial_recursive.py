#!/usr/bin/python3
import sys

def factorial(n):
    """
    Function Description:
        Computes the factorial of a non-negative integer using recursion.

    Parameters:
        n (int): The non-negative integer whose factorial is to be calculated.

    Returns:
        int: The factorial of the given integer n.
    """
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

f = factorial(int(sys.argv[1]))
print(f)
