from fastapi import  Response, Depends
from fastapi import APIRouter
from MODELS.models import *
from DTOS.dtos import CreateSubjectDTO,UpdateSubjectDTO,ResponseSubjectDTO
from datetime import datetime
from database.db import *
from typing import List
from sqlalchemy import event
from services.subject_service import SujectService  # Assuming the service is in a services folder
from sqlmodel import Session
from services.user_service import get_current_user
from authorization_authentication import auth



router2 = APIRouter(tags=["Subjects"])

def get_session():
    with Session(engine) as session:
        yield session  # Yield the session for use in endpoints
