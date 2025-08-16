from pydantic import BaseModel
from datetime import date

class User(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str

class JobApplication(BaseModel):
    job_title: str
    company: str
    date_applied: date
    status: str

class JobApplicationCreate(BaseModel):
    job_title: str
    company: str
    date_applied: date
    status: str

class Token(BaseModel):
    access_token: str
    token_type: str