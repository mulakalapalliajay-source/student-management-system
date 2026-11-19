class Student:
    """One student. The class is the template; each Student(...) is one object made from it."""

    def __init__(self, name, age, course, id=None):
        # __init__ runs when you write Student("Ravi", 24, "Python")
        # self = "this student", so every object keeps its own values
        self.id = id                       # None until the database gives one
        self.name = name
        self.age = age
        self.course = course

    def __repr__(self):
        # what print(student) and the terminal show
        return f"Student(id={self.id}, name={self.name!r}, age={self.age}, course={self.course!r})"

    def __eq__(self, other):
        # two Student objects with the same values count as equal
        if not isinstance(other, Student):
            return NotImplemented
        return self.to_dict() == other.to_dict()

    def to_dict(self):
        # object → dict, so the route can turn it into JSON
        return {"id": self.id, "name": self.name, "age": self.age, "course": self.course}

    @classmethod
    def from_dict(cls, data):
        # request JSON → Student, checking every field first (raises ValueError if bad)
        # cls = the Student class itself, so cls(...) is the same as Student(...)
        if not isinstance(data, dict):     # [], null, "text", or no valid JSON at all
            raise ValueError("Request body must be a JSON object")

        name = cls.require_text(data.get("name"), "Name")
        course = cls.require_text(data.get("course"), "Course")
        age = data.get("age")

        # bool is a subclass of int in Python (True == 1), so it has to be ruled out first
        if isinstance(age, bool) or not isinstance(age, int) or age <= 0:
            raise ValueError("Age must be a positive whole number")

        return cls(name, age, course)

    @classmethod
    def from_row(cls, row):
        # database row → Student
        return cls(row["name"], row["age"], row["course"], id=row["id"])

    @staticmethod
    def require_text(value, field):
        # a helper that needs no student and no class, just the value
        if value is None:                  # missing or null
            raise ValueError(f"{field} is required")
        if not isinstance(value, str):     # 123, ["a"], {...} are not text
            raise ValueError(f"{field} must be text")
        value = value.strip()
        if not value:                      # "   " → ""
            raise ValueError(f"{field} is required")
        return value
