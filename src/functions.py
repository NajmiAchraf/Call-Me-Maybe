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


def fn_get_square_root(a: int) -> float:
    """Return the square root of a number."""
    return math.sqrt(a)


def fn_substitute_string_with_regex(
    s: str, pattern: str, replacement: str
) -> str:
    """Substitute all occurrences of a pattern in a string with a replacement."""
    return re.sub(pattern, replacement, s)
