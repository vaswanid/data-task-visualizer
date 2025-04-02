from backend.database import SessionLocal
from backend import models

db = SessionLocal()

# Delete all cars first (since they are linked to tasks)
db.query(models.Car).delete()
# Then delete all tasks
db.query(models.Task).delete()

db.commit()
db.close()

print("✅ All tasks and cars deleted successfully.")