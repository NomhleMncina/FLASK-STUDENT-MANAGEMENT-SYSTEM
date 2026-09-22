from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.models import Student, LecturerAllocation
from utils.decorators import role_required

student_bp = Blueprint('student', __name__, url_prefix='/student')

# ----------------------------------------------------
# 1. STUDENT DASHBOARD (View Assigned Marks)
# ----------------------------------------------------
@student_bp.route('/dashboard')
@login_required
@role_required('Student')
def dashboard():
    student = current_user.student_profile
    
    # Retrieve marks allocated specifically to THIS student
    allocations = LecturerAllocation.query.filter_by(StudentID=student.StudentID).all()
    
    return render_template('student/dashboard.html', student=student, allocations=allocations)

# ----------------------------------------------------
# 2. VIEW & EDIT PROFILE
# ----------------------------------------------------
@student_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@role_required('Student')
def profile():
    student = current_user.student_profile
    if request.method == 'POST':
        student.FirstName = request.form.get('first_name', '').strip()
        student.LastName = request.form.get('last_name', '').strip()
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('student.profile'))

    return render_template('student/profile.html', student=student)