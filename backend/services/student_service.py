from database.db import (
    fetch_all_students,
    add_student,
    delete_student,
    fetch_student,
    update_student,
    search_students,
)
from models.student import Student


def get_students(search=""):
    search = search.strip()                # "  ra  " → "ra",   "   " → ""
    if not search:                         # nothing left to search for?
        return fetch_all_students()        # → everyone (the old behaviour)
    return search_students(search)         # → only the matches


def create_student(data):
    student = Student.from_dict(data)      # checks the data, or raises ValueError
    return add_student(student)            # the database fills in student.id


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
    student = Student.from_dict(data)      # checks the new data, or raises ValueError
    student.id = student_id                # this object replaces the student with this id
    if not update_student(student):
        raise LookupError("Student not found")
    return student
