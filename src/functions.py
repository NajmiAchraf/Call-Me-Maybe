from src import *


def fn_add_numbers(a: float, b: float) -> float:
    """Add two numbers and return their sum."""
    return float(a) + float(b)


def fn_greet(name: str) -> str:
    """Return a greeting message."""
    return f"Hello, {name}!"


def fn_reverse_string(s: str) -> str:
    """Reverse a string."""
    return s[::-1]
