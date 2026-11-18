from flask import Blueprint, jsonify, request
from services import student_service

student_routes = Blueprint("student_routes", __name__)


@student_routes.get("/api/students")
def list_students():
    search = request.args.get("search", "")               # ?search=ra → "ra",  no ?search → ""
    return jsonify(student_service.get_students(search))  # pass it down to the service


@student_routes.post("/api/students")
def create_student():
    try:
        # silent=True: broken JSON, form data or no body give None instead of an HTML error page
        student = student_service.create_student(request.get_json(silent=True))
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify(student), 201

@student_routes.delete("/api/students/<int:student_id>")
def delete_student(student_id):
    try:
        student_service.remove_student(student_id)
    except LookupError as error:
        return jsonify({"error": str(error)}), 404
    return "", 204

@student_routes.get("/api/students/<int:student_id>")
def get_student(student_id):
    try:
        student = student_service.get_student(student_id)
    except LookupError as error:
        return jsonify({"error": str(error)}), 404
    return jsonify(student)

@student_routes.put("/api/students/<int:student_id>")
def update_student(student_id):
    try:
        student = student_service.edit_student(student_id, request.get_json(silent=True))
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except LookupError as error:
        return jsonify({"error": str(error)}), 404
    return jsonify(student)
