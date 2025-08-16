from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
import json
import os

# OAuth2 Configuration
SECRET_KEY = "f92b1e88f56a48c7bde1e9c3c7c5f3f8a0d94e2d74b6420a9d6c78a1e53b7f92"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def load_students() -> dict:
    """Load students from JSON file"""
    try:
        if os.path.exists("students.json"):
            with open("students.json", "r") as f:
                return json.load(f)
        return {}
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_students(students: dict):
    """Save students to JSON file"""
    try:
        with open("students.json", "w") as f:
            json.dump(students, f, indent=2, default=str)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error saving student data: {str(e)}"
        )

def authenticate_student(username: str, password: str) -> Optional[dict]:
    """Authenticate student with username and password"""
    students = load_students()
    if username not in students:
        return None
    
    student_data = students[username]
    if not verify_password(password, student_data["password"]):
        return None
    
    return student_data

def verify_token(token: str = Depends(oauth2_scheme)) -> dict:
    """Verify OAuth2 token and return student data"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    students = load_students()
    if username not in students:
        raise credentials_exception
    
    return students[username]

def get_current_student(current_student: dict = Depends(verify_token)) -> dict:
    """Get current authenticated student"""
    return current_student