# Daily Task Manager

## Overview

A command-line task management application built with Python. The program allows users to create, view, delete, and persist daily tasks using a JSON file for storage.

This project demonstrates fundamental Python programming concepts including file handling, JSON serialization, exception handling, functions, loops, and data management.

## Features

### Task Management
- Add new tasks
- Delete existing tasks by ID
- View all saved tasks
- Automatic task ID assignment
- Automatic ID reordering after deletion

### Persistent Storage
- Save tasks to a JSON file
- Load tasks automatically when the program starts
- Preserve task data between application sessions

### Error Handling
- Handle invalid numeric inputs
- Detect corrupted or empty JSON files
- Validate task existence before deletion
- Prevent empty task descriptions

### User Interface
- Interactive command-line menu
- Clear task display with status information
- Simple and user-friendly workflow

## Technologies Used

- Python 3
- JSON
- OS Module

## Project Structure

- load_tasks() – Loads tasks from a JSON file
- save_tasks() – Saves tasks to persistent storage
- add_task() – Creates new tasks
- delete_task() – Removes tasks by ID
- show_tasks() – Displays all tasks
- display_menu() – Shows available options
- main() – Controls application flow

## Example Workflow

1. Start the application
2. Add one or more tasks
3. View the task list
4. Delete completed or unwanted tasks
5. Exit the application
6. Tasks remain stored for future sessions

## Technical Highlights

- Modular function-based design
- JSON-based data persistence
- Input validation and exception handling
- Dynamic task ID management
- Command-line application development

## Project Status

Completed ✔️

This project was developed as a Python practice project focused on file handling, data persistence, and console application developm