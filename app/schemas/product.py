from pydantic import BaseModel, Field
from typing import List, Optional

class ProductBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str
    price: float = Field(..., gt=0)
    
class ProductCreate(ProductBase):
    category_id: int
    stock_quantity: int = Field(..., ge=0)
    image_urls: List[str] = []
    
class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str]
    price: Optional[float] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    is_available: Optional[bool]
    
class ProductInDB(ProductBase):
    id: int
    category_id: int
    stock_quantity: int
    image_urls: List[str]
    is_available: bool
    
    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    name: str = Field(..., max_length=50)
    description: str
    
class CategoryCreate(CategoryBase):
    parent_category_id: Optional[int] = None
    
class CategoryInDB(CategoryBase):
    id: int
    parent_category_id: Optional[int]
    
    class Config:
        orm_mode = True