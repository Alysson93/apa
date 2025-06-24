from src.models.entities import User
from src.db import AsyncSession, get_session
from fastapi import Depends
from sqlalchemy import select

class UserRepository:
    
    def __init__(self, session: AsyncSession):
        self.session = session
    

    async def create(self, user: User):
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def check_if_exists(self, username: str = '', email: str = ''):
        user = await self.session.execute(
            select(User).where((User.username == username) | (User.email == email))
        )
        return user.scalar()


def get_user_repository(session: AsyncSession = Depends(get_session)):
    return UserRepository(session)