from flask import Flask
from database.db import init_db
from routes.student_routes import student_routes

app = Flask(__name__)
app.register_blueprint(student_routes)


@app.after_request
def allow_frontend(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE"
    return response


if __name__ == "__main__":
    init_db()
    app.run(port=5000, debug=True)
