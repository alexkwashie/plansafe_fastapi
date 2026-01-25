from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import uuid


##### User Schema #####
class UserBase(BaseModel):
  username: str
  email: str

  class Config():
    orm_mode = True

class UserDisplay(BaseModel): # what is displayed to the user
  username: str
  firstname: str
  lastname: str
  email: str
  uid: uuid.UUID

  class Config:
    orm_mode = True


######### Batch Assignee ###############

class BatchAssigneeBase(BaseModel):  
  batch_id: Optional[uuid.UUID] = None
  user_id: Optional[uuid.UUID] = None
  batch_assignees_id: Optional[uuid.UUID] = None

  class Config:
    orm_mode = True
    

class BatchAssigneeDisplay(BaseModel):  # what is displayed
  batch_id: Optional[uuid.UUID] = None
  user_id: Optional[uuid.UUID] = None
  batch_assignees_id: Optional[uuid.UUID] = None

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
    batch_id: Optional[uuid.UUID] = None
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

    class Config():
      orm_mode = True

class TaskDisplay(BaseModel):  # what is displayed
  task_id: uuid.UUID
  batch_id: uuid.UUID
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

  class Config():
    orm_mode = True


class UserAuth(BaseModel):
  id: int
  username: str
  email: str




######### Task Assignee ###############

class TaskAssigneeBase(BaseModel):  # what is displayed
  task_id: Optional[uuid.UUID] = None
  user_id: Optional[uuid.UUID] = None
  assignees_id: Optional[uuid.UUID] = None

  class Config():
    orm_mode = True
    

class TaskAssigneeDisplay(BaseModel):  # what is displayed
  assignees_id: Optional[uuid.UUID] = None
  task_id: Optional[uuid.UUID] = None
  user_id: Optional[uuid.UUID] = None

  class Config():
    orm_mode = True
    

######### Task Incidence ###############
class TaskIncidentDisplay(BaseModel):  
  task_incident_id: uuid.UUID
  task_id: Optional[uuid.UUID] = None
  incident_id: Optional[uuid.UUID] = None
  
  class Config():
    orm_mode = True
    

class TaskIncidentBase(BaseModel):  
  task_incident_id: uuid.UUID
  task_id: Optional[uuid.UUID] = None
  incident_id: Optional[uuid.UUID] = None
  
  class Config():
    orm_mode = True
    
    
######### Task Machinery ###############
class TaskMachineryDisplay(BaseModel):  
  task_machinery_id: uuid.UUID
  task_id: Optional[uuid.UUID] = None
  machinery_id: Optional[uuid.UUID] = None
  
  class Config():
    orm_mode = True
    

class TaskMachineryBase(BaseModel):  
  task_machinery_id: uuid.UUID
  task_id: Optional[uuid.UUID] = None
  machinery_id: Optional[uuid.UUID] = None
  
  class Config():
    orm_mode = True
    
    
######### Task Raw Materials ###############
class TaskRawMaterialDisplay(BaseModel):  
  task_raw_material_id: uuid.UUID
  task_id: Optional[uuid.UUID] = None
  raw_material_id: Optional[uuid.UUID] = None
  assigned_quantity: Optional[int] = None
  
  class Config():
    orm_mode = True
    

class TaskRawMaterialBase(BaseModel):  
  task_raw_material_id: uuid.UUID
  task_id: Optional[uuid.UUID] = None
  raw_material_id: Optional[uuid.UUID] = None
  assigned_quantity: Optional[int] = None
  
  class Config():
    orm_mode = True
    
    
    
######### Machinery Table ###############
class MachineryDisplay(BaseModel):  
  machinery_id: uuid.UUID
  machine_name: str
  machine_type: Optional[str] = None
  machine_manufacture: Optional[str] = None
  location: Optional[str] = None
  status: Optional[str] = 'pending'
  capacity:Optional[int] = None
  power_rating: Optional[int] = None
  created_at: Optional[datetime] = None
  created_by: Optional[uuid.UUID] = None
  updated_at: Optional[datetime] = None
  updated_by: Optional[uuid.UUID] = None
  
  class Config():
    orm_mode = True
    

class MachineryBase(BaseModel):  
  machine_name: str
  machine_type: Optional[str] = None
  machine_manufacture: Optional[str] = None
  location: Optional[str] = None
  status: Optional[str] = 'pending'
  capacity:Optional[int] = None
  power_rating: Optional[int] = None
  created_at: Optional[datetime] = None
  created_by: Optional[uuid.UUID] = None

  class Config():
    orm_mode = True
    
    
class MachineryBaseUpdate(BaseModel):
  machine_name: str
  machine_type: Optional[str] = None
  machine_manufacture: Optional[str] = None
  location: Optional[str] = None
  status: Optional[str] = 'pending'
  capacity:Optional[int] = None
  power_rating: Optional[int] = None
  updated_at: Optional[datetime] = None
  updated_by: Optional[uuid.UUID] = None
  
  class Config():
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
  
  class Config():
    orm_mode = True 

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

  class Config():
    orm_mode = True
    
    

######### RawMaterial Table ###############
class RawMaterialBase(BaseModel):
  raw_material_id: uuid.UUID
  raw_material_name: str
  raw_material_code: Optional[str] = None
  quantity: int
  reorder_level:Optional[int] = None
  unit_cost:Optional[int] = None
  category: Optional[str] = None
  created_at: Optional[datetime] = None
  created_by: Optional[uuid.UUID] = None
  
  
  class Config():
    orm_mode = True 

class RawMaterialUpdate(BaseModel):
  raw_material_name: str
  raw_material_code: Optional[str] = None
  quantity: int
  reorder_level:Optional[int] = None
  unit_cost:Optional[int] = None
  category: Optional[str] = None
  updated_at: Optional[datetime] = None
  updated_by: Optional[uuid.UUID] = None
  
  
  class Config():
    orm_mode = True 
    
class RawMaterialDisplay(BaseModel):
  raw_material_id: uuid.UUID
  raw_material_name: str
  raw_material_code: Optional[str] = None
  quantity: int
  reorder_level:Optional[int] = None
  unit_cost:Optional[int] = None
  category: Optional[str] = None
  created_by: Optional[uuid.UUID] = None

  class Config():
    orm_mode = True