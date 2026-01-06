from fastapi import  Response, Depends, HTTPException, status
from MODELS.models import *
from DTOS.dtos import CreateAssignmentDTO
from sqlmodel import Session,select
from database.db import *
from typing import List

def get_session():
    with Session(engine) as session:
        yield session  # Yield the session for use in endpoints

def assignment_service(response: Response, session: Session = Depends(get_session)):
    return AssignmentService(session=session, response=response)

class AssignmentService:
    def __init__(self,session,response):
        self.session = session  # Database session
        self.response = response
    
    def create_assignment(self, task: CreateAssignmentDTO, user_payload):
        userid: int = user_payload.get('id')
        db_item = Assignment(**task.model_dump())
        user = self.session.get(User, db_item.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not Found")
        if user.id != userid:
            raise HTTPException(status_code=401, detail="Unauthorized")
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        self.response.status_code = status.HTTP_201_CREATED
        return db_item

    def update_assignment(self, id,subject,user_payload):
        userid: int =  user_payload.get('id')
        assignment_item = self.session.get(Assignment, id)
        if not assignment_item:
            raise HTTPException(status_code=404, detail="Assignment Not Found!")
        if assignment_item.user_id != userid:
            raise HTTPException(status_code=401, detail="Unauthorized")
        assignment_data = task.model_dump(exclude_unset=False)  
        for key, value in assignment_data.items(): 
            setattr(ssignment_item, key, value)
        self.session.add(assignment_item)
        self.session.commit()
        self.session.refresh(assignment_item)
        return assignment_item

    def read_assignments(self,user_payload):
        userid: int =  user_payload.get('id')
        statement = select(Subject).where(Subject.user_id == userid)
        user = self.session.exec(statement).all()
        return user 
        
    def read_assignment(self, id, user_payload):
        userid: int =  user_payload.get('id')
        assignment = self.session.get(Assignment, id)
        if assignment.user_id != userid:
            raise HTTPException(status_code=404, detail="Assignment not found")
        return assignment

    def delete_assignment(self, id, user_payload):
        userid: int =  user_payload.get('id')
        assignment = self.session.get(Assignment, id)
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment hasn't been created")
        if sassignment.user_id != userid:
            raise HTTPException(status_code=401, detail="Unauthorized")
        self.session.delete(assignment)
        self.session.commit()
        self.response.status_code = status.HTTP_204_NO_CONTENT
        return self.response.status_code