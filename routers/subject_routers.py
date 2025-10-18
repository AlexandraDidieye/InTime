from fastapi import  Response, Depends
from fastapi import APIRouter
from MODELS.models import *
from DTOS.dtos import CreateSubjectDTO,UpdateSubjectDTO,ResponseSubjectDTO
from datetime import datetime
from database.db import *
from typing import List
from sqlalchemy import event
from services.subject_service import SubjectService  # Assuming the service is in a services folder
from sqlmodel import Session
from services.user_service import get_current_user
from AUTH import auth
from fastapi import Response, Depends
from fastapi import APIRouter
from MODELS.models import *
from DTOS.dtos import CreateSubjectDTO, UpdateSubjectDTO, ResponseSubjectDTO
from datetime import datetime
from database.db import *
from typing import List
from sqlalchemy import event



router2 = APIRouter(tags=["Subjects"])

def get_session():
    with Session(engine) as session:
        yield session  # Yield the session for use in endpoints


def subject_service(response: Response, session: Session = Depends(get_session)):
    return SubjectService(session=session, response=response)



@router2.post("", response_model=Subject, status_code=201)
def create_subject(task: CreateSubjectDTO, subject_service: SubjectService = Depends(subject_service), payload: dict = Depends(auth.jwt_decode_token)):
    db_item = subject_service.create_subject(task, payload)
    return db_item

@router2.get("/", response_model=List[Subject])
def read_subjects(subject_service: SubjectService = Depends(subject_service), payload: dict = Depends(auth.jwt_decode_token)):
    subjects = subject_service.read_subjects(payload)
    return subjects


@router2.get("/{subject_id}", response_model=ResponseSubjectDTO)
def read_subject(subject_id: int, subject_service: SubjectService = Depends(subject_service), payload: dict = Depends(auth.jwt_decode_token)):
    subject = subject_service.read_subject(subject_id, payload)
    return subject


@router2.put("/{subject_id}", response_model=Subject)
def update_todolist(subject_id: int, task: UpdateSubjectDTO, subject_service: SubjectService = Depends(subject_service), payload: dict = Depends(auth.jwt_decode_token)):
    update = subject_service.update_subjects(subject_id, task, payload)
    return update

@router2.delete("/{subject_id}", status_code=204)
def delete_todolist(subject_id: int, subject_service: SubjectService = Depends(subject_service), payload: dict = Depends(auth.jwt_decode_token)):
    delete = subject_service.delete_subject(subject_id, payload)
    return delete


