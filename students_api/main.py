from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import database  
import sqlite3
from typing import List

app = FastAPI(title="Student Grade Management API")

class GradeCreate(BaseModel):
    student_id: str       
    student_name: str       
    major: str              
    course_code: str        
    course_name: str         
    grade_value: float       

class StudentResponse(BaseModel):
    id: int
    student_id: str
    name: str
    major: str

class CourseResponse(BaseModel):
    id: int
    course_code: str
    course_name: str

@app.post("/grades")
def add_grade(grade: GradeCreate):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM students WHERE student_id = ?", (grade.student_id,))
    row = cursor.fetchone()
    if row:
        student_db_id = row["id"]
    else:
        cursor.execute(
            "INSERT INTO students (student_id, name, major) VALUES (?, ?, ?)",
            (grade.student_id, grade.student_name, grade.major)
        )
        conn.commit()
        student_db_id = cursor.lastrowid
    
    cursor.execute("SELECT id FROM courses WHERE course_code = ?", (grade.course_code,))
    row = cursor.fetchone()
    if row:
        course_db_id = row["id"]
    else:
        cursor.execute(
            "INSERT INTO courses (course_code, course_name) VALUES (?, ?)",
            (grade.course_code, grade.course_name)
        )
        conn.commit()
        course_db_id = cursor.lastrowid
    
    cursor.execute(
        "SELECT id FROM grades WHERE student_id = ? AND course_id = ?",
        (student_db_id, course_db_id)
    )
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Grade already recorded for this student and course")
    
    cursor.execute(
        "INSERT INTO grades (student_id, course_id, grade_value) VALUES (?, ?, ?)",
        (student_db_id, course_db_id, grade.grade_value)
    )
    conn.commit()
    new_grade_id = cursor.lastrowid
    
    cursor.execute("""
        SELECT s.student_id, s.name as student_name, s.major,
               c.course_code, c.course_name, g.grade_value
        FROM grades g
        JOIN students s ON g.student_id = s.id
        JOIN courses c ON g.course_id = c.id
        WHERE g.id = ?
    """, (new_grade_id,))
    result = cursor.fetchone()
    conn.close()
    
    return dict(result)

@app.get("/students/{student_id}")
def get_student_transcript(student_id: str):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, student_id, name, major FROM students WHERE student_id = ?", (student_id,))
    student = cursor.fetchone()
    if not student:
        conn.close()
        raise HTTPException(status_code=404, detail="Student not found")
    
    cursor.execute("""
        SELECT courses.course_code, courses.course_name, grades.grade_value
        FROM grades
        JOIN courses ON grades.course_id = courses.id
        WHERE grades.student_id = ?
    """, (student["id"],)) 
    grades = cursor.fetchall()
    conn.close()
    
    return {
        "student_id": student["student_id"],
        "name": student["name"],
        "major": student["major"],
        "grades": [dict(row) for row in grades]
    }

@app.get('/students')
def get_all_students():
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT student_id, name, major FROM students')
    rows = cursor.fetchall()
    cursor.close()
    return [dict(row) for row in rows]

@app.get("/students/{student_id}/gpa")
def get_student_gpa(student_id: str):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, student_id, name, major FROM students WHERE student_id = ?", (student_id,))
    student = cursor.fetchone()
    if not student:
        conn.close()
        raise HTTPException(status_code=404, detail="Student not found")
    
    cursor.execute("""
        SELECT AVG(grade_value) as average, COUNT(*) as courses_count
        FROM grades
        WHERE student_id = ?
    """, (student["id"],))
    result = cursor.fetchone()
    conn.close()
    
    average = result["average"] if result["average"] is not None else 0.0
    courses_count = result["courses_count"] if result["courses_count"] else 0
    
    return {
        "student_id": student["student_id"],
        "name": student["name"],
        "major": student["major"],
        "average": round(average, 2),
        "courses_count": courses_count
    }

@app.delete('/students/{student_id}')
def delete_student(student_id: str):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id FROM students WHERE student_id = ?',(student_id,)
    )
    rows = cursor.fetchone()
    if not rows:
        cursor.close()
        raise HTTPException(status_code=404, detail="Student not found")

    cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    conn.commit()
    conn.close()
    
    return {"message": f"Student with ID {student_id} deleted successfully"}
    