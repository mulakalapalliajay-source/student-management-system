const API_URL = "http://127.0.0.1:5000/api/students";
const searchBox = document.getElementById("search");
let latestRequest = 0;  // numbers each search, so a slow old answer can't overwrite a newer one

async function loadStudents() {
    const search = searchBox.value.trim();
    const thisRequest = ++latestRequest;

    const response = await fetch(`${API_URL}?search=${encodeURIComponent(search)}`);
    const students = await response.json();

    if (thisRequest !== latestRequest) {
        return;  // the user typed more while we waited, so a newer search is on its way
    }

    const list = document.getElementById("student-list");
    list.innerHTML = "";

    if (students.length === 0) {
        if (search) {
            showMessage(list, `No students match "${search}".`);
        } else {
            showMessage(list, 'No students yet. Click "+ Add Student" to add one.');
        }
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

function showMessage(list, text) {
    const row = document.createElement("tr");
    const cell = document.createElement("td");
    cell.colSpan = 5;
    cell.className = "empty";
    cell.textContent = text;  // textContent, not innerHTML: the search text is shown as plain text, never run as HTML
    row.appendChild(cell);
    list.appendChild(row);
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

searchBox.addEventListener("input", loadStudents);  // runs on every keystroke, and when ✕ clears the box
loadStudents();
