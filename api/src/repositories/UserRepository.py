from datetime import datetime
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select

from src.db import AsyncSession, get_session
from src.models.DTOs import UserRequest
from src.models.entities import User


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: UserRequest):
        user = User(
            username=data.username,
            password=data.password,
            name=data.name,
            last_name=data.last_name,
            email=data.email,
            phone=data.phone,
            role=data.role,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def read(self, offset: int, limit: int):
        users = await self.session.execute(select(User).offset(offset).limit(limit))
        return users.scalars()

    async def read_by_id(self, id: UUID):
        user = await self.session.execute(select(User).where(User.id == id))
        return user.scalar()

    async def update(self, user: User, data: UserRequest):
        user.username = data.username
        user.password = data.password
        user.name = data.name
        user.last_name = data.last_name
        user.email = data.email
        user.phone = data.phone
        user.role = data.role
        user.updated_at = datetime.now()
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user: User):
        await self.session.delete(user)
        await self.session.commit()

    async def check_if_exists(self, username: str = "", email: str = ""):
        user = await self.session.execute(
            select(User).where((User.username == username) | (User.email == email))
        )
        return user.scalar()

    async def check_conflicts(self, id: UUID, username: str = "", email: str = ""):
        """
        Verifica se, além do usuário com o id passado,  já existe outro usuário com mesmo username ou email
        """
        user = await self.session.execute(
            select(User).where(
                User.id != id, (User.username == username) | (User.email == email)
            )
        )
        return user.scalar()


def get_user_repository(session: AsyncSession = Depends(get_session)):
    return UserRepository(session)
