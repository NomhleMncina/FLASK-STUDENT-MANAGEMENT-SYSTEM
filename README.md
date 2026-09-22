# Nomhle Model School Student Management System

The Nomhle Model School Student Management System is a role-based web application designed to manage academic operations, user accounts, course allocations, and student grading. Built with Flask, SQL Server, and Tailwind CSS, the platform provides secure, tailored portals for Administrators, Lecturers, and Students.

## Learning Journey and Evolution

This project marks a key milestone in my software development journey, reflecting a progression from foundational programming to full-stack web development:

1. Command-Line Interface (CLI)
   Started by building a terminal-based student management tool to master Python fundamentals, object-oriented programming (OOP), data structures, and basic input validation.

2. Database Design & Persistence
   Moved from in-memory data storage to relational database architecture using SQL Server. Learned schema design, entity relationships, and database interaction via SQLAlchemy.

3. Full-Stack Web Development & APIs
   Expanded the application into a web platform using Flask Blueprints, Flask-Login, and Flask-Bcrypt. Focused on RESTful route design, secure authentication, role-based access control (RBAC), and responsive interface design using Tailwind CSS.

## Key Features

- Authentication & Security: Password hashing with Bcrypt and session management using Flask-Login.
- Administrator Portal: User management, course registration, and lecturer-to-course allocation.
- Lecturer Portal: Class roster overview, mark submission, and feedback management.
- Student Portal: Grade viewing, course enrollment tracking, and account management.
- Responsive Design: Consistent interface styled with Tailwind CSS.

## Default Access Credentials

For testing and demonstration purposes, the system supports three pre-configured accounts:

| Role | Email | Password | Primary Responsibilities |
| Admin | admin@nomhlemodelschool.ac.za | Admin123! | Full user and course administration |
| Lecturer | lecturer@nomhlemodelschool.ac.za | Lecturer123! | Grading and roster management |
| Student | student@nomhlemodelschool.ac.za | Student123! | Grade review and profile updates |

---

## Tech Stack

- Backend: Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-Bcrypt
- Database: Microsoft SQL Server (pyodbc)
- Frontend: Jinja2 Templates, Tailwind CSS
- Version Control: Git, GitHub

---

## Local Setup Instructions

1. Clone the repository:
   git clone https://github.com/YOUR_GITHUB_USERNAME/MY_SECOND_FLASK_APP.git
   cd MY_SECOND_FLASK_APP

2. Create and activate a virtual environment:
   python -m venv .venv
   .\.venv\Scripts\Activate

3. Install required dependencies:
   pip install -r requirements.txt

4. Configure environment variables (.env):
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key_here
   DATABASE_URL=mssql+pyodbc://sa:YourPassword@localhost/NomhleSMS?driver=ODBC+Driver+17+for+SQL+Server

5. Start the application:
   flask run
