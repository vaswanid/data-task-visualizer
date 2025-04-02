import asyncio
import random
from sqlalchemy.orm import Session
from utils import load_json_data, load_csv_data, clean_data, merge_sources
from database import SessionLocal
from time import sleep
import models
from utils import load_json_data, load_csv_data, clean_data, merge_sources
from datetime import datetime

# create a queue with a size limit
queue = asyncio.Queue(maxsize=100)

# Add task to queue
def put(task_data):
    queue.append(task_data)

# Handle individual task with simulated delay and DB update
async def task(queue):
    print('Task : Running')
    task_id = 0
    # make a task
    while True:
        delay = random.uniform(0.5, 3)  # simulate 0.5 to 3 seconds delay to prevent tight loop
        # wait for exactly 1 second
        await asyncio.sleep(delay)
        # push the task (could be task ID or anything)
        await queue.put(task_id)
         # signal: no more tasks
        print(f"Task added successfully")
        task_id += 1

# Handle individual task with simulated delay and DB update
async def handle_task(data):
     task_id, filters = data
     db: Session = SessionLocal()
     try:
        task = db.query(models.Task).filter(models.Task.id == task_id).first()
        if not task:
            return
# Simulate delay and update status to 'In Progress'        
        delay = random.uniform(5, 10)  # simulate 5 to 10 seconds delay to prevent tight loop
        await asyncio.sleep(delay)
        task.status = "In Progress"
        db.commit()
        print(f"✅ Task {task_id} is now 'In Progress' after {round(delay, 2)}s")
# Simulate another delay while loading/cleaning data
        await asyncio.sleep(5)
        source_a = clean_data(load_json_data())
        source_b = clean_data(load_csv_data())
        merged = merge_sources(source_a, source_b)

        for row in merged:
            car = models.Car(task_id=task_id, **row)
            db.add(car)

        task.status = "Completed"
        task.completed_at = datetime.utcnow()
        db.commit()
        print(f"✅✅✅ Task {task_id} COMPLETED!")
     except Exception as e:
        print(f"Error processing task {task_id}: {e}")
     finally:
        db.close()
