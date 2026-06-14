# Bookstore Management System

## Overview

A command-line bookstore management system built with Python and Pandas. The application allows users to manage products, customers, inventory, and sales while maintaining persistent data storage using CSV files.

The system provides a complete workflow for product management, customer tracking, stock control, and sales recording.

## Features

### Product Management
- Add new products with automatic ID generation
- Update product information
- Search products by ID or name
- Display complete product inventory
- Track purchase and selling prices
- Manage stock quantities

### Inventory Control
- Automatic stock updates after each sale
- Validation to prevent negative inventory
- Out-of-stock detection
- Quantity availability checks before sales

### Customer Management
- Register new customers automatically during purchases
- Search customers by phone number
- Display customer information
- Maintain customer purchase history
- Support guest purchases without registration

### Sales Management
- Record multi-item sales transactions
- Generate unique sale IDs automatically
- Store detailed sales history
- Calculate total purchase amounts
- Track transaction timestamps
- Generate sale summaries

### Purchase History Tracking
- Store customer purchase records
- Maintain cumulative purchase history
- Track purchased products and quantities
- Retrieve customer buying behavior

### Data Persistence
- Store products, customers, and sales in CSV files
- Automatic data loading on startup
- Automatic saving after updates
- Persistent records across program sessions

### Search & Reporting
- Product search by ID or name
- Customer search by phone number
- Inventory viewing and management
- Sales history storage and retrieval

### Data Validation & Error Handling
- Input validation for quantities and prices
- Phone number format validation
- Stock availability checks
- File existence validation
- Exception handling for data operations

## Technologies Used

- Python
- Pandas
- CSV File Storage
- Datetime Module
- File System Operations (os)

## Data Structure

### Products
- Product ID
- Product Name
- Quantity
- Purchase Price
- Selling Price

### Customers
- Phone Number
- Customer Name
- Purchase History

### Sales
- Sale ID
- Timestamp
- Customer Information
- Purchased Items
- Total Amount

## Technical Highlights

- Object-oriented and modular design
- Automatic identifier generation
- Inventory synchronization
- Customer purchase tracking
- Persistent CSV-based storage
- Data validation and exception handling
- Sales transaction processing
- Business logic implementation without external databases

## Learning Outcomes

This project demonstrates:

- Data manipulation using Pandas
- CSV-based data persistence
- Inventory management logic
- Customer relationship tracking
- Transaction processing systems
- Input validation techniques
- File handling in Python
- Real-world business workflow implementa