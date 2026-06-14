# Student Grade Management API

## Overview

A RESTful API built with FastAPI and SQLite for managing students, courses, and grades. The system supports automatic creation of related records, transcript generation, GPA calculation, and data integrity enforcement through relational database design.

## Features

### Student Management
- Create and manage student records
- Retrieve student information
- List all registered students
- Delete students with automatic grade cleanup using cascading relationships

### Course Management
- Store and manage course information
- Automatically create courses when registering grades
- Prevent duplicate course records

### Grade Management
- Register grades through a single API request
- Automatically create missing students or courses
- Prevent duplicate grade entries using database constraints
- Maintain relationships between students and courses through foreign keys

### Transcript Generation
- Retrieve a complete transcript for a student
- Display enrolled courses and corresponding grades
- Utilize SQL JOIN operations for efficient data retrieval

### GPA Calculation
- Calculate student GPA directly from the database
- Use SQLite aggregate functions (AVG)
- Return formatted results with appropriate precision

### Data Integrity & Validation
- Foreign Key relationships
- UNIQUE constraints to prevent duplicate records
- Cascading delete operations (ON DELETE CASCADE)
- HTTP exception handling with meaningful responses
- Request and response validation using Pydantic

## Technologies Used

- FastAPI
- SQLite
- Pydantic
- Uvicorn
- SQL (JOIN, AVG, FOREIGN KEY, UNIQUE, CASCADE)

## Example Endpoints

- POST /grades
- GET /students
- GET /students/{student_id}/transcript
- GET /students/{student_id}/gpa
- DELETE /students/{student_id}

## Technical Highlights

- Relational database design
- Foreign key relationships
- Automatic entity creation logic
- Data validation and error handling
- Aggregate SQL queries
- REST API development with FastAPI
- Auto-generated Swagger/OpenAPI docum