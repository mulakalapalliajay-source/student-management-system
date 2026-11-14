const API_URL = "http://127.0.0.1:5000/api/students";

async function loadStudents() {
    const response = await fetch(API_URL);
    const students = await response.json();

    const list = document.getElementById("student-list");
    list.innerHTML = "";

    if (students.length === 0) {
        list.innerHTML = '<tr><td colspan="5" class="empty">No students yet. Click "+ Add Student" to add one.</td></tr>';
        return;
    }

    for (const student of students) {
        const row = document.createElement("tr");

        for (const value of [student.id, student.name, student.age, student.course]) {
            const cell = document.createElement("td");
            cell.textContent = value;
            row.appendChild(cell);
        }

        const actions = document.createElement("td");
        actions.className = "actions";

        const editLink = document.createElement("a");
        editLink.textContent = "Edit";
        editLink.href = `edit_student.html?id=${student.id}`;
        editLink.className = "btn btn-small btn-secondary";
        actions.appendChild(editLink);

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.className = "btn btn-small btn-danger";
        deleteButton.addEventListener("click", () => deleteStudent(student.id, student.name));
        actions.appendChild(deleteButton);

        row.appendChild(actions);
        list.appendChild(row);
    }
}

async function deleteStudent(id, name) {
    if (!confirm(`Delete ${name}?`)) {
        return;
    }

    const response = await fetch(`${API_URL}/${id}`, { method: "DELETE" });

    if (!response.ok) {
        const result = await response.json();
        alert(result.error);
        return;
    }

    loadStudents();
}

loadStudents();
