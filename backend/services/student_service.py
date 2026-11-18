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


def require_text(value, field):
    if value is None:                      # missing or null
        raise ValueError(f"{field} is required")
    if not isinstance(value, str):         # 123, ["a"], {...} are not text
        raise ValueError(f"{field} must be text")
    value = value.strip()
    if not value:                          # "   " → ""
        raise ValueError(f"{field} is required")
    return value


def check_student_data(data):
    if not isinstance(data, dict):         # [], null, "text", or no valid JSON at all
        raise ValueError("Request body must be a JSON object")

    name = require_text(data.get("name"), "Name")
    course = require_text(data.get("course"), "Course")
    age = data.get("age")

    # bool is a subclass of int in Python (True == 1), so it has to be ruled out first
    if isinstance(age, bool) or not isinstance(age, int) or age <= 0:
        raise ValueError("Age must be a positive whole number")

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
