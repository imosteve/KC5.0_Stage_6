# Student Portal API

A secure FastAPI-based student portal where students can register, login, and view their grades with OAuth2 authentication.

## Features

- Student registration with secure password hashing
- OAuth2 authentication with JWT tokens
- Protected grade viewing endpoint
- JSON file storage for student data
- Comprehensive error handling

## Project Structure

```
task1_student_portal/
├── main.py          # Main FastAPI application
├── models.py        # Pydantic data models
├── auth.py          # Authentication utilities
├── students.json    # Student data storage (created automatically)
└── README.md        # This file
```

## Installation

1. Clone the repository
2. Install required dependencies:

```bash
pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] python-multipart
```

## Running the Application

```bash
# From the project root directory
uvicorn task1_student_portal.main:app --reload

# Or run directly
python -m task1_student_portal.main
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Register Student
**POST** `/register/`

Register a new student account.

**Request Body:**
```json
{
  "username": "user1",
  "password": "password1"
}
```

**Response:**
```json
{
  "message": "Student user1 registered successfully"
}
```

### 2. Student Login
**POST** `/login/`

Authenticate and receive access token.

**Request Body (Form Data):**
- `username`: Student username
- `password`: Student password

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Get Grades
**GET** `/grades/`

View student grades (requires authentication).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "username": "user1",
  "grades": [85.5, 90.0, 78.5, 92.0],
  "average": 86.5
}
```

## Authentication

This API uses OAuth2 with Bearer tokens (JWT). After logging in:

1. Include the token in the Authorization header
2. Format: `Authorization: Bearer <your_token>`
3. Tokens expire after 30 minutes

## Data Storage

- Student data is stored in `students.json`
- Passwords are securely hashed using bcrypt
- File operations include error handling for robustness
