from sqlalchemy import Column, String, Text, Float, Integer, Boolean, ForeignKey
from sqlalchemy.dialects.mysql import JSON
from .base import BaseModel

class Product(BaseModel):
    __tablename__ = "products"
    
    name = Column(String(100))
    description = Column(Text)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey("categories.id"))
    stock_quantity = Column(Integer)
    image_urls = Column(JSON)
    is_available = Column(Boolean, default=True)

class Category(BaseModel):
    __tablename__ = "categories"
    
    name = Column(String(50))
    description = Column(Text)
    parent_category_id = Column(Integer, ForeignKey("categories.id"))
    image_url = Column(String(255))