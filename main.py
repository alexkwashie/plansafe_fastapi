from os import name
from fastapi import FastAPI
from sqlalchemy.sql.functions import user
from db import models
from db.database import engine
from routers import user, batch, task
from fastapi.staticfiles import StaticFiles
from auth import authentication
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(authentication.router)

app.include_router(user.router)
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

# Database connection
models.Base.metadata.create_all(engine)

#app.mount('/images', StaticFiles(directory='images'), name='images')