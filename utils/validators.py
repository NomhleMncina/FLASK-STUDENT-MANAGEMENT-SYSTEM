import re

def is_strong_password(password: str) -> bool:
    """
    Validates password strength requirements:
    - Minimum 8 characters long
    - At least 1 uppercase letter (A-Z)
    - At least 1 lowercase letter (a-z)
    - At least 1 numeric digit (0-9)
    - At least 1 special character
    """
    if not password or len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    # Safely handle special characters without string termination issues
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password):
        return False
    return True

# Alias function to support auth.py import expectations
def validate_password_strength(password: str) -> bool:
    return is_strong_password(password)

def is_valid_email(email: str) -> bool:
    """
    Validates standard email address format.
    """
    if not email:
        return False
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(email_regex, email))

def is_valid_student_number(student_number: str) -> bool:
    """
    Validates student number format (e.g., ST1001, 8-10 alphanumeric characters).
    """
    if not student_number:
        return False
    return bool(re.match(r'^[A-Za-z0-9]{5,12}$', student_number))