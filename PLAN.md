# PLAN.md — PlanSafe360 Phase 1 & Phase 2 Implementation

## Context

PlanSafe360 is a manufacturing process & safety management SaaS. The backend has ~25% of Phase 1 built (basic CRUD for batches, tasks, assignments, machinery, raw materials, incidents) but with significant gaps: no auth on routes, no API versioning, no pagination, no notes system, no dashboards, no notifications, and several bugs. Phase 2 (safety workflows, reporting, OSHA logs) is 0% built.

**Decisions made:**
- Refactor all existing routes to `/api/v1/` with RESTful naming, pagination, and async handlers
- Keep logic in `db/` modules (no services layer)
- Skip multi-tenancy for now — defer `company_id` and RLS to a later phase
- Fix existing bugs as a prerequisite chunk before feature work

---

## Chunk 0: Codebase Cleanup & Bug Fixes

**Goal:** Fix known bugs, remove dead code, consolidate Supabase client usage.

### 0.1 — Consolidate Supabase client
- Make `db/supabase_client.py` the single shared client instance
- Update all `db/` modules to import from `db/supabase_client.py` instead of calling `create_client()` independently
- Remove `db/client_connection.py` (duplicate)
- Files to modify: `db/supabase_client.py`, `db/db_user.py`, `db/db_production_planning/db_batch.py`, `db/db_production_planning/db_task.py`, `db/db_production_planning/db_task_assignee.py`, `db/db_production_planning/db_batch_assignee.py`, `db/db_production_planning/db_task_machinery.py`, `db/db_production_planning/db_task_raw_materials.py`, `db/db_raw_materials/db_raw_material.py`, `db/db_machinery_equipement/db_machinery_equipement.py`, `db/db_incident/db_incident.py`

### 0.2 — Fix broken endpoints
- **`routers/users.py`**: Fix `PUT /user/{id}` — path param `id` doesn't match function param `uid`. Change to consistent naming
- **`db/db_production_planning/db_task_raw_materials.py`**: Fix `create_task_raw_material` — accesses `raw_material_item.material_name` on a Supabase response object (AttributeError)
- **`routers/incident.py`**: Fix `IncidentBase` schema — `incident_id` and `task_incident_id` should not be required on create (IDs are server-generated)
- **`routers/schemas.py`**: Fix `RawMaterialBase` — `raw_material_id` should not be required on create

### 0.3 — Remove dead code
- Delete `routers/machinery.py` (old, unregistered, imports deleted `db/db_machinery`)
- Delete `dependencies/getToken.py` (unused JWKS verifier)
- Clean up any orphaned `__pycache__` directories

### Verification
- Run `uvicorn main:app --reload` — app starts without import errors or warnings
- Hit each existing endpoint via Swagger docs to confirm no runtime errors

---

## Chunk 1: Route Refactoring & API Conventions

**Goal:** Migrate all existing endpoints to `/api/v1/` prefix, RESTful naming, pagination support, consistent response format, and async handlers.

### 1.1 — Create shared utilities
- Create `routers/pagination.py`: pagination dependency (`page`, `per_page` query params with defaults)
- Create `routers/response.py`: response envelope helper `{ "data": ..., "meta": { "page", "per_page", "total" } }` for list endpoints

### 1.2 — Refactor route naming & versioning
All routers get `prefix="/api/v1/..."` and RESTful naming:

| Current | New |
|---------|-----|
| `/batch/create-batch` | `POST /api/v1/batches` |
| `/batch/all` | `GET /api/v1/batches` |
| `/batch/update/{id}` | `PUT /api/v1/batches/{batch_id}` |
| `/batch/delete/{id}` | `DELETE /api/v1/batches/{batch_id}` |
| `/task/create-task/{batch_id}` | `POST /api/v1/batches/{batch_id}/tasks` |
| `/task/all/{batch_id}` | `GET /api/v1/batches/{batch_id}/tasks` |
| `/task/update/{id}` | `PUT /api/v1/tasks/{task_id}` |
| `/task/delete/{id}` | `DELETE /api/v1/tasks/{task_id}` |
| `/batch-assignee/add/...` | `POST /api/v1/batches/{batch_id}/assignees` |
| `/batch-assignee/all/{batch_id}` | `GET /api/v1/batches/{batch_id}/assignees` |
| `/batch-assignee/delete/...` | `DELETE /api/v1/batch-assignees/{assignee_id}` |
| `/task-assignee/add/...` | `POST /api/v1/tasks/{task_id}/assignees` |
| `/task-assignee/all/{task_id}` | `GET /api/v1/tasks/{task_id}/assignees` |
| `/task-assignee/delete/...` | `DELETE /api/v1/task-assignees/{assignee_id}` |
| `/task-machinery/add/...` | `POST /api/v1/tasks/{task_id}/machinery` |
| `/task-machinery/all/{task_id}` | `GET /api/v1/tasks/{task_id}/machinery` |
| `/task-machinery/delete/...` | `DELETE /api/v1/task-machinery/{id}` |
| `/task-raw-materials/create/...` | `POST /api/v1/tasks/{task_id}/raw-materials` |
| `/task-raw-materials/all/{task_id}` | `GET /api/v1/tasks/{task_id}/raw-materials` |
| `/task-raw-materials/delete/...` | `DELETE /api/v1/task-raw-materials/{id}` |
| `/machinery/create-machinery` | `POST /api/v1/machinery` |
| `/machinery/all` | `GET /api/v1/machinery` |
| `/machinery/update/{id}` | `PUT /api/v1/machinery/{machinery_id}` |
| `/machinery/delete/{id}` | `DELETE /api/v1/machinery/{machinery_id}` |
| `/raw-material/create-raw-material` | `POST /api/v1/raw-materials` |
| `/raw-material/all-raw-material` | `GET /api/v1/raw-materials` |
| `/raw-material/update/{id}` | `PUT /api/v1/raw-materials/{raw_material_id}` |
| `/raw-material/delete/{id}` | `DELETE /api/v1/raw-materials/{raw_material_id}` |
| `/incidents/create/{task_id}` | `POST /api/v1/tasks/{task_id}/incidents` |
| `/incidents/all/{task_id}` | `GET /api/v1/tasks/{task_id}/incidents` |
| `/incidents/delete/{id}` | `DELETE /api/v1/incidents/{incident_id}` |
| `/user/all-users/` | `GET /api/v1/users` |
| `/user/{id}` | `GET /api/v1/users/{user_id}` |

### 1.3 — Add missing single-record GET endpoints
- `GET /api/v1/batches/{batch_id}`
- `GET /api/v1/tasks/{task_id}`
- `GET /api/v1/machinery/{machinery_id}`
- `GET /api/v1/raw-materials/{raw_material_id}`
- `GET /api/v1/incidents/{incident_id}`

### 1.4 — Add pagination to all list endpoints
- Apply pagination dependency to all `GET` list routes
- Update `db/` modules to accept `offset` and `limit` params, use `.range()` on Supabase queries
- Return paginated envelope response

### 1.5 — Convert all route handlers to async
- Change `def` to `async def` on all route handlers
- Files: all router files

### Verification
- Run app — all routes show in Swagger under `/api/v1/`
- Test pagination params on list endpoints
- Confirm single-record GETs return correct data

---

## Chunk 2: Authentication

**Goal:** Wire real JWT auth into all routes using existing `dependencies/auth_token.py`.

### 2.1 — Create auth routes
- Create `routers/auth.py` with:
  - `POST /api/v1/auth/login` — accepts email+password, calls Supabase `auth.sign_in_with_password()`, returns JWT tokens
  - `POST /api/v1/auth/register` — accepts email+password+name, calls Supabase `auth.sign_up()`, returns user
  - `POST /api/v1/auth/logout` — calls Supabase `auth.sign_out()`
  - `POST /api/v1/auth/refresh` — refreshes JWT token
- Add auth schemas to `routers/schemas.py`: `LoginRequest`, `RegisterRequest`, `TokenResponse`

### 2.2 — Wire auth dependency into all routes
- Replace `Depends(verify_token)` with `Depends(get_current_user)` from `auth_token.py` on all protected routes
- Add `Depends(get_current_user)` to routes that currently have no auth
- Keep `GET /` and auth routes public
- Files: all router files, `dependencies/auth_token.py`

### 2.3 — Add current user context
- Update `get_current_user` to return a user dict with `user_id`, `email`, `role`
- Pass current user into db functions for `created_by`/`updated_by` fields (replace hardcoded values)

### Verification
- Attempt to call any protected endpoint without token → 401
- Login → get token → call protected endpoint → 200
- Confirm `created_by` / `updated_by` fields populate with actual user ID

---

## Chunk 3: Enrich Existing Resources

**Goal:** Add missing fields and capabilities to existing resources per SPEC.

### 3.1 — Enrich equipment/machinery schema
- Add fields: `serial_number`, `purchase_date`, `warranty_expiry`, `photo_url`, `notes`
- Update `MachineryBase`, `MachineryBaseUpdate`, `MachineryDisplay` in `schemas.py`
- Update `db_machinery_equipement.py` CRUD functions
- Add status enum validation: `Operational`, `In Use`, `Maintenance Scheduled`, `Under Maintenance`, `Out of Service`

### 3.2 — Enrich batch schema
- Add fields: `priority` (enum: low/medium/high/critical), `production_line`
- Update `BatchBase`, `BatchBaseUpdate`, `BatchDisplay` in `schemas.py`
- Update `db_batch.py`

### 3.3 — Enrich task schema
- Add fields: `sequence_order` (int), `depends_on_task_id` (optional UUID), `sop_document_url`
- Add status enum: `Not Started`, `In Progress`, `Paused`, `Completed`, `Skipped`
- Update schemas and `db_task.py`

### 3.4 — Enrich incident schema
- Add fields: `location`, `personnel_involved`, `immediate_actions`, `witness_info`, `is_anonymous`
- Remove `incident_id` and `task_incident_id` from `IncidentBase` (server-generated)
- Add `PUT /api/v1/incidents/{incident_id}` update endpoint
- Add `GET /api/v1/incidents` (global list, not scoped to task)
- Update schemas, router, and db module

### 3.5 — Enrich raw materials schema
- Remove `raw_material_id` from `RawMaterialBase` (server-generated)
- Add fields: `supplier`, `unit_of_measure`, `lot_number`
- Update schemas and db module

### Verification
- Create records with new fields via Swagger → confirm stored and returned correctly
- Confirm enum fields reject invalid values

---

## Chunk 4: Notes System

**Goal:** Build a dedicated notes system that can attach to batches, tasks, equipment, and incidents.

### 4.1 — Create notes module
- Supabase table: `notes` with columns: `id`, `entity_type` (enum: batch/task/equipment/incident), `entity_id` (UUID), `note_type` (enum: general/safety_concern/quality_issue/process_deviation/handover), `content` (text), `photo_url` (optional), `created_by`, `created_at`, `updated_at`
- Create `routers/schemas.py` additions: `NoteBase`, `NoteDisplay`, `NoteUpdate`
- Create `db/db_notes/db_note.py` with CRUD
- Create `db/db_notes/__init__.py`

### 4.2 — Create notes routes
- Create `routers/notes.py`:
  - `POST /api/v1/{entity_type}/{entity_id}/notes` — create note
  - `GET /api/v1/{entity_type}/{entity_id}/notes` — list notes for entity (paginated)
  - `GET /api/v1/notes/{note_id}` — get single note
  - `PUT /api/v1/notes/{note_id}` — update note
  - `DELETE /api/v1/notes/{note_id}` — delete note
- Register router in `main.py`

### 4.3 — File upload for note photos
- Add Supabase Storage integration utility in `db/storage.py`
- Add `POST /api/v1/upload` endpoint for file uploads → returns storage URL
- Notes reference the uploaded photo URL

### Verification
- Create notes on different entity types → confirm returned correctly
- Upload a photo → attach to note → confirm URL stored
- List notes for a batch/task → paginated response

---

## Chunk 5: Dashboard Endpoints

**Goal:** Provide summary/aggregation endpoints for the basic dashboard.

### 5.1 — Create dashboard module
- Create `routers/dashboard.py`:
  - `GET /api/v1/dashboard/summary` — returns active batch count, overdue task count, recent incident count, equipment status breakdown
  - `GET /api/v1/dashboard/active-batches` — batches with status "In Progress", with task completion percentage
  - `GET /api/v1/dashboard/overdue-tasks` — tasks past their `end_time` that aren't completed
  - `GET /api/v1/dashboard/recent-incidents` — last 10 incidents
- Create `db/db_dashboard.py` with aggregation queries
- Add dashboard schemas to `schemas.py`: `DashboardSummary`, `ActiveBatchSummary`, `OverdueTask`

### Verification
- Create test data (batches, tasks, incidents) → hit dashboard endpoints → confirm correct counts and data

---

## Chunk 6: Email Notifications

**Goal:** Send email notifications on task assignment and incident creation.

### 6.1 — Email infrastructure
- Add `fastapi-mail` to `requirements.txt`
- Create `notifications/email.py` with email sending utility using SMTP config from env vars
- Add env vars: `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `EMAIL_FROM`

### 6.2 — Notification triggers
- In task assignee creation: send email to assigned user
- In incident creation: send email to configured safety officer email(s)
- Use FastAPI `BackgroundTasks` to send emails asynchronously (non-blocking)

### 6.3 — Notification preferences (basic)
- Create `notifications` table: `id`, `user_id`, `type`, `entity_type`, `entity_id`, `message`, `read`, `created_at`
- `GET /api/v1/notifications` — list notifications for current user
- `PUT /api/v1/notifications/{id}/read` — mark as read

### Verification
- Assign a task → check email received (or check notification record created)
- Create an incident → check notification sent

---

## Chunk 7: Investigation Workflow & CAPA (Phase 2)

**Goal:** Build the incident investigation and corrective action tracking system.

### 7.1 — Investigation model
- Supabase table: `investigations` — `id`, `incident_id`, `assigned_to`, `status` (open/in_progress/closed), `investigation_type` (five_why/fishbone/root_cause), `findings`, `root_cause`, `created_at`, `updated_at`, `closed_at`
- Schemas: `InvestigationBase`, `InvestigationUpdate`, `InvestigationDisplay`
- CRUD in `db/db_investigations/db_investigation.py`

### 7.2 — CAPA tracking
- Supabase table: `capa_actions` — `id`, `investigation_id`, `action_type` (corrective/preventive), `description`, `assigned_to`, `due_date`, `status` (open/in_progress/completed/overdue), `completed_at`, `created_at`
- Schemas and CRUD
- Routes:
  - `POST /api/v1/investigations/{id}/capa-actions`
  - `GET /api/v1/investigations/{id}/capa-actions`
  - `PUT /api/v1/capa-actions/{id}`
  - `DELETE /api/v1/capa-actions/{id}`

### 7.3 — Investigation routes
- `POST /api/v1/incidents/{incident_id}/investigations`
- `GET /api/v1/incidents/{incident_id}/investigations`
- `GET /api/v1/investigations/{id}`
- `PUT /api/v1/investigations/{id}`

### Verification
- Create incident → create investigation → add CAPA actions → update statuses → confirm full workflow

---

## Chunk 8: Safety Checklists & Inspections (Phase 2)

**Goal:** Configurable inspection templates and scheduled inspections.

### 8.1 — Checklist templates
- Supabase table: `checklist_templates` — `id`, `name`, `type` (pre_shift/equipment/area), `created_by`, `created_at`
- Supabase table: `checklist_template_items` — `id`, `template_id`, `item_text`, `order`, `required`
- Schemas and CRUD
- Routes: CRUD under `/api/v1/checklist-templates`

### 8.2 — Inspections
- Supabase table: `inspections` — `id`, `template_id`, `inspector_id`, `status` (pending/in_progress/completed), `scheduled_date`, `completed_at`, `notes`, `created_at`
- Supabase table: `inspection_responses` — `id`, `inspection_id`, `template_item_id`, `response` (pass/fail/na), `notes`, `photo_url`
- Schemas and CRUD
- Routes:
  - `POST /api/v1/inspections` — schedule an inspection
  - `GET /api/v1/inspections` — list (filterable by status, date range)
  - `GET /api/v1/inspections/{id}` — get with responses
  - `PUT /api/v1/inspections/{id}` — update
  - `POST /api/v1/inspections/{id}/responses` — submit checklist responses
- Non-conformance items auto-create follow-up tasks

### Verification
- Create template → schedule inspection → submit responses → confirm non-conformance generates follow-up task

---

## Chunk 9: OSHA Log Generation (Phase 2)

**Goal:** Auto-generate OSHA 300, 300A, and 301 logs from incident data.

### 9.1 — OSHA data mapping
- Map incident fields to OSHA 300 columns (case number, employee name, job title, date of injury, description, days away, etc.)
- Add any missing fields to incident schema if needed: `days_away`, `days_restricted`, `job_title_at_time`

### 9.2 — Report generation endpoints
- `GET /api/v1/reports/osha-300?year=2026` — returns OSHA 300 log data as JSON
- `GET /api/v1/reports/osha-300a?year=2026` — returns OSHA 300A summary
- `GET /api/v1/reports/osha-301/{incident_id}` — returns OSHA 301 for a specific incident
- PDF export option via query param `?format=pdf`

### 9.3 — PDF generation
- Add `fpdf2` or `reportlab` to `requirements.txt`
- Create `reports/pdf_generator.py` utility
- Generate formatted OSHA log PDFs

### Verification
- Create incidents with required OSHA fields → generate 300 log → confirm correct data and formatting

---

## Chunk 10: Shift Handover System (Phase 2)

**Goal:** Structured shift handover forms.

### 10.1 — Handover model
- Supabase table: `shift_handovers` — `id`, `outgoing_user_id`, `incoming_user_id`, `shift_date`, `batch_status_summary`, `outstanding_issues`, `tasks_completed`, `tasks_remaining`, `equipment_notes`, `incidents_occurred`, `acknowledged`, `acknowledged_at`, `created_at`
- Schemas and CRUD

### 10.2 — Routes
- `POST /api/v1/shift-handovers` — create handover
- `GET /api/v1/shift-handovers` — list (filterable by date, user)
- `GET /api/v1/shift-handovers/{id}`
- `PUT /api/v1/shift-handovers/{id}/acknowledge` — incoming user acknowledges

### Verification
- Create handover → incoming user acknowledges → confirm state updates

---

## Chunk 11: Dashboards & Reporting (Phase 2)

**Goal:** Production and safety dashboards with export capabilities.

### 11.1 — Production dashboard
- `GET /api/v1/dashboards/production` — batch throughput, completion rates, on-time vs delayed
- `GET /api/v1/dashboards/production/operator-performance` — tasks completed per user, avg task time

### 11.2 — Safety dashboard
- `GET /api/v1/dashboards/safety` — TRIR, near miss frequency, incident trends by type/severity
- `GET /api/v1/dashboards/safety/open-capas` — aging CAPA actions

### 11.3 — Equipment dashboard
- `GET /api/v1/dashboards/equipment` — status breakdown, maintenance adherence

### 11.4 — Export
- Add `openpyxl` to `requirements.txt`
- `GET /api/v1/reports/export?type={report_type}&format={pdf|xlsx}&date_from=&date_to=`
- Report types: `production_summary`, `safety_summary`, `equipment_summary`

### Verification
- Populate data → hit dashboard endpoints → confirm aggregated numbers are correct
- Export as PDF and Excel → confirm files open correctly

---

## Chunk 12: Training Record Management (Phase 2)

**Goal:** Track employee safety training completion and expiry.

### 12.1 — Training model
- Supabase table: `training_courses` — `id`, `name`, `description`, `required_for_roles`, `validity_period_days`, `created_at`
- Supabase table: `training_records` — `id`, `user_id`, `course_id`, `completed_at`, `expires_at`, `certificate_url`, `created_at`
- Schemas and CRUD

### 12.2 — Routes
- CRUD under `/api/v1/training-courses`
- `POST /api/v1/users/{user_id}/training-records` — log completion
- `GET /api/v1/users/{user_id}/training-records` — list user's training
- `GET /api/v1/training-records/expiring?days=30` — list records expiring within N days
- `GET /api/v1/training-records/compliance` — compliance percentage per course

### Verification
- Create course → log completion for user → query expiring records → confirm compliance calculation

---

## Implementation Order

| Order | Chunk | Phase | Dependencies |
|-------|-------|-------|-------------|
| 1 | Chunk 0: Codebase Cleanup | Prereq | None |
| 2 | Chunk 1: Route Refactoring | Prereq | Chunk 0 |
| 3 | Chunk 2: Authentication | Phase 1 | Chunk 1 |
| 4 | Chunk 3: Enrich Resources | Phase 1 | Chunk 1 |
| 5 | Chunk 4: Notes System | Phase 1 | Chunk 1 |
| 6 | Chunk 5: Dashboard Endpoints | Phase 1 | Chunks 3, 4 |
| 7 | Chunk 6: Email Notifications | Phase 1 | Chunk 2 |
| 8 | Chunk 7: Investigation & CAPA | Phase 2 | Chunk 3 (enriched incidents) |
| 9 | Chunk 8: Safety Checklists | Phase 2 | Chunk 2 |
| 10 | Chunk 9: OSHA Logs | Phase 2 | Chunk 7 |
| 11 | Chunk 10: Shift Handover | Phase 2 | Chunk 2 |
| 12 | Chunk 11: Dashboards & Reporting | Phase 2 | Chunks 7, 8 |
| 13 | Chunk 12: Training Records | Phase 2 | Chunk 2 |

Note: Chunks 3, 4, and 2 can be worked on in parallel after Chunk 1 is complete. Chunks 8, 10, and 12 can also be parallelized.
