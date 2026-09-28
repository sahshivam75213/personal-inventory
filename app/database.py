import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv() # .env file load karega

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./inventory.db"
) # .env file se database URL lega

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db(): # routes ko list-memory (inventory = []) se hata kar actual SQLite database se connect kar rahe hain  
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

