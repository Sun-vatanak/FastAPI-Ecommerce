from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..schemas.product import ProductInDB, ProductCreate, ProductUpdate, CategoryInDB, CategoryCreate
from ..schemas.user import UserInDB  # Add this import
from ..services.products import (
    get_product, get_products, create_product, update_product, delete_product,
    get_category, get_categories, create_category
)
from ..utils.dependencies import get_db, get_current_user, get_current_active_user

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[ProductInDB])
async def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_products(db, skip=skip, limit=limit)

@router.get("/{product_id}", response_model=ProductInDB)
async def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.post("/", response_model=ProductInDB)
async def create_new_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user)
):
    # Only admin can create products
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create products")
    return create_product(db, product)

@router.put("/{product_id}", response_model=ProductInDB)
async def update_existing_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user)
):
    # Only admin can update products
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can update products")
    db_product = update_product(db, product_id, product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/{product_id}")
async def delete_existing_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user)
):
    # Only admin can delete products
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete products")
    success = delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

# Categories routes
@router.get("/categories/", response_model=List[CategoryInDB])
async def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_categories(db, skip=skip, limit=limit)

@router.get("/categories/{category_id}", response_model=CategoryInDB)
async def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = get_category(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.post("/categories/", response_model=CategoryInDB)
async def create_new_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user)
):
    # Only admin can create categories
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create categories")
    return create_category(db, category)