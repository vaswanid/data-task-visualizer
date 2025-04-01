const API_URL = "http://localhost:8000";

document.getElementById("taskForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const filters = document.getElementById("filters").value;

  const response = await fetch(`${API_URL}/tasks/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ filters }),
  });

  const task = await response.json();
  loadTasks();
});

async function loadTasks() {
  const res = await fetch(`${API_URL}/tasks/`);
  const tasks = await res.json();

  const taskList = document.getElementById("taskList");
  taskList.innerHTML = "<h2>Tasks</h2>";
  tasks.forEach((task) => {
    const div = document.createElement("div");
    div.classList.add("task-item");
    div.innerHTML = `
      <strong>ID:</strong> ${task.id}<br />
      <strong>Status:</strong> ${task.status}<br />
      <strong>Created:</strong> ${new Date(task.created_at).toLocaleString()}<br />
      <button onclick="loadCars(${task.id})">View Cars</button>
      <hr />
    `;
    taskList.appendChild(div);
  });
}

async function loadCars(taskId) {
  const res = await fetch(`${API_URL}/tasks/${taskId}/cars`);
  const cars = await res.json();

  const carData = document.getElementById("carData");
  carData.innerHTML = `<h2>Cars for Task ${taskId}</h2>`;
  cars.forEach((car) => {
    const div = document.createElement("div");
    div.classList.add("car-card");
    div.innerHTML = `
      <strong>${car.car_company} ${car.car_model}</strong><br/>
      Price: $${car.price} | Mileage: ${car.mileage}mi<br/>
      Date of Sale: ${car.date_of_sale}<br/><hr/>
    `;
    carData.appendChild(div);
  });
}

loadTasks();
