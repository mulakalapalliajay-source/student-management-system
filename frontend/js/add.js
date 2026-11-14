const API_URL = "http://127.0.0.1:5000/api/students";

const form = document.getElementById("student-form");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const newStudent = {
        name: document.getElementById("name").value,
        age: Number(document.getElementById("age").value),
        course: document.getElementById("course").value,
    };

    const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newStudent),
    });

    if (!response.ok) {
        const result = await response.json();
        alert(result.error);
        return;
    }

    window.location.href = "students.html";
});
