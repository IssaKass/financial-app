"""
Validation Patterns and Functions

This module provides predefined patterns and validation functions for common input types such as
username, email, and password.

Username Pattern:
    - pattern: Regular expression for validating usernames 
                (3-20 characters, letters, numbers, symbols).
    - message: Error message for invalid usernames.

Email Pattern:
    - pattern: Regular expression for validating email addresses.
    - message: Error message for invalid email addresses.

Password Pattern:
    - pattern: Regular expression for validating passwords 
                (minimum 8 characters, letters, numbers, symbols).
    - message: Error message for invalid passwords.

Validation Function:
    - validate: General validation function that takes a value and a pattern, returning True if the
                value matches the pattern, and False otherwise.

Example Usage:
    username = "user123"
    is_valid_username = validate(username, USERNAME_PATTERN)
    if not is_valid_username:
        print(USERNAME_PATTERN["message"])
"""

import re

USERNAME_PATTERN = {
    "pattern": re.compile(r"^[A-Za-z0-9@#$%^&+=\s]{3,20}$"),
    "message": "Invalid username. 3-20 chars, letters, nums, symbols.",
}
EMAIL_PATTERN = {
    "pattern": re.compile(
        r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
    ),
    "message": "Invalid email. Use a valid address, e.g., yourname@example.com.",
}
PASSWORD_PATTERN = {
    "pattern": re.compile(r"^[A-Za-z0-9@#$%^&+=]{8,}$"),
    "message": "Invalid password. Min 8 chars, letters, nums, symbols.",
}


def validate(value, pattern: re):
    """
    Validate a value against a predefined pattern.

    Args:
        value (str): The input value to be validated.
        pattern (dict): A dictionary containing the pattern as a compiled regular expression
                        and an error message for invalid inputs.

    Returns:
        bool: True if the value matches the pattern, False otherwise.

    Example:
        >>> username = "user123"
        >>> is_valid_username = validate(username, USERNAME_PATTERN)
        >>> print(is_valid_username)
        True
    """
    return bool(pattern.search(value))
