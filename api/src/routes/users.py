from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.models.DTOs import UserRequest, UserResponse
from src.repositories.UserRepository import UserRepository, get_user_repository
from src.security.security import get_current_user
from src.models.entities import User

router = APIRouter(prefix="/users", tags=["users"])
repository = Annotated[UserRepository, Depends(get_user_repository)]
current_user = Annotated[User, Depends(get_current_user)]


@router.post("/", status_code=HTTPStatus.CREATED, response_model=UserResponse)
async def create_user(repository: repository, data: UserRequest):
    user = await repository.check_if_exists(data.username, data.email)
    if user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="User already exists"
        )
    user = await repository.create(data)
    return user


@router.get("/", response_model=list[UserResponse])
async def read_users(repository: repository, offset: int = 0, limit: int = 25):
    return await repository.read(offset, limit)


@router.get("/{id}", response_model=UserResponse)
async def read_user(repository: repository, id: UUID):
    user = await repository.read_by_id(id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found.")
    return user


@router.put("/{id}", response_model=UserResponse)
async def update_user(repository: repository, current_user: current_user, id: UUID, data: UserRequest):
    if current_user.id != id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Not enough permission.")
    conflict = await repository.check_conflicts(id, data.username, data.email)
    if conflict:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="User already exists."
        )
    return await repository.update(current_user, data)


@router.delete("/{id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_user(repository: repository, current_user: current_user, id: UUID):
    if current_user.id != id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Not enough permission.")
    await repository.delete(current_user)
