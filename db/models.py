from sqlalchemy.sql.schema import ForeignKey
from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

class DbUser(Base):
  __tablename__ = 'user'
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String)
  email = Column(String)
  password = Column(String)
  items = relationship('DbBatch', back_populates='user')



class DbBatch(Base):
  __tablename__ = 'batch'
  id = Column(Integer, primary_key=True, index=True)
  batch_title = Column(String)
  color_tag = Column(String)
  start_date = Column(DateTime)
  end_date = Column(DateTime)
  description = Column(String)
  created_by = Column(Integer, ForeignKey('user.id'))
  user = relationship('DbUser', back_populates='items')
  tasks = relationship('DbTask', back_populates='batch')
  
  


class DbTask(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String)
    task_description = Column(String)
    username = Column(String)  # Add username column
    status = Column(String)
    task_notes = Column(String)
    updated_at = Column(DateTime)
    created_by = Column(Integer, ForeignKey('user.id'))
    batch_id = Column(Integer, ForeignKey('batch.id'))
    batch = relationship('DbBatch', back_populates='tasks')
    user = relationship('DbUser', foreign_keys=[created_by])
