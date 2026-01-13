from fastapi import  Response, Depends,APIRouter
from MODELS.models import *
from DTOS.dtos import CreateAssignmentDTO, UpdateAssignmentDTO, 
from datetime import datetime
from database.db import *
from typing import List
from services.subject_service import SubjectService  # Assuming the service is in a services folder
from sqlmodel import Session
from services.user_service import get_current_user
from AUTH import auth



