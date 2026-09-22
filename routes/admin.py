from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from extensions import db, bcrypt
from models.models import User, Course, Lecturer, Student, LecturerAllocation
from utils.decorators import admin_required
from utils.validators import is_strong_password

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    student_count = Student.query.count()
    lecturer_count = Lecturer.query.count()
    course_count = Course.query.count()
    allocation_count = LecturerAllocation.query.count()

    return render_template(
        'admin/dashboard.html',
        student_count=student_count,
        lecturer_count=lecturer_count,
        course_count=course_count,
        allocation_count=allocation_count
    )

@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/manage_users.html', users=users)

@admin_bp.route('/users/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        if not is_strong_password(password):
            flash('Password must be at least 8 chars long, contain an uppercase, digit, and special char.', 'danger')
            return redirect(url_for('admin.add_user'))

        existing_user = User.query.filter_by(Email=email).first()
        if existing_user:
            flash('Email address already registered.', 'danger')
            return redirect(url_for('admin.add_user'))

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(Email=email, PasswordHash=hashed_pw, Role=role)
        db.session.add(new_user)
        db.session.commit()

        flash(f'User {email} created successfully as {role}!', 'success')
        return redirect(url_for('admin.manage_users'))

    return render_template('admin/add_user.html')

@admin_bp.route('/lecturers')
@login_required
@admin_required
def manage_lecturers():
    lecturers = Lecturer.query.all()
    return render_template('admin/manage_lecturers.html', lecturers=lecturers)

@admin_bp.route('/students')
@login_required
@admin_required
def manage_students():
    students = Student.query.all()
    return render_template('admin/manage_students.html', students=students)

@admin_bp.route('/courses')
@login_required
@admin_required
def manage_courses():
    courses = Course.query.all()
    return render_template('admin/manage_courses.html', courses=courses)

@admin_bp.route('/courses/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_course():
    if request.method == 'POST':
        code = request.form.get('course_code')
        name = request.form.get('course_name')

        new_course = Course(CourseCode=code, CourseName=name)
        db.session.add(new_course)
        db.session.commit()

        flash('Course created successfully!', 'success')
        return redirect(url_for('admin.manage_courses'))

    return render_template('admin/add_course.html')

@admin_bp.route('/allocations')
@login_required
@admin_required
def manage_allocations():
    allocations = LecturerAllocation.query.all()
    return render_template('admin/manage_allocations.html', allocations=allocations)

@admin_bp.route('/allocations/add', methods=['GET', 'POST'])
@login_required
@admin_required
def allocate_lecturer():
    if request.method == 'POST':
        lecturer_id = request.form.get('lecturer_id')
        student_id = request.form.get('student_id')
        course_id = request.form.get('course_id')

        allocation = LecturerAllocation(
            LecturerID=lecturer_id,
            StudentID=student_id,
            CourseID=course_id
        )
        db.session.add(allocation)
        db.session.commit()

        flash('Lecturer allocated successfully!', 'success')
        return redirect(url_for('admin.manage_allocations'))

    lecturers = Lecturer.query.all()
    students = Student.query.all()
    courses = Course.query.all()
    return render_template('admin/allocate.html', lecturers=lecturers, students=students, courses=courses)