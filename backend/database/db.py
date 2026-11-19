import sqlite3

from models.student import Student

DB_PATH = "students.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()
    connection.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id     INTEGER PRIMARY KEY AUTOINCREMENT,
            name   TEXT    NOT NULL,
            age    INTEGER NOT NULL,
            course TEXT    NOT NULL
        )
    """)
    connection.commit()
    connection.close()


def fetch_all_students():
    connection = get_connection()
    rows = connection.execute("SELECT * FROM students").fetchall()
    connection.close()
    return [Student.from_row(row) for row in rows]

def add_student(student):
    connection = get_connection()
    cursor = connection.execute(
        "INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
        (student.name, student.age, student.course),
    )
    connection.commit()
    student.id = cursor.lastrowid          # the new object now knows its id
    connection.close()
    return student

def delete_student(student_id):
    connection = get_connection()
    cursor = connection.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,),
    )
    connection.commit()
    deleted = cursor.rowcount > 0
    connection.close()
    return deleted

def fetch_student(student_id):
    connection = get_connection()
    row = connection.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,),
    ).fetchone()
    connection.close()
    return Student.from_row(row) if row else None

def update_student(student):
    connection = get_connection()                          # open students.db
    sql = "UPDATE students SET name = ?, age = ?, course = ? WHERE id = ?"
    values = (student.name, student.age, student.course, student.id)
    cursor = connection.execute(sql, values)               # do it
    connection.commit()                                    # save the change
    updated = cursor.rowcount > 0                          # did a row change?
    connection.close()                                     # close students.db
    return updated                                         # True or False

def search_students(text):
    connection = get_connection()                          # open students.db
    pattern = f"%{text}%"                                  # "%ai%" = contains "ai" anywhere
    sql = "SELECT * FROM students WHERE name LIKE ? OR course LIKE ?"
    rows = connection.execute(sql, (pattern, pattern)).fetchall()  # same pattern for both ?
    connection.close()                                     # close students.db
    return [Student.from_row(row) for row in rows]         # rows → list of Student objects

