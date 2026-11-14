# Student Management System

A small full-stack web app to add, view, edit and delete students.

- **Frontend:** HTML, CSS, JavaScript (`fetch`)
- **Backend:** Python Flask REST API, split into routes, services and database layers
- **Database:** SQLite (`students.db`, created automatically on first run)

## Features

- Dashboard with total students, number of courses, average age and students per course
- Student list with Edit and Delete actions
- Add and Edit forms with server-side validation

## Project structure

```
backend/
├── app.py                        # starts Flask, registers routes, CORS
├── routes/student_routes.py      # API endpoints (HTTP in/out)
├── services/student_service.py   # business rules and validation
└── database/db.py                # SQL queries (SQLite)
frontend/
├── index.html                    # dashboard
├── students.html                 # student list
├── add_student.html
├── edit_student.html
├── css/style.css
└── js/                           # one script per page
```

Request flow: `page -> fetch -> route -> service -> db.py -> students.db`, and the JSON answer comes back the same way.

## How to run

Run every command from the project folder.

1. Install the Python package (one time):

   ```
   pip install -r requirements.txt
   ```

2. Terminal 1: start the backend API (port 5000):

   ```
   python backend/app.py
   ```

3. Terminal 2: start the frontend (port 5500):

   ```
   python -m http.server 5500 --bind 127.0.0.1 --directory frontend
   ```

4. Open http://127.0.0.1:5500/index.html

Press `Ctrl + C` in each terminal to stop.

## API

| Method | URL | Description |
|---|---|---|
| GET | `/api/students` | List all students |
| POST | `/api/students` | Add a student |
| GET | `/api/students/<id>` | Get one student |
| PUT | `/api/students/<id>` | Update a student |
| DELETE | `/api/students/<id>` | Delete a student |

Student JSON: `{"id": 1, "name": "Anu", "age": 20, "course": "HTML"}`
