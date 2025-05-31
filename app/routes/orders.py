from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..schemas.order import OrderInDB, OrderCreate, OrderUpdate, OrderStatus
from ..schemas.user import UserInDB  # Add this import
from ..services.orders import create_order, get_order, get_orders, update_order_status
from ..utils.dependencies import get_db, get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderInDB)
async def create_new_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    return create_order(db, order, current_user.id)

@router.get("/", response_model=List[OrderInDB])
async def read_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    return get_orders(db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/{order_id}", response_model=OrderInDB)
async def read_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    db_order = get_order(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    # Users can only see their own orders unless admin
    if db_order.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to view this order")
    return db_order

@router.put("/{order_id}/cancel")
async def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    db_order = get_order(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    # Only the owner or admin can cancel orders
    if db_order.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to cancel this order")
    # Only pending orders can be cancelled
    if db_order.status != OrderStatus.PENDING:
        raise HTTPException(status_code=400, detail="Only pending orders can be cancelled")
    
    updated_order = update_order_status(db, order_id, OrderStatus.CANCELLED)
    return {"message": "Order cancelled successfully", "order": updated_order}