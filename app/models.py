from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Column, Integer, String, ForeignKey 

from app.database import Base

# Database user table
class UserDB(Base): # ye SQLAlchemy database model hai matlab ye class actual database me table represent karti hai
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)

# User registration request schema
class UserCreate(BaseModel): # jab frontend/client registration request bhejta hai tab incoming data ko validate karega
    username: str = Field(min_length=3, max_length=50)
    email: str = Field
    password: str = Field(min_length=6, max_length=40)

# Login request schema
class UserLogin(BaseModel): # ye login ke liye request ko validate karega
    username: str
    password: str

# User response schema
class UserResponse(BaseModel): # ye registration/login ke baad client ko return krega kchh user data
    id: int
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True) # Pydantic SQLAlchemy object ke attributes se response data read kar sakta hai

class ItemDB(Base): # ye database ke andar table banane ke liye hai
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    category = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True) # ForeignKey personal data ko hi access karega saare users ke data ko nahi

# API request schema
class Item(BaseModel): # ye Api request validate krne ke liye hai
    name: str = Field( # user input me empty ya bahut jyada bara naam na type kr de ya invalid data na type kar de
        min_length = 2, 
        max_length = 100
    )
    quantity: int = Field(
        ge=0
    )
    category: str = Field(
        min_length=2,
        max_length=100
    )

# API response schema
class ItemResponse(BaseModel): # ye API response ko validate karne ke liye hai
    id: int
    name: str
    quantity: int
    category: str

    model_config = ConfigDict(from_attributes=True) # ye SQLAlchemy database ke model ko pydantic response me convert karne me help karta hai 
