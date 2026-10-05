from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def general_check(value: str) -> None:
    """Reject path strings containing unsupported characters or extensions.

    Args:
        value: The path-like string to validate.

    Returns:
        None.

    Raises:
        argparse.ArgumentTypeError: If the path contains invalid characters or
            does not end with ``.json``.
    """

    if (
        not value.replace("/", "")
        .replace(".", "")
        .replace("-", "")
        .replace("_", "")
        .replace(" ", "")
        .replace(":", "")
        .isalnum()
    ):
        raise argparse.ArgumentTypeError(
            f"Invalid characters in path: {value}"
        )
    if not value.endswith(".json"):
        raise argparse.ArgumentTypeError(f"Invalid file format: {value}")


def parse_path_accuracy(value: str) -> str:
    """Validate that each parent directory in the path exists.

    Args:
        value: The path-like string to validate.

    Returns:
        The original value when all parent directories exist.

    Raises:
        argparse.ArgumentTypeError: If one of the parent directories is
            missing.
    """

    general_check(value)

    slash = value.split("/")
    full_path = ""

    for folder in slash[:-1]:
        full_path += folder + "/"
        if not os.path.isdir(full_path):
            raise argparse.ArgumentTypeError(f"Folder not found: {full_path}")

    return value


def parse_path_file(value: str) -> str:
    """Validate a JSON file path and ensure the file contains valid JSON.

    Args:
        value: The file path to validate.

    Returns:
        The original value when the path exists and contains valid JSON.

    Raises:
        argparse.ArgumentTypeError: If the file is missing or not valid JSON.
    """

    value = parse_path_accuracy(value)

    if not os.path.exists(value):
        raise argparse.ArgumentTypeError(f"File not found: {value}")
    try:
        with open(value, "r") as f:
            json.load(f)
    except json.JSONDecodeError:
        raise argparse.ArgumentTypeError(
            f"The file '{value}' is not a valid JSON file."
        )

    return value


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for input, output, and definitions.

    Returns:
        The parsed command-line arguments namespace.
    """

    project_root = Path(__file__).resolve().parents[1]

    parser = argparse.ArgumentParser(description="Call Me Maybe")

    parser.add_argument(
        "--functions_definition",
        type=parse_path_file,
        default=f"{project_root}/data/input/functions_definition.json",
        help="Path to the functions definition file",
    )

    parser.add_argument(
        "--input",
        type=parse_path_file,
        default=f"{project_root}/data/input/function_calling_tests.json",
        help="Path to the function calling tests",
    )

    parser.add_argument(
        "--output",
        default=f"{project_root}/data/output/function_calling_results.json",
        help="Path to the output file",
    )

    return parser.parse_args()
