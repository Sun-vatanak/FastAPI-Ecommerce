from sqlalchemy.orm import Session
from ..models.order import Order
from ..schemas.order import OrderCreate, OrderStatus

def create_order(db: Session, order: OrderCreate, user_id: int):
    db_order = Order(**order.dict(), user_id=user_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def get_orders(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Order).filter(Order.user_id == user_id).offset(skip).limit(limit).all()

def update_order_status(db: Session, order_id: int, new_status: OrderStatus):
    db_order = get_order(db, order_id)
    if db_order:
        db_order.status = new_status
        db.commit()
        db.refresh(db_order)
    return db_order