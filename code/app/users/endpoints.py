from app.core.config import settings
from app.core.database import dynamodb
from fastapi import APIRouter
from fastapi import HTTPException

from .models import User


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


fake_users_db = [
    {"id": 1, "username": "user1", "first_name": "Carlo"},
    {"id": 2, "username": "user2", "first_name": "André"},
]


def search(user_id):
    return [user for user in fake_users_db if user["id"] == int(user_id)]


@router.post("/")
async def create_user(user: User):
    table = dynamodb.Table(settings.DB_TABLE)
    table.put_item(Item=user.dict())
    return user


@router.get("/{user_id}")
async def get_user(user_id: str):
    # TODO: Check if user exists in DynamoDB
    user = search(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}")
async def update_user(user_id: str):
    # TODO: Update user in DynamoDB
    user = search(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
