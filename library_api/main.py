from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import sqlite3
import database

database.create_tables()

app = FastAPI()


class MemberCreate(BaseModel):
    name: str
    national_id: str
    phone: str


class MemberResponse(BaseModel):
    id: int
    name: str
    national_id: str
    phone: str
    created_at: str


class BookCreate(BaseModel):
    title: str
    author: str
    category: str
    quantity: int


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    category: str
    quantity: int

class BorrowCreate(BaseModel):
    member_national_id: str
    book_id: int
    due_date: str

class BorrowResponse(BaseModel):
    id: int
    member_id: int
    book_id: int
    borrow_date: str
    due_date: str
    return_date: str | None
    status: str

class BorrowHistoryResponse(BaseModel):
    title: str
    borrow_date: str
    due_date: str
    return_date: str | None
    status: str

class MemberUpdate(BaseModel):
    name: str
    national_id: str
    phone: str


class BookUpdate(BaseModel):
    title: str
    author: str
    category: str
    quantity: int


class OverdueResponse(BaseModel):
    borrow_id: int
    member_name: str
    book_title: str
    borrow_date: str
    due_date: str


@app.post("/members", response_model=MemberResponse)
def create_member(member: MemberCreate):
    conn = database.get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO members (name, national_id, phone)
            VALUES (?, ?, ?)
            """,
            (member.name, member.national_id, member.phone)
        )

        conn.commit()

        new_id = cursor.lastrowid

        cursor.execute(
            """
            SELECT id, name, national_id, phone, created_at
            FROM members
            WHERE id = ?
            """,
            (new_id,)
        )

        row = cursor.fetchone()

    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="National ID or phone already exists"
        )

    conn.close()

    return dict(row)


@app.get("/members", response_model=list[MemberResponse])
def get_members():
    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, national_id, phone, created_at
        FROM members
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


@app.get("/members/{national_id}", response_model=MemberResponse)
def get_member(national_id: str):
    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, national_id, phone, created_at
        FROM members
        WHERE national_id = ?
        """,
        (national_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
    )

    return dict(row)

@app.post('/books', response_model=BookResponse)
def add_books(book: BookCreate):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO books (title, author, category, quantity)
        VALUES (?, ?, ?, ?)
        """,
        (book.title, book.author, book.category, book.quantity)
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor.execute(
        """
        SELECT id, title, author, category, quantity
        FROM books
        WHERE id = ?
        """,
        (new_id,)
    )
    row = cursor.fetchone()

    conn.close()

    return dict(row)

@app.get('/books', response_model=list[BookResponse])
def get_books():
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, title, author, category, quantity
        FROM books
        """
    )
    rows = cursor.fetchall()

    conn.close()
    return [dict(row) for row in rows]

@app.get('/books/{book_id}', response_model=BookResponse)

def get_book(book_id: int):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute(

        """
        SELECT id, title, author, category, quantity
        FROM books
        WHERE id = ?
        """,
        (book_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
    )

    return dict(row)

@app.post('/borrowings', response_model=BorrowResponse)
def borrowings(borrow : BorrowCreate):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id FROM members WHERE national_id = ?
        """,
        (borrow.member_national_id,)
    )
    row = cursor.fetchone()

    if row is None:
        conn.close()
        raise HTTPException(
        status_code=404,
        detail="Member not found"
    )

    cursor.execute(
        """
        SELECT id , quantity FROM books WHERE id = ?
        """,
        (borrow.book_id,)
    )

    row2 = cursor.fetchone()
    
    if row2 is None:
        conn.close()
        raise HTTPException(
        status_code=404,
        detail="book not found"
    )

    book_db_id = row2["id"]
    available_quantity = row2["quantity"]

    if available_quantity <= 0:
        conn.close()    
        raise HTTPException(
        status_code=400,
        detail="Book is not available"
    )

    member_id = row["id"]

    cursor.execute(
        """
        INSERT INTO borrowings (member_id, book_id, due_date)
        VALUES (?, ?, ?)
        """,
        (member_id, book_db_id, borrow.due_date)
    )

    borrow_id = cursor.lastrowid

    cursor.execute(
        """
        UPDATE books SET quantity = quantity - 1 WHERE id = ?
        """,
        (book_db_id,)
    )

    conn.commit()

    cursor.execute(
    """
    SELECT 
    id,
    member_id,
    book_id,
    borrow_date,
    due_date,
    return_date,
    status
    FROM borrowings
    WHERE id = ?
    """,
    (borrow_id,)
    )
    result = cursor.fetchone()

    conn.close()
    return dict(result)

@app.put("/borrowings/{borrow_id}/return", response_model=BorrowResponse)

def return_borrowing(borrow_id: int):
    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, book_id, status
        FROM borrowings
        WHERE id = ?
        """,
        (borrow_id,)
    )

    row = cursor.fetchone()

    if row is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Borrow record not found"
        )

    if row["status"] == "returned":
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Book already returned"
        )

    return_date = datetime.now()

    cursor.execute(
        """
        UPDATE borrowings
        SET return_date = ?, status = ?
        WHERE id = ?
        """,
        (return_date, "returned", borrow_id)
    )

    book_id = row["book_id"]

    cursor.execute(
        """
        UPDATE books
        SET quantity = quantity + 1
        WHERE id = ?
        """,
        (book_id,)
    )

    conn.commit()

    cursor.execute(
        """
        SELECT
            id,
            member_id,
            book_id,
            borrow_date,
            due_date,
            return_date,
            status
        FROM borrowings
        WHERE id = ?
        """,
        (borrow_id,)
    )

    result = cursor.fetchone()

    conn.close()

    return dict(result)

@app.get("/members/{national_id}/borrowings", response_model=list[BorrowHistoryResponse])

def borrow_history(national_id: str):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id FROM members WHERE national_id = ?
        """,
        (national_id,)
    )
    row = cursor.fetchone()

    if row is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="national_id not found"
        )
    
    member_id = row["id"]
    cursor.execute(
        """
        SELECT
            books.title,
            borrowings.borrow_date,
            borrowings.due_date,
            borrowings.return_date,
            borrowings.status
        FROM borrowings
        JOIN books
        ON books.id = borrowings.book_id
        WHERE borrowings.member_id = ?
        """,
        (member_id,)
    )

    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/borrowings/overdue", response_model=list[OverdueResponse])
def get_overdue_books():
    conn = database.get_db_connection()
    cursor = conn.cursor()

    today = datetime.now()

    cursor.execute(
        """
        SELECT
            borrowings.id AS borrow_id,
            members.name AS member_name,
            books.title AS book_title,
            borrowings.borrow_date,
            borrowings.due_date
        FROM borrowings
        JOIN members
            ON members.id = borrowings.member_id
        JOIN books
            ON books.id = borrowings.book_id
        WHERE borrowings.status = ?
        AND borrowings.due_date < ?
        """,
        ("borrowed", today)
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]

@app.put("/members/{national_id}", response_model=MemberResponse)
def update_member(national_id: str, member: MemberUpdate):
    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM members
        WHERE national_id = ?
        """,
        (national_id,)
    )

    row = cursor.fetchone()

    if row is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    cursor.execute(
        """
        UPDATE members
        SET name = ?,
            national_id = ?,
            phone = ?
        WHERE id = ?
        """,
        (
            member.name,
            member.national_id,
            member.phone,
            row["id"]
        )
    )

    conn.commit()

    cursor.execute(
        """
        SELECT
            id,
            name,
            national_id,
            phone,
            created_at
        FROM members
        WHERE id = ?
        """,
        (row["id"],)
    )

    result = cursor.fetchone()

    conn.close()

    return dict(result)

@app.delete("/members/{national_id}")
def delete_member(national_id: str):
    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM members
        WHERE national_id = ?
        """,
        (national_id,)
    )

    row = cursor.fetchone()

    if row is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    cursor.execute(
        """
        DELETE FROM members
        WHERE national_id = ?
        """,
        (national_id,)
    )

    conn.commit()

    conn.close()

    return {
        "message": "Member deleted successfully"
    }

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book: BookUpdate
):
    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM books
        WHERE id = ?
        """,
        (book_id,)
    )

    row = cursor.fetchone()

    if row is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    cursor.execute(
        """
        UPDATE books
        SET title = ?,
            author = ?,
            category = ?,
            quantity = ?
        WHERE id = ?
        """,
        (
            book.title,
            book.author,
            book.category,
            book.quantity,
            book_id
        )
    )

    conn.commit()

    cursor.execute(
        """
        SELECT
            id,
            title,
            author,
            category,
            quantity
        FROM books
        WHERE id = ?
        """,
        (book_id,)
    )

    result = cursor.fetchone()

    conn.close()

    return dict(result)

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    conn = database.get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM books
        WHERE id = ?
        """,
        (book_id,)
    )

    row = cursor.fetchone()

    if row is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    cursor.execute(
        """
        DELETE FROM books
        WHERE id = ?
        """,
        (book_id,)
    )

    conn.commit()

    conn.close()

    return {
        "message": "Book deleted successfully"
    }

