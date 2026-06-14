# Library Management API

## Overview

A RESTful API built with FastAPI and SQLite for managing library members, books, and borrowing operations. The system supports member registration, book inventory management, borrowing and returning books, overdue tracking, and borrowing history management through a relational database structure.

## Features

### Member Management
- Register new library members
- Retrieve member information by national ID
- List all registered members
- Prevent duplicate national IDs and phone numbers
- Automatically store membership registration date

### Book Management
- Add new books to the library catalog
- Retrieve book information
- List all available books
- Update book details and inventory
- Remove books from the catalog
- Track available book quantities

### Borrowing System
- Borrow books using member national ID and book ID
- Verify member and book existence before borrowing
- Prevent borrowing when inventory is unavailable
- Automatically decrease book quantity after successful borrowing
- Store borrowing and due dates

### Book Return Management
- Register returned books
- Automatically increase available inventory
- Prevent duplicate return operations
- Store return dates and update borrowing status

### Borrowing History
- View complete borrowing history for each member
- Display borrowed book titles, borrowing dates, due dates, return dates, and statuses
- Retrieve data using SQL JOIN operations between related tables

### Overdue Tracking
- Identify overdue borrowings
- Monitor books that have not been returned before the due date
- Support library staff in tracking delayed returns

### Data Integrity & Validation
- Foreign Key relationships between members, books, and borrowings
- Validation of incoming and outgoing data using Pydantic
- Prevention of invalid borrowing operations
- HTTP exception handling with meaningful error messages
- SQLite integrity constraints for data consistency

## Technologies Used

- FastAPI
- SQLite
- Pydantic
- Uvicorn
- SQL (JOIN, FOREIGN KEY, UPDATE, DELETE)
- Python Datetime

## Example Endpoints

- POST /members
- GET /members
- GET /members/{national_id}

- POST /books
- GET /books
- GET /books/{book_id}

- POST /borrowings
- PUT /borrowings/{borrow_id}/return

- GET /members/{national_id}/borrowings
- GET /borrowings/overdue

## Technical Highlights

- Relational database design with multiple related entities
- Foreign key relationships and referential integrity
- Inventory management logic
- Borrowing and return workflow implementation
- SQL JOIN operations for history retrieval
- Error handling and request validation
- REST API development with FastAPI
- Auto-generated Swagger/OpenAPI documentation
- Business logic implementation for library operatio