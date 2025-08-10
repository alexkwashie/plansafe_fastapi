from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


##### User Schema #####
class UserBase(BaseModel):
  username: str
  email: str
  password: str

class UserDisplay(BaseModel): # what is displayed to the user
  username: str
  email: str

  class Config:
    orm_mode = True


# For BatchDisplay
class User(BaseModel):
  id: int
  class Config:
    orm_mode = True
    
# For BatchDisplay
class Task(BaseModel):
  task_name: str
  task_description: str
  username: str
  status: str = 'Pending'
  task_notes: Optional[str] = None
  class Config():
    orm_mode = True
    
  
##### Batch Schema #####
class BatchBase(BaseModel):
    batch_title: str
    #assignees_id:int
    color_tag: str
    start_date: datetime
    #start_time: datetime
    end_date: datetime
    description: Optional[str] = None
    created_by: int

    class Config:
        orm_mode = True

class BatchDisplay(BaseModel): # what is displayed
    id: int
    batch_title: str
    description: Optional[str] = None
    tasks: List[Task] = []

    class Config:
        orm_mode = True





class TaskBase(BaseModel):
  batch_id: int #(FK)
  task_name: str
  task_description: str
  status: str # 'Pending', 'In progress', 'Complete', 'Aborted', 'Delayed', 'On hold'
  created_by: int
  user_id: str
  updated_at: datetime
  task_notes: Optional[str] = None

  class Config:
    orm_mode = True


class TaskDisplay(BaseModel):  # what is displayed
  id: int #(PK)
  task_name: str
  task_description: str
  status: str
  task_notes: Optional[str] = None
  created_by: int
  updated_at: datetime
  user_id: str
  batch_id: int

  class Config:
    orm_mode = True


class UserAuth(BaseModel):
  id: int
  username: str
  email: str
