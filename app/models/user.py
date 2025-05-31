from sqlalchemy import Column, String, Boolean, Enum,Integer
from .base import BaseModel
import enum

class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"

class User(BaseModel):
    __tablename__ = "users"
    
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password_hash = Column(String(255))
    role = Column(Enum(UserRole), default=UserRole.USER)
    first_name = Column(String(50))
    last_name = Column(String(50))
    phone_number = Column(String(20))
    is_active = Column(Boolean, default=True)
    # Example: models/user.py

