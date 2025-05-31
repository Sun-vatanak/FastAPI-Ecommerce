from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated

from ..schemas.user import Token, UserCreate, UserInDB
from ..services.auth import authenticate_user, create_access_token, get_current_user
from ..services.users import create_user
from ..utils.dependencies import get_db
from ..utils.security import get_password_hash

# Create the router instance
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserInDB)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if username or email already exists
    from ..models.user import User
    db_user = db.query(User).filter((User.username == user_data.username) | (User.email == user_data.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    # Hash the password
    hashed_password = get_password_hash(user_data.password)
    user_data_dict = user_data.dict()
    user_data_dict.pop("password")
    user_data_dict["password_hash"] = hashed_password
    
    # Create the user
    return create_user(db=db, user_data=user_data_dict)

@router.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserInDB)
async def read_users_me(current_user: Annotated[UserInDB, Depends(get_current_user)]):
    return current_user