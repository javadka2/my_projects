# Bank Account Management System

## Overview

A command-line banking application built with Python that allows users to create and manage bank accounts, perform financial transactions, and store account data persistently using JSON files.

The project demonstrates object-oriented programming (OOP), file handling, JSON serialization, transaction tracking, data persistence, and exception handling.

## Features

### Account Management
- Create new bank accounts
- Store account holder information
- Prevent duplicate account numbers
- Delete existing accounts
- Display account details

### Financial Operations
- Deposit money into accounts
- Withdraw money from accounts
- Balance validation before withdrawals
- Prevent negative or invalid transaction amounts
- Check current account balance

### Transaction History
- Record every transaction automatically
- Store transaction type, amount, timestamp, and resulting balance
- View complete transaction history for each account
- Maintain transaction records between program sessions

### Persistent Storage
- Save account data to a JSON file
- Automatically load existing accounts on startup
- Preserve balances and transaction history
- Handle missing or corrupted data files gracefully

### Error Handling & Validation
- Prevent negative initial balances
- Validate user input
- Detect invalid numeric values
- Handle corrupted JSON files
- Catch unexpected runtime errors

## Technologies Used

- Python 3
- Object-Oriented Programming (OOP)
- JSON
- OS Module
- Datetime Module

## Project Structure

### BankAccount Class
- Account creation and initialization
- Deposit operations
- Withdrawal operations
- Balance management
- Transaction recording
- Account information display
- Transaction history display

### Utility Functions
- save_accounts_to_file() – Saves account data
- load_accounts_from_file() – Loads account data
- display_menu() – Displays available options
- main() – Controls application workflow

## Example Features

- Create and manage multiple bank accounts
- Track deposits and withdrawals
- View detailed transaction logs
- Store all account information persistently
- Delete accounts with confirmation prompts

## Technical Highlights

- Object-oriented design using custom classes
- Persistent data storage with JSON
- Transaction logging system
- Input validation and exception handling
- Dynamic account management
- File integrity checking
- Modular and maintainable code structure

## Project Status

Completed ✔️

This project was developed as a Python practice project focused on object-oriented programming, file persistence, transaction management, and console application develo