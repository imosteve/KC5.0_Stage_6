from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Student(BaseModel):
    username: str
    password: str
    grades: List[float] = []
    created_at: datetime = datetime.now()

class StudentCreate(BaseModel):
    username: str
    password: str

class StudentLogin(BaseModel):
    username: str
    password: str

class GradeResponse(BaseModel):
    username: str
    grades: List[float]
    average: Optional[float] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None