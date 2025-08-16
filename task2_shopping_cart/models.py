from pydantic import BaseModel
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    customer = "customer"

class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole

class UserLogin(BaseModel):
    username: str
    password: str

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int

class CartAdd(BaseModel):
    product_name: str
    quantity: int

class Token(BaseModel):
    access_token: str
    token_type: str