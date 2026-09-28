from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.models import Item, ItemDB, ItemResponse
from app.database import get_db
from app.auth import get_current_user
from typing import Optional

router = APIRouter()

# Health check
@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Personal Inventory API"
    }

# Get all items
@router.get("/items", response_model=list[ItemResponse]) # response_model matlab hai ki response direct list hoga
def get_items(
    name: Optional[str] = None,
    category: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)):

    user_id = int(current_user["sub"])
    query = db.query(ItemDB).filter(ItemDB.user_id == user_id)

    if name:
        query = query.filter(ItemDB.name.ilike(f"%{name}%"))
    if category:
        query = query.filter(ItemDB.category == category)


    items = query.offset(skip).limit(limit).all()
    return items


# Add new item
@router.post("/items", response_model=ItemResponse)
def add_item(item: Item, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_id = int(current_user["sub"])

    # Checking duplicate items for same user only
    existing_item = db.query(ItemDB).filter(ItemDB.name == item.name, ItemDB.category == item.category).first()

    if existing_item:
        raise HTTPException(
            status_code=400,
            detail="Item already exists in Your Inventory"
        )

    new_item = ItemDB(
        name=item.name,
        quantity=item.quantity,
        category=item.category,
        user_id=user_id
    )

    db.add(new_item) # database me new item ko add kar rahe hain
    db.commit() #changes permanently save karta hai
    db.refresh(new_item) # ye new_item ko database se refresh karta hai taki uska id aur other fields update ho jaye

    return new_item # database se banaya hua actual item return karega 


# Get item by ID
@router.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_id = int(current_user["sub"])
    item = db.query(ItemDB).filter(ItemDB.id == item_id, ItemDB.user_id == user_id).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return item

# Update item
@router.put("/items/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int,
    item: Item,
    db: Session = Depends(get_db), # Iska matlab hai ki hum database session ko inject kar rahe hain
    current_user: dict = Depends(get_current_user)
):
    user_id = int(current_user["sub"])
    existing_item = db.query(ItemDB).filter(ItemDB.id == item_id, ItemDB.user_id == user_id).first()

    if not existing_item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    existing_item.name = item.name
    existing_item.quantity = item.quantity
    existing_item.category = item.category

    db.commit()
    db.refresh(existing_item)

    return existing_item


# Delete item
@router.delete("/items/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = int(current_user["sub"])

    existing_item = db.query(ItemDB).filter(
        ItemDB.id == item_id,
        ItemDB.user_id == user_id
    ).first()

    if not existing_item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    db.delete(existing_item)
    db.commit()

    return {
        "message": "Item deleted successfully"
    }