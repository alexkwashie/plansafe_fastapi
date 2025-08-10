from fastapi import FastAPI
from routers import batch, task
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(batch.router)
app.include_router(task.router)


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
