const API_URL = "http://127.0.0.1:5000/api/students";

async function loadDashboard() {
    const response = await fetch(API_URL);
    const students = await response.json();

    const courseCounts = {};
    let totalAge = 0;
    for (const student of students) {
        courseCounts[student.course] = (courseCounts[student.course] || 0) + 1;
        totalAge += student.age;
    }

    document.getElementById("total-students").textContent = students.length;
    document.getElementById("total-courses").textContent = Object.keys(courseCounts).length;
    if (students.length > 0) {
        document.getElementById("average-age").textContent = (totalAge / students.length).toFixed(1);
    }

    const list = document.getElementById("course-list");
    list.innerHTML = "";

    if (students.length === 0) {
        list.innerHTML = '<tr><td colspan="2" class="empty">No students yet.</td></tr>';
        return;
    }

    const sortedCourses = Object.entries(courseCounts).sort((a, b) => b[1] - a[1]);
    for (const [course, count] of sortedCourses) {
        const row = document.createElement("tr");

        const courseCell = document.createElement("td");
        courseCell.textContent = course;
        row.appendChild(courseCell);

        const countCell = document.createElement("td");
        countCell.textContent = count;
        row.appendChild(countCell);

        list.appendChild(row);
    }
}

loadDashboard();
