from fastapi import FastAPI
from routers import batch, task, task_assignee, task_dependency, task_incident, task_machinery, task_raw_materials
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
#app = FastAPI(docs_url=None, redoc_url=None)

app.include_router(batch.router)
app.include_router(task.router)
app.include_router(task_assignee.router)
app.include_router(task_dependency.router)
app.include_router(task_machinery.router)
app.include_router(task_raw_materials.router)
app.include_router(task_incident.router)


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
