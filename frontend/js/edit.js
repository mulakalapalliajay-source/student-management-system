const API_URL = "http://127.0.0.1:5000/api/students";

const params = new URLSearchParams(window.location.search);
const id = params.get("id");

async function loadStudent() {
    const response = await fetch(`${API_URL}/${id}`);
    const student = await response.json();

    if (!response.ok) {
        alert(student.error);
        return;
    }

    document.getElementById("name").value = student.name;
    document.getElementById("age").value = student.age;
    document.getElementById("course").value = student.course;
}

loadStudent();

const form = document.getElementById("edit-form");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const changes = {
        name: document.getElementById("name").value,
        age: Number(document.getElementById("age").value),
        course: document.getElementById("course").value,
    };

    const response = await fetch(`${API_URL}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(changes),
    });

    if (!response.ok) {
        const result = await response.json();
        alert(result.error);
        return;
    }

    window.location.href = "students.html";
});
