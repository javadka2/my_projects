# Student Grade Management System

Overview

A command-line Student Grade Management System built with Python and CSV file storage. The application allows users to manage student records, course grades, perform searches, calculate GPA, and maintain academic data through a simple interactive menu.

Features

Student Record Management

* Create student grade records
* Automatically reuse existing student information based on Student ID
* Store student details including ID, name, and major
* Delete student records from the system

Grade Management

* Add course grades for students
* Store course code, course name, and grade
* Validate grade input (0-20 range)
* Delete specific grade records for a student

Data Persistence

* Store all records in a CSV file
* Automatically create CSV file with headers if it does not exist
* Load and manage existing records across program executions

Student Transcript

* View all grades for a specific student
* Display enrolled courses and corresponding grades
* Generate a complete academic record from stored data

GPA Calculation

* Calculate GPA based on all recorded grades
* Handle invalid or corrupted grade entries safely
* Display GPA with formatted precision

Search Functionality

* Search students by course code
* View all students enrolled in a specific course
* Quickly locate academic records

File Handling & Validation

* CSV file initialization
* Input validation for grades
* Error handling for file operations
* Protection against missing or corrupted files

Technologies Used

* Python
* CSV Module
* File Handling
* Exception Handling
* OS Module

Main Functions

* Add Student Grade Entry
* View All Records
* View Student Grades
* Advanced Course Search
* Calculate GPA
* Delete Student Records
* Delete Specific Grade Entries

Technical Highlights

* CSV-based data storage system
* Input validation and error handling
* GPA calculation algorithms
* File persistence management
* Search and filtering operations
* Modular function-based design
* Command-line application development