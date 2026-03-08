from fastapi import FastAPI
from routers import users
from routers.auth import router as auth_router
from routers.production_planning import batch, batch_assignee, task, task_assignee, task_machinery, task_raw_materials
from routers.machinery_equipement.machinery_equipement import router as machinery_router
from routers.incident import router as incidents_router
from routers.raw_materials import router as raw_material_router
from routers.notes import router as notes_router
from routers.upload import router as upload_router
from routers.dashboard import router as dashboard_router
from routers.notifications import router as notifications_router
from routers.investigations import router as investigations_router
from routers.capa import router as capa_router
from routers.checklists import router as checklists_router
from routers.inspections_routes import router as inspections_router
from routers.reports import router as reports_router
from routers.shift_handovers import router as shift_handovers_router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
#app = FastAPI(docs_url=None, redoc_url=None)

app.include_router(auth_router)
app.include_router(batch.router)
app.include_router(batch_assignee.router)

app.include_router(task.router)
app.include_router(task_assignee.router)
app.include_router(task_machinery.router)
app.include_router(task_raw_materials.router)
app.include_router(users.router)

app.include_router(machinery_router)
app.include_router(raw_material_router)
app.include_router(incidents_router)
app.include_router(notes_router)
app.include_router(upload_router)
app.include_router(dashboard_router)
app.include_router(notifications_router)
app.include_router(investigations_router)
app.include_router(capa_router)
app.include_router(checklists_router)
app.include_router(inspections_router)
app.include_router(reports_router)
app.include_router(shift_handovers_router)


@app.get("/")
def root():
    return "Welcome to PlanSafe360 API Service"


origins = [
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:3002'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)



# Removed SQLAlchemy database connection since Supabase is used

# app.mount('/images', StaticFiles(directory='images'), name='images')
