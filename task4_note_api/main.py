from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from .models import User, Note, Token
from .auth import (
    hash_password, authenticate_user, create_access_token, 
    get_current_user, load_users, save_users,
    load_notes, save_notes, ACCESS_TOKEN_EXPIRE_MINUTES
)
from datetime import timedelta
from typing import List

app = FastAPI(title="Notes API")

@app.post("/register/", status_code=status.HTTP_201_CREATED)
def register_user(user: User):
    """Register a new user"""
    try:
        users = load_users()
        
        if user.username in users:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        
        hashed_password = hash_password(user.password)
        users[user.username] = {
            "username": user.username,
            "password": hashed_password
        }
        
        save_users(users)
        
        return {"message": f"User {user.username} registered successfully"}
    
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@app.post("/login/", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login endpoint that returns a JWT token"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/notes/", status_code=status.HTTP_201_CREATED)
def add_note(note: Note, current_user: dict = Depends(get_current_user)):
    """Add a new note (requires token)"""
    try:
        notes = load_notes()
        username = current_user["username"]
        
        # Initialize user notes if not exists
        if username not in notes:
            notes[username] = []
        
        # Create new note
        new_note = {
            "title": note.title,
            "content": note.content,
            "date": note.date
        }
        
        notes[username].append(new_note)
        save_notes(notes)
        
        return {"message": f"Note '{note.title}' added successfully"}
    
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add note: {str(e)}"
        )

@app.get("/notes/", response_model=List[Note])
def get_notes(current_user: dict = Depends(get_current_user)):
    """Get all notes for the current user (requires token)"""
    try:
        notes = load_notes()
        username = current_user["username"]
        
        # Return only current user's notes
        user_notes = notes.get(username, [])
        
        return user_notes
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching notes: {str(e)}"
        )
