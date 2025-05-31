from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime
from .user import UserInDB
from .product import ProductInDB

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)
    
class OrderItemCreate(OrderItemBase):
    pass
    
class OrderItemInDB(OrderItemBase):
    id: int
    product: ProductInDB
    
    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    shipping_address_id: int
    payment_method: str = Field(..., max_length=50)
    
class OrderCreate(OrderBase):
    items: List[OrderItemCreate]
    
class OrderUpdate(BaseModel):
    status: Optional[OrderStatus]
    tracking_number: Optional[str] = Field(None, max_length=100)
    
class OrderInDB(OrderBase):
    id: int
    user_id: int
    status: OrderStatus
    total_amount: float
    tracking_number: Optional[str]
    created_at: datetime
    user: UserInDB
    items: List[OrderItemInDB]
    
    class Config:
        orm_mode = True

class AddressBase(BaseModel):
    address_line1: str = Field(..., max_length=100)
    address_line2: Optional[str] = Field(None, max_length=100)
    city: str = Field(..., max_length=50)
    state: str = Field(..., max_length=50)
    postal_code: str = Field(..., max_length=20)
    country: str = Field(..., max_length=50)
    is_default: bool = False
    
class AddressCreate(AddressBase):
    pass
    
class AddressInDB(AddressBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True