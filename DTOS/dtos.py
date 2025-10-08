from pydantic import BaseModel
from datetime import datetime,timedelta
from typing import Optional,List
from sqlmodel import Field
from MODELS.models import Subject, Assignment


class CreateSubjectDTO(BaseModel):
    name: str
    user_id: int

class UpdateSubjectDTO(BaseModel):
    name: str = Field(index=True)
   
class ResponseSubjectDTO(BaseModel):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    progress: Optional[int] = Field(default=0)
    total_assignments: Optional[int] = Field(default=0)  # Default value
    completed_assignments: Optional[int] = Field(default=0)
    assignments: List[Assignment] = []

class CreateAssignmentDTO(BaseModel):
    name: str = Field(index=True) 
    deadline: Optional[datetime] = Field(default=datetime.now()+timedelta(days=1))
    description: Optional[str] = None
    priority: str = Field(index=True)
    number_of_questions: Optional[int] = Field(default=0)
    subject_id: int

class UpdateAssignmentDTO(BaseModel):
    name: str = Field(index=True) 
    deadline: Optional[datetime] = Field(default=datetime.now()+timedelta(days=1))
    description: Optional[str] = None
    priority: str = Field(index=True)
    number_of_questions: Optional[int] = Field(default=0)
    subject_id: int
