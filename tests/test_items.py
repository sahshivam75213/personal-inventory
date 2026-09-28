from fastapi.testclient import TestClient

from main import app

import uuid

from app.database import SessionLocal
from app.models import UserDB, ItemDB
from app.auth import hash_password, create_access_token

def create_test_user():
    db = SessionLocal()
    username = f"testuser_{uuid.uuid4().hex[:8]}"
    email = f"{username}@test.com"
    password = "test123456"

    user = UserDB(
        username=username,
        email=email,
        hashed_password=hash_password(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user.id, username, password

def get_test_token():
    user_id, username, password = create_test_user()

    token = create_access_token(
        data={
            "sub": str(user_id),
            "username": username
        }
    )

    return token

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Personal Inventory Management System API is running"
    }

def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() 
    ["status"] == "healthy"

def test_create_item():
    token = get_test_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    item_name = f"Test Milk {uuid.uuid4().hex[:8]}"

    response = client.post(
        "/items",
        json={
            "name": item_name,
            "quantity": 2,
            "category": "Food"
        },
        headers=headers
    )
    print(response.json())

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == item_name
    assert data["quantity"] == 2
    assert data["category"] == "Food"

def test_get_items():
    token = get_test_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.get(
        "/items",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

def test_get_item():
    token = get_test_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    item_name = f"Test Phone {uuid.uuid4().hex[:8]}"

    create_response = client.post(
        "/items",
        json={
            "name": item_name,
            "quantity": 1,
            "category": "Electronics"
        },
        headers=headers
    )

    assert create_response.status_code == 200

    item_id = create_response.json()["id"]

    response = client.get(
        f"/items/{item_id}",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == item_id
    assert data["name"] == item_name

def test_update_item():
    token = get_test_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    item_name = f"Test Laptop {uuid.uuid4().hex[:8]}"

    # Create item
    create_response = client.post(
        "/items",
        json={
            "name": item_name,
            "quantity": 1,
            "category": "Electronics"
        },
        headers=headers
    )

    assert create_response.status_code == 200

    item_id = create_response.json()["id"]

    # Update item
    response = client.put(
        f"/items/{item_id}",
        json={
            "name": "Updated Laptop",
            "quantity": 2,
            "category": "Electronics"
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == item_id
    assert data["name"] == "Updated Laptop"
    assert data["quantity"] == 2
    assert data["category"] == "Electronics"

def test_delete_item():
    token = get_test_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    item_name = f"Test Delete {uuid.uuid4().hex[:8]}"

    # Create item
    create_response = client.post(
        "/items",
        json={
            "name": item_name,
            "quantity": 1,
            "category": "Test"
        },
        headers=headers
    )

    assert create_response.status_code == 200

    item_id = create_response.json()["id"]

    # Delete item
    response = client.delete(
        f"/items/{item_id}",
        headers=headers
    )

    assert response.status_code == 200

    # Verify item is deleted
    get_response = client.get(
        f"/items/{item_id}",
        headers=headers
    )

    assert get_response.status_code == 404