from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from .models import UserCreate, UserLogin, ProductCreate, CartAdd, Token
from .auth import (
    hash_password, authenticate_user, create_access_token, 
    get_current_user, get_admin_user, load_users, save_users,
    load_products, save_products, load_cart, save_cart,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from datetime import timedelta
from typing import List

app = FastAPI(title="Shopping Cart API")

@app.post("/register/", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate):
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
            "password": hashed_password,
            "role": user.role
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
def login_user(form_data: UserLogin):
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

@app.post("/admin/add_product/", status_code=status.HTTP_201_CREATED)
def add_product(product: ProductCreate, current_user: dict = Depends(get_admin_user)):
    """Add a new product (admin only)"""
    try:
        products = load_products()
        
        if product.name in products:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product already exists"
            )
        
        products[product.name] = {
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock
        }
        
        save_products(products)
        
        return {"message": f"Product {product.name} added successfully"}
    
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add product: {str(e)}"
        )

@app.get("/products/")
def get_products():
    """Get all products (public endpoint)"""
    try:
        products = load_products()
        return {"products": list(products.values())}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching products: {str(e)}"
        )

@app.post("/cart/add/", status_code=status.HTTP_201_CREATED)
def add_to_cart(cart_item: CartAdd, current_user: dict = Depends(get_current_user)):
    """Add item to cart (authenticated users only)"""
    try:
        # Check if product exists
        products = load_products()
        if cart_item.product_name not in products:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        product = products[cart_item.product_name]
        
        # Check stock availability
        if product["stock"] < cart_item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock"
            )
        
        # Load cart
        cart = load_cart()
        username = current_user["username"]
        
        # Initialize user cart if not exists
        if username not in cart:
            cart[username] = {}
        
        # Add or update item in cart
        if cart_item.product_name in cart[username]:
            cart[username][cart_item.product_name]["quantity"] += cart_item.quantity
        else:
            cart[username][cart_item.product_name] = {
                "product_name": cart_item.product_name,
                "quantity": cart_item.quantity,
                "price": product["price"]
            }
        
        save_cart(cart)
        
        return {
            "message": f"Added {cart_item.quantity} {cart_item.product_name}(s) to cart",
            "total_in_cart": cart[username][cart_item.product_name]["quantity"]
        }
    
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding to cart: {str(e)}"
        )
