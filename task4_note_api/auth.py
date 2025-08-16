from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
import json
import os

# JWT Configuration
SECRET_KEY = "notes_api_secret_key_f92b1e88f56a48c7bde1e9c3c7c5f3f8a0d94e2d74b6420a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/")

# File paths
USERS_FILE = "task4_note_api/users.json"
NOTES_FILE = "task4_note_api/notes.json"

def hash_password(password: str) -> str:
    """Hash a plain password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
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

def load_users() -> dict:
    """Load users from JSON file"""
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r") as f:
                return json.load(f)
        return {}
    except (json.JSONDecodeError, FileNotFoundError, IOError):
        return {}

def save_users(users: dict):
    """Save users to JSON file"""
    try:
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=2)
    except (IOError, OSError) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving user data: {str(e)}"
        )

def load_notes() -> dict:
    """Load notes from JSON file"""
    try:
        if os.path.exists(NOTES_FILE):
            with open(NOTES_FILE, "r") as f:
                return json.load(f)
        return {}
    except (json.JSONDecodeError, FileNotFoundError, IOError):
        return {}

def save_notes(notes: dict):
    """Save notes to JSON file"""
    try:
        with open(NOTES_FILE, "w") as f:
            json.dump(notes, f, indent=2, default=str)
    except (IOError, OSError) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving notes data: {str(e)}"
        )

def authenticate_user(username: str, password: str) -> Optional[dict]:
    """Authenticate user with username and password"""
    users = load_users()
    if username not in users:
        return None
    
    user_data = users[username]
    if not verify_password(password, user_data["password"]):
        return None
    
    return user_data

def verify_token(token: str = Depends(oauth2_scheme)) -> dict:
    """Verify JWT Bearer token and return user data"""
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
    
    users = load_users()
    if username not in users:
        raise credentials_exception
    
    return users[username]

def get_current_user(current_user: dict = Depends(verify_token)) -> dict:
    """Get current authenticated user using JWT Bearer token dependency"""
    return current_user