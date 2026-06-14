import csv
import os

CSV_FILENAME = 'student_grades.csv'

def initialize_csv_file():

    if not os.path.exists(CSV_FILENAME):
        with open(CSV_FILENAME, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['student_id', 'student_name', 'major', 'course_code', 'course_name', 'grade_value'])
        print(f"File '{CSV_FILENAME}' created with headers.")
def get_student_info(student_id):

    if not os.path.exists(CSV_FILENAME):
        return None, None

    try:
        with open(CSV_FILENAME, 'r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file)
            try:
                next(reader) 
            except StopIteration:
                return None, None

            for row in reader:
                if row and row[0] == student_id: 
                    return row[1], row[2]
            return None, None
    except Exception as e:
        print(f"Error reading student info: {e}")
        return None, None

def add_entry():

    student_id = input("Please enter Student ID: ") 
    
    student_name, major = get_student_info(student_id)

    if student_name is None or major is None:
        print("Student with this ID not found. Please enter student details:")
        student_name = input("Student Name: ")
        major = input("Major: ")
        
        if not student_name or not major:
            print("Error: Student Name and Major cannot be empty.")
            return
            
    course_code = input("Course Code: ")
    course_name = input("Course Name: ")
    
    while True:
        try:
            grade_value = float(input("Grade Value (between 0 and 20): "))
            if 0 <= grade_value <= 20:
                break
            else:
                print("Error: Grade must be between 0 and 20.")
        except ValueError:
            print("Error: Please enter a valid number for the grade.")

    if not course_code or not course_name:
        print("Error: Course Code and Course Name cannot be empty.")
        return

    try:
        if not os.path.exists(CSV_FILENAME):
            initialize_csv_file() 

        with open(CSV_FILENAME, 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([student_id, student_name, major, course_code, course_name, str(grade_value)])
        
        print("Course information added successfully.")
        
    except IOError as e:
        print(f"File writing error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while adding the entry: {e}")

def view_all_entries():
    print("\n--- All Student Grade Entries ---")
    try:
        with open(CSV_FILENAME, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            print(f"{header[0]:<15} {header[1]:<20} {header[2]:<20} {header[3]:<15} {header[4]:<30} {header[5]:<10}")
            print("-" * 110)
            rows_found = False
            for row in reader:
                if row:
                    rows_found = True
                    print(f"{row[0]:<15} {row[1]:<20} {row[2]:<20} {row[3]:<15} {row[4]:<30} {row[5]:<10}")
            if not rows_found:
                print("No entries found in the file yet.")
        print("-" * 110)
    except FileNotFoundError:
        print(f"Error: The file '{CSV_FILENAME}' was not found. Please initialize the file first.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
def view_student_grades(student_id_to_view):

    if not os.path.exists(CSV_FILENAME):
        print(f"Error: File '{CSV_FILENAME}' not found. No data to display.")
        return

    found_grades = False
    try:
        with open(CSV_FILENAME, 'r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file)
            try:
                header = next(reader) 
            except StopIteration:
                print("The grade file is empty.")
                return 

            print(f"\n--- Grades for Student ID: {student_id_to_view} ---")

            for row in reader:
                if len(row) >= 6 and row[0] == student_id_to_view:
                    course_code = row[3]
                    course_name = row[4]
                    grade_value = row[5]
                    print(f"  - Course: {course_name} ({course_code}), Grade: {grade_value}")
                    found_grades = True
            
            if not found_grades:
                print("  No grades found for this student ID.")
            print("------------------------------------")

    except Exception as e:
        print(f"Error reading student grades: {e}")

def advance_search(advance_course_code):
    try:
        with open(CSV_FILENAME, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                header = next(reader)
                for row in reader:
                    if advance_course_code in row:
                        print('\n',row[1],'\n','-'*24)
    except Exception as e:
        print(f"Error,{e}")

def calculate_student_gpa():
    print("\n--- Calculate Student GPA ---")
    student_id = input("Enter Student ID to calculate GPA: ")

    total_grade_points = 0
    num_courses = 0
    student_found = False

    try:
        with open(CSV_FILENAME, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader) 

            for row in reader:
                if row and row[0] == student_id:
                    student_found = True
                    try:
                        grade_val = float(row[5])
                        total_grade_points += grade_val
                        num_courses += 1
                    except ValueError:
                        print(f"Warning: Invalid grade format '{row[5]}' for student {student_id}, course {row[3]}. Skipping.")
                    except IndexError:
                        print(f"Warning: Row format incorrect for student {student_id}, skipping.")

        if not student_found:
            print(f"Student with ID '{student_id}' not found.")
            return

        if num_courses == 0:
            print(f"No valid grades found for GPA calculation for student '{student_id}'.")
            return

        gpa = total_grade_points / num_courses
        print(f"GPA for Student ID '{student_id}': {gpa:.2f}")

    except FileNotFoundError:
        print(f"Error: The file '{CSV_FILENAME}' was not found. Please initialize the file first.")
    except Exception as e:
        print(f"An error occurred: {e}")
def delete_entry(filename="student_grades.csv"):

    student_id = input("Enter the Student ID you wish to delete: ")
    
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found. Please add some students first.")
        return

    students_data = []
    found = False
    
    try:
        with open(filename,'r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file)
            header = next(reader) 
            
            for row in reader:
                if row[0] == student_id:
                    found = True
                    print(f"Student with ID {student_id} found and will be removed.")
                else:
                    students_data.append(row)
        
        if not found:
            print(f"No student found with ID: {student_id}")
            return

        with open(filename, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(students_data)
        
        print(f"Student with ID {student_id} successfully deleted.")

    except Exception as e:
        print(f"An error occurred: {e}")

def delete_grade_entry(student_id_to_delete, course_code_to_delete):

    if not os.path.exists(CSV_FILENAME):
        print(f"Error: File '{CSV_FILENAME}' not found. Cannot delete entry.")
        return False

    rows_to_keep = []
    deleted = False
    
    try:
        with open(CSV_FILENAME, 'r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file)
            header = next(reader)
            rows_to_keep.append(header)

            for row in reader:
                if len(row) >= 6 and row[0] == student_id_to_delete and row[3] == course_code_to_delete:
                    deleted = True
                else:
                    rows_to_keep.append(row)

        if deleted:
            with open(CSV_FILENAME, 'w', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows_to_keep)
            print(f"Successfully deleted grade entry for Student ID: {student_id_to_delete}, Course Code: {course_code_to_delete}")
            return True
        else:
            print(f"No grade entry found for Student ID: {student_id_to_delete}, Course Code: {course_code_to_delete}. Nothing deleted.")
            return False

    except Exception as e:
        print(f"Error deleting grade entry: {e}")
        return False

def display_menu():
    print("\n===== Student Management System =====")
    print("1. Add New Student Grade Entry")
    print("2. View All Entries")
    print("3. View Student Grades")
    print("4. Advance Search")
    print("5. Calculate Student GPA")
    print("6. Delete Student")
    print("7. Delete Specifice Grade")
    print("8. Exit")
    print("===================================")

if __name__ == "__main__":
    initialize_csv_file()

    while True:
        display_menu()
        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            add_entry()
        elif choice == '2':
            view_all_entries()
        elif choice == '3':
            student_id_to_view = input("Please enter the Student ID to view grades: ")
            view_student_grades(student_id_to_view)
        elif choice == '4':
            advance_course_code = input("Please enter the course code for advance search: ")
            advance_search(advance_course_code)
        elif choice == '5':
            calculate_student_gpa()
        elif choice == '6':
            delete_entry()
        elif choice == '7':
            student_id_to_delete = input("Please enter the Student ID to delete the grade: ")
            course_code_to_delete = input("Please enter the course code to delete the grade: ")
            delete_grade_entry(student_id_to_delete , course_code_to_delete)
        elif choice == '8':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")
