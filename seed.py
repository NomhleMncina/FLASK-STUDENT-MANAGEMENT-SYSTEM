from app import create_app
from extensions import db, bcrypt
from models.models import User, Course, Lecturer, Student, StudentCourse, LecturerAllocation

app = create_app()

def seed_data():
    with app.app_context():
        print("Resetting database tables...")
        # Drop and recreate all tables
        db.drop_all()
        db.create_all()

        print("Seeding default users and records...")

        # 1. Admin User
        admin_pw = bcrypt.generate_password_hash("Admin123!").decode('utf-8')
        admin_user = User(Email="admin@sms.com", PasswordHash=admin_pw, Role="Admin")
        db.session.add(admin_user)

        # 2. Lecturer User & Profile
        lecturer_pw = bcrypt.generate_password_hash("Lecturer123!").decode('utf-8')
        lecturer_user = User(Email="lecturer@sms.com", PasswordHash=lecturer_pw, Role="Lecturer")
        db.session.add(lecturer_user)
        db.session.flush()  # Generates UserID for foreign key usage

        lecturer_profile = Lecturer(
            UserID=lecturer_user.UserID,
            FirstName="John",
            LastName="Smith",
            Department="Computer Science"
        )
        db.session.add(lecturer_profile)

        # 3. Student User & Profile
        student_pw = bcrypt.generate_password_hash("Student123!").decode('utf-8')
        student_user = User(Email="student@sms.com", PasswordHash=student_pw, Role="Student")
        db.session.add(student_user)
        db.session.flush()  # Generates UserID for foreign key usage

        student_profile = Student(
            UserID=student_user.UserID,
            StudentNumber="ST1001",
            FirstName="Alice",
            LastName="Johnson"
        )
        db.session.add(student_profile)

        # 4. Sample Course
        course = Course(CourseCode="CS101", CourseName="Introduction to Computer Science")
        db.session.add(course)
        db.session.flush()  # Generates CourseID

        # 5. Enroll Student in Course
        enrollment = StudentCourse(StudentID=student_profile.StudentID, CourseID=course.CourseID)
        db.session.add(enrollment)

        # 6. Allocate Lecturer to Student & Course
        allocation = LecturerAllocation(
            LecturerID=lecturer_profile.LecturerID,
            StudentID=student_profile.StudentID,
            CourseID=course.CourseID,
            Mark=85.50
        )
        db.session.add(allocation)

        # Save all changes
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_data()