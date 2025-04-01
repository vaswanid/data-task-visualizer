import asyncio
import random
from sqlalchemy.orm import Session
from utils import load_json_data, load_csv_data, clean_data, merge_sources
from database import SessionLocal
from time import sleep
import models
from utils import load_json_data, load_csv_data, clean_data, merge_sources

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
async def handle_task():
     