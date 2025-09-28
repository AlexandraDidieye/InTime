from typing import Optional,List
from sqlmodel import Field, SQLModel,Relationship
from datetime import datetime,timedelta
from sqlalchemy import Column,String

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str = Field(sa_column=Column("email", String, unique=True))
    first_name: str
    last_name:str

class Subject(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    progress: Optional[int] = Field(default=0)
    total_assignments: Optional[int] = Field(default=0)  # Default value
    completed_assignments: Optional[int] = Field(default=0)

class Assignments(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    is_completed: bool = Field(default=False)  # Default value for is_completed
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)  # Default factory for current timestamp
    completed_at: Optional[datetime] = Field(default_factory=None)
    deadline: Optional[datetime] = Field(default=datetime.now()+timedelta(days=1))
    updated_at: Optional[datetime] = Field(default_factory=None)
    priority: str = Field(index=True)
    number_of_questions: Optional[int] = Field(default=0)
    number_of_completed_questions: Optional[int] = Field(default=0)