import asyncio
import random
from sqlalchemy.orm import Session
from .utils import load_json_data, load_csv_data, clean_data, merge_sources
from . import models
from .database import SessionLocal
from datetime import datetime

queue = asyncio.Queue(maxsize=100)

async def put(task_data):
    await queue.put(task_data)

async def process_tasks():
    while True:
        if not queue.empty():
            task_data = await queue.get()
            await handle_task(task_data)
        await asyncio.sleep(1)

async def handle_task(data):
    task_id, filters = data
    db: Session = SessionLocal()
    try:
        task = db.query(models.Task).filter(models.Task.id == task_id).first()
        if not task:
            return

        delay = random.uniform(5, 10)
        await asyncio.sleep(delay)
        task.status = "In Progress"
        db.commit()
        print(f"✅ Task {task_id} is now 'In Progress' after {round(delay, 2)}s")

        await asyncio.sleep(5)

        try:
            cleaned_json = clean_data(load_json_data())
            print("✅ Cleaned JSON loaded:", cleaned_json)
        except Exception as e:
            print(f"❌ Failed loading JSON: {e}")
            cleaned_json = []

        try:
            cleaned_csv = clean_data(load_csv_data())
            print("✅ Cleaned CSV loaded:", cleaned_csv)
        except Exception as e:
            print(f"❌ Failed loading CSV: {e}")
            cleaned_csv = []

        merged = merge_sources(cleaned_json, cleaned_csv)
        print(f"✅ Merged data for task {task_id}: {merged}")

        for row in merged:
            car = models.Car(task_id=task_id, **row)
            db.add(car)

        task.status = "Completed"
        task.completed_at = datetime.utcnow()
        db.commit()
        print(f"✅✅✅ Task {task_id} COMPLETED!")

    except Exception as e:
        print(f"❌ Error processing task {task_id}: {e}")
    finally:
        db.close()
