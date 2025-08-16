from fastapi import FastAPI, HTTPException, Depends, status
from .models import StudentCreate, StudentLogin, GradeResponse, Token
from .auth import (
    hash_password, authenticate_student, create_access_token, 
    get_current_student, load_students, save_students, ACCESS_TOKEN_EXPIRE_MINUTES
)
from datetime import timedelta

app = FastAPI(title="Student Portal API", version="1.0.0")

@app.post("/register/", status_code=status.HTTP_201_CREATED)
def register_student(student: StudentCreate):
    """Register a new student"""
    try:
        students = load_students()
        
        if student.username in students:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        
        hashed_password = hash_password(student.password)
        students[student.username] = {
            "username": student.username,
            "password": hashed_password,
            "grades": student.grades
        }
        
        save_students(students)
        
        return {"message": f"Student {student.username} registered successfully"}
    
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@app.post("/login/", response_model=Token)
def login_student(form_data: StudentLogin):
    """Login endpoint that returns access token"""
    student = authenticate_student(form_data.username, form_data.password)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": student["username"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/grades/", response_model=GradeResponse)
def get_grades(current_student: dict = Depends(get_current_student)):
    """Get grades for authenticated student (requires authentication)"""
    try:
        grades = current_student.get("grades", [])
        average = sum(grades) / len(grades) if grades else None
        
        return GradeResponse(
            username=current_student["username"],
            grades=grades,
            average=round(average, 2) if average else None
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching grades: {str(e)}"
        )
