const $ = (selector) => document.querySelector(selector);

async function api(url, options = {}) {
  const response = await fetch(url, {
    ...options,
    headers: { "Content-Type": "application/json", ...(options.headers || {}) }
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.error || `Request failed (${response.status})`);
  return data;
}

async function loadStudents() {
  const students = await api("/api/students");
  const body = $("#students-table");
  body.replaceChildren();
  if (!students.length) {
    body.innerHTML = '<tr><td colspan="4">No students added yet.</td></tr>';
  }
  students.forEach((student) => {
    const row = document.createElement("tr");
    [student.id, student.name, student.email, student.course].forEach((value) => {
      const cell = document.createElement("td");
      cell.textContent = value;
      row.appendChild(cell);
    });
    body.appendChild(row);
  });

  const select = $("#student-select");
  const selected = select.value;
  select.replaceChildren(new Option("Select a student", ""));
  students.forEach((student) => {
    select.add(new Option(`${student.name} (#${student.id})`, student.id));
  });
  if (selected) select.value = selected;
}

async function loadMarks() {
  const marks = await api("/api/marks");
  const body = $("#marks-table");
  body.replaceChildren();
  if (!marks.length) {
    body.innerHTML = '<tr><td colspan="3">No marks recorded yet.</td></tr>';
  }
  marks.forEach((mark) => {
    const row = document.createElement("tr");
    [mark.student_name, mark.subject, `${mark.score}%`].forEach((value) => {
      const cell = document.createElement("td");
      cell.textContent = value;
      row.appendChild(cell);
    });
    body.appendChild(row);
  });
}

async function refresh() {
  await Promise.all([loadStudents(), loadMarks()]);
}

$("#student-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  try {
    await api("/api/students", {
      method: "POST",
      body: JSON.stringify({
        name: form.get("name"),
        email: form.get("email"),
        course: form.get("course")
      })
    });
    $("#student-message").textContent = "Student added successfully.";
    event.currentTarget.reset();
    await refresh();
  } catch (error) {
    $("#student-message").textContent = error.message;
  }
});

$("#marks-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  try {
    await api("/api/marks", {
      method: "POST",
      body: JSON.stringify({
        student_id: form.get("student_id"),
        subject: form.get("subject"),
        score: form.get("score")
      })
    });
    $("#marks-message").textContent = "Marks recorded successfully.";
    event.currentTarget.reset();
    await loadMarks();
  } catch (error) {
    $("#marks-message").textContent = error.message;
  }
});

$("#refresh-button").addEventListener("click", () => {
  refresh().catch((error) => alert(error.message));
});

api("/api/health")
  .then((health) => { $("#health-status").textContent = `Service: ${health.status}`; })
  .catch(() => { $("#health-status").textContent = "Service unavailable"; });

refresh().catch((error) => console.error("Unable to load application data:", error));
