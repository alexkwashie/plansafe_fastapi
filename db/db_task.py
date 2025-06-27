from fastapi import HTTPException, status
from routers.schemas import TaskBase
from sqlalchemy.orm.session import Session
from db.models import DbTask, DbUser, DbBatch
from datetime import datetime


def create_task(db: Session, request: TaskBase, user: DbUser):
  add_task = DbTask(
    batch_id = request.batch_id,
    task_name = request.task_name,
    task_description = request.task_description,
    username = user.username,  # Add username from the current user
    status = request.status,
    updated_at = datetime.now(),
    created_by = user.id,
    task_notes = request.task_notes
  )
  
  db.add(add_task)
  db.commit()
  db.refresh(add_task)
  return add_task



def get_all_task(db: Session, batch_id: int):
  tasks = db.query(DbTask).filter(DbTask.batch_id == batch_id).all()
  
  for task in tasks:
    if not task.username:
      # Find the user who created the batch
      batch = db.query(DbBatch).filter(DbBatch.id == batch_id).first()
      if batch:
        user = db.query(DbUser).filter(DbUser.id == batch.created_by).first()
        task.username = user.username if user else 'Unknown'
      else:
        task.username = 'Unknown'
  
  return tasks


def delete(id: int, db: Session):
  task = db.query(DbTask).filter(DbTask.id == id).first()
  if not task:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Task with id: {id} not found')
  db.delete(task)
  db.commit()
  return 'Deleted: Task with id:{id}'
