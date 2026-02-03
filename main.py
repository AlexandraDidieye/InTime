from fastapi import FastAPI
import argparse
import uvicorn
from database.db import *
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from routers.subject_routers import router2
from routers.user_routers import router_user
from routers.assignment_routers import router3

def create_db_and_table():
    SQLModel.metadata.create_all(engine)  # creates table for model


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_table()
    yield


app = FastAPI(lifespan=lifespan)

@app.get('/')
def example():
    return {"Title": "InTime"}

app.include_router(router_user,tags=['Auth'])
app.include_router(router2,prefix="/Subjects")
app.include_router(router3,prefix="/Assignments")







if __name__ == "__main__":
  
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )