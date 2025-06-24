from fastapi import APIRouter, Depends, HTTPException
from src.repositories.UserRepository import UserRepository, get_user_repository
from typing import Annotated
from src.models.DTOs import UserRequest, UserResponse
from http import HTTPStatus

router = APIRouter(prefix="/users", tags=["users"])
repository = Annotated[UserRepository, Depends(get_user_repository)]

@router.get("/")
async def create_user(repository: repository, user: UserRequest):
    user = await repository.check_if_exists(user.username, user.email)
    if user:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='User already exists')
    user = await repository.create(user)
    return user
