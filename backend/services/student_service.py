from database.db import (
    fetch_all_students,
    add_student,
    delete_student,
    fetch_student,
    update_student,
    search_students,
)


def get_students(search=""):
    search = search.strip()                # "  ra  " → "ra",   "   " → ""
    if not search:                         # nothing left to search for?
        return fetch_all_students()        # → everyone (the old behaviour)
    return search_students(search)         # → only the matches


def check_student_data(data):
    name = str(data.get("name", "")).strip()
    course = str(data.get("course", "")).strip()
    age = data.get("age")

    if not name or not course:
        raise ValueError("Name and course are required")
    if not isinstance(age, int) or age <= 0:
        raise ValueError("Age must be a positive number")

    return name, age, course


def create_student(data):
    name, age, course = check_student_data(data)
    return add_student(name, age, course)


def remove_student(student_id):
    deleted = delete_student(student_id)
    if deleted == False:
        raise LookupError("Student not found")

def get_student(student_id):
    student = fetch_student(student_id)
    if student is None:
        raise LookupError("Student not found")
    return student

def edit_student(student_id, data):
    name, age, course = check_student_data(data)
    if not update_student(student_id, name, age, course):
        raise LookupError("Student not found")
    return {"id": student_id, "name": name, "age": age, "course": course}
