from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def role_required(*roles):
    """
    Generic role requirement decorator.
    Usage: @role_required('Admin', 'Lecturer')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.Role not in roles:
                flash('Access denied. You do not have permission to view this page.', 'danger')
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Specific Role Decorators
def admin_required(f):
    return role_required('Admin')(f)

def lecturer_required(f):
    return role_required('Lecturer')(f)

def student_required(f):
    return role_required('Student')(f)