from sqlalchemy import Column, Integer, Float, String, ForeignKey, Enum, DateTime,Boolean
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum

class OrderStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Order(BaseModel):
    __tablename__ = "orders"
    
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    total_amount = Column(Float)
    shipping_address_id = Column(Integer, ForeignKey("addresses.id"))
    payment_method = Column(String(50))
    tracking_number = Column(String(100))
    
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    shipping_address = relationship("Address")

class OrderItem(BaseModel):
    __tablename__ = "order_items"
    
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    unit_price = Column(Float)
    
    order = relationship("Order", back_populates="items")
    product = relationship("Product")

class Address(BaseModel):
    __tablename__ = "addresses"
    
    user_id = Column(Integer, ForeignKey("users.id"))
    address_line1 = Column(String(100))
    address_line2 = Column(String(100))
    city = Column(String(50))
    state = Column(String(50))
    postal_code = Column(String(20))
    country = Column(String(50))
    is_default = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="addresses")

# Add relationships to User model
from .user import User
User.orders = relationship("Order", back_populates="user")
User.addresses = relationship("Address", back_populates="user")