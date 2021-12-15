from fastapi import APIRouter
from fastapi import HTTPException
from src.core.config import settings
from src.core.database import dynamodb

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
    table = dynamodb.Table(settings.DB_TABLE)
    response = table.get_item(Key={"UID": user_id})
    user = response.get("Item")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}")
async def update_user(user_id: str, user: User):
    table = dynamodb.Table(settings.DB_TABLE)
    response = table.get_item(Key={"UID": user_id})
    user = response.get("Item")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Update the user
    old_user = User.parse_raw(user)
    print(old_user.__dict__.items() ^ user.__dict__.items())
    # table.update_item(
    #     Key={"UID": user_id},
    #     UpdateExpression="SET age = :val1",
    #     ExpressionAttributeValues={":val1": 26},
    # )
    return user
