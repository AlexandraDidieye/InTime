from fastapi import  Response, Depends, HTTPException, status
from MODELS.models import *
from DTOS.dtos import CreateSubjectDTO
from sqlmodel import Session,select
from database.db import *
from typing import List

def get_session():
    with Session(engine) as session:
        yield session  # Yield the session for use in endpoints

def subject_service(response: Response, session: Session = Depends(get_session)):
    return SubjectService(session=session, response=response)

class SubjectService:
    def __init__(self,session,response):
        self.session = session  # Database session
        self.response = response
    
    def create_subject(self, task: CreateSubjectDTO, user_payload):
        userid: int = user_payload.get('id')
        db_item = Subject(**task.model_dump())
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

    def update_subject(self, id,subject,user_payload):
        userid: int =  user_payload.get('id')
        subject_item = self.session.get(Subject, id)
        if not subject_item:
            raise HTTPException(status_code=404, detail="Subject Not Found!")
        if subject_item.user_id != userid:
            raise HTTPException(status_code=401, detail="Unauthorized")
        subject_data = task.model_dump(exclude_unset=False)  
        for key, value in subject_data.items(): 
            setattr(subject_item, key, value)
        self.session.add(subject_item)
        self.session.commit()
        self.session.refresh(subject_item)
        return subject_item

    def read_subjects(self,user_payload):
        userid: int =  user_payload.get('id')
        statement = select(Subject).where(Subject.user_id == userid)
        user = self.session.exec(statement).all()
        return user 
        
    def read_subject(self, id, user_payload):
        userid: int =  user_payload.get('id')
        subject = self.session.get(Subject, id)
        if subject.user_id != userid:
            raise HTTPException(status_code=404, detail="Subject not found")
        return subject

    def delete_subject(self, id, user_payload):
        userid: int =  user_payload.get('id')
        subject = self.session.get(Subject, id)
        if not subject:
            raise HTTPException(status_code=404, detail="Subject hasn't been created")
        if subject.user_id != userid:
            raise HTTPException(status_code=401, detail="Unauthorized")
        self.session.delete(subject)
        self.session.commit()
        self.response.status_code = status.HTTP_204_NO_CONTENT
        return self.response.status_code