from extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'Users'

    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Email = db.Column(db.String(255), nullable=False, unique=True) # Used as Username
    PasswordHash = db.Column(db.String(255), nullable=False)
    Role = db.Column(db.String(20), nullable=False) # 'Admin', 'Lecturer', or 'Student'
    ResetToken = db.Column(db.String(255), nullable=True)
    ResetTokenExpiry = db.Column(db.DateTime, nullable=True)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    lecturer_profile = db.relationship('Lecturer', backref='user', uselist=False, cascade="all, delete")
    student_profile = db.relationship('Student', backref='user', uselist=False, cascade="all, delete")

    # Flask-Login requires a method to get the unique identifier
    def get_id(self):
        return str(self.UserID)


class Course(db.Model):
    __tablename__ = 'Courses'

    CourseID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CourseCode = db.Column(db.String(20), nullable=False, unique=True)
    CourseName = db.Column(db.String(100), nullable=False)

    # Relationships
    student_enrollments = db.relationship('StudentCourse', backref='course', cascade="all, delete")
    allocations = db.relationship('LecturerAllocation', backref='course', cascade="all, delete")


class Lecturer(db.Model):
    __tablename__ = 'Lecturers'

    LecturerID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID', ondelete='CASCADE'), nullable=False, unique=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    Department = db.Column(db.String(100), nullable=True)

    # Relationships
    allocations = db.relationship('LecturerAllocation', backref='lecturer', cascade="all, delete")


class Student(db.Model):
    __tablename__ = 'Students'

    StudentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID', ondelete='CASCADE'), nullable=False, unique=True)
    StudentNumber = db.Column(db.String(20), nullable=False, unique=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)

    # Relationships
    course_enrollments = db.relationship('StudentCourse', backref='student', cascade="all, delete")
    allocations = db.relationship('LecturerAllocation', backref='student', cascade="all, delete")


class StudentCourse(db.Model):
    __tablename__ = 'StudentCourses'

    EnrollmentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StudentID = db.Column(db.Integer, db.ForeignKey('Students.StudentID', ondelete='CASCADE'), nullable=False)
    CourseID = db.Column(db.Integer, db.ForeignKey('Courses.CourseID', ondelete='CASCADE'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('StudentID', 'CourseID', name='UQ_Student_Course'),
    )


class LecturerAllocation(db.Model):
    __tablename__ = 'LecturerAllocations'

    AllocationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    LecturerID = db.Column(db.Integer, db.ForeignKey('Lecturers.LecturerID'), nullable=False)
    StudentID = db.Column(db.Integer, db.ForeignKey('Students.StudentID'), nullable=False)
    CourseID = db.Column(db.Integer, db.ForeignKey('Courses.CourseID'), nullable=False)
    Mark = db.Column(db.Numeric(5, 2), nullable=True)

    __table_args__ = (
        db.UniqueConstraint('LecturerID', 'StudentID', 'CourseID', name='UQ_Lecturer_Student_Course'),
    )