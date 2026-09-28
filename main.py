from fastapi import FastAPI
from app.routes import router
from app.auth_routes import router as auth_router
from app.database import engine, Base
from app.models import ItemDB, UserDB


app = FastAPI(
    title="Personal Inventory Management System",
    description="Backend API for managing personal inventory",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine) # database me missing tables create kar degi

@app.get("/")
def home():
    return {
        "message": "Personal Inventory Management System API is running"
    }

app.include_router(router)
app.include_router(auth_router)