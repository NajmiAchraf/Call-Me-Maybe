from src import *


def fn_add_numbers(a: float, b: float) -> float:
    """Add two numbers and return their sum."""
    return float(a) + float(b)


def fn_get_square_root(n: float) -> float:
    """Return the square root of a number."""
    return math.sqrt(n)


def fn_greet(name: str) -> str:
    """Return a greeting message."""
    return f"Hello, {name}!"


def fn_reverse_string(s: str) -> str:
    """Reverse a string."""
    return s[::-1]


def fn_substitute_string_with_regex(
    source_string: str,
    regex: str,
    replacement: str,
) -> str:
    """Substitute parts of a string that match a regex pattern with a replacement string."""

    return re.sub(regex, replacement, source_string)
