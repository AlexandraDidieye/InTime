from fastapi import  Response, Depends,APIRouter
from MODELS.models import *
from DTOS.dtos import CreateAssignmentDTO, UpdateAssignmentDTO
from datetime import datetime
from database.db import *
from typing import List
from services.assignment_service import CreateAssignmentDTO, AssignmentService  # Assuming the service is in a services folder
from sqlmodel import Session
from services.user_service import get_current_user
from AUTH import auth



router3 = APIRouter(tags=["Assignments"])

def get_session():
    with Session(engine) as session:
        yield session  # Yield the session for use in endpoints


def assignment_serv(response: Response, session: Session = Depends(get_session)):
    return AssignmentService(session=session, response=response)



@router3.post("", response_model=Subject, status_code=201)
def create_assigt(task: CreateAssignmentDTO, assignment_serv: AssignmentService = Depends(assignment_serv), payload: dict = Depends(auth.jwt_decode_token)):
    db_item = assignment_serv.create_assignment(task, payload)
    return db_item

@router3.delete("/{assignment_id}", status_code=204)
def delete_assigy(assignment_id: int, assignment_serv: AssignmentService = Depends(assignment_serv), payload: dict = Depends(auth.jwt_decode_token)):
    delete = assignment_serv.delete_assignment(assignment_id, payload)
    return delete