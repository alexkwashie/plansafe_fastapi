# SPEC.md — PlanSafe360: Manufacturing Process & Safety Management SaaS

## 1. Product Overview

### 1.1 Vision
PlanSafe360 is a SaaS platform for small and medium-sized manufacturing and process companies that unifies batch production planning, task management, equipment monitoring, safety incident tracking, and AI-assisted decision-making into a single, intuitive application.

### 1.2 Problem Statement
Small and medium manufacturers currently juggle disconnected tools — spreadsheets for production scheduling, paper forms for safety incidents, email chains for task assignments, and tribal knowledge for equipment maintenance. This leads to:
- Production delays due to poor visibility into raw material availability and equipment readiness
- Safety incidents going unreported or under-documented
- Management lacking real-time insight into production status
- No institutional memory — when experienced operators leave, critical knowledge goes with them
- Regulatory compliance (OSHA, ISO, HACCP, etc.) being reactive rather than proactive

### 1.3 Target Users
| Role | Description |
|------|-------------|
| **Plant Manager** | Oversees all production, needs dashboards and reports |
| **Production Supervisor** | Plans batches, assigns tasks, monitors progress |
| **Machine Operator** | Executes tasks, logs notes, reports incidents |
| **Safety Officer** | Manages incidents, inspections, compliance records |
| **Maintenance Technician** | Tracks equipment condition, schedules maintenance |
| **Company Admin** | Manages users, roles, permissions, company settings |

### 1.4 Differentiation
Unlike enterprise ERPs (SAP, BatchMaster, Infor M3) that cost $50K–$500K+ and take months to implement, BatchFlow targets the SMB segment with:
- Setup in hours, not months
- Pricing accessible to 10–200 employee companies
- Mobile-first design for shop-floor use
- Built-in AI assistant for safety/manufacturing questions
- No IT department required to administer

---

## 2. Core Modules

### 2.1 Batch & Process Planning

#### 2.1.1 Batch Creation
- A **Batch** represents a single production run (e.g., "Batch #2024-0142 — 500kg Widget Compound")
- Each batch contains metadata: product name, target quantity, target start/end dates, priority level, assigned production line
- Batches can be created manually or cloned from templates
- Batch templates store reusable process sequences for recurring products

#### 2.1.2 Task Sequencing
- Each batch is composed of an ordered sequence of **Tasks**
- Tasks are linked in a dependency chain: Task B cannot start until Task A is marked complete (configurable: strict or soft dependencies)
- Each task contains:
  - **Name** and **description**
  - **Assigned user(s)** — one or more operators
  - **Estimated duration**
  - **Required equipment** — linked to equipment registry
  - **Required raw materials** — linked to inventory with quantity needed
  - **Safety checklist** — pre-task safety items that must be checked off before starting
  - **Standard Operating Procedure (SOP)** — attachable documents or inline instructions
  - **Status**: Not Started → In Progress → Paused → Completed → Skipped
- Parallel task branches supported (e.g., "Mixing" and "Label Prep" can run simultaneously before converging at "Filling")

#### 2.1.3 Visual Process Builder
- Drag-and-drop interface to design batch process flows
- Visual representation showing task sequence, dependencies, parallel branches
- Color-coded status indicators (grey = pending, blue = in progress, green = done, red = blocked, amber = overdue)

#### 2.1.4 Raw Material Checks
- Before a batch can be started, the system validates that sufficient raw materials are available in inventory
- Warnings displayed if stock is below the required threshold
- Auto-generates purchase requisition suggestions when materials are insufficient
- Tracks material lot numbers for traceability

#### 2.1.5 Scheduling & Calendar
- Gantt-style view showing all active and upcoming batches across production lines
- Calendar view for daily/weekly production planning
- Conflict detection: warns if equipment or personnel are double-booked
- Drag to reschedule batches and auto-recalculate downstream dates

---

### 2.2 Equipment & Asset Management

#### 2.2.1 Equipment Registry
- Catalogue of all manufacturing equipment, tools, and devices
- Each entry includes: name, type, location, serial number, manufacturer, purchase date, warranty info, photo(s)
- Custom fields per equipment type (e.g., pressure rating, capacity, temperature range)

#### 2.2.2 Equipment Status Tracking
- Real-time status per piece of equipment:
  - **Operational** — available for production
  - **In Use** — currently assigned to an active batch task
  - **Maintenance Scheduled** — upcoming planned maintenance
  - **Under Maintenance** — currently being serviced
  - **Out of Service** — broken or decommissioned
- Status changes logged with timestamps and user attribution

#### 2.2.3 Maintenance Scheduling
- Preventive maintenance schedules (time-based or usage-based triggers)
- Maintenance task templates with checklists
- Maintenance history log per equipment item
- Alerts when maintenance is overdue
- Integration point: if equipment is "Under Maintenance" or "Out of Service," batch tasks requiring that equipment are automatically flagged/blocked

#### 2.2.4 IoT Integration (Phase 2)
- API endpoints for receiving sensor data (temperature, pressure, vibration, run-hours)
- Threshold-based alerts when readings exceed safe operating ranges
- Historical sensor data charts per equipment item
- Predictive maintenance suggestions powered by AI (see Section 2.5)

---

### 2.3 Incident & Safety Management

#### 2.3.1 Incident Reporting
- Mobile-friendly incident reporting form accessible by any user
- Incident types: Injury, Near Miss, Property Damage, Environmental, Equipment Failure, Process Deviation, Other
- Capture fields:
  - Date, time, location (production line / area)
  - Personnel involved
  - Severity level (1–5 scale)
  - Description of what happened
  - Immediate actions taken
  - Photo/video attachments
  - Witness information
- Anonymous reporting option for sensitive incidents

#### 2.3.2 Investigation Workflow
- Incidents trigger an investigation workflow assigned to the Safety Officer
- Built-in investigation tools:
  - **5-Why Analysis** template
  - **Fishbone (Ishikawa) Diagram** builder
  - **Root Cause Analysis** form
- Corrective and Preventive Actions (CAPA) tracking with due dates and assigned owners
- Follow-up reminders until all actions are closed

#### 2.3.3 Safety Checklists & Inspections
- Configurable safety inspection templates (pre-shift, equipment-specific, area-specific)
- Scheduled inspections with reminders
- Digital sign-off with timestamp and user identity
- Non-conformance items automatically generate follow-up tasks

#### 2.3.4 Compliance & Recordkeeping
- OSHA 300, 300A, and 301 log generation (auto-populated from incident data)
- Configurable for regional standards (UK HSE, EU directives, etc.)
- Audit trail for all safety-related actions
- Document storage for safety policies, SOPs, Material Safety Data Sheets (MSDS/SDS)
- Training record management: track which employees have completed which safety training, with expiry dates and renewal reminders

---

### 2.4 Process Notes & Communication

#### 2.4.1 Notes System
- Any user can attach notes to:
  - A specific **batch**
  - A specific **task** within a batch
  - A specific piece of **equipment**
  - A specific **incident**
- Note types: General Observation, Safety Concern, Quality Issue, Process Deviation, Handover Note
- Notes support: text, photo attachments, voice-to-text (mobile)
- Timestamped and attributed to the authoring user
- Notes are searchable and filterable

#### 2.4.2 Shift Handover
- Structured shift handover form summarizing:
  - Batch status at end of shift
  - Outstanding issues or concerns
  - Tasks completed and tasks remaining
  - Equipment status changes
  - Any incidents that occurred
- Incoming shift personnel must acknowledge receipt of handover

#### 2.4.3 Notification System
- Configurable notifications via in-app, email, and push (mobile)
- Trigger events:
  - Task assigned to you
  - Task dependency completed (your task is now unblocked)
  - Batch status change
  - Incident reported in your area
  - Equipment status change
  - Maintenance overdue
  - Safety inspection due
  - Approaching material shortage

---

### 2.5 AI Assistant

#### 2.5.1 Domain-Specific Q&A
- Chat-based AI assistant available throughout the app
- Trained/prompted to answer questions about:
  - Safety regulations and best practices (OSHA, HSE, ISO 45001)
  - Manufacturing processes and terminology
  - Equipment troubleshooting guidance
  - Chemical handling and MSDS interpretation
  - First aid procedures
- Context-aware: if the user is viewing a specific batch or piece of equipment, the AI has that context

#### 2.5.2 Smart Suggestions
- **Production optimisation**: suggest task reordering to reduce downtime
- **Risk alerts**: flag when a batch plan involves equipment that's overdue for maintenance
- **Incident pattern detection**: identify recurring incident types, locations, or contributing factors
- **Material forecasting**: predict raw material needs based on historical batch data and upcoming schedule
- **Anomaly detection**: flag unusual patterns in process notes, equipment logs, or production metrics

#### 2.5.3 Report Generation (AI-Assisted)
- Natural language prompt to generate reports: "Generate a summary of last week's production for management"
- AI drafts the report pulling from batch data, incident logs, equipment status, and notes
- User reviews, edits, and approves before sending
- Templates for: Daily Production Summary, Weekly Management Report, Monthly Safety Report, Incident Investigation Report, Equipment Maintenance Report

#### 2.5.4 SOP Assistant
- Upload existing SOPs and the AI can answer questions about them
- AI can draft new SOPs based on existing process data and best practices
- Suggest SOP updates when process deviations are frequently noted

---

### 2.6 Reporting & Analytics Dashboard

#### 2.6.1 Production Dashboards
- Real-time overview: active batches, completion percentages, on-time vs. delayed
- Production throughput over time (daily/weekly/monthly)
- Batch yield tracking: planned vs. actual output
- Operator performance metrics (tasks completed, average task time)
- Production line utilisation rates

#### 2.6.2 Safety Dashboards
- Total Recordable Incident Rate (TRIR)
- Days Away, Restricted, or Transferred (DART) rate
- Near miss frequency
- Incident trends by type, severity, location, shift
- Open CAPA actions and aging
- Safety inspection completion rates
- Training compliance percentage

#### 2.6.3 Equipment Dashboards
- Overall Equipment Effectiveness (OEE)
- Mean Time Between Failures (MTBF)
- Mean Time To Repair (MTTR)
- Maintenance schedule adherence
- Equipment utilisation rates

#### 2.6.4 Exportable Reports
- PDF and Excel export for all reports
- Scheduled auto-generation and email delivery (e.g., weekly management summary every Monday at 8am)
- Custom report builder for ad-hoc queries

---

## 3. User Roles & Permissions

### 3.1 Role-Based Access Control (RBAC)
| Permission | Admin | Plant Manager | Supervisor | Operator | Safety Officer | Maintenance Tech |
|---|---|---|---|---|---|---|
| Manage users & roles | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Create/edit batch templates | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Create/schedule batches | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Assign tasks to users | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Update task status | ✅ | ✅ | ✅ | ✅ (own) | ❌ | ❌ |
| Add notes | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Report incidents | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Manage investigations | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| Manage equipment | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |
| View dashboards | ✅ | ✅ | ✅ (own line) | ❌ | ✅ (safety) | ✅ (equipment) |
| Generate reports | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ |
| Access AI assistant | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Company settings | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

### 3.2 Multi-Tenancy
- Each company is an isolated tenant with its own data
- Company admin can invite users via email
- Support for multiple facilities/sites under one company account

---

## 4. Technical Architecture (Recommended)

### 4.1 Stack
| Layer | Technology | Rationale |
|---|---|---|
| Frontend | React/Next.js + TypeScript + Tailwind CSS | Modern, component-based, great ecosystem |
| Mobile | React Native | Shop-floor accessibility |
| Backend API | Python (FastAPI) | Rapid development, good AI library support |
| Database | PostgreSQL/Supabase | Relational data, strong for structured manufacturing data |
| Search | PostgreSQL full-text search (upgrade to Elasticsearch later) | Keep it simple initially |
| File Storage | Supabase Storage | Photos, documents, SOPs |
| AI | Anthropic Claude API (via Messages API) | Domain Q&A, report generation, suggestions |
| Auth | Supabase Auth | Multi-tenant, role-based, SSO-ready |
| Hosting | Vercel (frontend) + Railway(backend) | Easy scaling for SaaS |
| Real-time | WebSockets or Server-Sent Events | Live task status updates, notifications |
| Background Jobs | BullMQ (Redis) or similar | Report generation, notification dispatch, AI processing |

### 4.2 Database Schema (Core Entities)
```
companies
├── users (belongs_to company, has role)
├── facilities (belongs_to company)
├── equipment (belongs_to facility)
│   ├── equipment_maintenance_logs
│   ├── equipment_status_history
│   └── equipment_sensor_readings (Phase 2)
├── raw_materials (inventory)
├── batch_templates
├── batches (belongs_to facility)
│   ├── batch_tasks (ordered, linked dependencies)
│   │   ├── task_assignments (user ↔ task)
│   │   ├── task_material_requirements
│   │   ├── task_equipment_requirements
│   │   ├── task_safety_checklists
│   │   └── task_notes
│   └── batch_notes
├── incidents
│   ├── incident_investigations
│   ├── incident_capa_actions
│   └── incident_notes
├── safety_inspections
│   ├── inspection_items
│   └── inspection_responses
├── training_records
├── documents (SOPs, MSDS, policies)
├── notifications
└── audit_logs
```

### 4.3 API Design
- RESTful API with consistent patterns: `GET /api/v1/batches`, `POST /api/v1/batches/:id/tasks`
- Pagination, filtering, and sorting on all list endpoints
- WebSocket channels for real-time updates per facility
- Rate limiting and API key support for future third-party integrations

---

## 5. Implementation Phases

### Phase 1 — MVP (Weeks 1–8)
**Goal: Core batch planning + task management + basic safety**
- User authentication and multi-tenant setup
- Company, facility, and user management
- Equipment registry (basic CRUD, manual status updates)
- Batch creation with sequential task chains
- Task assignment and status tracking
- Basic notes system (text + photo on batches and tasks)
- Incident reporting (simple form, no investigation workflow yet)
- Basic dashboard: active batches, overdue tasks, recent incidents
- Email notifications for task assignments and incident reports

### Phase 2 — Safety & Reporting (Weeks 9–14)
**Goal: Full safety module + management reporting**
- Investigation workflow (5-Why, root cause, CAPA tracking)
- Safety checklists and scheduled inspections
- OSHA log generation (300, 300A, 301)
- Shift handover system
- Production and safety dashboards with charts
- PDF/Excel report export
- Scheduled report delivery
- Training record management

### Phase 3 — AI Integration (Weeks 15–20)
**Goal: AI assistant + smart features**
- AI chat assistant (Claude API) with manufacturing/safety domain knowledge
- AI-assisted report generation
- Context-aware AI (aware of current batch/equipment being viewed)
- Smart suggestions: equipment maintenance warnings in batch planning
- Incident pattern detection and alerts
- SOP upload and AI Q&A against SOPs

### Phase 4 — Advanced Features (Weeks 21–28)
**Goal: Optimisation + integrations**
- Visual drag-and-drop process builder
- Gantt chart / scheduling calendar with conflict detection
- Raw material inventory management with shortage alerts
- Material forecasting based on historical data
- Mobile app (React Native) or enhanced PWA
- IoT integration endpoints for equipment sensor data
- Predictive maintenance suggestions
- API for third-party integrations (ERP, accounting)
- Audit trail and compliance export

---

## 6. Non-Functional Requirements

### 6.1 Performance
- Page load under 2 seconds on standard connections
- API response times under 500ms for standard queries
- Support for 50+ concurrent users per tenant without degradation
- Real-time updates delivered within 2 seconds of event

### 6.2 Security
- All data encrypted at rest (AES-256) and in transit (TLS 1.3)
- SOC 2 compliance path
- Row-level security for multi-tenancy (tenant data isolation)
- Session management with secure token handling
- IP allowlisting option for enterprise clients
- Full audit log of all data modifications

### 6.3 Reliability
- 99.9% uptime SLA target
- Automated daily database backups with 30-day retention
- Disaster recovery plan with < 4-hour RTO

### 6.4 Accessibility
- WCAG 2.1 AA compliance
- Mobile-responsive design for all core workflows
- Support for screen readers on critical paths
- High contrast mode for shop-floor visibility

### 6.5 Localisation
- Multi-language support (English first, with i18n framework for future languages)
- Multi-timezone support (critical for companies with facilities in different regions)
- Configurable date/time formats
- Configurable units of measurement (metric/imperial)

---

## 7. Pricing Model (Suggested)

| Plan | Target | Price | Includes |
|---|---|---|---|
| **Starter** | Small teams (up to 10 users) | £49/mo | Core batch planning, basic safety, 1 facility |
| **Professional** | Growing manufacturers (up to 50 users) | £149/mo | All modules, AI assistant, 3 facilities, advanced reporting |
| **Enterprise** | Larger operations (unlimited users) | Custom | SSO, API access, IoT integration, dedicated support, unlimited facilities |

Free 14-day trial on Professional plan. No credit card required.

---

## 8. Success Metrics

| Metric | Target (6 months post-launch) |
|---|---|
| Active paying companies | 20+ |
| User retention (monthly) | > 80% |
| Average batch planning time reduction (user-reported) | 40%+ |
| Incident reporting compliance | 90%+ (vs. industry avg ~60%) |
| NPS score | > 40 |
| OSHA log generation time | < 5 minutes (vs. hours manually) |

---

## 9. Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| SMBs resistant to new software | Low adoption | Offer white-glove onboarding, import existing data from spreadsheets |
| Competing with established ERPs | Loss of enterprise deals | Don't compete — position as complement or stepping stone, not ERP replacement |
| AI hallucination on safety-critical questions | Liability, trust loss | Always include disclaimers, cite sources, allow users to flag bad answers, human review for safety-critical guidance |
| Data loss or breach | Legal, reputation | Encryption, backups, security audits, SOC 2 path |
| Scope creep toward full ERP | Delayed launch, unfocused product | Strict MVP scope, say no to features outside core value prop |
| Regulatory variation by region/industry | Complex compliance | Start with OSHA (US) and HSE (UK), modular compliance framework for adding others |

---

## 10. Open Questions for Further Discovery

1. **Industry vertical focus**: Should V1 target a specific sub-sector (food & beverage, chemicals, pharmaceuticals) or stay general?
2. **Offline capability**: How reliable is internet connectivity on the shop floors of target customers? Do we need offline-first architecture?
3. **Integration priorities**: Which existing tools (QuickBooks, Xero, SAP Business One) are most common among target customers?
4. **Regulatory scope**: Which compliance frameworks beyond OSHA should be prioritised for launch?
5. **AI model hosting**: Self-hosted vs. API — what are the data sensitivity concerns of target customers when sending manufacturing data to an external AI?
6. **Hardware**: Should the product support barcode/QR scanning for equipment and material identification from day one?
