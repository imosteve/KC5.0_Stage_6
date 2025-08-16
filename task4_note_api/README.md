# Notes API with JWT Authentication

A secure notes management API where users can create and view their personal notes using JWT tokens.

## Installation

```bash
pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] python-multipart
```

## Run

```bash
uvicorn task4_note_api.main:app --reload
```

## Endpoints

### 1. Register
**POST** `/register/`
```json
{
  "username": "user1",
  "password": "password1"
}
```

### 2. Login (Get Token)
**POST** `/login/`
- Form data: `username=user1&password=password1`
- Returns: JWT token

### 3. Add Note
**POST** `/notes/`
- Headers: `Authorization: Bearer <token>`
```json
{
  "title": "Meeting Notes",
  "content": "Discussed project timeline",
  "date": "2024-01-15"
}
```

### 4. Get My Notes
**GET** `/notes/`
- Headers: `Authorization: Bearer <token>`
- Returns: All your notes

## Features

- JWT Bearer token authentication
- Each user sees only their own notes
- Notes stored per user in JSON file

