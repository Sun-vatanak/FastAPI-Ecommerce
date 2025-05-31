# app/routes/users.py

from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/")
async def get_users():
    return {"message": "Users list"}
