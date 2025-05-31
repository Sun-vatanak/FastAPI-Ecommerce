from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta

from ..schemas.user import UserInDB, UserCreate, Token
from ..schemas.order import OrderInDB, OrderStatus, OrderUpdate
from ..services.users import get_users, create_user, get_user_by_username, authenticate_user
from ..services.orders import get_orders, update_order_status
from ..utils.dependencies import get_db, get_current_active_admin
from ..config import settings



router = APIRouter(prefix="/admin", tags=["admin"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/token")

@router.post("/register", response_model=UserInDB)
async def register_admin(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    db_user = get_user_by_username(db, username=user_data.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    return create_user(db=db, user=user_data, is_admin=True)



@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not an admin user"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users", response_model=List[UserInDB])
async def read_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_admin)
):
    return get_users(db, skip=skip, limit=limit)

@router.get("/orders", response_model=List[OrderInDB])
async def read_all_orders(
    skip: int = 0,
    limit: int = 100,
    status: OrderStatus = None,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_admin)
):
    return get_orders(db, skip=skip, limit=limit, status=status)

@router.put("/orders/{order_id}/status", response_model=OrderInDB)
async def update_order_status_admin(
    order_id: int,
    status_update: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_admin)
):
    db_order = update_order_status(db, order_id, status_update.status)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order