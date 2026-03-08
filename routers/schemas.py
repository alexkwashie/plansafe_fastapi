from pydantic import BaseModel
from datetime import date, datetime, time
from typing import List, Optional
from enum import Enum
import uuid


class BatchPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class MachineStatus(str, Enum):
    available = "available"
    in_use = "in_use"
    maintenance = "maintenance"
    out_of_service = "out_of_service"


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    paused = "paused"
    skipped = "skipped"


class IncidentSeverity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


##### User Schema #####
class UserBase(BaseModel):
  username: str
  email: str

  class Config():
    from_attributes = True

class UserDisplay(BaseModel):
  username: str
  firstname: str
  lastname: str
  email: str
  uid: uuid.UUID

  class Config:
    from_attributes = True


######### Batch Assignee ###############

class BatchAssigneeBase(BaseModel):
  batch_id: Optional[uuid.UUID] = None
  user_id: Optional[uuid.UUID] = None
  batch_assignees_id: Optional[uuid.UUID] = None

  class Config:
    from_attributes = True


class BatchAssigneeDisplay(BaseModel):
  batch_id: Optional[uuid.UUID] = None
  user_id: Optional[uuid.UUID] = None
  batch_assignees_id: Optional[uuid.UUID] = None

  class Config:
    from_attributes = True


##### Batch Schema #####
class BatchBase(BaseModel):
    batch_title: str
    batch_description: Optional[str] = None
    batch_status: str
    start_date: datetime
    start_time: Optional[time] = None
    end_date: datetime
    end_time: Optional[time] = None
    location: Optional[str] = None
    color: Optional[str] = None
    estimated_duration: Optional[int] = None
    process_duration: Optional[int] = None
    priority: Optional[BatchPriority] = BatchPriority.medium
    production_line: Optional[str] = None
    created_at: Optional[datetime] = None
    created_by: uuid.UUID

    class Config:
      from_attributes = True

class BatchBaseUpdate(BaseModel):
    batch_title: str
    batch_description: Optional[str] = None
    batch_status: str
    start_date: datetime
    start_time: Optional[time] = None
    end_date: datetime
    end_time: Optional[time] = None
    location: Optional[str] = None
    color: Optional[str] = None
    estimated_duration: Optional[int] = None
    process_duration: Optional[int] = None
    priority: Optional[BatchPriority] = None
    production_line: Optional[str] = None
    updated_by: uuid.UUID
    updated_at: Optional[datetime] = None

    class Config:
      from_attributes = True


class BatchDisplay(BaseModel):
    batch_id: Optional[uuid.UUID] = None
    batch_title: str
    batch_description: Optional[str] = None
    batch_status: str
    start_date: datetime
    start_time: Optional[time] = None
    end_date: datetime
    end_time: Optional[time] = None
    location: Optional[str] = None
    color: Optional[str] = None
    estimated_duration: Optional[int] = None
    process_duration: Optional[int] = None
    priority: Optional[str] = None
    production_line: Optional[str] = None
    created_at: Optional[datetime] = None
    created_by: uuid.UUID
    updated_at: Optional[datetime] = None
    updated_by: Optional[uuid.UUID] = None

    class Config:
      from_attributes = True


##### Task Schema #####
class TaskBase(BaseModel):
    batch_id: uuid.UUID
    task_name: str
    task_description: Optional[str] = None
    task_notes: Optional[str] = None
    estimated_duration: Optional[int] = None
    status: Optional[TaskStatus] = TaskStatus.pending
    output_product: Optional[str] = None
    outputs_quantity: Optional[int] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    sequence_order: Optional[int] = None
    depends_on_task_id: Optional[uuid.UUID] = None
    sop_document_url: Optional[str] = None
    created_at: Optional[datetime] = None
    created_by: Optional[uuid.UUID] = None

    class Config:
      from_attributes = True


class TaskUpdateBase(BaseModel):
    task_name: str
    task_description: Optional[str] = None
    task_notes: Optional[str] = None
    estimated_duration: Optional[int] = None
    status: Optional[TaskStatus] = TaskStatus.pending
    output_product: Optional[str] = None
    outputs_quantity: Optional[int] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    sequence_order: Optional[int] = None
    depends_on_task_id: Optional[uuid.UUID] = None
    sop_document_url: Optional[str] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[uuid.UUID] = None

    class Config():
      from_attributes = True

class TaskDisplay(BaseModel):
  task_id: uuid.UUID
  batch_id: uuid.UUID
  task_name: str
  task_description: Optional[str] = None
  task_notes: Optional[str] = None
  estimated_duration: Optional[int] = None
  status: Optional[str] = 'pending'
  output_product: Optional[str] = None
  outputs_quantity: Optional[int] = None
  start_time: Optional[time] = None
  end_time: Optional[time] = None
  sequence_order: Optional[int] = None
  depends_on_task_id: Optional[uuid.UUID] = None
  sop_document_url: Optional[str] = None
  created_at: Optional[datetime] = None
  created_by: Optional[uuid.UUID] = None
  updated_at: Optional[datetime] = None
  updated_by: Optional[uuid.UUID] = None

  class Config():
    from_attributes = True


class UserAuth(BaseModel):
  id: int
  username: str
  email: str


######### Task Assignee ###############

class TaskAssigneeBase(BaseModel):
  task_id: Optional[uuid.UUID] = None
  user_id: Optional[uuid.UUID] = None
  assignees_id: Optional[uuid.UUID] = None

  class Config():
    from_attributes = True


class TaskAssigneeDisplay(BaseModel):
  assignees_id: Optional[uuid.UUID] = None
  task_id: Optional[uuid.UUID] = None
  user_id: Optional[uuid.UUID] = None

  class Config():
    from_attributes = True


######### Task Incidence ###############
class TaskIncidentDisplay(BaseModel):
  task_incident_id: uuid.UUID
  task_id: Optional[uuid.UUID] = None
  incident_id: Optional[uuid.UUID] = None

  class Config():
    from_attributes = True


class TaskIncidentBase(BaseModel):
  task_incident_id: uuid.UUID
  task_id: Optional[uuid.UUID] = None
  incident_id: Optional[uuid.UUID] = None

  class Config():
    from_attributes = True


######### Task Machinery ###############
class TaskMachineryDisplay(BaseModel):
  task_machinery_id: uuid.UUID
  task_id: Optional[uuid.UUID] = None
  machinery_id: Optional[uuid.UUID] = None

  class Config():
    from_attributes = True


class TaskMachineryBase(BaseModel):
  task_machinery_id: uuid.UUID
  task_id: Optional[uuid.UUID] = None
  machinery_id: Optional[uuid.UUID] = None

  class Config():
    from_attributes = True


######### Task Raw Materials ###############
class TaskRawMaterialDisplay(BaseModel):
  task_raw_material_id: uuid.UUID
  task_id: Optional[uuid.UUID] = None
  raw_material_id: Optional[uuid.UUID] = None
  assigned_quantity: Optional[int] = None

  class Config():
    from_attributes = True


class TaskRawMaterialBase(BaseModel):
  task_raw_material_id: uuid.UUID
  task_id: Optional[uuid.UUID] = None
  raw_material_id: Optional[uuid.UUID] = None
  assigned_quantity: Optional[int] = None

  class Config():
    from_attributes = True


######### Machinery Table ###############
class MachineryDisplay(BaseModel):
  machinery_id: uuid.UUID
  machine_name: str
  machine_type: Optional[str] = None
  machine_manufacture: Optional[str] = None
  location: Optional[str] = None
  status: Optional[str] = 'available'
  capacity: Optional[int] = None
  power_rating: Optional[int] = None
  serial_number: Optional[str] = None
  purchase_date: Optional[date] = None
  warranty_expiry: Optional[date] = None
  photo_url: Optional[str] = None
  notes: Optional[str] = None
  created_at: Optional[datetime] = None
  created_by: Optional[uuid.UUID] = None
  updated_at: Optional[datetime] = None
  updated_by: Optional[uuid.UUID] = None

  class Config():
    from_attributes = True


class MachineryBase(BaseModel):
  machine_name: str
  machine_type: Optional[str] = None
  machine_manufacture: Optional[str] = None
  location: Optional[str] = None
  status: Optional[MachineStatus] = MachineStatus.available
  capacity: Optional[int] = None
  power_rating: Optional[int] = None
  serial_number: Optional[str] = None
  purchase_date: Optional[date] = None
  warranty_expiry: Optional[date] = None
  photo_url: Optional[str] = None
  notes: Optional[str] = None
  created_at: Optional[datetime] = None
  created_by: Optional[uuid.UUID] = None

  class Config():
    from_attributes = True


class MachineryBaseUpdate(BaseModel):
  machine_name: str
  machine_type: Optional[str] = None
  machine_manufacture: Optional[str] = None
  location: Optional[str] = None
  status: Optional[MachineStatus] = MachineStatus.available
  capacity: Optional[int] = None
  power_rating: Optional[int] = None
  serial_number: Optional[str] = None
  purchase_date: Optional[date] = None
  warranty_expiry: Optional[date] = None
  photo_url: Optional[str] = None
  notes: Optional[str] = None
  updated_at: Optional[datetime] = None
  updated_by: Optional[uuid.UUID] = None

  class Config():
    from_attributes = True


######### Incident Table ###############
class IncidentBase(BaseModel):
  incident_name: str
  incident_type: Optional[str] = None
  incident_video_id: Optional[uuid.UUID] = None
  incident_voice_id: Optional[uuid.UUID] = None
  incident_photo_id: Optional[uuid.UUID] = None
  incident_time: Optional[datetime] = None
  incident_notes: Optional[str] = None
  incident_severity: Optional[IncidentSeverity] = None
  location: Optional[str] = None
  personnel_involved: Optional[str] = None
  immediate_actions: Optional[str] = None
  witness_info: Optional[str] = None
  is_anonymous: Optional[bool] = False
  # OSHA fields
  employee_name: Optional[str] = None
  job_title_at_time: Optional[str] = None
  date_of_injury: Optional[date] = None
  injury_description: Optional[str] = None
  body_part_affected: Optional[str] = None
  injury_type: Optional[str] = None
  days_away: Optional[int] = 0
  days_restricted: Optional[int] = 0
  death: Optional[bool] = False
  treated_in_er: Optional[bool] = False
  hospitalized: Optional[bool] = False

  class Config():
    from_attributes = True

class IncidentUpdate(BaseModel):
  incident_name: Optional[str] = None
  incident_type: Optional[str] = None
  incident_video_id: Optional[uuid.UUID] = None
  incident_voice_id: Optional[uuid.UUID] = None
  incident_photo_id: Optional[uuid.UUID] = None
  incident_time: Optional[datetime] = None
  incident_notes: Optional[str] = None
  incident_severity: Optional[IncidentSeverity] = None
  location: Optional[str] = None
  personnel_involved: Optional[str] = None
  immediate_actions: Optional[str] = None
  witness_info: Optional[str] = None
  is_anonymous: Optional[bool] = None
  # OSHA fields
  employee_name: Optional[str] = None
  job_title_at_time: Optional[str] = None
  date_of_injury: Optional[date] = None
  injury_description: Optional[str] = None
  body_part_affected: Optional[str] = None
  injury_type: Optional[str] = None
  days_away: Optional[int] = None
  days_restricted: Optional[int] = None
  death: Optional[bool] = None
  treated_in_er: Optional[bool] = None
  hospitalized: Optional[bool] = None

  class Config():
    from_attributes = True

class IncidentDisplay(BaseModel):
  incident_id: uuid.UUID
  task_incident_id: Optional[uuid.UUID] = None
  incident_name: str
  incident_type: Optional[str] = None
  incident_video_id: Optional[uuid.UUID] = None
  incident_voice_id: Optional[uuid.UUID] = None
  incident_photo_id: Optional[uuid.UUID] = None
  incident_time: Optional[datetime] = None
  incident_notes: Optional[str] = None
  incident_severity: Optional[str] = None
  incident_created_by: Optional[uuid.UUID] = None
  incident_created_at: Optional[datetime] = None
  location: Optional[str] = None
  personnel_involved: Optional[str] = None
  immediate_actions: Optional[str] = None
  witness_info: Optional[str] = None
  is_anonymous: Optional[bool] = False
  # OSHA fields
  employee_name: Optional[str] = None
  job_title_at_time: Optional[str] = None
  date_of_injury: Optional[date] = None
  injury_description: Optional[str] = None
  body_part_affected: Optional[str] = None
  injury_type: Optional[str] = None
  days_away: Optional[int] = 0
  days_restricted: Optional[int] = 0
  death: Optional[bool] = False
  treated_in_er: Optional[bool] = False
  hospitalized: Optional[bool] = False

  class Config():
    from_attributes = True


######### RawMaterial Table ###############
class RawMaterialBase(BaseModel):
  raw_material_name: str
  raw_material_code: Optional[str] = None
  quantity: int
  reorder_level: Optional[int] = None
  unit_cost: Optional[int] = None
  category: Optional[str] = None
  supplier: Optional[str] = None
  unit_of_measure: Optional[str] = None
  lot_number: Optional[str] = None
  created_at: Optional[datetime] = None
  created_by: Optional[uuid.UUID] = None

  class Config():
    from_attributes = True

class RawMaterialUpdate(BaseModel):
  raw_material_name: str
  raw_material_code: Optional[str] = None
  quantity: int
  reorder_level: Optional[int] = None
  unit_cost: Optional[int] = None
  category: Optional[str] = None
  supplier: Optional[str] = None
  unit_of_measure: Optional[str] = None
  lot_number: Optional[str] = None
  updated_at: Optional[datetime] = None
  updated_by: Optional[uuid.UUID] = None

  class Config():
    from_attributes = True

class RawMaterialDisplay(BaseModel):
  raw_material_id: uuid.UUID
  raw_material_name: str
  raw_material_code: Optional[str] = None
  quantity: int
  reorder_level: Optional[int] = None
  unit_cost: Optional[int] = None
  category: Optional[str] = None
  supplier: Optional[str] = None
  unit_of_measure: Optional[str] = None
  lot_number: Optional[str] = None
  created_at: Optional[datetime] = None
  created_by: Optional[uuid.UUID] = None
  updated_at: Optional[datetime] = None
  updated_by: Optional[uuid.UUID] = None

  class Config():
    from_attributes = True


######### Notes ###############
class NoteEntityType(str, Enum):
    batch = "batch"
    task = "task"
    equipment = "equipment"
    incident = "incident"


class NoteType(str, Enum):
    general = "general"
    safety_concern = "safety_concern"
    quality_issue = "quality_issue"
    process_deviation = "process_deviation"
    handover = "handover"


class NoteBase(BaseModel):
    note_type: Optional[NoteType] = NoteType.general
    content: str
    photo_url: Optional[str] = None

    class Config():
        from_attributes = True


class NoteUpdate(BaseModel):
    note_type: Optional[NoteType] = None
    content: Optional[str] = None
    photo_url: Optional[str] = None

    class Config():
        from_attributes = True


class NoteDisplay(BaseModel):
    note_id: uuid.UUID
    entity_type: str
    entity_id: uuid.UUID
    note_type: Optional[str] = None
    content: str
    photo_url: Optional[str] = None
    created_by: Optional[uuid.UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config():
        from_attributes = True


######### Dashboard ###############
class EquipmentStatusBreakdown(BaseModel):
    available: int = 0
    in_use: int = 0
    maintenance: int = 0
    out_of_service: int = 0

    class Config():
        from_attributes = True


class DashboardSummary(BaseModel):
    active_batch_count: int = 0
    overdue_task_count: int = 0
    recent_incident_count: int = 0
    equipment_status: EquipmentStatusBreakdown = EquipmentStatusBreakdown()

    class Config():
        from_attributes = True


class ActiveBatchSummary(BaseModel):
    batch_id: uuid.UUID
    batch_title: str
    batch_status: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    priority: Optional[str] = None
    total_tasks: int = 0
    completed_tasks: int = 0
    completion_percentage: float = 0.0

    class Config():
        from_attributes = True


class OverdueTask(BaseModel):
    task_id: uuid.UUID
    batch_id: uuid.UUID
    task_name: str
    status: Optional[str] = None
    end_time: Optional[str] = None
    sequence_order: Optional[int] = None

    class Config():
        from_attributes = True


######### Notifications ###############
class NotificationDisplay(BaseModel):
    notification_id: uuid.UUID
    user_id: Optional[uuid.UUID] = None
    type: str
    entity_type: Optional[str] = None
    entity_id: Optional[uuid.UUID] = None
    message: str
    read: bool = False
    created_at: Optional[datetime] = None

    class Config():
        from_attributes = True


######### Investigations ###############
class InvestigationStatusEnum(str, Enum):
    open = "open"
    in_progress = "in_progress"
    closed = "closed"


class InvestigationTypeEnum(str, Enum):
    five_why = "five_why"
    fishbone = "fishbone"
    root_cause = "root_cause"


class InvestigationBase(BaseModel):
    assigned_to: Optional[uuid.UUID] = None
    investigation_type: Optional[InvestigationTypeEnum] = None
    findings: Optional[str] = None
    root_cause: Optional[str] = None

    class Config():
        from_attributes = True


class InvestigationUpdate(BaseModel):
    assigned_to: Optional[uuid.UUID] = None
    status: Optional[InvestigationStatusEnum] = None
    investigation_type: Optional[InvestigationTypeEnum] = None
    findings: Optional[str] = None
    root_cause: Optional[str] = None

    class Config():
        from_attributes = True


class InvestigationDisplay(BaseModel):
    investigation_id: uuid.UUID
    incident_id: uuid.UUID
    assigned_to: Optional[uuid.UUID] = None
    status: Optional[str] = None
    investigation_type: Optional[str] = None
    findings: Optional[str] = None
    root_cause: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None

    class Config():
        from_attributes = True


######### CAPA Actions ###############
class CAPAActionTypeEnum(str, Enum):
    corrective = "corrective"
    preventive = "preventive"


class CAPAStatusEnum(str, Enum):
    open = "open"
    in_progress = "in_progress"
    completed = "completed"
    overdue = "overdue"


class CAPABase(BaseModel):
    action_type: CAPAActionTypeEnum
    description: str
    assigned_to: Optional[uuid.UUID] = None
    due_date: Optional[date] = None

    class Config():
        from_attributes = True


class CAPAUpdate(BaseModel):
    action_type: Optional[CAPAActionTypeEnum] = None
    description: Optional[str] = None
    assigned_to: Optional[uuid.UUID] = None
    due_date: Optional[date] = None
    status: Optional[CAPAStatusEnum] = None

    class Config():
        from_attributes = True


class CAPADisplay(BaseModel):
    capa_id: uuid.UUID
    investigation_id: uuid.UUID
    action_type: Optional[str] = None
    description: str
    assigned_to: Optional[uuid.UUID] = None
    due_date: Optional[date] = None
    status: Optional[str] = None
    completed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config():
        from_attributes = True


######### Checklist Templates ###############
class ChecklistTypeEnum(str, Enum):
    pre_shift = "pre_shift"
    equipment = "equipment"
    area = "area"


class ChecklistTemplateBase(BaseModel):
    name: str
    type: ChecklistTypeEnum = ChecklistTypeEnum.pre_shift

    class Config():
        from_attributes = True


class ChecklistTemplateUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[ChecklistTypeEnum] = None

    class Config():
        from_attributes = True


class ChecklistTemplateDisplay(BaseModel):
    template_id: uuid.UUID
    name: str
    type: Optional[str] = None
    created_by: Optional[uuid.UUID] = None
    created_at: Optional[datetime] = None

    class Config():
        from_attributes = True


class TemplateItemBase(BaseModel):
    item_text: str
    sort_order: Optional[int] = 0
    required: Optional[bool] = True

    class Config():
        from_attributes = True


class TemplateItemDisplay(BaseModel):
    item_id: uuid.UUID
    template_id: uuid.UUID
    item_text: str
    sort_order: Optional[int] = 0
    required: Optional[bool] = True
    created_at: Optional[datetime] = None

    class Config():
        from_attributes = True


######### Inspections ###############
class InspectionStatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class InspectionResponseValueEnum(str, Enum):
    pass_val = "pass"
    fail = "fail"
    na = "na"


class InspectionBase(BaseModel):
    template_id: uuid.UUID
    inspector_id: Optional[uuid.UUID] = None
    scheduled_date: Optional[date] = None
    notes: Optional[str] = None

    class Config():
        from_attributes = True


class InspectionUpdate(BaseModel):
    status: Optional[InspectionStatusEnum] = None
    scheduled_date: Optional[date] = None
    notes: Optional[str] = None

    class Config():
        from_attributes = True


class InspectionDisplay(BaseModel):
    inspection_id: uuid.UUID
    template_id: uuid.UUID
    inspector_id: Optional[uuid.UUID] = None
    status: Optional[str] = None
    scheduled_date: Optional[date] = None
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config():
        from_attributes = True


class InspectionResponseBase(BaseModel):
    template_item_id: uuid.UUID
    response: InspectionResponseValueEnum
    notes: Optional[str] = None
    photo_url: Optional[str] = None

    class Config():
        from_attributes = True


class InspectionResponseDisplay(BaseModel):
    response_id: uuid.UUID
    inspection_id: uuid.UUID
    template_item_id: uuid.UUID
    response: Optional[str] = None
    notes: Optional[str] = None
    photo_url: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config():
        from_attributes = True


######### Shift Handovers ###############
class ShiftHandoverBase(BaseModel):
    incoming_user_id: Optional[uuid.UUID] = None
    shift_date: date
    batch_status_summary: Optional[str] = None
    outstanding_issues: Optional[str] = None
    tasks_completed: Optional[str] = None
    tasks_remaining: Optional[str] = None
    equipment_notes: Optional[str] = None
    incidents_occurred: Optional[str] = None

    class Config():
        from_attributes = True


class ShiftHandoverDisplay(BaseModel):
    handover_id: uuid.UUID
    outgoing_user_id: Optional[uuid.UUID] = None
    incoming_user_id: Optional[uuid.UUID] = None
    shift_date: Optional[date] = None
    batch_status_summary: Optional[str] = None
    outstanding_issues: Optional[str] = None
    tasks_completed: Optional[str] = None
    tasks_remaining: Optional[str] = None
    equipment_notes: Optional[str] = None
    incidents_occurred: Optional[str] = None
    acknowledged: Optional[bool] = False
    acknowledged_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config():
        from_attributes = True


##### Auth Schemas #####
class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    username: str
    firstname: Optional[str] = None
    lastname: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: str
    email: str

class RefreshRequest(BaseModel):
    refresh_token: str
