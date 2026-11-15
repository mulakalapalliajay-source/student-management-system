import sqlite3

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
    return [dict(row) for row in rows]

def add_student(name, age, course):
    connection = get_connection()
    cursor = connection.execute(
        "INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
        (name, age, course),
    )
    connection.commit()
    new_id = cursor.lastrowid
    connection.close()
    return {"id": new_id, "name": name, "age": age, "course": course}

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
    return dict(row) if row else None

def update_student(student_id, name, age, course):
    connection = get_connection()                          # open students.db
    sql = "UPDATE students SET name = ?, age = ?, course = ? WHERE id = ?"
    cursor = connection.execute(sql, (name, age, course, student_id))  # do it
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
    return [dict(row) for row in rows]                     # rows → list of dicts

