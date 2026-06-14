# Contact Management System

## Overview

A command-line Contact Management System built with Python and CSV file storage. The application allows users to create, search, update, view, and delete contacts while maintaining persistent contact records across program executions.

## Features

### Contact Management
- Add new contacts
- Store contact name, phone number, email address, and creation timestamp
- Prevent empty required fields during contact creation
- View all saved contacts in a formatted table

### Search Functionality
- Search contacts by name
- Case-insensitive search
- Display multiple matching results

### Contact Updates
- Edit existing contact information
- Update name, phone number, and email address
- Preserve original creation date
- Support adding multiple phone numbers to a single contact

### Multiple Phone Numbers
- Store multiple phone numbers for a contact
- Append new phone numbers without overwriting existing ones
- Prevent duplicate phone numbers for the same contact

### Contact Deletion
- Remove contacts from the address book
- Automatically update stored records
- Confirm successful deletion operations

### Data Persistence
- Store contact information in CSV format
- Automatically create the CSV file if it does not exist
- Load existing contacts on startup
- Preserve data between program executions

### Validation & Error Handling
- File existence validation
- CSV read/write error handling
- Empty input validation
- Safe contact lookup and update operations

## Technologies Used

- Python
- CSV Module
- Datetime Module
- OS Module
- File Handling
- Exception Handling

## Main Functions

- Add Contact
- Update Contact
- Show All Contacts
- Search Contact
- Delete Contact

## Technical Highlights

- CSV-based persistent storage
- Dictionary-based data management
- Contact search and filtering algorithms
- Dynamic table formatting
- Multiple phone number support
- Timestamp tracking for contact creation
- Modular function-based architecture
- Command-line application develop