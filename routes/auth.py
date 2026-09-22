import secrets
from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from extensions import db, bcrypt, mail, login_manager
from models.models import User
from utils.validators import validate_password_strength

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect_to_role_dashboard(current_user.Role)

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(Email=email).first()

        if user and bcrypt.check_password_hash(user.PasswordHash, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect_to_role_dashboard(user.Role)
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('auth/login.html')


# Helper function to route users based on role
def redirect_to_role_dashboard(role):
    if role == 'Admin':
        return redirect(url_for('admin.dashboard'))
    elif role == 'Lecturer':
        return redirect(url_for('lecturer.dashboard'))
    elif role == 'Student':
        return redirect(url_for('student.dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out securely.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        action = request.form.get('action')

        # Action A: Change Username / Email Address
        if action == 'change_username':
            new_email = request.form.get('email', '').strip().lower()
            
            if new_email == current_user.Email:
                flash('The new email address is identical to your current email.', 'warning')
            elif User.query.filter_by(Email=new_email).first():
                flash('This email address is already taken by another account.', 'danger')
            else:
                current_user.Email = new_email
                db.session.commit()
                flash('Your email (username) has been updated successfully!', 'success')

        # Action B: Change Password
        elif action == 'change_password':
            current_password = request.form.get('current_password', '')
            new_password = request.form.get('new_password', '')
            confirm_password = request.form.get('confirm_password', '')

            # Verify current password
            if not bcrypt.check_password_hash(current_user.PasswordHash, current_password):
                flash('Current password is incorrect.', 'danger')
            elif new_password != confirm_password:
                flash('New passwords do not match.', 'danger')
            else:
                # Validate new password strength
                is_valid, msg = validate_password_strength(new_password)
                if not is_valid:
                    flash(msg, 'danger')
                else:
                    hashed_pw = bcrypt.generate_password_hash(new_password).decode('utf-8')
                    current_user.PasswordHash = hashed_pw
                    db.session.commit()
                    flash('Your password has been changed successfully!', 'success')

        return redirect(url_for('auth.profile'))

    return render_template('auth/profile.html', user=current_user)


# reset password

@auth_bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect_to_role_dashboard(current_user.Role)

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        user = User.query.filter_by(Email=email).first()

        if user:
            # Generate secure random token valid for 1 hour
            token = secrets.token_urlsafe(32)
            user.ResetToken = token
            user.ResetTokenExpiry = datetime.utcnow() + timedelta(hours=1)
            db.session.commit()

            # Send Email
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            msg = Message('Password Reset Request',
                          sender='noreply@studentmgmt.com',
                          recipients=[user.Email])
            msg.body = f'''To reset your password, visit the following link:
{reset_url}

If you did not make this request, simply ignore this email.
Link expires in 1 hour.
'''
            try:
                mail.send(msg)
                flash('An email with instructions to reset your password has been sent.', 'info')
            except Exception as e:
                flash('Error sending email. Please verify SMTP settings.', 'danger')
        else:
            # Mask user non-existence for security
            flash('An email with instructions to reset your password has been sent.', 'info')

        return redirect(url_for('auth.login'))

    return render_template('auth/reset_request.html')


@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect_to_role_dashboard(current_user.Role)

    # Find user with matching, non-expired token
    user = User.query.filter(
        User.ResetToken == token,
        User.ResetTokenExpiry > datetime.utcnow()
    ).first()

    if not user:
        flash('Invalid or expired password reset token.', 'danger')
        return redirect(url_for('auth.reset_password_request'))

    if request.method == 'POST':
        new_password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if new_password != confirm_password:
            flash('Passwords do not match.', 'danger')
        else:
            is_valid, msg = validate_password_strength(new_password)
            if not is_valid:
                flash(msg, 'danger')
            else:
                user.PasswordHash = bcrypt.generate_password_hash(new_password).decode('utf-8')
                user.ResetToken = None
                user.ResetTokenExpiry = None
                db.session.commit()
                flash('Your password has been reset! You can now log in.', 'success')
                return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', token=token)