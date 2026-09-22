-- Create Database
CREATE DATABASE StudentManagementDB;
GO

USE StudentManagementDB;
GO

-- 1. Users Table (Stores authentication credentials)
CREATE TABLE Users (
    UserID INT IDENTITY(1,1) PRIMARY KEY,
    Email NVARCHAR(255) NOT NULL UNIQUE, -- Email is used as the username
    PasswordHash NVARCHAR(255) NOT NULL,
    Role NVARCHAR(20) NOT NULL CHECK (Role IN ('Admin', 'Lecturer', 'Student')),
    ResetToken NVARCHAR(255) NULL,
    ResetTokenExpiry DATETIME NULL,
    CreatedAt DATETIME DEFAULT GETDATE()
);
GO

-- 2. Courses Table
CREATE TABLE Courses (
    CourseID INT IDENTITY(1,1) PRIMARY KEY,
    CourseCode NVARCHAR(20) NOT NULL UNIQUE,
    CourseName NVARCHAR(100) NOT NULL
);
GO

-- 3. Lecturers Table
CREATE TABLE Lecturers (
    LecturerID INT IDENTITY(1,1) PRIMARY KEY,
    UserID INT NOT NULL UNIQUE FOREIGN KEY REFERENCES Users(UserID) ON DELETE CASCADE,
    FirstName NVARCHAR(50) NOT NULL,
    LastName NVARCHAR(50) NOT NULL,
    Department NVARCHAR(100) NULL
);
GO

-- 4. Students Table
CREATE TABLE Students (
    StudentID INT IDENTITY(1,1) PRIMARY KEY,
    UserID INT NOT NULL UNIQUE FOREIGN KEY REFERENCES Users(UserID) ON DELETE CASCADE,
    StudentNumber NVARCHAR(20) NOT NULL UNIQUE,
    FirstName NVARCHAR(50) NOT NULL,
    LastName NVARCHAR(50) NOT NULL
);
GO

-- 5. Student Course Enrollments Table (Student <-> Course relationship)
CREATE TABLE StudentCourses (
    EnrollmentID INT IDENTITY(1,1) PRIMARY KEY,
    StudentID INT NOT NULL FOREIGN KEY REFERENCES Students(StudentID) ON DELETE CASCADE,
    CourseID INT NOT NULL FOREIGN KEY REFERENCES Courses(CourseID) ON DELETE CASCADE,
    CONSTRAINT UQ_Student_Course UNIQUE (StudentID, CourseID)
);
GO

-- 6. Lecturer Allocations & Marks Table
-- Links Lecturer to a Student's Course, and stores the allocated Mark
CREATE TABLE LecturerAllocations (
    AllocationID INT IDENTITY(1,1) PRIMARY KEY,
    LecturerID INT NOT NULL FOREIGN KEY REFERENCES Lecturers(LecturerID),
    StudentID INT NOT NULL FOREIGN KEY REFERENCES Students(StudentID),
    CourseID INT NOT NULL FOREIGN KEY REFERENCES Courses(CourseID),
    Mark DECIMAL(5, 2) NULL CHECK (Mark >= 0 AND Mark <= 100),
    CONSTRAINT UQ_Lecturer_Student_Course UNIQUE (LecturerID, StudentID, CourseID)
);
GO