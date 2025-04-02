const API_URL = "http://localhost:8000";
console.log("JS loaded");
document.getElementById("create-task").addEventListener("click", async () => {
  console.log("Button clicked!");
});
document.getElementById("create-task").addEventListener("click", async () => {
  const filters = document.getElementById("filters").value;
  const response = await fetch("/tasks/", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify({ filters }),
  });
  const result = await response.json();
  // Show simple feedback
      alert(`✅ Task created with ID: ${result.task_id}`);
    });

    async function loadCars() {
      const res = await fetch("/cars");
      const cars = await res.json();
    
      const list = document.getElementById("car-list");
      list.innerHTML = "";
    
      cars.forEach((car) => {
        const item = document.createElement("li");
        item.textContent = `${car.brand} ${car.model} (${car.year})`;
        list.appendChild(item);
      });
    }

    window.onload = function () {
      loadTasks();
      loadCars(); 
    };


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

async function viewCars(taskId) {
  const res = await fetch(`/tasks/${taskId}/cars`);
  const cars = await res.json();

  const carSection = document.getElementById("car-section");
  carSection.innerHTML = `<h3>Cars for Task ${taskId}</h3>`;

  if (cars.length === 0) {
    carSection.innerHTML += "<p>No cars found for this task.</p>";
    return;
  }

  const list = document.createElement("ul");
  cars.forEach((car) => {
    const item = document.createElement("li");
    item.textContent = `${car.brand} ${car.model} (${car.year})`;
    list.appendChild(item);
  });

  carSection.appendChild(list);
}

btn.onclick = () => viewCars(task.id);

async function loadCars(taskId) {
  const res = await fetch(`${API_URL}/tasks/${taskId}/cars`);
  const cars = await res.json();

  const carData = document.getElementById("carData");
  carData.innerHTML = `<h2>Cars for Task ${taskId}</h2>`;
  cars.forEach((car) => {
    const div = document.createElement("div");
    div.classList.add("car-card");
    div.innerHTML = `
     async def put(task_data):
    await queue.put(task_data)
    `;
    carData.appendChild(div);
  });
}

loadTasks();
