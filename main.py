from fastapi import FastAPI
import argparse
import uvicorn
from database.db import *
from sqlmodel import SQLModel
from contextlib import asynccontextmanager


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









if __name__ == "__main__":
  
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )