from pydantic import BaseModel
from typing import List, Optional

class StudentCreate(BaseModel):
    username: str
    password: str
    grades: List[float] = []

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