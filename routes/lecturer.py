from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.models import Lecturer, LecturerAllocation
from utils.decorators import role_required

lecturer_bp = Blueprint('lecturer', __name__, url_prefix='/lecturer')

# ----------------------------------------------------
# 1. LECTURER DASHBOARD
# ----------------------------------------------------
@lecturer_bp.route('/dashboard')
@login_required
@role_required('Lecturer')
def dashboard():
    lecturer = current_user.lecturer_profile
    allocations = LecturerAllocation.query.filter_by(LecturerID=lecturer.LecturerID).all()
    return render_template('lecturer/dashboard.html', lecturer=lecturer, allocations=allocations)

# ----------------------------------------------------
# 2. VIEW & EDIT PROFILE
# ----------------------------------------------------
@lecturer_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@role_required('Lecturer')
def profile():
    lecturer = current_user.lecturer_profile
    if request.method == 'POST':
        lecturer.FirstName = request.form.get('first_name', '').strip()
        lecturer.LastName = request.form.get('last_name', '').strip()
        lecturer.Department = request.form.get('department', '').strip()
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('lecturer.profile'))

    return render_template('lecturer/profile.html', lecturer=lecturer)

# ----------------------------------------------------
# 3. ASSIGN / EDIT MARKS FOR ALLOCATED STUDENTS ONLY
# ----------------------------------------------------
@lecturer_bp.route('/assign-mark/<int:allocation_id>', methods=['GET', 'POST'])
@login_required
@role_required('Lecturer')
def assign_mark(allocation_id):
    lecturer = current_user.lecturer_profile
    
    # SECURITY: Ensure lecturer can ONLY edit allocations assigned to THEM
    allocation = LecturerAllocation.query.filter_by(
        AllocationID=allocation_id,
        LecturerID=lecturer.LecturerID
    ).first_or_404()

    if request.method == 'POST':
        mark_input = request.form.get('mark', '').strip()
        try:
            mark_val = float(mark_input)
            if 0.0 <= mark_val <= 100.0:
                allocation.Mark = mark_val
                db.session.commit()
                flash(f'Mark assigned successfully for {allocation.student.FirstName}!', 'success')
                return redirect(url_for('lecturer.dashboard'))
            else:
                flash('Mark must be between 0 and 100.', 'danger')
        except ValueError:
            flash('Invalid mark input. Please enter a valid number.', 'danger')

    return render_template('lecturer/assign_mark.html', allocation=allocation)