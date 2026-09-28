# Personal Inventory Management System

A backend API for managing personal inventory items with user authentication, JWT authorization, CRUD operations, search, filtering, pagination, validation, and automated testing.

## Features

- User Registration
- User Login
- JWT Authentication
- User-wise Inventory Ownership
- Create Inventory Item
- Read Inventory Items
- Update Inventory Item
- Delete Inventory Item
- Search Items by Name
- Filter Items by Category
- Pagination
- Input Validation
- Error Handling
- Automated API Testing with Pytest


## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT Authentication
- Passlib
- Pytest
- Uvicorn


## Installation

### 1. Clone the repository

`bash
git clone <your-github-repository-url>
cd personal-inventory


## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | /auth/register | Register a new user |
| POST | /auth/login | Login and get JWT token |

### Inventory

| Method | Endpoint | Description |
|---|---|---|
| POST | /items | Create an inventory item |
| GET | /items | Get user's inventory |
| GET | /items/{item_id} | Get a single item |
| PUT | /items/{item_id} | Update an item |
| DELETE | /items/{item_id} | Delete an item |

### Search, Filter & Pagination

```text
GET /items?name=milk
GET /items?category=food
GET /items?skip=0&limit=10
GET /items?name=milk&category=food&skip=0&limit=10

## Authentication

This API uses JWT (JSON Web Token) authentication.

After login, use the returned access token:

`text
Authorization: Bearer <your-access-token>


Protected inventory endpoints require a valid JWT token.

## Testing

Run tests using:

`bash
pytest


All tests should pass successfully.

## Running the Application

Start the FastAPI server:

`bash
uvicorn main:app --reload --port 8001

