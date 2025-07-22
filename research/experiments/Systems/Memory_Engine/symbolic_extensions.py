"""
Symbolic Extensions for UML Calculator
Provides additional mathematical functions beyond basic arithmetic.
"""

import math
from typing import Union, List, Tuple, Optional

def base52_encode(num: int) -> str:
    """
    Encode an integer in base-52 using A-Z, a-z notation.
    
    Args:
        num: Integer to encode
        
    Returns:
        Base-52 encoded string
    """
    if num < 1:
        return "0"
    
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    base = len(chars)
    result = ""
    
    while num > 0:
        num, remainder = divmod(num, base)
        result = chars[remainder] + result
        
    return result

def fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number.
    
    Args:
        n: Position in the Fibonacci sequence (0-based)
        
    Returns:
        nth Fibonacci number
    """
    if n < 0:
        raise ValueError("Fibonacci sequence undefined for negative indices")
    
    if n <= 1:
        return n
        
    # Fast calculation using matrix exponentiation
    def matrix_multiply(A, B):
        a = A[0][0] * B[0][0] + A[0][1] * B[1][0]
        b = A[0][0] * B[0][1] + A[0][1] * B[1][1]
        c = A[1][0] * B[0][0] + A[1][1] * B[1][0]
        d = A[1][0] * B[0][1] + A[1][1] * B[1][1]
        return [[a, b], [c, d]]
    
    def matrix_power(A, n):
        if n == 1:
            return A
        if n % 2 == 0:
            return matrix_power(matrix_multiply(A, A), n // 2)
        else:
            return matrix_multiply(A, matrix_power(A, n - 1))
    
    result = matrix_power([[1, 1], [1, 0]], n)
    return result[0][1]

def is_prime(n: int) -> bool:
    """
    Check if a number is prime.
    
    Args:
        n: Number to check
        
    Returns:
        True if the number is prime, False otherwise
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
        
    # Check all possible divisors up to sqrt(n)
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
        
    return True

def gcd(a: int, b: int) -> int:
    """
    Calculate the Greatest Common Divisor of two integers.
    
    Args:
        a: First integer
        b: Second integer
        
    Returns:
        Greatest Common Divisor
    """
    a, b = abs(int(a)), abs(int(b))
    
    # Handle special cases
    if a == 0 and b == 0:
        return 0
    if a == 0:
        return b
    if b == 0:
        return a
        
    # Euclidean algorithm
    while b:
        a, b = b, a % b
        
    return a

def lcm(a: int, b: int) -> int:
    """
    Calculate the Least Common Multiple of two integers.
    
    Args:
        a: First integer
        b: Second integer
        
    Returns:
        Least Common Multiple
    """
    a, b = abs(int(a)), abs(int(b))
    
    # Handle special cases
    if a == 0 or b == 0:
        return 0
        
    # LCM = (a * b) / gcd(a, b)
    return (a * b) // gcd(a, b)

def ris(a, b):
    from core.uml_core import ris_meta_operator
    result, _ = ris_meta_operator(a, b)
    return result

def safe_pow(a, b):
    try:
        return a ** b
    except Exception:
        return float('nan')
