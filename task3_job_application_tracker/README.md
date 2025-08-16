# Job Application Tracker API

A secure API where users can track their job applications privately.

## Installation

```bash
pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] python-multipart
```

## Run

```bash
uvicorn task3_job_tracker.main:app --reload
```

## Endpoints

### 1. Register
**POST** `/register/`
```json
{
  "username": "user1",
  "password": "pass123"
}
```

### 2. Login  
**POST** `/login/`
- Form data: `username=user1&password=pass123`
- Returns: JWT token

### 3. Add Job Application
**POST** `/applications/`
- Headers: `Authorization: Bearer <token>`
```json
{
  "job_title": "Software Engineer",
  "company": "Tech Corp", 
  "date_applied": "2024-01-15",
  "status": "applied"
}
```

### 4. Get My Applications
**GET** `/applications/`
- Headers: `Authorization: Bearer <token>`
- Returns: Only your applications

## Features

- Each user sees only their own job applications
- JWT authentication required for applications
- Data stored in JSON files

## Example

```bash
# Register
curl -X POST "http://localhost:8000/register/" \
     -H "Content-Type: application/json" \
     -d '{"username": "user1", "password": "pass123"}'

# Login
curl -X POST "http://localhost:8000/login/" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=user1&password=pass123"

# Add application
curl -X POST "http://localhost:8000/applications/" \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{"job_title": "Developer", "company": "ABC Corp", "date_applied": "2024-01-15", "status": "applied"}'

# Get applications
curl -X GET "http://localhost:8000/applications/" \
     -H "Authorization: Bearer <token>"
```