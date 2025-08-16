from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from .models import User, JobApplication, Token
from .auth import (
    hash_password, authenticate_user, create_access_token, 
    get_current_user, load_users, save_users,
    load_applications, save_applications, ACCESS_TOKEN_EXPIRE_MINUTES
)
from datetime import timedelta
from typing import List

app = FastAPI(title="Job Application Tracker API")

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
def login_user(form_data: User):
    """Login endpoint that returns access token"""
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

@app.post("/applications/", status_code=status.HTTP_201_CREATED)
def add_application(application: JobApplication, current_user: dict = Depends(get_current_user)):
    """Add a new job application"""
    try:
        applications = load_applications()
        username = current_user["username"]
        
        # Initialize user applications if not exists
        if username not in applications:
            applications[username] = []
        
        # Create new application
        new_application = {
            "job_title": application.job_title,
            "company": application.company,
            "date_applied": application.date_applied,
            "status": application.status
        }
        
        applications[username].append(new_application)
        save_applications(applications)
        
        return {"message": f"Job application for {application.job_title} at {application.company} added successfully"}
    
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add application: {str(e)}"
        )

@app.get("/applications/", response_model=List[JobApplication])
def get_applications(current_user: dict = Depends(get_current_user)):
    """Get all job applications for the current user only"""
    try:
        applications = load_applications()
        username = current_user["username"]
        
        # Return only current user's applications
        user_applications = applications.get(username, [])
        
        return user_applications
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching applications: {str(e)}"
        )
