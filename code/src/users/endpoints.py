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


@router.post("/", response_model=User)
async def create_user(user: User):
    table = dynamodb.Table(settings.DB_TABLE)
    table.put_item(Item=user.dict())
    return user


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str):
    table = dynamodb.Table(settings.DB_TABLE)
    response = table.get_item(Key={"UID": user_id})
    user = response.get("Item")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=User)
async def update_user(user_id: str, user: User):
    table = dynamodb.Table(settings.DB_TABLE)
    response = table.get_item(Key={"UID": user_id})
    current_user = response.get("Item")
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    # Update the user
    user_dict = user.dict()
    current_user.update(user_dict)

    update_expression = "SET"
    expression_attribute_values = {}
    counter = 1

    for key, value in current_user.items():
        if key != "UID":
            update_expression += f" {key} = :val{counter},"
            expression_attribute_values[f":val{counter}"] = value
            counter += 1
    table.update_item(
        Key={"UID": user_id},
        UpdateExpression=update_expression[:-1],
        ExpressionAttributeValues=expression_attribute_values,
    )

    return current_user
