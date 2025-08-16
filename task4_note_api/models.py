from pydantic import BaseModel
from datetime import date

class User(BaseModel):
    username: str
    password: str

class Note(BaseModel):
    title: str
    content: str
    date: date

class Token(BaseModel):
    access_token: str
    token_type: str