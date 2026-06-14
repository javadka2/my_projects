# Bookstore Management API

## Overview

A RESTful API built with FastAPI and SQLite for managing products, customers, and sales operations in a bookstore environment.

This project was developed to practice backend development concepts including API design, database management, data validation, business logic implementation, and reporting.

---

## Features

### Product Management
- Create new products
- Retrieve product list
- Retrieve product details
- Delete products
- Track product inventory
- Automatically decrease stock after successful sales

### Customer Management
- Register customers
- Store customer information
- Unique phone number validation
- Search customers by phone number
- Retrieve customer list
- Automatic customer creation during sales process when needed

### Sales Management
- Record sales transactions
- Link sales to customers and products
- Update inventory after purchase
- Maintain purchase history for each customer
- Store transaction timestamps
- Prevent sales when stock is insufficient

### Reporting
- Best-selling product report
- Sales statistics based on transaction history

### Error Handling & Validation
- HTTP status code handling (400, 404, 500)
- Inventory validation before sale
- Duplicate phone number protection
- Database integrity error handling
- Input validation using Pydantic

---

## Technologies Used

- Python
- FastAPI
- SQLite
- Pydantic
- Uvicorn

---

## Database Structure

### Products
Stores product information and inventory data.

### Customers
Stores customer details and purchase history.

### Sales
Stores transaction records and relationships between customers and products.

---

## Learning Outcomes

Through this project I practiced:

- REST API development
- CRUD operations
- SQLite database design
- Foreign Key relationships
- Data validation with Pydantic
- Business logic implementation
- Error handling
- Inventory management
- API testing and debugging

---

## Future Improvements

- Authentication and Authorization (JWT)
- Product update endpoint
- Customer update endpoint
- Advanced sales reports
- Pagination and filtering
- PostgreSQL support
- Docker deployment
- Unit and Integration Te