from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import uuid


##### User Schema #####
class UserBase(BaseModel):
  username: str
  email: str


class UserDisplay(BaseModel): # what is displayed to the user
  username: str
  email: str
  uid: uuid.UUID

  class Config:
    orm_mode = True


# For BatchDisplay
class User(BaseModel):
  id: int
  class Config:
    orm_mode = True
    
    
  
##### Batch Schema #####
class BatchBase(BaseModel):
    batch_title: str
    batch_description: Optional[str] = None
    batch_status: str
    start_date: datetime
    start_time: Optional[str] = None
    end_date: datetime
    end_time: Optional[str] = None
    location: Optional[str] = None
    color: Optional[str] = None
    estimated_duration: Optional[int] = None
    process_duration: Optional[int] = None
    created_at: Optional[datetime] = None
    created_by: uuid.UUID

    class Config:
        orm_mode = True
        
class BatchBaseUpdate(BaseModel):
    batch_title: str
    batch_description: Optional[str] = None
    batch_status: str
    start_date: datetime
    start_time: Optional[str] = None
    end_date: datetime
    end_time: Optional[str] = None
    location: Optional[str] = None
    color: Optional[str] = None
    estimated_duration: Optional[int] = None
    process_duration: Optional[int] = None
    updated_by: uuid.UUID
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class BatchDisplay(BaseModel): # what is displayed
    batch_title: str
    batch_description: Optional[str] = None
    batch_status: str
    start_date: datetime
    start_time: Optional[str] = None
    end_date: datetime
    end_time: Optional[str] = None
    location: Optional[str] = None
    color: Optional[str] = None
    estimated_duration: Optional[int] = None
    process_duration: Optional[int] = None
    created_at: Optional[datetime] = None
    created_by: uuid.UUID
    updated_at: Optional[datetime] = None
    updated_by: Optional[uuid.UUID] = None

    class Config:
        orm_mode = True





class TaskBase(BaseModel):
    batch_id: uuid.UUID
    task_seq: Optional[int] = None
    task_name: str
    task_description: Optional[str] = None
    task_notes: Optional[str] = None
    estimated_duration: Optional[int] = None  # Could be str or timedelta depending on usage
    status: Optional[str] = 'pending'
    output_product: Optional[str] = None
    outputs_quantity: Optional[int] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    created_at: Optional[datetime] = None
    created_by: Optional[uuid.UUID] = None
    

    class Config:
        orm_mode = True


class TaskUpdateBase(BaseModel):
    task_seq: Optional[int] = None
    task_name: str
    task_description: Optional[str] = None
    task_notes: Optional[str] = None
    estimated_duration: Optional[int] = None  # Could be str or timedelta depending on usage
    status: Optional[str] = 'pending'
    output_product: Optional[str] = None
    outputs_quantity: Optional[int] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[uuid.UUID] = None

    class Config:
        orm_mode = True

class TaskDisplay(BaseModel):  # what is displayed
  task_id: uuid.UUID
  batch_id: uuid.UUID
  task_seq: Optional[int] = None
  task_name: str
  task_description: Optional[str] = None
  task_notes: Optional[str] = None
  estimated_duration: Optional[int] = None  # Could be str or timedelta depending on usage
  status: Optional[str] = 'pending'
  output_product: Optional[str] = None
  outputs_quantity: Optional[int] = None
  start_time: Optional[str] = None
  end_time: Optional[str] = None
  created_at: Optional[datetime] = None
  created_by: Optional[uuid.UUID] = None
  updated_at: Optional[datetime] = None
  updated_by: Optional[uuid.UUID] = None

  class Config:
    orm_mode = True


class UserAuth(BaseModel):
  id: int
  username: str
  email: str




######### Task Assignee ###############

class TaskAssigneeBase(BaseModel):  # what is displayed
  task_id: Optional[uuid.UUID] = None
  user_id: Optional[uuid.UUID] = None
  assignee_id: Optional[uuid.UUID] = None

  class Config:
    orm_mode = True
    

class TaskAssigneeDisplay(BaseModel):  # what is displayed
  task_id: Optional[uuid.UUID] = None
  user_id: Optional[uuid.UUID] = None
  assignee_id: Optional[uuid.UUID] = None

  class Config:
    orm_mode = True
    
    
######### Task Dependency ###############
class TaskDependencyDisplay(BaseModel):  
  dependency_id: uuid.UUID
  seq_no: Optional[int] = None
  task_id_1: Optional[uuid.UUID] = None
  task_id_2: Optional[uuid.UUID] = None

  class Config:
    orm_mode = True
    

class TaskDependencyBase(BaseModel):  
  dependency_id: uuid.UUID
  seq_no: Optional[int] = None
  task_id_1: Optional[uuid.UUID] = None
  task_id_2: Optional[uuid.UUID] = None
  
  class Config:
    orm_mode = True
    

######### Task Incidence ###############
class TaskIncidentDisplay(BaseModel):  
  task_incident_id: uuid.UUID
  task_id: Optional[uuid.UUID] = None
  incident_id: Optional[uuid.UUID] = None
  
  class Config:
    orm_mode = True
    

class TaskIncidentBase(BaseModel):  
  task_incident_id: uuid.UUID
  task_id: Optional[uuid.UUID] = None
  incident_id: Optional[uuid.UUID] = None
  
  class Config:
    orm_mode = True
    
    
######### Task Machinery ###############
class TaskMachineryDisplay(BaseModel):  
  task_machinery_id: uuid.UUID
  task_id: Optional[uuid.UUID] = None
  machinery_id: Optional[uuid.UUID] = None
  
  class Config:
    orm_mode = True
    

class TaskMachineryBase(BaseModel):  
  task_machinery_id: uuid.UUID
  task_id: Optional[uuid.UUID] = None
  machinery_id: Optional[uuid.UUID] = None
  
  class Config:
    orm_mode = True
    
    
######### Task Raw Materials ###############
class TaskRawMaterialDisplay(BaseModel):  
  task_raw_material_id: uuid.UUID
  task_id: Optional[uuid.UUID] = None
  raw_material_id: Optional[uuid.UUID] = None
  assigned_quantity: Optional[int] = None
  
  class Config:
    orm_mode = True
    

class TaskRawMaterialBase(BaseModel):  
  task_raw_material_id: uuid.UUID
  task_id: Optional[uuid.UUID] = None
  raw_material_id: Optional[uuid.UUID] = None
  assigned_quantity: Optional[int] = None
  
  class Config:
    orm_mode = True
    
    
    
######### Machinery Table ###############
class MachineryDisplay(BaseModel):  
  machinery_id: uuid.UUID
  machine_name: str
  machine_type: Optional[str] = None
  machine_manufacture: Optional[str] = None
  location: Optional[str] = None
  status: Optional[str] = 'pending'
  capacity:Optional[str] = None
  power_rating: Optional[str] = None
  created_at: Optional[datetime] = None
  created_by: Optional[uuid.UUID] = None
  updated_at: Optional[datetime] = None
  updated_by: Optional[uuid.UUID] = None
  
  class Config:
    orm_mode = True
    

class MachineryBase(BaseModel):  
  machinery_id: uuid.UUID
  machine_name: str
  machine_type: Optional[str] = None
  machine_manufacture: Optional[str] = None
  location: Optional[str] = None
  status: Optional[str] = 'pending'
  capacity:Optional[str] = None
  power_rating: Optional[str] = None
  created_at: Optional[datetime] = None
  created_by: Optional[uuid.UUID] = None
  updated_at: Optional[datetime] = None
  updated_by: Optional[uuid.UUID] = None
  
  class Config:
    orm_mode = True
    
    

######### Incident Table ###############
class IncidentBase(BaseModel):
  incident_id: uuid.UUID
  task_incident_id: uuid.UUID
  incident_name: str
  incident_type: Optional[str] = None
  incident_video_id: Optional[uuid.UUID] = None
  incident_voice_id: Optional[uuid.UUID] = None
  incident_photo_id: Optional[uuid.UUID] = None
  incident_time: Optional[datetime] = None
  incident_notes: Optional[str] = None
  incident_severity: Optional[str] = 'pending'
  


class IncidentDisplay(BaseModel):
  incident_id: uuid.UUID
  task_incident_id: uuid.UUID
  incident_name: str
  incident_type: Optional[str] = None
  incident_video_id: Optional[uuid.UUID] = None
  incident_voice_id: Optional[uuid.UUID] = None
  incident_photo_id: Optional[uuid.UUID] = None
  incident_time: Optional[datetime] = None
  incident_notes: Optional[str] = None
  incident_severity: Optional[str] = 'pending'
