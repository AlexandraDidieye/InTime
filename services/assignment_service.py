from fastapi import  Response, Depends, HTTPException, status
from MODELS.models import *
from DTOS.dtos import CreateAssignmentDTO
from sqlmodel import Session,select
from database.db import *
from typing import List,Dict
from datetime import date, timedelta


def get_session():
    with Session(engine) as session:
        yield session  # Yield the session for use in endpoints

def assignment_service(response: Response, session: Session = Depends(get_session)):
    return AssignmentService(session=session, response=response)

def days_between(start: date, end: date):
    days = []
    current = start
    while current <= end:
        days.append(current)
        current += timedelta(days=1)
    return days


def generate_chunks(
    start_date: datetime,
    deadline: datetime,
    total_questions: int
):

    days = days_between(start_date.date(), deadline.date())
    if not days:
        return []

    per_day = max(1, total_questions // len(days))
    remainder = total_questions % len(days)

    chunks = []
    for i, day in enumerate(days):
        questions = per_day + (1 if i < remainder else 0)
        chunks.append({
            "chunk_id": str(day),
            "date": str(day),
            "total_questions": questions,
            "completed_questions": 0,
            "status": "pending"
        })

    return chunks

class AssignmentService:
    def __init__(self,session,response):
        self.session = session  # Database session
        self.response = response
    
    def create_assignment(self, task: CreateAssignmentDTO, user_payload):
        userid: int = user_payload.get('id')
        assignment = Assignment(**task.model_dump())
        user = self.session.get(User, assignment.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not Found")
        if user.id != userid:
            raise HTTPException(status_code=401, detail="Unauthorized")
        today = datetime.now()
        dline = assignment.deadline

        if dline is None:
            raise HTTPException(status_code=400, detail="Deadline is required")
        if assignment.number_of_questions is None:
            raise HTTPException(status_code=400, detail="Deadline is required")

        assignment.chunks = generate_chunks(
            start_date=today,
            deadline=dline,
            total_questions=assignment.number_of_questions
        )
        self.session.add(assignment)
        self.session.commit()
        self.session.refresh(assignment)
        self.response.status_code = status.HTTP_201_CREATED
        return assignment

    def update_assignment(self, id,subject,user_payload):
        userid: int =  user_payload.get('id')
        assignment_item = self.session.get(Assignment, id)
        if not assignment_item:
            raise HTTPException(status_code=404, detail="Assignment Not Found!")
        if assignment_item.user_id != userid:
            raise HTTPException(status_code=401, detail="Unauthorized")
        assignment_data = assignment_item.model_dump(exclude_unset=False)  
        for key, value in assignment_data.items(): 
            setattr(assignment_item, key, value)
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
        if assignment.user_id != userid:
            raise HTTPException(status_code=401, detail="Unauthorized")
        self.session.delete(assignment)
        self.session.commit()
        self.response.status_code = status.HTTP_204_NO_CONTENT
        return self.response.status_code