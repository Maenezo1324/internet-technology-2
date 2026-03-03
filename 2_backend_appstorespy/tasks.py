import os
import time
from celery import Celery
from database import FileTask, SessionLocal

CELERY_BROKER = os.getenv('CELERY_BROKER', 'redis://redis:6379/0')
celery_app = Celery('tasks', broker=CELERY_BROKER, backend=CELERY_BROKER)

@celery_app.task
def process_file_task(task_id: int, file_content: str):
    time.sleep(5)  # Имитация долгой обработки файла
    db = SessionLocal()
    task = db.query(FileTask).filter(FileTask.id == task_id).first()
    if task:
        task.lines_count = len(file_content.splitlines())
        task.status = 'completed'
        db.commit()
    db.close()