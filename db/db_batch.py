from fastapi import HTTPException, status
from routers.schemas import BatchBase, TaskBase
from sqlalchemy.orm.session import Session
from db.models import DbBatch, DbTask, DbUser
import datetime


def create_batch(db: Session, request: BatchBase):
  # Create the batch first
  new_batch = DbBatch(
    batch_title = request.batch_title,
    color_tag = request.color_tag,
    start_date = request.start_date,
    end_date = request.end_date,
    created_by = request.created_by,
    description = request.description
  )
  
  db.add(new_batch)
  db.commit()
  db.refresh(new_batch)

  return new_batch

def get_all(db: Session):
  batches = db.query(DbBatch).all()
  
  # Ensure each task has a username
  for batch in batches:
    for task in batch.tasks:
      if not task.username:
        # Find the user who created the batch
        user = db.query(DbUser).filter(DbUser.id == batch.created_by).first()
        task.username = user.username if user else 'Unknown'
  
  return batches


def delete(id: int, db: Session):
  batch = db.query(DbBatch).filter(DbBatch.id == id).first()
  if not batch:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Batch with id: {id} not found')
  db.delete(batch)
  db.commit()
  return 'Deleted: Batch with id:{id}'
