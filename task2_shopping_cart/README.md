# Shopping Cart API

A secure FastAPI-based shopping cart system with role-based access control. Admins can manage products while all authenticated users can browse and shop.

## Features

- **User Registration & Authentication** with role-based access (admin/customer)
- **Admin-only product management** - Only admins can add products
- **Public product browsing** - Anyone can view products
- **Authenticated shopping cart** - Only logged-in users can add to cart
- **JSON file storage** for users, products, and cart data
- **Dependency injection** for role-based access control

## Project Structure

```
task2_shopping_cart/
├── main.py          # Main FastAPI application
├── models.py        # Pydantic data models
├── auth.py          # Authentication & role checking module
├── users.json       # User data storage (created automatically)
├── products.json    # Product data storage (created automatically)
├── cart.json        # Shopping cart data storage (created automatically)
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
uvicorn task2_shopping_cart.main:app --reload

# Or run directly
python -m task2_shopping_cart.main
```

The API will be available at `http://localhost:8000`

## User Roles

- **admin**: Can add products + browse + shop
- **customer**: Can browse + shop (cannot add products)

## API Endpoints

### 1. Register User
**POST** `/register/`

Register a new user with a role.

**Request Body:**
```json
{
  "username": "john_admin",
  "password": "secure_password",
  "role": "admin"
}
```

**Response:**
```json
{
  "message": "User john_admin registered successfully"
}
```

### 2. User Login
**POST** `/login/`

Authenticate and receive access token.

**Request Body (Form Data):**
- `username`: Username
- `password`: Password

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Add Product (Admin Only)
**POST** `/admin/add_product/`

Add a new product (requires admin role).

**Headers:**
```
Authorization: Bearer <admin_token>
```

**Request Body:**
```json
{
  "name": "Laptop",
  "description": "High-performance laptop",
  "price": 999.99,
  "stock": 10
}
```

**Response:**
```json
{
  "message": "Product Laptop added successfully"
}
```

### 4. Get Products (Public)
**GET** `/products/`

View all products (no authentication required).

**Response:**
```json
{
  "products": [
    {
      "name": "Laptop",
      "description": "High-performance laptop",
      "price": 999.99,
      "stock": 10
    }
  ]
}
```

### 5. Add to Cart (Authenticated)
**POST** `/cart/add/`

Add item to shopping cart (requires authentication).

**Headers:**
```
Authorization: Bearer <user_token>
```

**Request Body:**
```json
{
  "product_name": "Laptop",
  "quantity": 2
}
```

**Response:**
```json
{
  "message": "Added 2 Laptop(s) to cart",
  "total_in_cart": 2
}
```

## Authentication & Authorization

- **OAuth2 with Bearer tokens (JWT)**
- **Role-based access control** using dependency injection
- **Token expiration**: 30 minutes
- **Admin verification**: `get_admin_user` dependency
- **User authentication**: `get_current_user` dependency

## Data Storage

All data is stored in JSON files:
- `users.json` - User accounts with hashed passwords and roles
- `products.json` - Product catalog
- `cart.json` - User shopping carts

